"""
Base publisher interface.

All platform publishers inherit from BasePublisher and implement
the `publish()` method.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PublishResult:
    """Result of a publish operation."""

    platform: str
    success: bool
    url: str | None = None
    post_id: str | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BasePublisher(ABC):
    """Abstract publisher for a single platform."""

    platform: str = "base"

    @abstractmethod
    def publish(self, content: str, **kwargs: Any) -> PublishResult:
        """Publish content to the platform.

        Args:
            content: Text content to publish.
            **kwargs: Platform-specific options (title, tags, draft, etc.)

        Returns:
            PublishResult with status and metadata.
        """

    def _fail(self, error: str) -> PublishResult:
        logger.error("[%s] %s", self.platform, error)
        return PublishResult(platform=self.platform, success=False, error=error)
