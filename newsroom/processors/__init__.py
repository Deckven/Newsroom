"""Built-in article processors."""

from newsroom.processors.base import BaseProcessor
from newsroom.processors.dedup import Deduplicator
from newsroom.processors.filter import KeywordFilter
from newsroom.processors.llm import LLMSummarizer

PROCESSOR_REGISTRY: dict[str, type[BaseProcessor]] = {
    "filter": KeywordFilter,
    "dedup": Deduplicator,
    "llm": LLMSummarizer,
}

__all__ = [
    "BaseProcessor",
    "KeywordFilter",
    "Deduplicator",
    "LLMSummarizer",
    "PROCESSOR_REGISTRY",
]
