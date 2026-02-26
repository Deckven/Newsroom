"""Data models for the Newsroom framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Article:
    """A single news article collected from any source."""

    title: str
    url: str
    source_name: str
    published_at: datetime | None = None
    content: str = ""
    summary: str = ""
    tags: list[str] = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Article):
            return NotImplemented
        return self.url == other.url


@dataclass
class Digest:
    """A collection of articles on a topic, ready for formatting."""

    topic: str
    articles: list[Article]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = field(default_factory=dict)
