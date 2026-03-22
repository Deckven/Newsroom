# Сессия 2026-03-22 — cc_skills

## Тема
Исследование архитектуры Claude Code: агенты, скиллы, хуки, MCP, инструменты, Agent SDK.

## Что сделано

### 1. Исследование Claude Code architecture
- Использован claude-code-guide агент для сбора детальной информации по всем компонентам
- Собран материал по 8 направлениям: Tools, Agents, Skills, Hooks, MCP, Settings, Commands vs Skills, Agent SDK

### 2. Написан черновик для Technocrats
- **Файл**: `docs/technocrats/claude_code_architecture/claude_code_architecture_2026_03_22.md`
- **Формат**: news (аналитический, ~1700 слов)
- **Содержание**:
  - Tools — встроенные инструменты, система разрешений (allow/deny/ask)
  - Agents — субагенты (Explore, Plan, general-purpose), foreground/background, worktree isolation
  - Skills — SKILL.md формат, аргументы, динамический контекст, отличие от legacy commands
  - Hooks — детерминированные обработчики событий (4 типа: command, http, prompt, agent)
  - MCP — Model Context Protocol, .mcp.json конфигурация, интеграции
  - Settings — иерархия конфигурации, структура .claude/
  - Agent SDK — сравнение с CLI, кейсы для продакшн-агентов
  - Итоговая сравнительная таблица

### 3. Организация файлов
- Создана директория `docs/technocrats/claude_code_architecture/`
- Черновик перемещён в неё

### 4. Коммит и пуш
- Коммит: `ee8b41f` — "Add Claude Code architecture draft for Technocrats, update EVE Frontier rewrite"
- Запушено в main

## Источники
- Claude Code Documentation (sub-agents, skills, hooks, MCP, settings, tools, permissions)
- Claude Agent SDK Documentation

## Статус
- Черновик написан, status: draft
- Рерайт в стиле блога не выполнялся (ожидает подтверждения)
