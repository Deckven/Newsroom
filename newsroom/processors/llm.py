"""Optional LLM-based summarization processor."""

from __future__ import annotations

import logging
from typing import Any

from newsroom.models import Article
from newsroom.processors.base import BaseProcessor
from newsroom.utils import truncate

logger = logging.getLogger(__name__)

SUMMARY_PROMPT = (
    "Summarize the following news article in 2-3 concise sentences. "
    "Focus on the key facts.\n\n"
    "Title: {title}\n\n"
    "Content:\n{content}"
)


class LLMSummarizer(BaseProcessor):
    """Generate article summaries using an LLM (OpenAI or Anthropic)."""

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.provider: str | None = config.get("provider")
        self.model: str | None = config.get("model")
        self.api_key: str | None = config.get("api_key")

    def process(self, articles: list[Article], topic: str) -> list[Article]:
        if not self.provider or not self.api_key:
            logger.debug("LLM summarizer disabled (no provider/key).")
            return articles

        for article in articles:
            if article.summary:
                continue
            try:
                article.summary = self._summarize(article)
            except Exception:
                logger.warning("LLM summary failed for: %s", article.title, exc_info=True)

        return articles

    def _summarize(self, article: Article) -> str:
        prompt = SUMMARY_PROMPT.format(
            title=article.title,
            content=truncate(article.content, 3000),
        )

        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            logger.warning("Unknown LLM provider: %s", self.provider)
            return ""

    def _call_openai(self, prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model or "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
        )
        return resp.choices[0].message.content or ""

    def _call_anthropic(self, prompt: str) -> str:
        import anthropic

        client = anthropic.Anthropic(api_key=self.api_key)
        resp = client.messages.create(
            model=self.model or "claude-haiku-4-5-20251001",
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text
