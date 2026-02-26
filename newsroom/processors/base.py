"""Abstract base class for article processors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from newsroom.models import Article


class BaseProcessor(ABC):
    """Every processor must subclass this and implement *process*."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    def process(self, articles: list[Article], topic: str) -> list[Article]:
        """Process / filter / transform a list of articles and return the result."""
        ...
