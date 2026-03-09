"""YAML configuration loading and validation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger(__name__)

# Per-domain default source directories
DOMAIN_SOURCE_DIRS: dict[str, list[str]] = {
    "wowcasual": [
        "sources/wowcasual/diablo_iv_sources",
        "sources/wowcasual/eve_online_sources",
        "sources/wowcasual/wow_sources",
        "sources/wowcasual/ghost_of_yotei_sources",
        "sources/wowcasual/general_gaming_sources",
        "sources/wowcasual/videogames_sources",
    ],
    "technocrats": [
        "sources/technocrats/technology_sources",
    ],
}

DEFAULTS: dict[str, Any] = {
    "domain": None,  # "wowcasual" | "technocrats"
    "source_dirs": [],
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
        "data_dir": None,
        "corpus_path": None,
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


def _resolve_domain(raw: dict[str, Any]) -> dict[str, Any]:
    """Fill in domain-dependent defaults (source_dirs, rewriter paths)."""
    domain = raw.get("domain")
    if not domain:
        return raw

    # Auto-fill source_dirs if not explicitly provided
    if "source_dirs" not in raw:
        raw["source_dirs"] = list(DOMAIN_SOURCE_DIRS.get(domain, []))

    # Auto-fill rewriter paths if not explicitly provided
    rw = raw.setdefault("rewriter", {})
    if "data_dir" not in rw:
        rw["data_dir"] = f"rewriter_data/{domain}"
    if "corpus_path" not in rw:
        rw["corpus_path"] = f"rewriter_data/{domain}/corpus.db"

    return raw


def load_config(path: str | Path, *, domain: str | None = None) -> dict[str, Any]:
    """Load a YAML config file and merge with defaults."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh) or {}

    # CLI domain override takes precedence
    if domain:
        raw["domain"] = domain

    # Resolve domain-dependent defaults before merging
    _resolve_domain(raw)

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
        corpus_path_str = rw.get("corpus_path")
        if not corpus_path_str:
            issues.append(
                "Rewriter is enabled but no corpus_path is set. "
                "Set 'domain' or 'rewriter.corpus_path' in config."
            )
        elif not Path(corpus_path_str).exists():
            issues.append(
                f"Rewriter is enabled but corpus file '{corpus_path_str}' not found. "
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
