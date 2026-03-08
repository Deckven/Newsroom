"""
Newsroom Agency — Base agency class.

Provides the common orchestration pattern with three-tier pipeline:
  1. Editorial  — reporters create content
  2. Production — fact-check, edit, rewrite
  3. Distribution — SMM, SEO, community engagement

Subclasses control which tiers and roles are active.
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
        """Create and return editorial agents for this run."""

    @abstractmethod
    def _define_reporter_tasks(
        self,
        reporters: list[Agent],
        brief: str,
    ) -> list[Task]:
        """Create editorial tasks (one per reporter)."""

    def _enable_distribution(self) -> bool:
        """Override to disable distribution tier (default: enabled)."""
        return True

    # -- Common workflow ----------------------------------------------------

    def run(
        self,
        topic: str,
        brief: str = "",
        roles: list[str] | None = None,
        skip_distribution: bool = False,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Execute the full agency workflow.

        Args:
            topic: Subject to cover.
            brief: Editorial brief / prompt describing what to produce.
            roles: Optional subset of editorial roles to activate.
            skip_distribution: If True, skip SMM/SEO/community tier.

        Returns:
            Dict with ``output``, ``session_data``, ``log_file``.
        """
        from newsroom.agency.agents import (
            create_community_manager,
            create_editor,
            create_fact_checker,
            create_rewriter,
            create_seo_specialist,
            create_smm_manager,
        )

        session_start = datetime.now()
        context = self._build_context(topic, **kwargs)

        # ── 1. Editorial ──────────────────────────────────────────────
        reporters = self._select_reporters(topic, context, roles)
        logger.info(
            "[%s] %d reporter(s) activated for '%s'",
            self.name, len(reporters), topic,
        )

        if not brief:
            brief = f"Тема: {topic}"

        reporter_tasks = self._define_reporter_tasks(reporters, brief)

        # ── 2. Production: Fact-check ─────────────────────────────────
        fact_checker = create_fact_checker(
            context, model=self.model, base_url=self.ollama_base_url,
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

        # ── 3. Production: Edit ───────────────────────────────────────
        editor = create_editor(
            context, style_guide=self.style_guide,
            model=self.model, base_url=self.ollama_base_url,
        )
        task_edit = Task(
            description=(
                "Собери финальный материал на основе работы редакции "
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

        # ── 4. Production: Rewrite ────────────────────────────────────
        rewriter = create_rewriter(
            context, model=self.model, base_url=self.ollama_base_url,
        )
        task_rewrite = Task(
            description=(
                "На основе финального материала редактора создай "
                "адаптированные версии:\n\n"
                "1. **Короткая заметка** — 3–5 предложений, суть\n"
                "2. **Дайджест** — буллет-поинты, ключевые факты\n"
                "3. **Тезисы** — 5–7 главных тезисов для рассылки\n\n"
                "Весь текст на русском языке."
            ),
            expected_output="Три адаптированные версии материала. На русском языке.",
            agent=rewriter,
            context=[task_edit],
        )

        # Collect production agents and tasks
        all_agents = reporters + [fact_checker, editor, rewriter]
        all_tasks = reporter_tasks + [task_fact_check, task_edit, task_rewrite]

        # ── 5. Distribution (optional) ────────────────────────────────
        run_distribution = self._enable_distribution() and not skip_distribution

        if run_distribution:
            smm = create_smm_manager(
                context, model=self.model, base_url=self.ollama_base_url,
            )
            task_smm = Task(
                description=(
                    "На основе материала редактора и адаптаций рерайтера "
                    "создай посты для соцсетей:\n\n"
                    "1. **Telegram** — информативный пост с форматированием\n"
                    "2. **Twitter/X** — тред из 2–4 твитов (до 280 символов каждый)\n"
                    "3. **Discord** — пост для новостного канала\n\n"
                    "Добавь хештеги и CTA для каждой платформы.\n"
                    "Весь текст на русском языке."
                ),
                expected_output="Посты для Telegram, Twitter/X, Discord. На русском языке.",
                agent=smm,
                context=[task_edit, task_rewrite],
            )

            seo = create_seo_specialist(
                context, model=self.model, base_url=self.ollama_base_url,
            )
            task_seo = Task(
                description=(
                    "На основе финального материала создай SEO-пакет:\n\n"
                    "1. SEO-заголовок (до 60 символов)\n"
                    "2. Мета-описание (до 160 символов)\n"
                    "3. 5–10 ключевых слов/фраз\n"
                    "4. Рекомендации по структуре H1/H2/H3\n\n"
                    "Весь текст на русском языке."
                ),
                expected_output="SEO-пакет: заголовок, мета, ключевые слова, структура. На русском языке.",
                agent=seo,
                context=[task_edit],
            )

            community = create_community_manager(
                context, model=self.model, base_url=self.ollama_base_url,
            )
            task_community = Task(
                description=(
                    "На основе материала создай контент для вовлечения:\n\n"
                    "1. 2–3 дискуссионных вопроса для комментариев\n"
                    "2. Опрос (poll) с 3–4 вариантами\n"
                    "3. Провокационный тезис для обсуждения\n"
                    "4. Рекомендация по таймингу публикации\n\n"
                    "Весь текст на русском языке."
                ),
                expected_output="Контент для вовлечения аудитории. На русском языке.",
                agent=community,
                context=[task_edit, task_rewrite],
            )

            all_agents += [smm, seo, community]
            all_tasks += [task_smm, task_seo, task_community]

        # ── 6. Run crew ───────────────────────────────────────────────
        crew = Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()

        # ── 7. Save session ───────────────────────────────────────────
        session_end = datetime.now()
        duration = (session_end - session_start).total_seconds()

        session_data = {
            "agency": self.name,
            "timestamp": session_start.isoformat(),
            "duration_seconds": duration,
            "topic": topic,
            "brief": brief,
            "editorial": [a.role for a in reporters],
            "production": ["Фактчекер", "Главный редактор", "Рерайтер"],
            "distribution": ["SMM-менеджер", "SEO-специалист", "Комьюнити-менеджер"]
            if run_distribution else [],
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
