# Newsroom

Фреймворк для агрегации новостей из нескольких источников (RSS, веб-скрейпинг, NewsAPI) с фильтрацией, дедупликацией, опциональной LLM-суммаризацией и выводом в разных форматах.

## Установка

```bash
pip install -r requirements.txt
```

Для LLM-суммаризации (опционально):

```bash
pip install openai        # для OpenAI
pip install anthropic     # для Anthropic
```

## Быстрый старт

```bash
cp config.example.yaml config.yaml
python -m newsroom --topic "AI" --format markdown
```

По умолчанию в конфиге уже есть три RSS-ленты (Ars Technica, NYT Tech, The Verge), так что работает сразу.

## Использование CLI

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

## Настройка config.yaml

### Источники (sources)

#### RSS / Atom

Самый простой вариант — указать список URL лент:

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
```

### LLM-суммаризация

Когда `processors.llm.enabled: true`, фреймворк генерирует краткое содержание каждой статьи через LLM:

```yaml
llm:
  provider: openai       # "openai" или "anthropic"
  model: gpt-4o-mini     # название модели
  api_key: YOUR_KEY      # API-ключ
```

### Вывод (output)

```yaml
output:
  format: markdown       # markdown | json | html | plaintext
  path: null             # путь к файлу или null для stdout
```

Параметры CLI (`--format`, `--output`) имеют приоритет над конфигом.

## Архитектура

```
newsroom/
├── __main__.py          # CLI точка входа
├── config.py            # Загрузка YAML-конфига
├── models.py            # Датаклассы Article и Digest
├── pipeline.py          # Оркестратор: fetch → process → format
├── utils.py             # Вспомогательные функции
├── sources/             # Плагины источников
│   ├── base.py          # Абстрактный базовый класс BaseSource
│   ├── rss.py           # RSS/Atom через feedparser
│   ├── web.py           # Скрейпинг через BeautifulSoup
│   └── newsapi.py       # NewsAPI.org
├── processors/          # Обработчики
│   ├── base.py          # Абстрактный базовый класс BaseProcessor
│   ├── filter.py        # Фильтрация по ключевым словам
│   ├── dedup.py         # Дедупликация по URL и заголовку
│   └── llm.py           # LLM-суммаризация (OpenAI / Anthropic)
└── formatters/          # Форматирование вывода
    ├── base.py          # Абстрактный базовый класс BaseFormatter
    ├── markdown.py      # Markdown
    ├── json_fmt.py      # JSON
    ├── html_fmt.py      # HTML (Jinja2)
    └── plaintext.py     # Простой текст
```

## Расширение

Все три слоя (источники, процессоры, форматтеры) расширяются через наследование от базовых классов:

```python
from newsroom.sources.base import BaseSource
from newsroom.models import Article

class MySource(BaseSource):
    async def fetch(self, topic: str) -> list[Article]:
        # своя логика получения статей
        ...
```

Затем зарегистрируй класс в соответствующем реестре (`SOURCE_REGISTRY`, `PROCESSOR_REGISTRY`, `FORMATTER_REGISTRY`) в `__init__.py` пакета.
