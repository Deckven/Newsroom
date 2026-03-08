"""
Telegram publisher — sends messages via Bot API.

Supports plain text and HTML formatting.
Long messages are automatically split at 4096 chars.
"""

from __future__ import annotations

from typing import Any

import requests

from newsroom.publisher.base import BasePublisher, PublishResult
from newsroom.publisher.config import TelegramConfig

_MAX_LENGTH = 4096


class TelegramPublisher(BasePublisher):
    """Publish messages to a Telegram chat/channel."""

    platform = "telegram"

    def __init__(self, config: TelegramConfig | None = None) -> None:
        self.config = config or TelegramConfig.from_env()

    def publish(
        self,
        content: str,
        *,
        parse_mode: str = "HTML",
        disable_preview: bool = False,
        **kwargs: Any,
    ) -> PublishResult:
        """Send a message to a Telegram chat/channel.

        Args:
            content: Message text.
            parse_mode: "HTML" (default) or "Markdown".
            disable_preview: Disable link preview.
        """
        if not self.config:
            return self._fail("Telegram not configured. Set TELEGRAM_* env vars.")

        api_url = f"https://api.telegram.org/bot{self.config.bot_token}/sendMessage"

        # Split long messages
        chunks = self._split(content)
        message_ids = []

        for chunk in chunks:
            payload = {
                "chat_id": self.config.chat_id,
                "text": chunk,
                "parse_mode": parse_mode,
                "disable_web_page_preview": disable_preview,
            }
            try:
                resp = requests.post(api_url, json=payload, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                if data.get("ok"):
                    message_ids.append(str(data["result"]["message_id"]))
                else:
                    return self._fail(f"Telegram API error: {data.get('description')}")
            except requests.RequestException as e:
                return self._fail(f"Request failed: {e}")

        return PublishResult(
            platform=self.platform,
            success=True,
            post_id=",".join(message_ids),
            metadata={"message_count": len(chunks)},
        )

    @staticmethod
    def _split(text: str) -> list[str]:
        """Split text into chunks of at most _MAX_LENGTH chars."""
        if len(text) <= _MAX_LENGTH:
            return [text]
        chunks = []
        while text:
            if len(text) <= _MAX_LENGTH:
                chunks.append(text)
                break
            # Try to split at last newline within limit
            cut = text.rfind("\n", 0, _MAX_LENGTH)
            if cut == -1:
                cut = _MAX_LENGTH
            chunks.append(text[:cut])
            text = text[cut:].lstrip("\n")
        return chunks
