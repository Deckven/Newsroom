"""Plain-text output formatter."""

from __future__ import annotations

from newsroom.formatters.base import BaseFormatter
from newsroom.models import Digest


class PlainTextFormatter(BaseFormatter):
    """Render a digest as plain text."""

    def format(self, digest: Digest) -> str:
        lines: list[str] = []
        lines.append(f"NEWS DIGEST: {digest.topic.upper()}")
        lines.append(f"Generated: {digest.generated_at:%Y-%m-%d %H:%M UTC}")
        lines.append(f"Articles: {len(digest.articles)}")
        lines.append("=" * 60)
        lines.append("")

        for i, article in enumerate(digest.articles, 1):
            lines.append(f"[{i}] {article.title}")
            lines.append(f"    Source: {article.source_name}")
            if article.published_at:
                lines.append(f"    Date:   {article.published_at:%Y-%m-%d}")
            if article.url:
                lines.append(f"    URL:    {article.url}")
            if article.summary:
                lines.append(f"    Summary: {article.summary}")
            elif article.content:
                preview = article.content[:200].replace("\n", " ")
                if len(article.content) > 200:
                    preview += "\u2026"
                lines.append(f"    {preview}")
            if article.tags:
                lines.append(f"    Tags: {', '.join(article.tags)}")
            lines.append("-" * 60)
            lines.append("")

        return "\n".join(lines)
