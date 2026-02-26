"""Keyword-based relevance filter."""

from __future__ import annotations

import logging
import re
from typing import Any

from newsroom.models import Article
from newsroom.processors.base import BaseProcessor

logger = logging.getLogger(__name__)


class KeywordFilter(BaseProcessor):
    """Keep only articles whose title or content match the topic keywords."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.extra_keywords: list[str] = config.get("keywords", [])

    def process(self, articles: list[Article], topic: str) -> list[Article]:
        keywords = [topic.lower()] + [k.lower() for k in self.extra_keywords]
        patterns = [re.compile(re.escape(kw), re.IGNORECASE) for kw in keywords]

        filtered: list[Article] = []
        for article in articles:
            searchable = f"{article.title} {article.content}"
            if any(p.search(searchable) for p in patterns):
                filtered.append(article)

        logger.info(
            "KeywordFilter: kept %d / %d articles for topic '%s'",
            len(filtered),
            len(articles),
            topic,
        )
        return filtered
