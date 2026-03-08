"""
Newsroom Publisher — multi-platform content distribution.

Usage:
    from newsroom.publisher import publish, publish_many

    # Single platform
    result = publish("wordpress", content, title="My Post", status="draft")

    # Multiple platforms at once
    results = publish_many(
        ["telegram", "discord", "twitter"],
        content,
        twitter_kwargs={"as_thread": True},
    )
"""

from __future__ import annotations

from typing import Any

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.discord import DiscordPublisher
from newsroom.publisher.facebook import FacebookPublisher
from newsroom.publisher.instagram import InstagramPublisher
from newsroom.publisher.linkedin import LinkedInPublisher
from newsroom.publisher.reddit import RedditPublisher
from newsroom.publisher.telegram import TelegramPublisher
from newsroom.publisher.twitter import TwitterPublisher
from newsroom.publisher.wordpress import WordPressPublisher

__all__ = [
    "PublishResult",
    "publish",
    "publish_many",
    "get_publisher",
    "available_platforms",
]

_REGISTRY: dict[str, type[BasePublisher]] = {
    "wordpress": WordPressPublisher,
    "telegram": TelegramPublisher,
    "discord": DiscordPublisher,
    "twitter": TwitterPublisher,
    "linkedin": LinkedInPublisher,
    "reddit": RedditPublisher,
    "facebook": FacebookPublisher,
    "instagram": InstagramPublisher,
}


def available_platforms() -> list[str]:
    """Return list of supported platform names."""
    return list(_REGISTRY.keys())


def get_publisher(platform: str) -> BasePublisher:
    """Create a publisher instance for the given platform."""
    cls = _REGISTRY.get(platform)
    if cls is None:
        raise ValueError(
            f"Unknown platform '{platform}'. "
            f"Available: {', '.join(_REGISTRY)}"
        )
    return cls()


def publish(platform: str, content: str, **kwargs: Any) -> PublishResult:
    """Publish content to a single platform.

    Args:
        platform: Platform name (wordpress, telegram, discord, etc.)
        content: Text content to publish.
        **kwargs: Platform-specific options.

    Returns:
        PublishResult with status and metadata.
    """
    publisher = get_publisher(platform)
    return publisher.publish(content, **kwargs)


def publish_many(
    platforms: list[str],
    content: str,
    **per_platform_kwargs: Any,
) -> dict[str, PublishResult]:
    """Publish content to multiple platforms.

    Per-platform kwargs can be passed as {platform}_kwargs dicts:
        publish_many(
            ["wordpress", "twitter"],
            content,
            wordpress_kwargs={"title": "My Post", "status": "draft"},
            twitter_kwargs={"as_thread": True},
        )

    Returns:
        Dict mapping platform name to PublishResult.
    """
    results = {}
    for platform in platforms:
        kwargs = per_platform_kwargs.get(f"{platform}_kwargs", {})
        results[platform] = publish(platform, content, **kwargs)
    return results
