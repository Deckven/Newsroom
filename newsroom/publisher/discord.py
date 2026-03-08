"""
Discord publisher — sends messages via webhook.

Supports plain text and embeds. Long messages are split at 2000 chars.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import DiscordConfig

_MAX_LENGTH = 2000


class DiscordPublisher(BasePublisher):
    """Publish messages to a Discord channel via webhook."""

    platform = "discord"

    def __init__(self, config: DiscordConfig | None = None) -> None:
        self.config = config or DiscordConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        username: str = "Newsroom",
        embed_title: str | None = None,
        embed_color: int = 0x5865F2,
        **kwargs: Any,
    ) -> PublishResult:
        """Send a message to a Discord channel.

        Args:
            content: Message text.
            username: Bot display name.
            embed_title: If set, sends as an embed instead of plain text.
            embed_color: Embed sidebar color (hex).
        """
        if not self.config:
            return self._fail("Discord not configured. Set DISCORD_WEBHOOK_URL env var.")

        if embed_title:
            return self._send_embed(content, embed_title, embed_color, username)

        # Plain text — split if needed
        chunks = self._split(content)
        for chunk in chunks:
            payload = {"content": chunk, "username": username}
            try:
                resp = requests.post(
                    self.config.webhook_url, json=payload, timeout=15,
                )
                resp.raise_for_status()
            except requests.RequestException as e:
                return self._fail(f"Webhook request failed: {e}")

        return PublishResult(
            platform=self.platform,
            success=True,
            metadata={"message_count": len(chunks)},
        )

    def _send_embed(
        self, content: str, title: str, color: int, username: str,
    ) -> PublishResult:
        # Embed description limit is 4096
        desc = content[:4096]
        payload = {
            "username": username,
            "embeds": [{"title": title, "description": desc, "color": color}],
        }
        try:
            resp = requests.post(
                self.config.webhook_url, json=payload, timeout=15,  # type: ignore[union-attr]
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return self._fail(f"Webhook request failed: {e}")

        return PublishResult(platform=self.platform, success=True)

    @staticmethod
    def _split(text: str) -> list[str]:
        if len(text) <= _MAX_LENGTH:
            return [text]
        chunks = []
        while text:
            if len(text) <= _MAX_LENGTH:
                chunks.append(text)
                break
            cut = text.rfind("\n", 0, _MAX_LENGTH)
            if cut == -1:
                cut = _MAX_LENGTH
            chunks.append(text[:cut])
            text = text[cut:].lstrip("\n")
        return chunks
