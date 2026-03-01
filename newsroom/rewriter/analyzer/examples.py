"""TF-IDF clustering + few-shot example selection."""

from __future__ import annotations

import logging
from pathlib import Path

import joblib
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from newsroom.rewriter.adapter import RewriterConfig
from newsroom.rewriter.corpus.models import Article, FewShotExample
from newsroom.rewriter.corpus.store import CorpusStore

logger = logging.getLogger(__name__)


class ExampleSelector:
    """TF-IDF + K-Means based example selection and retrieval."""

    def __init__(self, settings: RewriterConfig, store: CorpusStore) -> None:
        self.settings = settings
        self.store = store
        self._vectorizer: TfidfVectorizer | None = None
        self._tfidf_matrix: np.ndarray | None = None
        self._article_ids: list[int] = []

    def build_clusters(self) -> list[FewShotExample]:
        """Build TF-IDF model, cluster articles, select representatives."""
        articles = self.store.get_all_articles()
        if not articles:
            raise RuntimeError("No articles in corpus")

        logger.info("Building TF-IDF model over %d articles...", len(articles))

        # Build TF-IDF
        texts = [f"{a.title} {a.content}" for a in articles]
        self._article_ids = [a.id for a in articles]

        self._vectorizer = TfidfVectorizer(
            max_features=10_000,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        self._tfidf_matrix = self._vectorizer.fit_transform(texts)

        # K-Means clustering
        n_clusters = min(self.settings.n_clusters, len(articles))
        logger.info("Clustering into %d groups...", n_clusters)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(self._tfidf_matrix)

        # Select closest to centroid from each cluster
        examples: list[FewShotExample] = []
        for cluster_id in range(n_clusters):
            mask = labels == cluster_id
            indices = np.where(mask)[0]

            if len(indices) == 0:
                continue

            cluster_vectors = self._tfidf_matrix[indices]
            centroid = kmeans.cluster_centers_[cluster_id].reshape(1, -1)
            distances = cosine_similarity(cluster_vectors, centroid).flatten()

            best_idx = indices[np.argmax(distances)]
            article_id = self._article_ids[best_idx]

            examples.append(
                FewShotExample(
                    article_id=article_id,
                    cluster_id=cluster_id,
                    distance_to_centroid=float(1 - distances[np.argmax(distances)]),
                )
            )

        # Save
        self.store.save_examples(examples)
        self._save_model()

        logger.info("Selected %d representative examples", len(examples))
        return examples

    def find_similar(self, text: str, n: int = 3) -> list[Article]:
        """Find the most similar example articles to the given text."""
        self._ensure_model()

        example_ids = set(self.store.get_example_article_ids())
        if not example_ids:
            raise RuntimeError(
                "No examples selected. Run `python -m newsroom rewriter-setup analyze` first."
            )

        # Transform input
        input_vec = self._vectorizer.transform([text])

        # Find example indices
        example_indices = [
            i for i, aid in enumerate(self._article_ids) if aid in example_ids
        ]

        if not example_indices:
            raise RuntimeError("Example articles not found in TF-IDF model")

        example_matrix = self._tfidf_matrix[example_indices]
        similarities = cosine_similarity(input_vec, example_matrix).flatten()

        # Top-n
        top_n = min(n, len(example_indices))
        top_idx = np.argsort(similarities)[-top_n:][::-1]

        article_ids = [self._article_ids[example_indices[i]] for i in top_idx]
        return self.store.get_articles_by_ids(article_ids)

    def _save_model(self) -> None:
        """Persist TF-IDF model to disk."""
        self.settings.ensure_data_dir()
        model_data = {
            "vectorizer": self._vectorizer,
            "tfidf_matrix": self._tfidf_matrix,
            "article_ids": self._article_ids,
        }
        joblib.dump(model_data, str(self.settings.tfidf_model_path))
        logger.debug("TF-IDF model saved to %s", self.settings.tfidf_model_path)

    def _ensure_model(self) -> None:
        """Load TF-IDF model from disk if not in memory."""
        if self._vectorizer is not None and self._tfidf_matrix is not None:
            return

        model_path = self.settings.tfidf_model_path
        if not model_path.exists():
            raise RuntimeError(
                f"TF-IDF model not found at {model_path}. "
                "Run `python -m newsroom rewriter-setup analyze` first."
            )

        model_data = joblib.load(str(model_path))
        self._vectorizer = model_data["vectorizer"]
        self._tfidf_matrix = model_data["tfidf_matrix"]
        self._article_ids = model_data["article_ids"]
