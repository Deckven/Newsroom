"""JSON output formatter."""

from __future__ import annotations

import json
from typing import Any

from newsroom.formatters.base import BaseFormatter
from newsroom.models import Digest


class JSONFormatter(BaseFormatter):
    """Render a digest as a JSON document."""

    def format(self, digest: Digest) -> str:
        data: dict[str, Any] = {
            "topic": digest.topic,
            "generated_at": digest.generated_at.isoformat(),
            "article_count": len(digest.articles),
            "articles": [
                {
                    "title": a.title,
                    "url": a.url,
                    "source": a.source_name,
                    "published_at": a.published_at.isoformat() if a.published_at else None,
                    "summary": a.summary or None,
                    "content_preview": a.content[:500] if a.content else None,
                    "tags": a.tags,
                }
                for a in digest.articles
            ],
            "metadata": digest.metadata,
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
