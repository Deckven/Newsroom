"""Built-in article processors."""

from newsroom.processors.base import BaseProcessor
from newsroom.processors.dedup import Deduplicator
from newsroom.processors.filter import KeywordFilter
from newsroom.processors.llm import LLMSummarizer
from newsroom.processors.rewriter import StyleRewriter

PROCESSOR_REGISTRY: dict[str, type[BaseProcessor]] = {
    "filter": KeywordFilter,
    "dedup": Deduplicator,
    "llm": LLMSummarizer,
    "rewriter": StyleRewriter,
}

__all__ = [
    "BaseProcessor",
    "KeywordFilter",
    "Deduplicator",
    "LLMSummarizer",
    "StyleRewriter",
    "PROCESSOR_REGISTRY",
]
