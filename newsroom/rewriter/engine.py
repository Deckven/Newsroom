"""Rewrite engine: prompt assembly + API call + postprocessing."""

from __future__ import annotations

import logging
import re

from newsroom.rewriter.adapter import RewriterConfig
from newsroom.rewriter.analyzer.examples import ExampleSelector
from newsroom.rewriter.corpus.store import CorpusStore
from newsroom.rewriter.llm_client import LLMClient
from newsroom.rewriter.rewrite_prompts import build_system_prompt, build_user_prompt

logger = logging.getLogger(__name__)


class RewriteEngine:
    """Orchestrates the style-transfer rewriting process."""

    def __init__(self, settings: RewriterConfig, store: CorpusStore) -> None:
        self.settings = settings
        self.store = store
        self.llm = LLMClient(settings)
        self.selector = ExampleSelector(settings, store)

    def rewrite(
        self,
        text: str,
        *,
        intensity: str | None = None,
        n_examples: int | None = None,
        extra_examples: list[str] | None = None,
        preserve_structure: bool | None = None,
        temperature: float | None = None,
    ) -> str:
        """Rewrite text in the blog's style."""
        intensity = intensity or self.settings.intensity
        n_examples = n_examples if n_examples is not None else self.settings.n_examples
        preserve_structure = (
            preserve_structure if preserve_structure is not None
            else self.settings.preserve_structure
        )
        temperature = temperature if temperature is not None else self.settings.temperature

        # Load style guide
        style_guide_md = self._load_style_guide()
        logger.debug("Style guide loaded (%d chars)", len(style_guide_md))

        # Select examples
        examples = self._select_examples(text, n_examples)

        # Prepend user-provided examples
        if extra_examples:
            logger.debug("Adding %d user-provided example(s)", len(extra_examples))
            examples = extra_examples + examples

        # Build prompts
        system_prompt = build_system_prompt(style_guide_md, intensity)
        user_prompt = build_user_prompt(
            text,
            examples,
            preserve_structure=preserve_structure,
        )

        logger.debug("Calling Claude API...")
        result = self.llm.complete_cached(
            system_text=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=temperature,
        )

        # Postprocess
        result = self._postprocess(result)
        return result

    def _load_style_guide(self) -> str:
        """Load style guide from file or database."""
        md_path = self.settings.style_guide_md_path
        if md_path.exists():
            return md_path.read_text(encoding="utf-8")

        guide = self.store.get_latest_style_guide()
        if guide:
            return guide.markdown

        raise RuntimeError(
            "Style guide not found. Run `python -m newsroom rewriter-setup analyze` first."
        )

    def _select_examples(self, text: str, n: int) -> list[str]:
        """Select the most relevant few-shot examples."""
        articles = self.selector.find_similar(text, n=n)
        logger.debug("Selected %d examples", len(articles))
        return [
            f"**{a.title}**\n\n{a.content}"
            for a in articles
        ]

    @staticmethod
    def _postprocess(text: str) -> str:
        """Clean up the LLM output."""
        text = text.strip()

        # Remove potential wrapper commentary
        lines = text.split("\n")
        if lines and re.match(
            r"^(Вот|Here|Переписанный|Готово|Результат)",
            lines[0],
            re.IGNORECASE,
        ):
            text = "\n".join(lines[1:]).strip()

        # Remove trailing commentary
        for marker in ["\n---\n", "\n***\n"]:
            if marker in text:
                idx = text.rfind(marker)
                after = text[idx + len(marker):].strip()
                if len(after) < 200:
                    text = text[:idx].strip()

        # Normalize whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text
