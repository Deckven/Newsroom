# Newsroom

Фреймворк для агрегации новостей из нескольких источников (RSS, веб-скрейпинг, NewsAPI, Obsidian, Google Drive) с фильтрацией, дедупликацией, опциональной LLM-суммаризацией, стилизацией через Rewriter и выводом в разных форматах. Поддерживает экспорт результатов в Obsidian vault и Google Drive.

## Установка

```bash
pip install -r requirements.txt
```

Для LLM-суммаризации (опционально):

```bash
pip install openai        # для OpenAI
pip install anthropic     # для Anthropic
```

Для Rewriter — стилизации статей (опционально):

```bash
pip install anthropic scikit-learn joblib tiktoken pydantic
```

Для Google Drive (источник и/или экспортёр, опционально):

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

Obsidian не требует дополнительных зависимостей.

## Быстрый старт

```bash
cp config.example.yaml config.yaml
python -m newsroom --topic "AI" --format markdown
```

По умолчанию в конфиге уже есть три RSS-ленты (Ars Technica, NYT Tech, The Verge), так что работает сразу.

## Использование CLI

### Основная команда — сбор новостей

```
python -m newsroom --topic <тема> [опции]
```

| Флаг | Описание |
|------|----------|
| `-t`, `--topic` | Тема поиска (обязательный параметр) |
| `-c`, `--config` | Путь к конфигу (по умолчанию `config.yaml`) |
| `-f`, `--format` | Формат вывода: `markdown`, `json`, `html`, `plaintext` |
| `-o`, `--output` | Записать результат в файл вместо вывода в консоль |
| `-v`, `--verbose` | Подробное логирование |
| `--no-export` | Пропустить все экспортёры (даже если настроены) |

### Примеры

```bash
# Markdown в консоль
python -m newsroom --topic "technology" --format markdown

# JSON в файл
python -m newsroom --topic "climate" --format json -o digest.json

# HTML-страница
python -m newsroom --topic "space" --format html -o digest.html

# Простой текст с подробным логом
python -m newsroom --topic "finance" --format plaintext --verbose
```

### Управление Rewriter

```
python -m newsroom rewriter-setup [-c CONFIG] [-v] {import,analyze,stats}
```

| Команда | Описание |
|---------|----------|
| `import <xml_file>` | Импорт WordPress WXR XML в корпус |
| `analyze` | Анализ стиля корпуса и генерация style guide |
| `stats` | Статистика корпуса |

```bash
# Импорт блога из WordPress-экспорта
python -m newsroom rewriter-setup import myblog-export.xml

# Анализ стиля (требуется Anthropic API key в конфиге)
python -m newsroom rewriter-setup analyze

# Просмотр статистики корпуса
python -m newsroom rewriter-setup stats
```

