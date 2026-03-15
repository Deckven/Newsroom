# /publish-obsidian — Публикация документов в Obsidian vault

Ты — ассистент Newsroom. Твоя задача: перенести готовые документы из `docs/` в Obsidian vault, адаптировав frontmatter под формат Obsidian.

## Маппинг доменов → папок vault

Базовый путь vault: `C:/ObsidianDataStorage/`

### Домен wowcasual

Основная целевая папка: `ST (1st SubL) PC Games/`

Маппинг подпапок docs → vault (папки vault начинаются с `! `):

| Путь в проекте | Папка в vault |
|---------------|--------------|
| `docs/wowcasual/black_myth_wukong/` | `ST (1st SubL) PC Games/! Black Myth Wukong/` |
| `docs/wowcasual/clair_obscure_expedition_33/` | `ST (1st SubL) PC Games/! Clair Obscure Expedition 33/` |
| `docs/wowcasual/diablo_iv/` | `ST (1st SubL) PC Games/! Diablo IV/` |
| `docs/wowcasual/elden_ring_nightreign/` | `ST (1st SubL) PC Games/! Elden Ring Nightreign/` |
| `docs/wowcasual/eve_frontier/` | `ST (1st SubL) PC Games/! EVE Frontier/` |
| `docs/wowcasual/eve_online/` | `ST (1st SubL) PC Games/! EVE Online/` |
| `docs/wowcasual/eve_vanguard/` | `ST (1st SubL) PC Games/! EVE Vanguard/` |
| `docs/wowcasual/ghost_of_yotei/` | `ST (1st SubL) PC Games/! Ghost of Yotei/` |
| `docs/wowcasual/wow/` | `ST (1st SubL) PC Games/! WoW Midnight/` |
| `docs/wowcasual/general_gaming/` | `ST (1st SubL) PC Games/Gaming News/` |
| `docs/wowcasual/external_docs/` | `ST (1st SubL) PC Games/Gaming News/` |

Связанные vault-папки (НЕ для автоматического экспорта, только при явном указании):
- `ST (2nd SubL) WoW Casual/` — контент блога WoW Casual (готовые посты)
- `ST (2nd SubL) TGCasual/` — контент Telegram-канала
- `ST (2nd SubL) YTCasual/` — контент YouTube-канала
- `ST (2nd SubL) YTWoW/` — контент YouTube WoW-канала

### Домен technocrats

Основная целевая папка: `Prof (1st SubL) Technocrats/`

| Путь в проекте | Папка в vault |
|---------------|--------------|
| `docs/technocrats/` | `Prof (1st SubL) Technocrats/` |

Связанные vault-папки:
- `ST (1st SubL) Futurology/` — футурологические материалы

## Аргументы

Пользователь передаёт аргументы после `/publish-obsidian`. Разбери их:

- **Файл или паттерн** (обязательно) — путь к файлу или glob-паттерн относительно `docs/` (например, `wowcasual/diablo_iv/season_8_2026_03_15.md` или `wowcasual/**/*.md`)
- **--all** — опубликовать все файлы со `status: rewritten` или `status: draft` из указанного домена
- **--domain** — домен (`wowcasual` или `technocrats`), нужен только с `--all`
- **--subfolder** — подпапка внутри целевой папки vault (например, `Diablo IV`). Если не указана, определяется автоматически из пути файла или его тематики
- **--status** — фильтр по статусу frontmatter (по умолчанию: любой). Например: `--status rewritten`
- **--force** — перезаписать файл в vault, если он уже существует (по умолчанию: спрашивать)

Примеры:
```
/publish-obsidian wowcasual/diablo_iv/season_8_2026_03_15.md
/publish-obsidian wowcasual/wow/dragonflight_*.md --subfolder "WoW/Dragonflight"
/publish-obsidian --all --domain wowcasual --status rewritten
/publish-obsidian technocrats/ai_agents_2026_03_15.md
```

Аргументы: $ARGUMENTS

---

## Алгоритм

### Шаг 1: Найди файлы

1. Если указан конкретный файл — проверь его существование через Read
2. Если указан glob-паттерн — используй Glob для поиска в `docs/`
3. Если `--all` — используй Glob `docs/{domain}/**/*.md` и отфильтруй по `--status`
4. Если файлов не найдено — сообщи пользователю и остановись

### Шаг 2: Определи домен и целевую папку

Для каждого файла:
1. Определи домен из пути (`docs/wowcasual/...` → wowcasual, `docs/technocrats/...` → technocrats)
2. Определи целевую папку vault по таблице маппинга выше
3. Определи подпапку:
   - Если указан `--subfolder` — используй его (добавь `! ` к имени если это игровая папка)
   - Иначе — определи из пути файла по таблице маппинга
   - **Важно**: папки игр в vault начинаются с `! ` (например, `! Diablo IV`). Не забывай этот префикс!
   - Создай подпапку в vault (`mkdir -p`) если её нет

### Шаг 3: Покажи план

Выведи таблицу:
```
Файлы для публикации в Obsidian:

| # | Файл | Статус | → Vault путь |
|---|------|--------|-------------|
| 1 | docs/wowcasual/diablo_iv/season_8.md | rewritten | ST (1st SubL) PC Games/! Diablo IV/season_8.md |
```

Спроси подтверждение. **СТОП — жди ответа.**

### Шаг 4: Адаптируй frontmatter

Для каждого файла:
1. Прочитай файл
2. Адаптируй YAML frontmatter для Obsidian:
   - Сохрани: `title`, `date`, `tags`
   - Добавь: `source_project: newsroom`, `published_to_obsidian: YYYY-MM-DD`
   - Конвертируй `domain` в тег: `newsroom/wowcasual` или `newsroom/technocrats`
   - Конвертируй `format` в тег: `format/news`, `format/guide` и т.д.
   - Убери служебные поля пайплайна: `sources_used`, `status`, `source_file`
   - Объедини все теги в поле `tags:` как список
3. Тело документа оставь без изменений

Пример адаптированного frontmatter:
```yaml
---
title: "Заголовок статьи"
date: 2026-03-15
tags:
  - newsroom/wowcasual
  - format/guide
  - diablo-iv
  - season-8
source_project: newsroom
published_to_obsidian: 2026-03-15
---
```

### Шаг 5: Скопируй файлы

Для каждого файла:
1. Проверь, существует ли файл с таким именем в целевой папке vault
   - Если да и нет `--force` — спроси пользователя
   - Если да и есть `--force` — перезаписать
2. Запиши файл с адаптированным frontmatter в целевую папку vault через Write
3. Обнови frontmatter исходного файла в `docs/`: добавь `published_to_obsidian: YYYY-MM-DD`

### Шаг 6: Отчёт

Выведи:
```
Опубликовано в Obsidian: N файлов

- ✓ docs/wowcasual/diablo_iv/season_8.md → C:/ObsidianDataStorage/ST (1st SubL) PC Games/! Diablo IV/season_8.md
```

---

## Важные правила

- Не удаляй исходные файлы из `docs/` — только копируй
- Не модифицируй тело документа — только frontmatter
- Если файл уже был опубликован (`published_to_obsidian` есть в frontmatter) — предупреди о повторной публикации
- При копировании файлов БЕЗ модификации контента используй `cp` через Bash (экономия токенов). Используй Read+Write только когда нужно адаптировать frontmatter
- Убедись что целевые директории существуют (mkdir -p) перед записью
