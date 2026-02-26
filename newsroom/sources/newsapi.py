"""NewsAPI.org source."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import requests

from newsroom.models import Article
from newsroom.sources.base import BaseSource
from newsroom.utils import parse_date

logger = logging.getLogger(__name__)

NEWSAPI_URL = "https://newsapi.org/v2/everything"


class NewsAPISource(BaseSource):
    """Fetch articles from the NewsAPI.org service (requires an API key)."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.api_key: str = config.get("api_key", "")
        self.page_size: int = config.get("page_size", 20)
        self.language: str = config.get("language", "en")
        self.sort_by: str = config.get("sort_by", "publishedAt")
        self.name: str = config.get("name", "newsapi")

    async def fetch(self, topic: str) -> list[Article]:
        if not self.api_key:
            logger.warning("NewsAPI source skipped — no api_key configured.")
            return []
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._query, topic)

    def _query(self, topic: str) -> list[Article]:
        params = {
            "q": topic,
            "pageSize": self.page_size,
            "language": self.language,
            "sortBy": self.sort_by,
            "apiKey": self.api_key,
        }
        resp = requests.get(NEWSAPI_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "ok":
            logger.error("NewsAPI error: %s", data.get("message", "unknown"))
            return []

        articles: list[Article] = []
        for item in data.get("articles", []):
            articles.append(
                Article(
                    title=item.get("title", "Untitled"),
                    url=item.get("url", ""),
                    source_name=item.get("source", {}).get("name", self.name),
                    published_at=parse_date(item.get("publishedAt")),
                    content=item.get("content", "") or item.get("description", ""),
                )
            )
        return articles
