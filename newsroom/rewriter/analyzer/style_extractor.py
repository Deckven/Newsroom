"""Hierarchical style analysis: chunk -> merge -> synthesize."""

from __future__ import annotations

import json
import logging
from typing import Any

from newsroom.rewriter.adapter import RewriterConfig
from newsroom.rewriter.analyzer.prompts import (
    CHUNK_ANALYSIS_SYSTEM,
    CHUNK_ANALYSIS_USER,
    SYNTHESIS_SYSTEM,
    SYNTHESIS_USER,
    SYNTHESIS_JSON_USER,
)
from newsroom.rewriter.analyzer.sampler import chunk_articles, stratified_sample
from newsroom.rewriter.corpus.models import Article, ChunkAnalysis, StyleGuide
from newsroom.rewriter.corpus.store import CorpusStore
from newsroom.rewriter.llm_client import LLMClient

logger = logging.getLogger(__name__)


class StyleExtractor:
    """Hierarchical style analysis pipeline."""

    def __init__(self, settings: RewriterConfig, store: CorpusStore) -> None:
        self.settings = settings
        self.store = store
        self.llm = LLMClient(settings)

    def run(
        self,
        *,
        use_batch: bool = True,
        resume: bool = False,
    ) -> StyleGuide:
        """Execute the full analysis pipeline.

        1. Stratified sample
        2. Chunk analysis (batch or sequential)
        3. Synthesis into style guide
        """
        # Step 1: Sample
        articles = self.store.get_all_articles()
        if not articles:
            raise RuntimeError(
                "No articles in corpus. Run `python -m newsroom rewriter-setup import` first."
            )

        sample = stratified_sample(articles, self.settings)
        logger.info(
            "Sampled %d articles out of %d (%.1f%%)",
            len(sample), len(articles), len(sample) / len(articles) * 100,
        )

        # Step 2: Chunk analysis
        if resume:
            existing = self.store.get_chunk_analyses()
            if existing:
                logger.info("Resuming: found %d existing chunk analyses", len(existing))
                chunk_analyses = existing
            else:
                chunk_analyses = self._analyze_chunks(sample, use_batch=use_batch)
        else:
            self.store.clear_analyses()
            chunk_analyses = self._analyze_chunks(sample, use_batch=use_batch)

        # Step 3: Synthesis
        guide = self._synthesize(chunk_analyses, sample_size=len(sample))

        # Save
        self.store.save_style_guide(guide)
        self._save_to_files(guide)

        logger.info("Style guide generated!")
        logger.info("  Markdown: %s", self.settings.style_guide_md_path)
        logger.info("  JSON: %s", self.settings.style_guide_json_path)

        return guide

    def estimate_cost(self) -> dict[str, Any]:
        """Estimate the cost of running analysis."""
        articles = self.store.get_all_articles()
        sample = stratified_sample(articles, self.settings)

        chunks = chunk_articles(sample, self.settings, self.llm.count_tokens)

        total_input_tokens = 0
        for chunk in chunks:
            articles_text = self._format_chunk(chunk)
            prompt_text = CHUNK_ANALYSIS_SYSTEM + CHUNK_ANALYSIS_USER.format(
                articles_text=articles_text
            )
            total_input_tokens += self.llm.count_tokens(prompt_text)

        est_output_per_chunk = 2000
        chunk_output_tokens = len(chunks) * est_output_per_chunk

        synthesis_input = total_input_tokens // 4
        synthesis_output = 4000

        total_input = total_input_tokens + synthesis_input
        total_output = chunk_output_tokens + synthesis_output

        cost_batch = self.llm.estimate_cost(total_input, total_output, batch=True)
        cost_direct = self.llm.estimate_cost(total_input, total_output, batch=False)

        return {
            "sample_size": len(sample),
            "n_chunks": len(chunks),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "estimated_cost_batch": cost_batch,
            "estimated_cost_direct": cost_direct,
        }

    def _analyze_chunks(
        self,
        sample: list[Article],
        *,
        use_batch: bool,
    ) -> list[ChunkAnalysis]:
        """Run chunk-level analysis (batch or sequential)."""
        chunks = chunk_articles(sample, self.settings, self.llm.count_tokens)
        logger.info("Split into %d chunks for analysis", len(chunks))

        # Build requests
        requests = []
        for i, chunk in enumerate(chunks):
            articles_text = self._format_chunk(chunk)
            requests.append({
                "custom_id": f"chunk_{i}",
                "system": CHUNK_ANALYSIS_SYSTEM,
                "messages": [
                    {
                        "role": "user",
                        "content": CHUNK_ANALYSIS_USER.format(articles_text=articles_text),
                    }
                ],
            })

        # Execute
        if use_batch:
            from newsroom.rewriter.batch import BatchProcessor

            batch = BatchProcessor(self.settings)
            try:
                results = batch.submit_and_wait(requests)
            except Exception as e:
                logger.warning("Batch API failed (%s), falling back to sequential", e)
                results = batch.fallback_sequential(requests)
        else:
            results = self._run_sequential(requests)

        # Save chunk analyses
        analyses = []
        for i, chunk in enumerate(chunks):
            custom_id = f"chunk_{i}"
            text = results.get(custom_id, "")
            analysis = ChunkAnalysis(
                chunk_id=i,
                article_ids=[a.id for a in chunk if a.id],
                analysis_text=text,
                token_count=self.llm.count_tokens(text),
            )
            self.store.save_chunk_analysis(analysis)
            analyses.append(analysis)

        return analyses

    def _run_sequential(self, requests: list[dict[str, Any]]) -> dict[str, str]:
        """Run requests one by one (no batch API)."""
        results: dict[str, str] = {}
        for i, req in enumerate(requests):
            logger.info("Analyzing chunk %s (%d/%d)...", req["custom_id"], i + 1, len(requests))
            text = self.llm.complete(
                system=req.get("system", ""),
                messages=req["messages"],
                max_tokens=4096,
                temperature=0.3,
            )
            results[req["custom_id"]] = text
        return results

    def _synthesize(
        self,
        analyses: list[ChunkAnalysis],
        *,
        sample_size: int,
    ) -> StyleGuide:
        """Synthesize chunk analyses into a unified style guide."""
        logger.info("Synthesizing style guide...")

        analyses_text = "\n\n---\n\n".join(
            f"### Анализ чанка {a.chunk_id + 1}\n\n{a.analysis_text}"
            for a in analyses
            if a.analysis_text
        )

        # Generate markdown style guide
        md = self.llm.complete(
            system=SYNTHESIS_SYSTEM,
            messages=[
                {
                    "role": "user",
                    "content": SYNTHESIS_USER.format(
                        n_chunks=len(analyses),
                        analyses_text=analyses_text,
                    ),
                }
            ],
            max_tokens=8192,
            temperature=0.3,
        )

        # Generate structured JSON
        json_text = self.llm.complete(
            system="Ты — помощник по структуризации данных. Возвращай только валидный JSON.",
            messages=[
                {
                    "role": "user",
                    "content": SYNTHESIS_JSON_USER.format(style_guide_md=md),
                }
            ],
            max_tokens=4096,
            temperature=0.1,
        )

        structured = self._parse_json(json_text)

        return StyleGuide(
            markdown=md,
            structured=structured,
            sample_size=sample_size,
            n_chunks=len(analyses),
        )

    def _save_to_files(self, guide: StyleGuide) -> None:
        """Save style guide to markdown and JSON files."""
        self.settings.ensure_data_dir()

        self.settings.style_guide_md_path.write_text(
            guide.markdown, encoding="utf-8"
        )
        self.settings.style_guide_json_path.write_text(
            json.dumps(guide.structured, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _format_chunk(articles: list[Article]) -> str:
        """Format a chunk of articles for the analysis prompt."""
        parts = []
        for a in articles:
            header = f"### «{a.title}»"
            if a.categories:
                header += f" [{', '.join(a.categories)}]"
            if a.published_at:
                header += f" ({a.published_at.strftime('%Y-%m-%d')})"
            parts.append(f"{header}\n\n{a.content}")
        return "\n\n---\n\n".join(parts)

    @staticmethod
    def _parse_json(text: str) -> dict[str, Any]:
        """Extract and parse JSON from LLM response."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [line for line in lines if not line.strip().startswith("```")]
            text = "\n".join(lines)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
            return {"raw": text, "parse_error": True}
