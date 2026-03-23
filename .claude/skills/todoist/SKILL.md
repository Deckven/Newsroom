# /todoist — Управление задачами через Gatekeeper Todoist

Ты — ассистент Newsroom. Твоя задача: управлять задачами в Todoist через CLI Gatekeeper (`gatekeeper todoist`).

## Конфигурация

- CLI: `gatekeeper -c M:/Gatekeeper/config.yaml todoist <command>`
- Sync dir: `C:/ObsidianDataStorage/Todoist/`
- Проекты:
  - `6X2Mxq75JW4qmfCw` — **WoWCasual**
  - `6Crf434CrP6JPVP6` — **Technocrats**
  - `6Crf434CrfVCCC2g` — **Planning**

## Аргументы

Пользователь передаёт команду после `/todoist`. Разбери:

- **projects** — показать список всех проектов Todoist
- **pull [project]** — скачать задачи из Todoist в markdown
- **push [project]** — отправить локальные изменения в Todoist
- **sync [project | --all]** — двусторонняя синхронизация
- **status** — показать статус синхронизации

`[project]` — имя проекта (WoWCasual, Technocrats, Planning) или ID. Если не указан для sync — предложи выбрать или использовать `--all`.

Примеры вызовов:
```
/todoist sync --all
/todoist pull WoWCasual
/todoist push Technocrats
/todoist status
/todoist projects
```

Аргументы: $ARGUMENTS

---

## Маппинг имён → ID

| Имя | Project ID |
|-----|-----------|
| WoWCasual | 6X2Mxq75JW4qmfCw |
| Technocrats | 6Crf434CrP6JPVP6 |
| Planning | 6Crf434CrfVCCC2g |

## Выполнение

### 1. Определи команду и проект

Разбери аргументы пользователя. Если указано имя проекта (WoWCasual и т.п.), подставь соответствующий ID.

### 2. Выполни команду

Базовый формат вызова:
```bash
gatekeeper -c M:/Gatekeeper/config.yaml todoist <command> [options]
```

Конкретные команды:

```bash
# Список проектов
gatekeeper -c M:/Gatekeeper/config.yaml todoist projects

# Pull
gatekeeper -c M:/Gatekeeper/config.yaml todoist pull -p <PROJECT_ID>

# Push
gatekeeper -c M:/Gatekeeper/config.yaml todoist push -p <PROJECT_ID>

# Sync одного проекта
gatekeeper -c M:/Gatekeeper/config.yaml todoist sync -p <PROJECT_ID>

# Sync всех проектов
gatekeeper -c M:/Gatekeeper/config.yaml todoist sync --all

# Статус
gatekeeper -c M:/Gatekeeper/config.yaml todoist status
```

Добавь `--dry-run` если пользователь просит предварительный просмотр.

### 3. Покажи результат

Выведи результат выполнения команды пользователю. При sync/pull/push покажи количество задач (pulled, pushed, closed, reopened).

### 4. Просмотр/редактирование задач

После pull/sync markdown-файлы находятся в `C:/ObsidianDataStorage/Todoist/`:
- `WoWCasual.md`
- `Technocrats.md`
- `Planning.md`

Если пользователь просит показать задачи, прочитай соответствующий файл. Если просит добавить/изменить задачу — отредактируй markdown и выполни push.

Формат задач в markdown:
```markdown
---
todoist_project_id: "PROJECT_ID"
last_synced: "2026-03-23T12:00:00"
---

## Section Name

- [ ] Task content <!-- td:id=XXX p=2 due=2026-03-25 labels=bug,urgent -->
- [x] Completed task <!-- td:id=YYY -->
- [ ] New local task (no metadata = will be created on push)
```

## Важно

- **Не изменяй** metadata-комментарии (`<!-- td:... -->`) вручную, если не знаешь что делаешь
- Для новых задач просто добавь `- [ ] Task content` без metadata — при push они создадутся в Todoist
- Для завершения задачи измени `- [ ]` на `- [x]` и сделай push
- Приоритеты: p=1 (обычный) до p=4 (срочный)
