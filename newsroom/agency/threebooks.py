"""
Technocrats — Techno-futurological research agency.

Serves the ThreeBooks project — three interconnected non-fiction books:
  1. "Контуры расколотого мира" — futurology, geopolitics
  2. "Пятая информационная революция" — AI, quantum, neurointerfaces
  3. "Поколение двойного шторма" — Ukrainian generation X, war, independence

Editorial:    Корреспондент, Аналитик, Футуролог, Историограф, Рецензент
Production:   Фактчекер, Редактор, Рерайтер (provided by BaseAgency)
Distribution: SMM-менеджер, SEO-специалист, Комьюнити-менеджер (provided by BaseAgency)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from crewai import Agent, Task

from newsroom.agency import agents as role_factory
from newsroom.agency.base import BaseAgency

_REPORTER_REGISTRY: dict[str, Any] = {
    "корреспондент": role_factory.create_correspondent,
    "аналитик": role_factory.create_analyst,
    "футуролог": role_factory.create_futurologist,
    "историограф": role_factory.create_historiographer,
    "рецензент": role_factory.create_book_reviewer,
}

_BOOKS = {
    "book1": {
        "slug": "countors-fractured-world",
        "title": "Контуры расколотого мира",
        "focus": "футурология, геополитика, демография, климат, конфликты цивилизаций",
    },
    "book2": {
        "slug": "fifth-information-revolution",
        "title": "Пятая информационная революция",
        "focus": "ИИ, квантовые вычисления, нейроинтерфейсы, трансформация общества",
    },
    "book3": {
        "slug": "double-storm-generation",
        "title": "Поколение двойного шторма",
        "focus": "украинское поколение X, война с Россией, 35 лет независимости",
    },
}

# Default editorial roles for research-oriented work
_DEFAULT_ROLES = ["корреспондент", "аналитик", "футуролог"]


class TechnocratsAgency(BaseAgency):
    """Techno-futurological research agency for the ThreeBooks project."""

    name = "technocrats"

    def __init__(
        self,
        threebooks_path: str | Path = "M:/AIZoo/ThreeBooks/ThreeBooks",
        target_book: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.threebooks_path = Path(threebooks_path)
        self.target_book = target_book

    def _load_book_context(self, book_key: str) -> str:
        """Load outline and recent research for a book."""
        info = _BOOKS[book_key]
        book_dir = self.threebooks_path / info["slug"]

        sections = [f"Книга: {info['title']}\nФокус: {info['focus']}"]

        outline = book_dir / "outline.md"
        if outline.exists():
            text = outline.read_text(encoding="utf-8")
            if len(text) > 3000:
                text = text[:3000] + "\n...(обрезано)"
            sections.append(f"=== СТРУКТУРА КНИГИ ===\n{text}")

        return "\n\n".join(sections)

    def _build_context(self, topic: str, **kwargs: Any) -> str:
        book = kwargs.get("target_book", self.target_book)

        header = (
            "Ты работаешь в исследовательском агентстве Technocrats, "
            "обслуживающем проект ThreeBooks — три взаимосвязанные нон-фикшн книги.\n\n"
        )

        if book and book in _BOOKS:
            book_ctx = self._load_book_context(book)
            header += f"{book_ctx}\n\n"
        else:
            for key, info in _BOOKS.items():
                header += f"- {info['title']}: {info['focus']}\n"
            header += "\n"

        header += (
            f"Тема исследования: {topic}\n\n"
            f"Стандарт качества: каждое утверждение должно опираться на источник. "
            f"Оценка надёжности: high / medium / low / unverified. "
            f"Гипотезы должны содержать аргументы за и против.\n\n"
            f"Тон: экспертный, аналитический. "
            f"Соцсети: LinkedIn, Telegram, Twitter/X."
        )
        return header

    def _select_reporters(
        self,
        topic: str,
        context: str,
        roles: list[str] | None = None,
    ) -> list[Agent]:
        selected = roles or _DEFAULT_ROLES
        agents = []
        for slug in selected:
            factory = _REPORTER_REGISTRY.get(slug)
            if factory is None:
                continue
            agents.append(
                factory(context, model=self.model, base_url=self.ollama_base_url)
            )
        return agents

    def _define_reporter_tasks(
        self,
        reporters: list[Agent],
        brief: str,
    ) -> list[Task]:
        tasks = []
        for reporter in reporters:
            task = Task(
                description=(
                    f"Ты — {reporter.role}.\n\n"
                    f"=== ЗАДАНИЕ ===\n{brief}\n\n"
                    f"Напиши свой материал в соответствии со своей ролью.\n"
                    f"Для каждого утверждения указывай источник и оценку "
                    f"надёжности (high/medium/low/unverified).\n"
                    f"Весь текст на русском языке."
                ),
                expected_output=f"Исследовательский материал от {reporter.role}. На русском языке.",
                agent=reporter,
            )
            tasks.append(task)
        return tasks

    @staticmethod
    def available_roles() -> list[str]:
        return list(_REPORTER_REGISTRY.keys())

    @staticmethod
    def available_books() -> dict[str, dict]:
        return dict(_BOOKS)
