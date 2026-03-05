"""Obsidian vault source — reads .md notes as Articles."""

from __future__ import annotations

import asyncio
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from newsroom.models import Article
from newsroom.sources.base import BaseSource
from newsroom.utils import parse_date

logger = logging.getLogger(__name__)

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_H1_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


class ObsidianSource(BaseSource):
    """Read markdown notes from an Obsidian vault and convert to Articles.

    Config keys:
        vault_path:      Absolute path to the vault root (required).
        folders:         List of sub-folders to scan (optional, default: entire vault).
        filter:
            tags:            Only include notes with at least one matching tag.
            frontmatter:     Key-value pairs that must match in frontmatter.
            modified_after:  ISO date string — skip files older than this.
        recursive:       Recurse into sub-folders (default: true).
    """

    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.vault_path = Path(config["vault_path"])
        self.folders: list[str] = config.get("folders", [])
        self.filter_cfg: dict[str, Any] = config.get("filter", {})
        self.recursive: bool = config.get("recursive", True)
        self.name: str = config.get("name", "obsidian")

    async def fetch(self, topic: str) -> list[Article]:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._read_vault)

    # -- private helpers -----------------------------------------------------

    def _read_vault(self) -> list[Article]:
        if not self.vault_path.is_dir():
            logger.error("Obsidian vault not found: %s", self.vault_path)
            return []

        articles: list[Article] = []
        for fp in self._collect_files():
            try:
                article, fm = self._parse_note(fp)
            except Exception:
                logger.debug("Failed to parse %s, skipping.", fp, exc_info=True)
                continue
            if self._matches_filters(article, fm, fp):
                articles.append(article)

        logger.info("Obsidian source '%s': loaded %d notes from %s.",
                     self.name, len(articles), self.vault_path)
        return articles

    def _collect_files(self) -> list[Path]:
        """Glob for *.md files in the configured folders (or entire vault)."""
        pattern = "**/*.md" if self.recursive else "*.md"
        roots: list[Path] = []
        if self.folders:
            for folder in self.folders:
                root = self.vault_path / folder
                if root.is_dir():
                    roots.append(root)
                else:
                    logger.warning("Obsidian folder not found: %s", root)
        else:
            roots.append(self.vault_path)

        files: list[Path] = []
        for root in roots:
            files.extend(root.glob(pattern))
        return sorted(files)

    def _parse_note(self, fp: Path) -> tuple[Article, dict[str, Any]]:
        """Parse a single .md file into an Article + raw frontmatter dict."""
        text = fp.read_text(encoding="utf-8")
        fm: dict[str, Any] = {}
        body = text

        m = _FRONTMATTER_RE.match(text)
        if m:
            fm = yaml.safe_load(m.group(1)) or {}
            body = text[m.end():]

        # Title: frontmatter → first H1 → filename
        title = fm.get("title")
        if not title:
            h1 = _H1_RE.search(body)
            title = h1.group(1).strip() if h1 else fp.stem

        # Tags: list or comma-separated string
        raw_tags = fm.get("tags", [])
        if isinstance(raw_tags, str):
            tags = [t.strip() for t in raw_tags.split(",") if t.strip()]
        else:
            tags = [str(t) for t in raw_tags]

        # Date
        published_at = parse_date(fm.get("date") or fm.get("created"))

        return Article(
            title=title,
            url=fp.as_uri(),
            source_name=self.name,
            published_at=published_at,
            content=body.strip(),
            tags=tags,
        ), fm

    def _matches_filters(
        self,
        article: Article,
        fm: dict[str, Any],
        fp: Path,
    ) -> bool:
        """Check whether the note passes user-configured filters."""
        flt = self.filter_cfg
        if not flt:
            return True

        # Tag filter (intersection)
        required_tags = flt.get("tags", [])
        if required_tags:
            article_tags_lower = {t.lower() for t in article.tags}
            if not article_tags_lower & {t.lower() for t in required_tags}:
                return False

        # Frontmatter key-value matching
        fm_filters = flt.get("frontmatter", {})
        for key, value in fm_filters.items():
            if str(fm.get(key, "")).lower() != str(value).lower():
                return False

        # Modified-after filter (file mtime)
        modified_after = flt.get("modified_after")
        if modified_after:
            cutoff = parse_date(modified_after)
            if cutoff:
                mtime = datetime.fromtimestamp(os.path.getmtime(fp))
                if mtime < cutoff:
                    return False

        return True
