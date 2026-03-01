"""Main pipeline orchestrator."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import Any

from newsroom.formatters import FORMATTER_REGISTRY
from newsroom.models import Article, Digest
from newsroom.processors import PROCESSOR_REGISTRY
from newsroom.sources import SOURCE_REGISTRY

logger = logging.getLogger(__name__)


class Pipeline:
    """Orchestrates the fetch -> process -> format pipeline."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.sources = self._build_sources()
        self.processors = self._build_processors()

    def _build_sources(self) -> list:
        sources = []
        for src_cfg in self.config.get("sources", []):
            src_type = src_cfg.get("type")
            cls = SOURCE_REGISTRY.get(src_type)
            if cls is None:
                logger.warning("Unknown source type: %s — skipping.", src_type)
                continue
            sources.append(cls(src_cfg))
        return sources

    def _build_processors(self) -> list:
        proc_cfg = self.config.get("processors", {})
        processors = []
        # Ordered: filter -> dedup -> llm -> rewriter
        for name in ("filter", "dedup", "llm", "rewriter"):
            section = proc_cfg.get(name, {})
            if not section.get("enabled", False):
                continue
            cls = PROCESSOR_REGISTRY.get(name)
            if cls is None:
                continue
            # For LLM and rewriter processors, merge in top-level config
            if name == "llm":
                merged = {**self.config.get("llm", {}), **section}
                processors.append(cls(merged))
            elif name == "rewriter":
                merged = {**self.config.get("rewriter", {}), **section}
                processors.append(cls(merged))
            else:
                processors.append(cls(section))
        return processors

    async def _fetch_all(self, topic: str) -> list[Article]:
        """Fetch articles from all sources concurrently."""
        if not self.sources:
            logger.warning("No sources configured.")
            return []

        tasks = [source.fetch(topic) for source in self.sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        articles: list[Article] = []
        for result in results:
            if isinstance(result, Exception):
                logger.error("Source fetch failed: %s", result)
                continue
            articles.extend(result)

        logger.info("Fetched %d articles from %d source(s).", len(articles), len(self.sources))
        return articles

    def _process(self, articles: list[Article], topic: str) -> list[Article]:
        """Run articles through the processor chain."""
        for proc in self.processors:
            articles = proc.process(articles, topic)
        return articles

    def _format(self, digest: Digest, fmt: str | None = None) -> str:
        """Format the digest using the configured or overridden formatter."""
        fmt = fmt or self.config.get("output", {}).get("format", "markdown")
        formatter_cls = FORMATTER_REGISTRY.get(fmt)
        if formatter_cls is None:
            logger.warning("Unknown format '%s', falling back to markdown.", fmt)
            formatter_cls = FORMATTER_REGISTRY["markdown"]
        return formatter_cls().format(digest)

    async def run_async(self, topic: str, fmt: str | None = None) -> str:
        """Execute the full pipeline asynchronously and return formatted output."""
        articles = await self._fetch_all(topic)
        articles = self._process(articles, topic)

        digest = Digest(
            topic=topic,
            articles=articles,
            generated_at=datetime.utcnow(),
            metadata={"source_count": len(self.sources)},
        )

        return self._format(digest, fmt)

    def run(self, topic: str, fmt: str | None = None) -> str:
        """Synchronous convenience wrapper around *run_async*."""
        return asyncio.run(self.run_async(topic, fmt))
