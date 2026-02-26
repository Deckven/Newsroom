"""Built-in source plugins."""

from newsroom.sources.base import BaseSource
from newsroom.sources.newsapi import NewsAPISource
from newsroom.sources.rss import RSSSource
from newsroom.sources.web import WebSource

SOURCE_REGISTRY: dict[str, type[BaseSource]] = {
    "rss": RSSSource,
    "web": WebSource,
    "newsapi": NewsAPISource,
}

__all__ = [
    "BaseSource",
    "RSSSource",
    "WebSource",
    "NewsAPISource",
    "SOURCE_REGISTRY",
]
