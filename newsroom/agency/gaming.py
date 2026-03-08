"""
WoWCasual — Gaming news agency.

Editorial:    Корреспондент, Аналитик, Обозреватель, Лоровед, Гайдовод
Production:   Фактчекер, Редактор, Рерайтер (provided by BaseAgency)
Distribution: SMM-менеджер, SEO-специалист, Комьюнити-менеджер (provided by BaseAgency)
"""

from __future__ import annotations

from typing import Any

from crewai import Agent, Task

from newsroom.agency import agents as role_factory
from newsroom.agency.base import BaseAgency

# Mapping from role slug to factory function
_REPORTER_REGISTRY: dict[str, Any] = {
    "корреспондент": role_factory.create_correspondent,
    "аналитик": role_factory.create_analyst,
    "обозреватель": role_factory.create_reviewer,
    "лоровед": role_factory.create_lore_expert,
    "гайдовод": role_factory.create_guide_writer,
}

# Default set of editorial roles if none specified
_DEFAULT_ROLES = ["корреспондент", "аналитик", "обозреватель"]


class WoWCasualAgency(BaseAgency):
    """Gaming news agency — video game news, reviews, guides, and analysis."""

    name = "wowcasual"

    def __init__(
        self,
        game: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.game = game

    def _build_context(self, topic: str, **kwargs: Any) -> str:
        game = kwargs.get("game", self.game) or topic
        return (
            f"Ты работаешь в игровом новостном агентстве WoWCasual.\n"
            f"Игра/тема: {game}\n"
            f"Тема выпуска: {topic}\n\n"
            f"Целевая аудитория — геймеры, которые ценят конкретику, "
            f"честность и глубину. Без кликбейта, без воды.\n"
            f"Тон: неформальный, но компетентный. "
            f"Соцсети: Discord, Twitter/X, Telegram, Reddit."
        )

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
                    f"Напиши свой материал в соответствии со своей ролью. "
                    f"Будь конкретен, используй факты. "
                    f"Весь текст на русском языке."
                ),
                expected_output=f"Материал от {reporter.role}. На русском языке.",
                agent=reporter,
            )
            tasks.append(task)
        return tasks

    @staticmethod
    def available_roles() -> list[str]:
        """Return slugs of all available editorial roles."""
        return list(_REPORTER_REGISTRY.keys())
