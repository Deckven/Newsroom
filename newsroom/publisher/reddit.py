"""
Reddit publisher — submits posts via Reddit API (OAuth2).

Creates text (self) posts in a target subreddit.
Requires a Reddit "script" app with username/password auth.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import RedditConfig

_AUTH_URL = "https://www.reddit.com/api/v1/access_token"
_API_BASE = "https://oauth.reddit.com"
_USER_AGENT = "Newsroom/1.0"


class RedditPublisher(BasePublisher):
    """Publish text posts to a Reddit subreddit."""

    platform = "reddit"

    def __init__(self, config: RedditConfig | None = None) -> None:
        self.config = config or RedditConfig.from_env()
        self._token: str | None = None

    def _authenticate(self) -> str | None:
        """Obtain an OAuth2 bearer token."""
        if not self.config:
            return None
        try:
            resp = requests.post(
                _AUTH_URL,
                auth=(self.config.client_id, self.config.client_secret),
                data={
                    "grant_type": "password",
                    "username": self.config.username,
                    "password": self.config.password,
                },
                headers={"User-Agent": _USER_AGENT},
                timeout=15,
            )
            resp.raise_for_status()
            self._token = resp.json().get("access_token")
            return self._token
        except requests.RequestException:
            return None

    def publish(
        self,
        content: str,
        *,
        title: str = "Без заголовка",
        subreddit: str | None = None,
        flair_id: str | None = None,
        **kwargs: Any,
    ) -> PublishResult:
        """Submit a text post to a subreddit.

        Args:
            content: Post body (Markdown).
            title: Post title.
            subreddit: Override target subreddit (without r/).
            flair_id: Optional flair ID.
        """
        if not self.config:
            return self._fail("Reddit not configured. Set REDDIT_* env vars.")

        token = self._token or self._authenticate()
        if not token:
            return self._fail("Reddit authentication failed.")

        sub = subreddit or self.config.subreddit
        payload: dict[str, Any] = {
            "sr": sub,
            "kind": "self",
            "title": title,
            "text": content,
        }
        if flair_id:
            payload["flair_id"] = flair_id

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": _USER_AGENT,
        }

        try:
            resp = requests.post(
                f"{_API_BASE}/api/submit",
                data=payload, headers=headers, timeout=15,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"Reddit submit failed: {e}")

        data = resp.json()
        # Reddit returns nested JSON
        post_data = data.get("json", {}).get("data", {})
        post_url = post_data.get("url", "")
        post_id = post_data.get("id", "")

        if not post_id:
            errors = data.get("json", {}).get("errors", [])
            if errors:
                return self._fail(f"Reddit errors: {errors}")

        return PublishResult(
            platform=self.platform,
            success=True,
            url=post_url,
            post_id=post_id,
            metadata={"subreddit": sub},
        )
