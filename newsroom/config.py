"""YAML configuration loading and validation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "source_dirs": [
        "sources/technology_sources",
        "sources/videogames_sources",
    ],
    "sources": [],
    "exporters": [],
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


def _load_source_dirs(dirs: list[str], base_path: Path) -> list[dict]:
    """Load source definitions from YAML files in *dirs*.

    Each directory is resolved relative to *base_path* (the folder that
    contains the main config file).  Files are sorted by name for
    deterministic ordering.
    """
    sources: list[dict] = []
    for dir_rel in dirs:
        dir_path = base_path / dir_rel
        if not dir_path.is_dir():
            log.debug("source_dirs: skipping %s (not a directory)", dir_path)
            continue
        dir_name = dir_path.name
        files = sorted(
            p for p in dir_path.iterdir()
            if p.suffix in (".yaml", ".yml") and p.is_file()
        )
        for fp in files:
            try:
                data = yaml.safe_load(fp.read_text(encoding="utf-8"))
            except Exception:
                log.warning("Failed to parse source file %s, skipping", fp)
                continue
            if not isinstance(data, dict):
                log.warning("Source file %s is not a mapping, skipping", fp)
                continue
            if "sources" in data:
                for src in data["sources"]:
                    src["_source_dir"] = dir_name
                    sources.append(src)
            elif "type" in data:
                data["_source_dir"] = dir_name
                sources.append(data)
            else:
                log.warning(
                    "Source file %s has neither 'type' nor 'sources' key, skipping",
                    fp,
                )
    return sources


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a YAML config file and merge with defaults."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    # Load modular sources from directories
    source_dirs = raw.get("source_dirs", DEFAULTS["source_dirs"])
    dir_sources = _load_source_dirs(source_dirs, path.parent)
    if dir_sources:
        inline = raw.get("sources", [])
        raw["sources"] = dir_sources + inline

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
    # Exporter validation
    for i, exp in enumerate(cfg.get("exporters", [])):
        if "type" not in exp:
            issues.append(f"Exporter #{i} is missing a 'type' field.")
            continue
        etype = exp["type"]
        if etype == "obsidian" and not exp.get("vault_path"):
            issues.append(f"Exporter #{i} (obsidian): 'vault_path' is required.")
        if etype == "gdrive":
            if not exp.get("folder_id"):
                issues.append(f"Exporter #{i} (gdrive): 'folder_id' is required.")
            creds = exp.get("credentials_path", "credentials.json")
            if not Path(creds).exists():
                issues.append(
                    f"Exporter #{i} (gdrive): credentials file '{creds}' not found."
                )
    return issues
