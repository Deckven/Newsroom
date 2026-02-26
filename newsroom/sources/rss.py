"""RSS / Atom feed source."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import feedparser

from newsroom.models import Article
from newsroom.sources.base import BaseSource
from newsroom.utils import parse_date

logger = logging.getLogger(__name__)


class RSSSource(BaseSource):
    """Fetch articles from one or more RSS/Atom feeds."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.feeds: list[str] = config.get("feeds", [])
        self.name: str = config.get("name", "rss")

    async def fetch(self, topic: str) -> list[Article]:
        loop = asyncio.get_running_loop()
        tasks = [loop.run_in_executor(None, self._parse_feed, url) for url in self.feeds]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        articles: list[Article] = []
        for result in results:
            if isinstance(result, Exception):
                logger.warning("Failed to fetch RSS feed: %s", result)
                continue
            articles.extend(result)
        return articles

    def _parse_feed(self, url: str) -> list[Article]:
        feed = feedparser.parse(url)
        articles: list[Article] = []
        for entry in feed.entries:
            content = ""
            if hasattr(entry, "summary"):
                content = entry.summary
            elif hasattr(entry, "content"):
                content = entry.content[0].value if entry.content else ""

            articles.append(
                Article(
                    title=entry.get("title", "Untitled"),
                    url=entry.get("link", ""),
                    source_name=self.name,
                    published_at=parse_date(entry.get("published")),
                    content=content,
                    tags=[t.get("term", "") for t in entry.get("tags", [])],
                )
            )
        return articles
