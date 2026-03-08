"""
Facebook publisher — creates page posts via Graph API.

Posts are created as published or unpublished (scheduled/draft).
Requires a Page Access Token with pages_manage_posts permission.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import FacebookConfig

_GRAPH_API = "https://graph.facebook.com/v21.0"


class FacebookPublisher(BasePublisher):
    """Publish posts to a Facebook Page."""

    platform = "facebook"

    def __init__(self, config: FacebookConfig | None = None) -> None:
        self.config = config or FacebookConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        published: bool = True,
        link: str | None = None,
        **kwargs: Any,
    ) -> PublishResult:
        """Create a Facebook Page post.

        Args:
            content: Post text.
            published: If False, creates an unpublished (draft) post.
            link: Optional link to attach.
        """
        if not self.config:
            return self._fail("Facebook not configured. Set FACEBOOK_* env vars.")

        url = f"{_GRAPH_API}/{self.config.page_id}/feed"

        payload: dict[str, Any] = {
            "message": content,
            "access_token": self.config.page_token,
            "published": published,
        }
        if link:
            payload["link"] = link

        try:
            resp = requests.post(url, data=payload, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"Graph API failed: {e}")

        data = resp.json()
        post_id = data.get("id", "")

        if not post_id:
            error = data.get("error", {}).get("message", "Unknown error")
            return self._fail(f"Facebook error: {error}")

        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=post_id,
            url=f"https://facebook.com/{post_id}",
            metadata={"published": published},
        )
