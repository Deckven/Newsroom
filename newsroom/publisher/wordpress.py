"""
WordPress publisher — creates posts via REST API.

Posts are created as drafts by default so the editor can review
before publishing.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import WordPressConfig


class WordPressPublisher(BasePublisher):
    """Publish articles to a WordPress site via REST API."""

    platform = "wordpress"

    def __init__(self, config: WordPressConfig | None = None) -> None:
        self.config = config or WordPressConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        title: str = "Без заголовка",
        status: str = "draft",
        categories: list[int] | None = None,
        tags: list[int] | None = None,
        excerpt: str = "",
        featured_media: int | None = None,
        **kwargs: Any,
    ) -> PublishResult:
        """Create a WordPress post.

        Args:
            content: HTML content of the post.
            title: Post title.
            status: "draft" (default), "publish", "pending", "private".
            categories: List of category IDs.
            tags: List of tag IDs.
            excerpt: Short excerpt/description.
            featured_media: Media attachment ID for featured image.
        """
        if not self.config:
            return self._fail("WordPress not configured. Set WORDPRESS_* env vars.")

        api_url = f"{self.config.url.rstrip('/')}/wp-json/wp/v2/posts"

        payload: dict[str, Any] = {
            "title": title,
            "content": content,
            "status": status,
        }
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags
        if excerpt:
            payload["excerpt"] = excerpt
        if featured_media:
            payload["featured_media"] = featured_media

        try:
            resp = requests.post(
                api_url,
                json=payload,
                auth=(self.config.user, self.config.app_password),
                timeout=30,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"API request failed: {e}")

        data = resp.json()
        post_url = data.get("link", "")
        post_id = str(data.get("id", ""))

        return PublishResult(
            platform=self.platform,
            success=True,
            url=post_url,
            post_id=post_id,
            metadata={"status": status, "title": title},
        )
