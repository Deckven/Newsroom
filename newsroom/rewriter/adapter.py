"""Bridge between Newsroom dict-config and Rewriter modules.

Replaces the original ``rewriter.config.Settings`` (Pydantic Settings)
with a plain object that reads everything from a ``dict``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal


class RewriterConfig:
    """Configuration facade consumed by every Rewriter sub-module.

    All values are extracted from the dict that Newsroom passes in.
    Sensible defaults mirror the original ``Settings`` class.
    """

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw

        # API -----------------------------------------------------------
        llm_section = raw.get("llm", {})
        self.anthropic_api_key: str = llm_section.get("api_key") or ""
        self.model: str = llm_section.get("model") or "claude-sonnet-4-20250514"
        self.analysis_model: str = llm_section.get("analysis_model") or self.model
        self.max_tokens: int = int(llm_section.get("max_tokens", 4096))
        self.temperature: float = float(llm_section.get("temperature", 0.7))

        # Paths ---------------------------------------------------------
        self.data_dir: Path = Path(raw.get("data_dir") or "rewriter_data")
        self.corpus_path: Path = Path(
            raw.get("corpus_path") or str(self.data_dir / "corpus.db")
        )

        # Import --------------------------------------------------------
        self.min_words: int = int(raw.get("min_words", 50))

        # Analysis ------------------------------------------------------
        self.sample_fraction: float = float(raw.get("sample_fraction", 0.18))
        self.chunk_max_tokens: int = int(raw.get("chunk_max_tokens", 90_000))
        self.chunk_articles: int = int(raw.get("chunk_articles", 12))
        self.n_clusters: int = int(raw.get("n_clusters", 25))

        # Rewrite -------------------------------------------------------
        self.intensity: Literal["light", "medium", "full"] = raw.get(
            "intensity", "medium"
        )  # type: ignore[assignment]
        self.n_examples: int = int(raw.get("num_examples", raw.get("n_examples", 3)))
        self.preserve_structure: bool = bool(raw.get("preserve_structure", False))
        self.max_article_length: int = int(raw.get("max_article_length", 4000))

    # Derived paths (mirror original Settings properties) ---------------

    @property
    def db_path(self) -> Path:
        return self.corpus_path

    @property
    def style_guide_md_path(self) -> Path:
        return self.data_dir / "style_guide.md"

    @property
    def style_guide_json_path(self) -> Path:
        return self.data_dir / "style_guide.json"

    @property
    def tfidf_model_path(self) -> Path:
        return self.data_dir / "tfidf_model.pkl"

    def ensure_data_dir(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
