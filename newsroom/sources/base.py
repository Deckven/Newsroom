"""Abstract base class for news sources."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from newsroom.models import Article


class BaseSource(ABC):
    """Every source plugin must subclass this and implement *fetch*."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    async def fetch(self, topic: str) -> list[Article]:
        """Fetch articles related to *topic* and return them."""
        ...
