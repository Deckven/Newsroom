"""Abstract base class for output formatters."""

from __future__ import annotations

from abc import ABC, abstractmethod

from newsroom.models import Digest


class BaseFormatter(ABC):
    """Every formatter must subclass this and implement *format*."""

    @abstractmethod
    def format(self, digest: Digest) -> str:
        """Render the digest into a string representation."""
        ...
