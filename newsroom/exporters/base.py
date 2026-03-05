"""Abstract base class for exporters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from newsroom.models import Digest


class BaseExporter(ABC):
    """Every exporter plugin must subclass this and implement *export*."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config

    @abstractmethod
    async def export(self, digest: Digest, formatted: str) -> str:
        """Export the digest to a destination.

        Returns a short status string (e.g. file path or URL).
        """
        ...
