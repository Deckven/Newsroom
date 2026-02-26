"""Shared utilities for the Newsroom framework."""

from __future__ import annotations

import logging
from datetime import datetime
from difflib import SequenceMatcher

from dateutil import parser as dateutil_parser

logger = logging.getLogger("newsroom")


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the framework."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_date(value: str | datetime | None) -> datetime | None:
    """Best-effort date parsing. Returns None on failure."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        return dateutil_parser.parse(value)
    except (ValueError, TypeError):
        return None


def text_similarity(a: str, b: str) -> float:
    """Return a 0-1 similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def truncate(text: str, max_length: int = 300) -> str:
    """Truncate text to *max_length* characters, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "\u2026"
