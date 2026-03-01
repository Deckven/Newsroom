"""Corpus statistics utilities."""

from __future__ import annotations

import logging

from newsroom.rewriter.corpus.models import CorpusStats
from newsroom.rewriter.corpus.store import CorpusStore

logger = logging.getLogger(__name__)


def compute_stats(store: CorpusStore) -> CorpusStats:
    """Compute summary statistics for the corpus."""
    articles = store.get_all_articles()

    if not articles:
        return CorpusStats()

    word_counts = [a.word_count for a in articles]
    categories = store.get_categories_distribution()

    dates = [a.published_at for a in articles if a.published_at]
    date_range = None
    if dates:
        date_range = (
            min(dates).strftime("%Y-%m-%d"),
            max(dates).strftime("%Y-%m-%d"),
        )

    examples = store.get_examples()
    guide = store.get_latest_style_guide()

    return CorpusStats(
        total_articles=len(articles),
        total_words=sum(word_counts),
        avg_words=sum(word_counts) / len(word_counts),
        min_words=min(word_counts),
        max_words=max(word_counts),
        categories=categories,
        date_range=date_range,
        n_examples=len(examples),
        has_style_guide=guide is not None,
    )


def print_stats(stats: CorpusStats) -> None:
    """Print corpus statistics to stdout."""
    print(f"Total articles:    {stats.total_articles}")
    print(f"Total words:       {stats.total_words:,}")
    print(f"Avg words/article: {stats.avg_words:.0f}")
    print(f"Min words:         {stats.min_words}")
    print(f"Max words:         {stats.max_words}")

    if stats.date_range:
        print(f"Date range:        {stats.date_range[0]} -> {stats.date_range[1]}")

    print(f"Few-shot examples: {stats.n_examples}")
    print(f"Style guide:       {'Yes' if stats.has_style_guide else 'No'}")

    if stats.categories:
        print("\nCategories (top 20):")
        for cat, count in list(stats.categories.items())[:20]:
            print(f"  {cat}: {count}")
