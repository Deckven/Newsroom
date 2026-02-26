"""Deduplication processor."""

from __future__ import annotations

import logging
from typing import Any

from newsroom.models import Article
from newsroom.processors.base import BaseProcessor
from newsroom.utils import text_similarity

logger = logging.getLogger(__name__)


class Deduplicator(BaseProcessor):
    """Remove duplicate articles by URL or title similarity."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.threshold: float = config.get("similarity_threshold", 0.8)

    def process(self, articles: list[Article], topic: str) -> list[Article]:
        seen_urls: set[str] = set()
        unique: list[Article] = []

        for article in articles:
            # Exact URL match
            if article.url in seen_urls:
                continue

            # Title similarity check against already-accepted articles
            is_dup = False
            for accepted in unique:
                if text_similarity(article.title, accepted.title) >= self.threshold:
                    is_dup = True
                    break

            if not is_dup:
                seen_urls.add(article.url)
                unique.append(article)

        removed = len(articles) - len(unique)
        if removed:
            logger.info("Deduplicator: removed %d duplicate(s).", removed)
        return unique
