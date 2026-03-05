"""Obsidian vault exporter — writes digest results as .md files."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from newsroom.exporters.base import BaseExporter
from newsroom.models import Digest

logger = logging.getLogger(__name__)


class ObsidianExporter(BaseExporter):
    """Export digest results into an Obsidian vault.

    Config keys:
        vault_path:        Absolute path to the vault root (required).
        output_folder:     Sub-folder for output (default: "Newsroom/Digests").
        mode:              "single_file" or "per_article" (default: "single_file").
        date_in_filename:  Include date in filename (default: true).
        frontmatter:
            extra_tags:    Tags to add to every generated note.
            properties:    Extra key-value pairs for YAML frontmatter.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.vault_path = Path(config["vault_path"])
        self.output_folder: str = config.get("output_folder", "Newsroom/Digests")
        self.mode: str = config.get("mode", "single_file")
        self.date_in_filename: bool = config.get("date_in_filename", True)
        self.fm_cfg: dict[str, Any] = config.get("frontmatter", {})

    async def export(self, digest: Digest, formatted: str) -> str:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._export_sync, digest, formatted)

    # -- private helpers -----------------------------------------------------

    def _export_sync(self, digest: Digest, formatted: str) -> str:
        out_dir = self.vault_path / self.output_folder
        out_dir.mkdir(parents=True, exist_ok=True)

        if self.mode == "per_article":
            return self._export_per_article(digest, out_dir)
        return self._export_single_file(digest, formatted, out_dir)

    def _make_filename(self, topic: str, suffix: str = "") -> str:
        """Build a filename from topic and optional date prefix."""
        safe_topic = "".join(c if c.isalnum() or c in " -_" else "" for c in topic).strip()
        safe_topic = safe_topic.replace(" ", "-")
        if self.date_in_filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            return f"{date_str}-{safe_topic}{suffix}.md"
        return f"{safe_topic}{suffix}.md"

    def _build_frontmatter(self, extra: dict[str, Any] | None = None) -> str:
        """Build YAML frontmatter string."""
        fm: dict[str, Any] = {}

        # Extra tags
        tags = list(self.fm_cfg.get("extra_tags", []))
        if tags:
            fm["tags"] = tags

        # Custom properties
        props = self.fm_cfg.get("properties", {})
        fm.update(props)

        # Caller-provided overrides
        if extra:
            fm.update(extra)

        if not fm:
            return ""

        lines = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
        return f"---\n{lines}\n---\n\n"

    # -- single_file mode ----------------------------------------------------

    def _export_single_file(self, digest: Digest, formatted: str, out_dir: Path) -> str:
        filename = self._make_filename(digest.topic)
        fp = out_dir / filename

        frontmatter = self._build_frontmatter({
            "title": f"Digest: {digest.topic}",
            "date": digest.generated_at.strftime("%Y-%m-%d"),
            "article_count": len(digest.articles),
        })

        fp.write_text(frontmatter + formatted, encoding="utf-8")
        logger.info("Obsidian exporter: wrote single file %s", fp)
        return str(fp)

    # -- per_article mode ----------------------------------------------------

    def _export_per_article(self, digest: Digest, out_dir: Path) -> str:
        folder_name = self._make_filename(digest.topic).replace(".md", "")
        article_dir = out_dir / folder_name
        article_dir.mkdir(parents=True, exist_ok=True)

        written: list[str] = []
        for i, article in enumerate(digest.articles, 1):
            safe_title = "".join(
                c if c.isalnum() or c in " -_" else "" for c in article.title
            ).strip()[:80]
            safe_title = safe_title.replace(" ", "-") or f"article-{i}"
            filename = f"{safe_title}.md"

            frontmatter = self._build_frontmatter({
                "title": article.title,
                "source": article.source_name,
                "url": article.url,
                "date": article.published_at.strftime("%Y-%m-%d") if article.published_at else None,
                "tags": article.tags + list(self.fm_cfg.get("extra_tags", [])),
            })

            body = article.summary or article.content or ""
            content = f"{frontmatter}# {article.title}\n\n{body}\n"
            if article.url:
                content += f"\n[Source]({article.url})\n"

            fp = article_dir / filename
            fp.write_text(content, encoding="utf-8")
            written.append(safe_title)

        # MOC (Map of Content) with wikilinks
        moc_filename = f"_MOC-{folder_name}.md"
        moc_frontmatter = self._build_frontmatter({
            "title": f"MOC: {digest.topic}",
            "date": digest.generated_at.strftime("%Y-%m-%d"),
            "article_count": len(digest.articles),
        })
        moc_lines = [
            f"{moc_frontmatter}# {digest.topic} — Map of Content\n",
            f"Generated: {digest.generated_at.strftime('%Y-%m-%d %H:%M')}\n",
            f"Articles: {len(digest.articles)}\n\n",
        ]
        for name in written:
            moc_lines.append(f"- [[{name}]]\n")

        moc_path = article_dir / moc_filename
        moc_path.write_text("".join(moc_lines), encoding="utf-8")

        logger.info("Obsidian exporter: wrote %d articles + MOC to %s",
                     len(written), article_dir)
        return str(article_dir)