Подробнее — в разделе [Rewriter](#rewriter--стилизация-статей).

### Управление Google Drive OAuth

```
python -m newsroom gdrive-auth {login,revoke,status} [--credentials FILE] [--token FILE]
```

| Команда | Описание |
|---------|----------|
| `login` | Запустить OAuth2-авторизацию (откроет браузер) |
| `revoke` | Отозвать токен и удалить файл |
| `status` | Показать информацию о сохранённом токене |

```bash
# Авторизация в Google Drive
python -m newsroom gdrive-auth login

# Проверка статуса
python -m newsroom gdrive-auth status

# Отзыв токена
python -m newsroom gdrive-auth revoke
```

## Настройка config.yaml

### Модульные источники (source_dirs)

Источники можно выносить в отдельные YAML-файлы, организованные по тематическим папкам. Это удобно, когда источников много — каждый файл описывает один source-блок, а добавление нового источника не требует правки `config.yaml`.

```
sources/
  technology_sources/
    arstechnica.yaml
    nytimes_tech.yaml
    theverge.yaml
  videogames_sources/
    ign.yaml
    kotaku.yaml
    pcgamer.yaml
```

В `config.yaml` указываются директории для сканирования:

```yaml
source_dirs:
  - sources/technology_sources
  - sources/videogames_sources
```

#### Формат YAML-файла источника

**Вариант 1** — один источник (ключ `type` на верхнем уровне):

```yaml
# sources/technology_sources/arstechnica.yaml
type: rss
name: ars-technica
feeds:
  - https://feeds.arstechnica.com/arstechnica/index
```

**Вариант 2** — несколько источников в одном файле (ключ `sources:`):

```yaml
sources:
  - type: rss
    name: feed-one
    feeds:
      - https://example.com/feed1
  - type: rss
    name: feed-two
    feeds:
      - https://example.com/feed2
```

Источники из `source_dirs` загружаются первыми, затем дополняются inline-источниками из `sources:` в `config.yaml` (обратная совместимость сохраняется).

### Источники (sources)

Inline-источники по-прежнему можно определять прямо в `config.yaml`.  Они добавляются после модульных.

#### RSS / Atom

```yaml
sources:
  - type: rss
    name: tech-feeds
    feeds:
      - https://feeds.arstechnica.com/arstechnica/index
      - https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml
      - https://www.theverge.com/rss/index.xml
```

#### NewsAPI

Требуется бесплатный API-ключ с [newsapi.org](https://newsapi.org):

```yaml
sources:
  - type: newsapi
    name: newsapi
    api_key: YOUR_API_KEY_HERE
    page_size: 20       # кол-во статей за запрос
    language: en         # язык
    sort_by: publishedAt # сортировка: publishedAt, relevancy, popularity
```

#### Web scraping

Скрейпинг произвольных сайтов через CSS-селекторы:

```yaml
sources:
  - type: web
    name: custom-scraper
    sites:
      - url: https://example.com/news
        selectors:
          article: "article"    # контейнер каждой статьи
          title: "h2 a"         # элемент заголовка (текст + href)
          content: "p"          # элемент контента/описания
          date: "time"          # элемент даты (атрибут datetime или текст)
```

#### Obsidian vault

Чтение `.md` заметок из Obsidian vault. Не требует дополнительных зависимостей.

```yaml
sources:
  - type: obsidian
    name: my-vault
    vault_path: "C:/Users/me/MyVault"    # абсолютный путь к vault
    folders: ["Articles", "Blog/Published"]  # подпапки (пусто = весь vault)
    filter:
      tags: [technology]                  # фильтр по тегам (пересечение)
      frontmatter:                        # фильтр по frontmatter полям
        status: published
      modified_after: "2025-01-01"        # только файлы изменённые после даты
    recursive: true                        # рекурсивный обход (по умолчанию)
```

Заметки парсятся: YAML frontmatter → заголовок (frontmatter `title` → первый `# H1` → имя файла) → теги, дата, контент. Topic не используется для фильтрации — используйте процессор `filter`.

#### Google Drive

Чтение документов из Google Drive. Требует `pip install google-auth google-auth-oauthlib google-api-python-client` и OAuth2-авторизацию (`python -m newsroom gdrive-auth login`).

```yaml
sources:
  - type: gdrive
    name: research-docs
    credentials_path: "credentials.json"   # OAuth client secrets
    token_path: "token.json"               # сохранённый токен
    folders: ["FOLDER_ID"]                 # ID папок из URL Google Drive
    file_types: [gdoc, md, txt]            # типы файлов
    max_files: 50                          # максимум файлов
```

Поддерживаемые типы: `gdoc` (Google Docs → экспорт как text), `md`, `txt`.

### Процессоры (processors)

```yaml
processors:
  filter:
    enabled: true
    keywords:              # дополнительные ключевые слова (помимо topic)
      - machine learning
      - deep learning

  dedup:
    enabled: true
    similarity_threshold: 0.8  # 0–1, выше = строже совпадение заголовков

  llm:
    enabled: false             # включить LLM-суммаризацию

  rewriter:
    enabled: false             # включить стилизацию через Rewriter
```

Порядок выполнения процессоров: `filter` → `dedup` → `llm` → `rewriter`.

### LLM-суммаризация

Когда `processors.llm.enabled: true`, фреймворк генерирует краткое содержание каждой статьи через LLM:

```yaml
llm:
  provider: openai       # "openai" или "anthropic"
  model: gpt-4o-mini     # название модели
  api_key: YOUR_KEY      # API-ключ
```

### Rewriter — стилизация статей

Rewriter переписывает собранные новости в стиле вашего блога. Под капотом: анализ стиля через LLM, TF-IDF кластеризация для подбора few-shot примеров, prompt caching для экономии токенов.

#### Настройка в 3 шага

**1. Импортировать корпус** — загрузить ваши статьи из WordPress-экспорта:

```bash
python -m newsroom rewriter-setup import myblog-export.xml
```

**2. Запустить анализ стиля** — LLM проанализирует корпус и сгенерирует style guide:

```bash
python -m newsroom rewriter-setup analyze
```

Результат: `rewriter_data/style_guide.md` (стайл-гайд) + `rewriter_data/tfidf_model.pkl` (модель для подбора примеров).

**3. Включить в конфиге:**

```yaml
processors:
  rewriter:
    enabled: true

rewriter:
  corpus_path: rewriter_corpus.db   # путь к SQLite-файлу корпуса
  intensity: medium                  # light / medium / full
  num_examples: 3                    # кол-во few-shot примеров
  max_article_length: 4000           # макс. длина статьи (символов)
  llm:
    api_key: YOUR_ANTHROPIC_KEY      # Anthropic API key
    model: claude-sonnet-4-20250514  # модель для перезаписи
    max_tokens: 4096
```

#### Уровни интенсивности

| Уровень | Описание |
|---------|----------|
| `light` | Минимальные изменения: тон, отдельные формулировки. Структура сохраняется. |
| `medium` | Ощутимая стилизация: лексика, ритм, тон. Общая структура сохраняется. |
| `full` | Полная перезапись в стиле блога. Структура может меняться. |

#### Graceful degradation

Если Rewriter включён, но не настроен (нет API key или корпуса), процессор пропускается без ошибки — пайплайн продолжает работу.

### Экспортёры (exporters)

Экспортёры — это выходные назначения, которые записывают результат пайплайна во внешние системы (Obsidian vault, Google Drive). В отличие от форматтеров (чистые функции `Digest → str`), экспортёры выполняют побочные эффекты (запись файлов, загрузка). Можно настроить несколько экспортёров — они запускаются параллельно.

Флаг `--no-export` отключает все экспортёры.

#### Obsidian Exporter

```yaml
exporters:
  - type: obsidian
    vault_path: "/path/to/vault"          # абсолютный путь к vault (обязательный)
    output_folder: "Newsroom/Digests"      # подпапка для вывода
    mode: single_file                      # single_file | per_article
    date_in_filename: true
    frontmatter:
      extra_tags: [newsroom, auto-generated]
      properties:
        source: newsroom
```

Режимы:
- **single_file** — один `.md` файл с YAML frontmatter + отформатированный дайджест
- **per_article** — каждая статья в отдельном `.md` + `_MOC-{topic}.md` с `[[wikilinks]]`

#### Google Drive Exporter

```yaml
exporters:
  - type: gdrive
    credentials_path: "credentials.json"
    token_path: "token.json"
    folder_id: "FOLDER_ID"                 # ID целевой папки (обязательный)
    upload_as: file                        # file | gdoc
    file_format: markdown                  # markdown | html | plaintext | json
    filename_template: "{topic}_{date}"
```

Режимы:
- **file** — загрузка как обычный файл (markdown, html, txt, json)
- **gdoc** — загрузка с автоконвертацией в Google Doc

### Вывод (output)

```yaml
output:
  format: markdown       # markdown | json | html | plaintext
  path: null             # путь к файлу или null для stdout
```

Параметры CLI (`--format`, `--output`) имеют приоритет над конфигом.

## Архитектура

```
sources/                     # Модульные определения источников (YAML)
├── technology_sources/      #   Технологические RSS-ленты
│   ├── arstechnica.yaml
│   ├── nytimes_tech.yaml
│   └── theverge.yaml
├── videogames_sources/      #   Игровые RSS-ленты
│   ├── ign.yaml
│   ├── kotaku.yaml
│   └── pcgamer.yaml
├── obsidian_sources/        #   Примеры Obsidian-источников
│   └── my_vault.yaml
└── gdrive_sources/          #   Примеры Google Drive-источников
    └── research_folder.yaml

newsroom/
├── __main__.py          # CLI точка входа (pipeline + rewriter-setup + gdrive-auth)
├── config.py            # Загрузка YAML-конфига
├── models.py            # Датаклассы Article и Digest
├── pipeline.py          # Оркестратор: fetch → process → format → export
├── utils.py             # Вспомогательные функции
├── gdrive_auth.py       # Общий модуль OAuth2 для Google Drive
├── sources/             # Плагины источников
│   ├── base.py          # Абстрактный базовый класс BaseSource
│   ├── rss.py           # RSS/Atom через feedparser
│   ├── web.py           # Скрейпинг через BeautifulSoup
│   ├── newsapi.py       # NewsAPI.org
│   ├── obsidian.py      # Чтение .md заметок из Obsidian vault
│   └── gdrive.py        # Чтение документов из Google Drive
├── processors/          # Обработчики
│   ├── base.py          # Абстрактный базовый класс BaseProcessor
│   ├── filter.py        # Фильтрация по ключевым словам
│   ├── dedup.py         # Дедупликация по URL и заголовку
│   ├── llm.py           # LLM-суммаризация (OpenAI / Anthropic)
│   └── rewriter.py      # Стилизация через Rewriter
├── formatters/          # Форматирование вывода
│   ├── base.py          # Абстрактный базовый класс BaseFormatter
│   ├── markdown.py      # Markdown
│   ├── json_fmt.py      # JSON
│   ├── html_fmt.py      # HTML (Jinja2)
│   └── plaintext.py     # Простой текст
├── exporters/           # Экспортёры (выходные назначения)
│   ├── base.py          # Абстрактный базовый класс BaseExporter
│   ├── obsidian.py      # Экспорт в Obsidian vault (single_file / per_article)
│   └── gdrive.py        # Загрузка в Google Drive (file / gdoc)
└── rewriter/            # Движок стилизации (адаптация github.com/Deckven/Rewriter)
    ├── adapter.py       # Мост между dict-конфигом Newsroom и модулями Rewriter
    ├── engine.py        # Оркестратор перезаписи
    ├── rewrite_prompts.py # Промпты для стилизации
    ├── llm_client.py    # Anthropic API обёртка с retry и кэшированием
    ├── corpus/          # SQLite-хранилище корпуса
    │   ├── store.py     # CorpusStore — CRUD для статей, анализов, гайда
    │   ├── models.py    # Pydantic-модели данных
    │   └── stats.py     # Статистика корпуса
    ├── analyzer/        # Анализ стиля
    │   ├── style_extractor.py  # Иерархический анализ: chunk → merge → synthesize
    │   ├── examples.py  # TF-IDF + K-Means подбор few-shot примеров
    │   ├── sampler.py   # Стратифицированная выборка из корпуса
    │   └── prompts.py   # Промпты для анализа стиля
    └── importer/        # Импорт контента
        ├── wordpress.py # Парсер WordPress WXR XML
        └── cleaner.py   # HTML → markdown-like plaintext
```

## Расширение

Все четыре слоя (источники, процессоры, форматтеры, экспортёры) расширяются через наследование от базовых классов:

```python
from newsroom.sources.base import BaseSource
from newsroom.models import Article

class MySource(BaseSource):
    async def fetch(self, topic: str) -> list[Article]:
        # своя логика получения статей
        ...
```

```python
from newsroom.exporters.base import BaseExporter
from newsroom.models import Digest

class MyExporter(BaseExporter):
    async def export(self, digest: Digest, formatted: str) -> str:
        # своя логика экспорта, вернуть статус/путь
        ...
```

Затем зарегистрируй класс в соответствующем реестре (`SOURCE_REGISTRY`, `PROCESSOR_REGISTRY`, `FORMATTER_REGISTRY`, `EXPORTER_REGISTRY`) в `__init__.py` пакета.
