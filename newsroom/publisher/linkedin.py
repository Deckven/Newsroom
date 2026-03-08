"""
LinkedIn publisher — creates posts via LinkedIn API v2.

Posts are created on behalf of a person or organization.
Requires an OAuth 2.0 access token with w_member_social scope.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import LinkedInConfig

_API_BASE = "https://api.linkedin.com/v2"


class LinkedInPublisher(BasePublisher):
    """Publish posts to LinkedIn."""

    platform = "linkedin"

    def __init__(self, config: LinkedInConfig | None = None) -> None:
        self.config = config or LinkedInConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        visibility: str = "PUBLIC",
        **kwargs: Any,
    ) -> PublishResult:
        """Create a LinkedIn post.

        Args:
            content: Post text (up to 3000 chars).
            visibility: "PUBLIC" (default) or "CONNECTIONS".
        """
        if not self.config:
            return self._fail("LinkedIn not configured. Set LINKEDIN_* env vars.")

        # Determine if person or organization
        person_id = self.config.person_id
        if person_id.startswith("urn:"):
            author = person_id
        else:
            author = f"urn:li:person:{person_id}"

        payload = {
            "author": author,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": content[:3000]},
                    "shareMediaCategory": "NONE",
                },
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility,
            },
        }

        headers = {
            "Authorization": f"Bearer {self.config.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        }

        try:
            resp = requests.post(
                f"{_API_BASE}/ugcPosts", json=payload,
                headers=headers, timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"LinkedIn API failed: {e}")

        data = resp.json()
        post_id = data.get("id", "")

        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=str(post_id),
            metadata={"visibility": visibility},
        )
