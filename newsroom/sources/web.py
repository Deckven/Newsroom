"""Web-scraping source using requests + BeautifulSoup."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import requests
from bs4 import BeautifulSoup

from newsroom.models import Article
from newsroom.sources.base import BaseSource
from newsroom.utils import parse_date

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; Newsroom/0.1; "
        "+https://github.com/newsroom)"
    ),
}


class WebSource(BaseSource):
    """Scrape articles from web pages using CSS selectors."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.sites: list[dict[str, Any]] = config.get("sites", [])
        self.name: str = config.get("name", "web")

    async def fetch(self, topic: str) -> list[Article]:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(None, self._scrape_site, site)
            for site in self.sites
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        articles: list[Article] = []
        for result in results:
            if isinstance(result, Exception):
                logger.warning("Failed to scrape site: %s", result)
                continue
            articles.extend(result)
        return articles

    def _scrape_site(self, site: dict[str, Any]) -> list[Article]:
        url = site["url"]
        selectors = site.get("selectors", {})
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        article_sel = selectors.get("article", "article")
        title_sel = selectors.get("title", "h2 a")
        content_sel = selectors.get("content", "p")
        date_sel = selectors.get("date", "time")

        articles: list[Article] = []
        for block in soup.select(article_sel):
            title_el = block.select_one(title_sel)
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            link = title_el.get("href", "")
            if link and not link.startswith("http"):
                link = url.rstrip("/") + "/" + link.lstrip("/")

            content_el = block.select_one(content_sel)
            content = content_el.get_text(strip=True) if content_el else ""

            date_el = block.select_one(date_sel)
            pub_date = None
            if date_el:
                pub_date = parse_date(date_el.get("datetime") or date_el.get_text(strip=True))

            articles.append(
                Article(
                    title=title,
                    url=link,
                    source_name=self.name,
                    published_at=pub_date,
                    content=content,
                )
            )
        return articles
