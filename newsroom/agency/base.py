"""
Newsroom Agency — Base agency class.

Provides the common orchestration pattern: create agents, define tasks,
run a CrewAI sequential workflow, save session log.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

from crewai import Agent, Crew, Process, Task

logger = logging.getLogger(__name__)


class BaseAgency(ABC):
    """Abstract base class for a Newsroom agency."""

    name: str = "base"

    def __init__(
        self,
        model: str = "mistral-small",
        ollama_base_url: str = "http://localhost:11434",
        data_dir: Path | None = None,
        style_guide: str = "",
    ) -> None:
        self.model = model
        self.ollama_base_url = ollama_base_url
        self.style_guide = style_guide
        self.data_dir = data_dir or Path(__file__).parent.parent.parent / "data" / "agency"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    # -- Subclass interface ------------------------------------------------

    @abstractmethod
    def _build_context(self, topic: str, **kwargs: Any) -> str:
        """Return a context string injected into every agent's backstory."""

    @abstractmethod
    def _select_reporters(
        self,
        topic: str,
        context: str,
        roles: list[str] | None = None,
    ) -> list[Agent]:
        """Create and return reporter agents for this run."""

    @abstractmethod
    def _define_reporter_tasks(
        self,
        reporters: list[Agent],
        brief: str,
    ) -> list[Task]:
        """Create reporter tasks (one per reporter)."""

    # -- Common workflow ----------------------------------------------------

    def run(
        self,
        topic: str,
        brief: str = "",
        roles: list[str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute the full agency workflow.

        Args:
            topic: Subject to cover.
            brief: Editorial brief / prompt describing what to produce.
            roles: Optional subset of reporter roles to activate.

        Returns:
            Dict with ``output``, ``session_data``, ``log_file``.
        """
        from newsroom.agency.agents import create_editor, create_fact_checker

        session_start = datetime.now()
        context = self._build_context(topic, **kwargs)

        # 1. Reporters
        reporters = self._select_reporters(topic, context, roles)
        logger.info(
            "[%s] %d reporter(s) activated for '%s'",
            self.name, len(reporters), topic,
        )

        if not brief:
            brief = f"Тема: {topic}"

        reporter_tasks = self._define_reporter_tasks(reporters, brief)

        # 2. Fact-checker reviews all reporter outputs
        fact_checker = create_fact_checker(
            context,
            model=self.model,
            base_url=self.ollama_base_url,
        )
        task_fact_check = Task(
            description=(
                "Проверь материалы всех репортёров на фактическую точность.\n\n"
                "Для каждого материала укажи:\n"
                "- Подтверждённые факты\n"
                "- Спорные или непроверяемые утверждения\n"
                "- Явные ошибки (если есть)\n\n"
                "Весь текст на русском языке."
            ),
            expected_output="Отчёт фактчекера с пометками по каждому материалу. На русском языке.",
            agent=fact_checker,
            context=reporter_tasks,
        )

        # 3. Editor assembles final output
        editor = create_editor(
            context,
            style_guide=self.style_guide,
            model=self.model,
            base_url=self.ollama_base_url,
        )
        task_edit = Task(
            description=(
                "Собери финальный материал на основе работы репортёров "
                "и замечаний фактчекера.\n\n"
                "Требования:\n"
                "- Убери дублирование и противоречия\n"
                "- Исправь фактические ошибки, отмеченные фактчекером\n"
                "- Обеспечь единый стиль и логичную структуру\n"
                "- Материал должен быть готов к публикации\n\n"
                "Весь текст на русском языке."
            ),
            expected_output="Финальный материал публикационного качества. На русском языке.",
            agent=editor,
            context=[task_fact_check] + reporter_tasks,
        )

        # 4. Assemble crew and run
        all_agents = reporters + [fact_checker, editor]
        all_tasks = reporter_tasks + [task_fact_check, task_edit]

        crew = Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        # 5. Save session
        session_end = datetime.now()
        duration = (session_end - session_start).total_seconds()

        session_data = {
            "agency": self.name,
            "timestamp": session_start.isoformat(),
            "duration_seconds": duration,
            "topic": topic,
            "brief": brief,
            "reporters": [a.role for a in reporters],
            "model": self.model,
            "output": str(result),
        }

        log_file = self._save_session(session_data)
        logger.info("[%s] Done in %.1fs. Log: %s", self.name, duration, log_file)

        return {
            "output": str(result),
            "session_data": session_data,
            "log_file": str(log_file),
        }

    def _save_session(self, data: dict) -> Path:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = self.data_dir / f"{self.name}_{ts}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path
