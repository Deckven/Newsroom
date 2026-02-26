"""Markdown output formatter."""

from __future__ import annotations

from newsroom.formatters.base import BaseFormatter
from newsroom.models import Digest


class MarkdownFormatter(BaseFormatter):
    """Render a digest as a Markdown document."""

    def format(self, digest: Digest) -> str:
        lines: list[str] = []
        lines.append(f"# News Digest: {digest.topic}")
        lines.append(f"*Generated: {digest.generated_at:%Y-%m-%d %H:%M UTC}*")
        lines.append(f"*Articles: {len(digest.articles)}*\n")
        lines.append("---\n")

        for i, article in enumerate(digest.articles, 1):
            lines.append(f"## {i}. {article.title}")
            meta_parts: list[str] = [f"**Source:** {article.source_name}"]
            if article.published_at:
                meta_parts.append(f"**Date:** {article.published_at:%Y-%m-%d}")
            lines.append(" | ".join(meta_parts))

            if article.summary:
                lines.append(f"\n> {article.summary}\n")
            elif article.content:
                preview = article.content[:300]
                if len(article.content) > 300:
                    preview += "\u2026"
                lines.append(f"\n{preview}\n")

            if article.url:
                lines.append(f"[Read more]({article.url})\n")
            if article.tags:
                lines.append("Tags: " + ", ".join(f"`{t}`" for t in article.tags) + "\n")
            lines.append("---\n")

        return "\n".join(lines)
