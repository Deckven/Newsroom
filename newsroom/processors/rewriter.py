"""Style-transfer rewriting processor powered by the Rewriter engine."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from newsroom.models import Article
from newsroom.processors.base import BaseProcessor
from newsroom.utils import truncate

logger = logging.getLogger(__name__)


class StyleRewriter(BaseProcessor):
    """Rewrite article content in a personal blog style.

    Lazy-initializes the RewriteEngine so heavy dependencies (anthropic,
    scikit-learn, etc.) are only loaded when the processor actually runs.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self._engine = None  # lazy init
        self._init_error: str | None = None

    def _ensure_engine(self) -> bool:
        """Initialize the RewriteEngine on first use. Returns True if ready."""
        if self._engine is not None:
            return True
        if self._init_error is not None:
            return False

        # Check prerequisites
        api_key = self.config.get("llm", {}).get("api_key")
        if not api_key:
            self._init_error = "no api_key"
            logger.debug("Rewriter disabled: no API key configured.")
            return False

        corpus_path_str = self.config.get("corpus_path")
        if not corpus_path_str:
            self._init_error = "no corpus_path configured"
            logger.debug("Rewriter disabled: no corpus_path in config.")
            return False
        corpus_path = Path(corpus_path_str)
        if not corpus_path.exists():
            self._init_error = "no corpus"
            logger.debug("Rewriter disabled: corpus file %s not found.", corpus_path)
            return False

        try:
            from newsroom.rewriter.adapter import RewriterConfig
            from newsroom.rewriter.corpus.store import CorpusStore
            from newsroom.rewriter.engine import RewriteEngine

            settings = RewriterConfig(self.config)
            store = CorpusStore(settings.db_path)
            self._engine = RewriteEngine(settings, store)
            return True
        except Exception:
            self._init_error = "init failed"
            logger.warning("Rewriter init failed.", exc_info=True)
            return False

    def process(self, articles: list[Article], topic: str) -> list[Article]:
        if not self._ensure_engine():
            return articles

        max_length = self.config.get("max_article_length", 4000)
        rewritten = 0

        for article in articles:
            if "rewritten" in article.tags:
                continue
            if not article.content:
                continue

            try:
                text = truncate(article.content, max_length)
                result = self._engine.rewrite(text)
                article.content = result
                article.tags.append("rewritten")
                rewritten += 1
            except Exception:
                logger.warning(
                    "Rewrite failed for: %s", article.title, exc_info=True,
                )

        logger.info("Rewrote %d / %d articles.", rewritten, len(articles))
        return articles
