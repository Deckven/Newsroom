"""
Instagram publisher — creates posts via Instagram Graph API.

Requires a Facebook Page linked to an Instagram Professional account.
Supports single image posts, carousels, and reels.

Note: Instagram Graph API does NOT support text-only posts.
An image_url (publicly accessible) is always required.
"""

from __future__ import annotations

import time
from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import InstagramConfig

_GRAPH_API = "https://graph.facebook.com/v21.0"


class InstagramPublisher(BasePublisher):
    """Publish posts to Instagram via Graph API."""

    platform = "instagram"

    def __init__(self, config: InstagramConfig | None = None) -> None:
        self.config = config or InstagramConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        image_url: str | None = None,
        image_urls: list[str] | None = None,
        video_url: str | None = None,
        is_reel: bool = False,
        **kwargs: Any,
    ) -> PublishResult:
        """Create an Instagram post.

        Args:
            content: Caption text.
            image_url: Public URL of the image (single image post).
            image_urls: List of public image URLs (carousel, 2-10 items).
            video_url: Public URL of the video (reel).
            is_reel: If True with video_url, publishes as Reel.
        """
        if not self.config:
            return self._fail("Instagram not configured. Set INSTAGRAM_* env vars.")

        if video_url:
            return self._publish_video(content, video_url, is_reel)
        if image_urls and len(image_urls) >= 2:
            return self._publish_carousel(content, image_urls)
        if image_url:
            return self._publish_single(content, image_url)
        if image_urls and len(image_urls) == 1:
            return self._publish_single(content, image_urls[0])

        return self._fail("Instagram requires image_url, image_urls, or video_url.")

    def _publish_single(self, caption: str, image_url: str) -> PublishResult:
        """Single image post."""
        container = self._create_container(
            image_url=image_url, caption=caption
        )
        if container is None:
            return self._fail("Failed to create media container.")
        return self._publish_container(container)

    def _publish_carousel(
        self, caption: str, image_urls: list[str]
    ) -> PublishResult:
        """Carousel post (2-10 images)."""
        if len(image_urls) > 10:
            return self._fail("Carousel supports max 10 images.")

        children_ids = []
        for url in image_urls:
            child = self._create_container(image_url=url, is_carousel_item=True)
            if child is None:
                return self._fail(f"Failed to create carousel item for {url}")
            children_ids.append(child)

        # Create carousel container
        resp = self._api_post(
            f"/{self.config.user_id}/media",
            {
                "media_type": "CAROUSEL",
                "caption": caption,
                "children": ",".join(children_ids),
            },
        )
        if resp is None:
            return self._fail("Failed to create carousel container.")

        container_id = resp.get("id")
        if not container_id:
            return self._fail("No container ID in carousel response.")
        return self._publish_container(container_id)

    def _publish_video(
        self, caption: str, video_url: str, is_reel: bool
    ) -> PublishResult:
        """Video / Reel post."""
        params: dict[str, Any] = {
            "video_url": video_url,
            "caption": caption,
            "media_type": "REELS" if is_reel else "VIDEO",
        }
        resp = self._api_post(f"/{self.config.user_id}/media", params)
        if resp is None:
            return self._fail("Failed to create video container.")

        container_id = resp.get("id")
        if not container_id:
            return self._fail("No container ID in video response.")

        # Videos need processing time
        if not self._wait_for_container(container_id):
            return self._fail("Video processing timed out.")

        return self._publish_container(container_id)

    def _create_container(
        self,
        *,
        image_url: str,
        caption: str | None = None,
        is_carousel_item: bool = False,
    ) -> str | None:
        """Create a media container, return container ID or None."""
        params: dict[str, Any] = {"image_url": image_url}
        if caption:
            params["caption"] = caption
        if is_carousel_item:
            params["is_carousel_item"] = "true"

        resp = self._api_post(f"/{self.config.user_id}/media", params)
        if resp is None:
            return None
        return resp.get("id")

    def _publish_container(self, container_id: str) -> PublishResult:
        """Publish a ready container."""
        resp = self._api_post(
            f"/{self.config.user_id}/media_publish",
            {"creation_id": container_id},
        )
        if resp is None:
            return self._fail("Failed to publish media container.")

        post_id = resp.get("id", "")
        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=post_id,
            url=f"https://www.instagram.com/p/{post_id}/",
            metadata={"container_id": container_id},
        )

    def _wait_for_container(
        self, container_id: str, timeout: int = 60, interval: int = 5
    ) -> bool:
        """Poll container status until FINISHED or timeout."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            resp = self._api_get(
                f"/{container_id}",
                {"fields": "status_code"},
            )
            if resp and resp.get("status_code") == "FINISHED":
                return True
            if resp and resp.get("status_code") == "ERROR":
                return False
            time.sleep(interval)
        return False

    def _api_post(
        self, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any] | None:
        """POST to Graph API with access token."""
        params["access_token"] = self.config.access_token
        try:
            resp = requests.post(
                f"{_GRAPH_API}{endpoint}", data=params, timeout=30
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            self._fail(f"Instagram API error: {e}")
            return None

    def _api_get(
        self, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any] | None:
        """GET from Graph API with access token."""
        params["access_token"] = self.config.access_token
        try:
            resp = requests.get(
                f"{_GRAPH_API}{endpoint}", params=params, timeout=15
            )
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            return None
