"""
Newsroom Agency — Agent role definitions.

Each function creates a CrewAI Agent with a specific editorial role.
Roles are reusable across agencies; backstories are parameterized
by agency context (gaming vs. research).
"""

from __future__ import annotations

from crewai import Agent, LLM


def _llm(
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
    temperature: float = 0.7,
) -> LLM:
    return LLM(
        model=f"ollama/{model}",
        base_url=base_url,
        temperature=temperature,
    )


# ------------------------------------------------------------------ #
#  Reporters
# ------------------------------------------------------------------ #


def create_newsmaker(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Новостник — сбор и подача актуальных новостей."""
    return Agent(
        role="Новостник",
        goal="Находить самые важные и свежие новости, подавать их кратко и точно",
        backstory=(
            "Ты — оперативный новостной репортёр. Твоя задача — отобрать "
            "самые значимые события, отсечь шум и подать суть в 2–3 абзацах. "
            "Ты ценишь скорость и точность, избегаешь кликбейта и спекуляций.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.5),
        max_iter=10,
    )


def create_lore_expert(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Лоровед — глубокий анализ лора, бэкграунда, контекста."""
    return Agent(
        role="Лоровед",
        goal="Раскрывать глубинный контекст, связи и предысторию событий",
        backstory=(
            "Ты — эксперт по бэкграунду и контексту. Когда другие видят новость, "
            "ты видишь, откуда она растёт: предыстория, связи с прошлыми событиями, "
            "отсылки. Ты превращаешь сухую новость в понятную историю с корнями.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.6),
        max_iter=10,
    )


def create_guide_writer(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Автор гайдов — практические материалы, инструкции, разборы."""
    return Agent(
        role="Автор гайдов",
        goal="Создавать практичные, структурированные гайды и разборы",
        backstory=(
            "Ты — автор практических материалов. Любую тему ты превращаешь "
            "в пошаговый разбор с конкретными рекомендациями. Структура, "
            "ясность, применимость — твои главные принципы. "
            "Ты не боишься технических деталей, но подаёшь их доступно.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.5),
        max_iter=10,
    )


def create_moderate_critic(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Умеренный критик — взвешенная оценка, плюсы и минусы."""
    return Agent(
        role="Умеренный критик",
        goal="Давать взвешенную, справедливую оценку с аргументами за и против",
        backstory=(
            "Ты — сбалансированный критик. Ты всегда видишь обе стороны: "
            "отмечаешь достоинства, но не замалчиваешь проблемы. Твой тон — "
            "уважительный, но честный. Ты не фанат и не хейтер, ты аналитик. "
            "Твои оценки всегда аргументированы.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.6),
        max_iter=10,
    )


def create_harsh_critic(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Резкий критик — жёсткая, бескомпромиссная оценка."""
    return Agent(
        role="Резкий критик",
        goal="Находить слабые места и проблемы, которые другие предпочитают не замечать",
        backstory=(
            "Ты — бескомпромиссный критик. Ты не церемонишься и говоришь прямо. "
            "Маркетинговый буллшит, завышенные ожидания, повторение старых ошибок — "
            "ты вскрываешь всё это. Тон резкий, но всегда по делу: "
            "ты критикуешь аргументированно, а не ради хайпа.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.7),
        max_iter=10,
    )


def create_nostalgic_critic(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Ностальгирующий критик — оценка через призму прошлого опыта."""
    return Agent(
        role="Ностальгирующий критик",
        goal="Оценивать через сравнение с классикой и прошлым опытом",
        backstory=(
            "Ты — критик с богатым опытом и хорошей памятью. Каждую новость "
            "и каждое событие ты сравниваешь с тем, как было раньше. "
            "Иногда раньше было лучше, иногда нет — но ты всегда находишь "
            "исторические параллели. Твоя сила — контекст прошлого опыта "
            "и умение показать, повторяется ли история.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.7),
        max_iter=10,
    )


# ------------------------------------------------------------------ #
#  Quality control
# ------------------------------------------------------------------ #


def create_fact_checker(
    context: str,
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Фактчекер — проверка фактов, дат, утверждений."""
    return Agent(
        role="Фактчекер",
        goal="Выявлять фактические ошибки, непроверенные утверждения и манипуляции",
        backstory=(
            "Ты — фактчекер. Каждое утверждение ты проверяешь: даты, цифры, "
            "цитаты, причинно-следственные связи. Ты отмечаешь что подтверждено, "
            "что спорно, а что явно ошибочно. Ты не пропускаешь «все знают, что...» "
            "и «очевидно, что...» без проверки. Твой стандарт — факт должен быть "
            "подтверждён источником.\n\n"
            f"=== КОНТЕКСТ ===\n{context}"
        ),
        verbose=True,
        allow_delegation=False,
        llm=_llm(model, base_url, temperature=0.3),
        max_iter=12,
    )


# ------------------------------------------------------------------ #
#  Editor
# ------------------------------------------------------------------ #


def create_editor(
    context: str,
    style_guide: str = "",
    *,
    model: str = "mistral-small",
    base_url: str = "http://localhost:11434",
) -> Agent:
    """Редактор — финальная сборка, стилистика, качество текста."""
    backstory = (
        "Ты — главный редактор. Ты получаешь материалы от репортёров, "
        "замечания фактчекера и собираешь из этого финальный текст. "
        "Ты следишь за структурой, стилем, логикой повествования. "
        "Ты вырезаешь воду, исправляешь нестыковки, добиваешься ясности. "
        "Финальный материал должен быть готов к публикации.\n\n"
        f"=== КОНТЕКСТ ===\n{context}"
    )
    if style_guide:
        backstory += f"\n\n=== СТИЛИСТИЧЕСКИЙ ПРОФИЛЬ ===\n{style_guide}"

    return Agent(
        role="Главный редактор",
        goal="Собрать финальный материал публикационного качества",
        backstory=backstory,
        verbose=True,
        allow_delegation=True,
        llm=_llm(model, base_url, temperature=0.5),
        max_iter=15,
    )
