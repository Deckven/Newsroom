"""YAML configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

DEFAULTS: dict[str, Any] = {
    "sources": [],
    "processors": {
        "filter": {"enabled": True},
        "dedup": {"enabled": True, "similarity_threshold": 0.8},
        "llm": {"enabled": False},
        "rewriter": {"enabled": False},
    },
    "output": {
        "format": "markdown",
        "path": None,
    },
    "llm": {
        "provider": None,  # "openai" | "anthropic"
        "model": None,
        "api_key": None,
    },
    "rewriter": {
        "corpus_path": "rewriter_corpus.db",
        "intensity": "medium",
        "num_examples": 3,
        "max_article_length": 4000,
        "llm": {
            "api_key": None,
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4096,
        },
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base*, returning a new dict."""
    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file and merge with defaults."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}
    return _deep_merge(DEFAULTS, raw)


def validate_config(cfg: dict[str, Any]) -> list[str]:
    """Return a list of warnings/errors about the config (empty = OK)."""
    issues: list[str] = []
    if not cfg.get("sources"):
        issues.append("No sources defined — pipeline will produce no articles.")
    for i, src in enumerate(cfg.get("sources", [])):
        if "type" not in src:
            issues.append(f"Source #{i} is missing a 'type' field.")
    llm = cfg.get("llm", {})
    if cfg.get("processors", {}).get("llm", {}).get("enabled"):
        if not llm.get("provider"):
            issues.append("LLM processor is enabled but no provider is set.")
        if not llm.get("api_key"):
            issues.append("LLM processor is enabled but no api_key is set.")
    # Rewriter validation
    if cfg.get("processors", {}).get("rewriter", {}).get("enabled"):
        rw = cfg.get("rewriter", {})
        rw_api_key = rw.get("llm", {}).get("api_key")
        if not rw_api_key:
            issues.append("Rewriter is enabled but no rewriter.llm.api_key is set.")
        corpus_path = Path(rw.get("corpus_path", "rewriter_corpus.db"))
        if not corpus_path.exists():
            issues.append(
                f"Rewriter is enabled but corpus file '{corpus_path}' not found. "
                "Run `python -m newsroom rewriter-setup import` first."
            )
    return issues
