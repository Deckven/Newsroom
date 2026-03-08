"""
Twitter/X publisher — posts tweets via API v2.

Supports single tweets and threads. Uses OAuth 1.0a (User Context).
Requires a paid API plan (Basic or higher).
"""

from __future__ import annotations

import hashlib
import hmac
import time
import urllib.parse
import uuid
from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import TwitterConfig

_MAX_TWEET = 280


class TwitterPublisher(BasePublisher):
    """Publish tweets/threads to Twitter/X."""

    platform = "twitter"

    def __init__(self, config: TwitterConfig | None = None) -> None:
        self.config = config or TwitterConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        as_thread: bool = False,
        **kwargs: Any,
    ) -> PublishResult:
        """Post a tweet or thread.

        Args:
            content: Tweet text. If as_thread=True, split by double newline
                     into separate tweets.
            as_thread: If True, post as a thread (each paragraph = tweet).
        """
        if not self.config:
            return self._fail("Twitter not configured. Set TWITTER_* env vars.")

        if as_thread:
            parts = [p.strip() for p in content.split("\n\n") if p.strip()]
        else:
            parts = [content[:_MAX_TWEET]]

        tweet_ids = []
        reply_to: str | None = None

        for part in parts:
            result = self._post_tweet(part, reply_to=reply_to)
            if not result.success:
                return result
            tweet_ids.append(result.post_id)
            reply_to = result.post_id

        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=tweet_ids[0],
            url=f"https://x.com/i/status/{tweet_ids[0]}" if tweet_ids[0] else None,
            metadata={"tweet_count": len(tweet_ids), "tweet_ids": tweet_ids},
        )

    def _post_tweet(
        self, text: str, reply_to: str | None = None,
    ) -> PublishResult:
        url = "https://api.x.com/2/tweets"
        payload: dict[str, Any] = {"text": text[:_MAX_TWEET]}
        if reply_to:
            payload["reply"] = {"in_reply_to_tweet_id": reply_to}

        headers = self._oauth_headers("POST", url, self.config)  # type: ignore[arg-type]
        headers["Content-Type"] = "application/json"

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"Tweet failed: {e}")

        data = resp.json().get("data", {})
        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=data.get("id"),
        )

    @staticmethod
    def _oauth_headers(method: str, url: str, config: TwitterConfig) -> dict[str, str]:
        """Generate OAuth 1.0a authorization header."""
        oauth_params = {
            "oauth_consumer_key": config.api_key,
            "oauth_nonce": uuid.uuid4().hex,
            "oauth_signature_method": "HMAC-SHA256",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": config.access_token,
            "oauth_version": "1.0",
        }

        # Build signature base string
        params_str = "&".join(
            f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
            for k, v in sorted(oauth_params.items())
        )
        base_string = (
            f"{method.upper()}&"
            f"{urllib.parse.quote(url, safe='')}&"
            f"{urllib.parse.quote(params_str, safe='')}"
        )

        signing_key = (
            f"{urllib.parse.quote(config.api_secret, safe='')}&"
            f"{urllib.parse.quote(config.access_secret, safe='')}"
        )

        signature = hmac.new(
            signing_key.encode(), base_string.encode(), hashlib.sha256,
        ).digest()

        import base64
        oauth_params["oauth_signature"] = base64.b64encode(signature).decode()

        auth_header = "OAuth " + ", ".join(
            f'{k}="{urllib.parse.quote(v, safe="")}"'
            for k, v in sorted(oauth_params.items())
        )
        return {"Authorization": auth_header}
