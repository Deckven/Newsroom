# Агенты Gemini Enterprise: Agent Designer и Agent Development Kit (ADK)

> Дата: 2026-03-12 | Техническое руководство для финтех-компаний

---

## Содержание

1. [Архитектура агентной платформы](#1-архитектура-агентной-платформы)
2. [Pre-built агенты (Made by Google)](#2-pre-built-агенты-made-by-google)
3. [Agent Gallery](#3-agent-gallery)
4. [Agent Designer (No-code)](#4-agent-designer-no-code)
5. [Agent Development Kit — ADK (Pro-code)](#5-agent-development-kit--adk-pro-code)
6. [Сравнение Agent Designer vs ADK](#6-сравнение-agent-designer-vs-adk)
7. [Практические сценарии для финтеха](#7-практические-сценарии-для-финтеха)
8. [Безопасность агентов](#8-безопасность-агентов)

---

# 1. Архитектура агентной платформы

Gemini Enterprise — полноценная **агентная платформа**, позволяющая создавать автономных или полуавтономных помощников, которые рассуждают, планируют и выполняют действия в различных бизнес-системах.

## Ключевые архитектурные концепции

### Grounding (заземление на данных)

Агент подключается к корпоративным данным через коннекторы и отвечает строго на основе этих данных, а не генерирует ответы «из головы». Для финтеха это критично — точность данных и отсутствие галлюцинаций обязательны.

Три типа grounding:

| Тип | Источник данных | Пример использования |
|:----|:---------------|:--------------------|
| **Ground with Google Search** | Актуальная информация из интернета | Мониторинг рыночных трендов, новости регуляторов |
| **Ground with enterprise data** | Корпоративные системы через коннекторы (Drive, Salesforce, Jira, BigQuery) | Анализ внутренних данных, поиск по документации |
| **Ground with uploaded sources** | Конкретные загруженные документы (NotebookLM) | Анализ контрактов, нормативных документов |

### Model Context Protocol (MCP)

Стандартизированный протокол для подключения AI к специфическим API и базам данных:

- **Описание инструментов** — стандартизированный формат, понятный модели
- **Безопасный доступ к БД** — параметризированные SQL-запросы (без прямого доступа LLM к БД)
- **Локальное развёртывание** — MCP-серверы работают на машине пользователя, данные не покидают периметр
- **Read-only режим** — поддержка токенов только для чтения
- **Кастомные функции** — разработчики определяют callable-функции (например, `check_credit_limit`, `verify_kyc_status`), которые модель Gemini вызывает по мере необходимости

### Agent-to-Agent Protocol (A2A)

Открытый протокол для взаимодействия между агентами разных платформ. Позволяет интегрировать агентов из Dialogflow, LangChain, CrewAI и других фреймворков в экосистему Gemini Enterprise.

### Vertex AI Agent Engine

Управляемая среда исполнения для pro-code агентов:

- Масштабируемость и безопасность корпоративного уровня
- Автоматическое управление сессиями, состоянием и мониторингом
- Интеграция с IAM-ролями (например, `Discovery Engine Editor`)
- Контейнеризация, auto-scaling, observability из коробки
- Деплой через `adk deploy agent-engine`

### Общая схема платформы

```
┌──────────────────────────────────────────────────────┐
│                  Пользователи                         │
│    Бизнес-аналитики │ Разработчики │ Compliance       │
├──────────────────────────────────────────────────────┤
│              Gemini Enterprise UI                     │
│         Side panel │ Chat │ Agent Gallery             │
├──────────────────────────────────────────────────────┤
│              Агентный слой                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Pre-built   │  │    Agent     │  │    ADK     │ │
│  │   Agents     │  │   Designer   │  │  Pro-code  │ │
│  │ (Deep Research│  │  (No-code)   │  │  Agents   │ │
│  │  NotebookLM  │  │              │  │           │ │
│  │  Code Assist)│  │              │  │           │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
├──────────────────────────────────────────────────────┤
│              Инфраструктурный слой                    │
│  Grounding │ MCP │ A2A │ Vertex AI Agent Engine      │
├──────────────────────────────────────────────────────┤
│              Данные и коннекторы                      │
│  Google Workspace │ Jira │ Salesforce │ BigQuery     │
│  GitHub │ Confluence │ PostgreSQL │ SAP │ Custom     │
└──────────────────────────────────────────────────────┘
```

---

# 2. Pre-built агенты (Made by Google)

Готовые агенты, не требующие настройки — доступны сразу после активации Gemini Enterprise.

### Deep Research

- Автоматическое исследование **сотен источников** в интернете
- Создание детальных структурированных отчётов
- **Лимит**: 10 отчётов за 30-дневный период для Workspace Enterprise (20/день — лимит consumer AI Pro, не корпоративного тарифа)
- **Финтех-применение**: исследование конкурентов, анализ регуляторных изменений, мониторинг рынков

### NotebookLM Enterprise

- Загрузка PDF, Google Docs, URL → NotebookLM становится экспертом по этим данным
- Ответы строго в рамках загруженных источников с **цитатами на конкретные страницы и абзацы**
- Исключает галлюцинации и обеспечивает проверяемость
- **Audio Overviews** — генерация подкастов из загруженных документов
- **Доступность**: чат — все издания; создание блокнотов — Business и Plus
- **Финтех-применение**: анализ Earnings Calls конкурентов, синтез регуляторных директив (GDPR, EBA), Due Diligence

### Gemini Code Assist

- Генерация и дебаг кода в IDE (VS Code, JetBrains, Android Studio) и через Gemini CLI
- **Agent Mode** — многоступенчатые задачи: рефакторинг модуля, обновление зависимостей во всём проекте
- **Local codebase awareness** — учитывает внутренние библиотеки и стандарты кодирования
- Автоматическая генерация модульных тестов
- **Квоты**: Enterprise — 2,000 RPD / 120 RPM; Standard — 1,500 RPD / 120 RPM
- **Доступность**: Standard и Plus издания (НЕ Business)

### Data Insights Agent

- Автоматический анализ данных для бизнес-пользователей
- Natural language запросы к подключённым источникам данных
- **Доступность**: Business и Standard (НЕ Plus)

### Idea Generation

- Tournament-style brainstorming — генерирует множество идей, затем сталкивает их в «турнире»
- Выбирает лучшие идеи на основе заданных критериев

---

# 3. Agent Gallery

Централизованный каталог агентов организации — «магазин приложений» для AI-помощников.

## Состав

- **Made by Google** — pre-built агенты (Deep Research, NotebookLM, Code Assist и др.)
- **From your organization** — кастомные агенты, созданные через Agent Designer или ADK
- **Partner agents** — агенты от партнёров Google (Dialogflow, A2A)

## Возможности

- **Поиск и обнаружение** — сотрудники находят нужных агентов по описанию и категориям
- **Управление доступом** — администраторы контролируют, кто видит и может использовать каждого агента
- **Мониторинг использования** — статистика по использованию агентов через Admin Dashboard
- **Версионирование** — обновление агентов без нарушения работы существующих пользователей

## Публикация агента

1. **Agent Designer**: агент публикуется прямо из интерфейса конструктора одним кликом
2. **ADK**: агент развёртывается на Agent Engine → регистрируется в Gemini Enterprise через UI или REST API → появляется в секции «From your organization»

---

# 4. Agent Designer (No-code)

Визуальный конструктор для создания AI-агентов без написания кода. Предназначен для бизнес-пользователей, аналитиков, риск-менеджеров и юристов.

## Возможности

- **Создание на естественном языке** — описание роли и логики агента простым языком
- **Flow-редактор** — визуальное редактирование логики в интерактивном конструкторе
- **Многошаговые агенты** — оркестрация субагентов для сложных задач
- **30+ коннекторов** — Google (Drive, Gmail, BigQuery) + сторонние (Jira, Salesforce, ServiceNow)
- **Планирование по расписанию** — автоматический запуск агентов в заданное время
- **Предустановленные инструменты** — набор готовых действий (поиск, отправка, создание документа)
- **Публикация в Agent Gallery** — шеринг внутри организации

## Пошаговый процесс создания агента

### Шаг 1: Определение роли и инструкций

Пользователь описывает агента на естественном языке:

> «Ты — ассистент по проверке KYC-документации. Твоя задача — принимать загруженные документы клиентов, проверять их полноту, сопоставлять с чек-листом требований из Google Drive, и формировать отчёт о результатах проверки. Если документы неполны — указывать, какие именно отсутствуют.»

### Шаг 2: Подключение источников данных (Grounding)

Указываются источники, на основе которых агент будет работать:
- Google Drive — папка с шаблонами и чек-листами
- Google Sheets — таблица с историей проверок
- Salesforce — CRM с данными клиентов

### Шаг 3: Определение действий (Actions)

Агент может не только искать информацию, но и инициировать процессы:
- Отправить уведомление в Slack/Chat
- Обновить статус клиента в CRM
- Создать задачу в Jira
- Заполнить Google Sheet с результатами

### Шаг 4: Тестирование

Интерактивное тестирование прямо в интерфейсе Agent Designer:
- Ввод тестовых запросов
- Просмотр цепочки рассуждений агента
- Проверка вызываемых инструментов и источников

### Шаг 5: Публикация

Одним кликом агент публикуется в Agent Gallery и становится доступен сотрудникам с соответствующими правами.

## Ограничения Agent Designer

- **Ограниченная кастомизация логики** — сложные алгоритмы и условные переходы за пределами возможностей платформы
- **Закрытый набор инструментов** — только предоставленные Google коннекторы и действия
- **Нет прямого подключения к on-premise БД** — без дополнительных коннекторов
- **Производительность** — может быть ниже для задач с большим объёмом вычислений
- **Лимит**: ~500 взаимодействий в месяц

## Примеры агентов для финтеха (Agent Designer)

| Агент | Описание | Источники данных |
|:------|:---------|:----------------|
| **KYC Checker** | Проверка полноты документов клиентов | Drive, Salesforce |
| **Compliance FAQ Bot** | Ответы на вопросы по внутренним политикам | Confluence, Drive |
| **Weekly Report Generator** | Автоматическое составление еженедельных отчётов | Sheets, BigQuery |
| **Incident Triage** | Классификация входящих инцидентов по приоритету | Jira, ServiceNow |
| **Onboarding Assistant** | Помощь новым сотрудникам с FAQ | Drive, Chat |

---

# 5. Agent Development Kit — ADK (Pro-code)

Набор инструментов и библиотек для профессиональных разработчиков, позволяющий создавать сложных, полностью кастомизированных AI-агентов.

## Возможности

- **Полный контроль над логикой** — любая бизнес-логика, условные переходы, обработка ошибок
- **Многоагентные системы** — иерархия агентов с делегированием и оркестрацией
- **Неограниченная интеграция** — подключение к любым API, базам данных, внутренним системам
- **Выбор модели** — любая LLM из Vertex AI Model Garden (Gemini, open-source)
- **Паттерн ReAct** — многошаговое планирование (Reason and Act)
- **Управление памятью и состоянием** — долгосрочная память агента между сессиями
- **Кастомные функции (Tools)** — Python-функции с docstrings, которые модель понимает и вызывает
- **MCP интеграция** — подключение к БД через MCP Toolbox
- **Языки**: Python (основной), Java

## Полный жизненный цикл разработки агента

### Шаг 1: Настройка окружения

**Требования:**
- Python 3.10+
- Google Cloud проект с включённым биллингом
- Активированные API: Vertex AI, Cloud Storage

**Установка:**
```bash
# Установка SDK
pip install --upgrade --quiet google-cloud-aiplatform[agent_engines,adk]

# Аутентификация
gcloud auth application-default login

# Проверка
adk --version
```

### Шаг 2: Создание структуры проекта

```
my_fintech_agent/
├── agent.py          # Основная логика агента
├── tools.py          # Кастомные инструменты
├── tools.yaml        # Конфигурация MCP Toolbox (для БД)
├── requirements.txt  # Зависимости
└── tests/
    ├── test_tools.py      # Unit-тесты инструментов
    └── test_agent.py      # Интеграционные тесты
```

### Шаг 3: Определение инструментов (Tools)

Инструменты — это Python-функции, которые агент вызывает для взаимодействия с внешними системами. Модель использует **docstrings** для понимания, когда и как вызывать инструмент.

**Пример: инструмент для проверки кредитного лимита**

```python
def check_credit_limit(user_id: str) -> dict:
    """Проверяет текущий кредитный лимит клиента.

    Используй этот инструмент, когда пользователь спрашивает
    о кредитном лимите или доступных средствах.

    Args:
        user_id: Уникальный идентификатор клиента (например, "USR-12345")

    Returns:
        dict с полями: credit_limit, used_amount, available_amount, currency
    """
    # Вызов внутреннего API банка
    response = bank_api.get_credit_info(user_id)
    return {
        "credit_limit": response.limit,
        "used_amount": response.used,
        "available_amount": response.limit - response.used,
        "currency": response.currency
    }
```

### Шаг 4: Подключение к базе данных через MCP Toolbox

Для безопасного доступа к PostgreSQL используется **MCP Toolbox for Databases** — шлюз между агентом и БД, исключающий прямой доступ LLM к базе.

**Конфигурация `tools.yaml`:**

```yaml
sources:
  - name: fintech_postgres
    type: postgresql
    uri: postgresql://user:password@host:port/dbname

toolsets:
  - name: transaction_tools
    source: fintech_postgres
    tools:
      - name: get_user_transactions
        description: "Получить последние транзакции пользователя"
        query: >
          SELECT transaction_id, amount, currency, status, created_at
          FROM transactions
          WHERE user_id = :user_id
          ORDER BY created_at DESC
          LIMIT :limit;

      - name: get_fraud_alerts
        description: "Получить активные fraud-алерты для пользователя"
        query: >
          SELECT alert_id, alert_type, severity, description, created_at
          FROM fraud_alerts
          WHERE user_id = :user_id AND status = 'active'
          ORDER BY severity DESC;
```

**Запуск MCP Toolbox Server:**
```bash
# Сервер выступает шлюзом между агентом и БД
mcp-toolbox-server --config tools.yaml --port 8080
```

### Шаг 5: Код агента

```python
from google.adk.agents import LlmAgent
from adk.mcp.toolset import McpToolset

# Подключение к MCP Toolbox
mcp_tools = McpToolset(mcp_server_url="http://localhost:8080")

# Определение агента
transaction_agent = LlmAgent(
    model="gemini-3.1-pro",
    instruction="""
    Ты — агент для анализа транзакций финтех-компании.
    Используй доступные инструменты для ответа на вопросы
    о транзакциях, кредитных лимитах и fraud-алертах.

    Правила:
    - Никогда не раскрывай полные номера счетов — маскируй: ****1234
    - При обнаружении подозрительной активности — предлагай эскалацию
    - Все суммы указывай с валютой
    - Отвечай на русском языке
    """,
    tools=[
        check_credit_limit,
        *mcp_tools.get_all_tools()
    ]
)
```

**Многоагентная система (оркестратор + субагенты):**

```python
from google.adk.agents import LlmAgent

# Субагент для транзакций
transaction_agent = LlmAgent(
    model="gemini-3-flash",
    instruction="Анализируй транзакции пользователя...",
    tools=[get_user_transactions]
)

# Субагент для комплаенса
compliance_agent = LlmAgent(
    model="gemini-3.1-pro",
    instruction="Проверяй операции на соответствие AML/KYC...",
    tools=[check_sanctions_list, get_kyc_status]
)

# Оркестратор
orchestrator = LlmAgent(
    model="gemini-3.1-pro",
    instruction="""
    Ты — главный аналитик. Делегируй задачи субагентам:
    - Вопросы о транзакциях → transaction_agent
    - Вопросы о комплаенсе → compliance_agent
    Синтезируй ответы из нескольких источников.
    """,
    sub_agents=[transaction_agent, compliance_agent]
)
```

### Шаг 6: Безопасное подключение к внутренней БД

Для on-premise или VPC-расположенной PostgreSQL:

1. **Private Service Connect (PSC)** — приватная конечная точка к Google API внутри VPC. Трафик к Vertex AI не покидает сеть Google
2. **Гибридное подключение** — Cloud VPN или Cloud Interconnect между on-premise и Google Cloud VPC
3. **VPC Service Controls** — защищённый периметр, ограничивающий взаимодействие сервисов только авторизованными ресурсами
4. **Secret Manager** — безопасное хранение credentials (хост, порт, пароль). Передаются агенту в runtime, не хранятся в коде
5. **Cloud SQL Auth Proxy** — безопасный туннель к БД, шифрование трафика и IAM-аутентификация. Агент подключается к БД через proxy как к `localhost`
6. **IAM** — сервис-аккаунт с минимально необходимыми ролями (`Cloud SQL Client`)

### Шаг 7: Тестирование

**Локальное тестирование (веб-интерфейс):**
```bash
adk web
# Запускает локальный сервер для интерактивного тестирования
# Видны: промпт → рассуждение → вызов инструмента → ответ
```

**Unit-тесты:**
```python
def test_check_credit_limit():
    result = check_credit_limit("USR-12345")
    assert "credit_limit" in result
    assert result["available_amount"] >= 0
```

**Интеграционные тесты:**
- Проверка вызовов инструментов с реальными/mock API
- Стресс-тестирование под нагрузкой
- E2E-тесты — симуляция полных диалогов

**Evaluation sets:**
- Набор эталонных вопросов и ожидаемых действий агента
- Систематическая проверка качества ответов и правильности выбора инструментов

### Шаг 8: Развёртывание на Vertex AI Agent Engine

```bash
# Создание staging bucket
gsutil mb gs://my-fintech-agent-staging

# Развёртывание (автоматическая контейнеризация)
adk deploy agent-engine \
  --display-name="Transaction Analysis Agent" \
  --staging-bucket="gs://my-fintech-agent-staging"
```

После развёртывания агент появляется в **Vertex AI > Agent Engine** в Google Cloud Console. Доступен Playground для тестирования.

**CI/CD для агентов (Cloud Build):**

```yaml
# cloudbuild.yaml
steps:
  - name: 'python'
    entrypoint: 'pip'
    args: ['install', '-r', 'requirements.txt']

  - name: 'python'
    entrypoint: 'pytest'
    args: ['tests/']

  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        adk deploy agent-engine \
          --display-name="Transaction Agent v${SHORT_SHA}" \
          --staging-bucket="gs://my-staging-bucket"
```

### Шаг 9: Публикация в Agent Gallery

1. В консоли Gemini Enterprise → выбрать приложение
2. **Add agent** → **Custom agent via Agent Engine**
3. Указать путь к развёрнутому Agent Engine агенту
4. Настроить авторизацию через **OAuth 2.0** — агент действует от имени пользователя, соблюдая его права
5. Агент появляется в **Agent Gallery** → «From your organization»

Также можно зарегистрировать агента через **REST API** для автоматизации.

---

# 6. Сравнение Agent Designer vs ADK

## Детальная сравнительная таблица

| Критерий | Agent Designer (No-code) | ADK (Pro-code) |
|:---------|:------------------------|:---------------|
| **Основное назначение** | Быстрое создание и прототипирование агентов для автоматизации бизнес-процессов | Разработка сложных, кастомизированных агентов с глубокой интеграцией |
| **Целевая аудитория** | Бизнес-пользователи, аналитики, citizen-разработчики | Профессиональные разработчики, ML-инженеры |
| **Требуемые навыки** | Низкие. Знание предметной области и умение формулировать инструкции | Высокие. Python/Java, API, облачная архитектура, CI/CD |
| **Создание** | Естественный язык + визуальный Flow-редактор | Код (Python/Java) + ADK CLI |
| **Коннекторы** | 30+ предустановленных (Google, Jira, Salesforce) | Любые — через кастомный код, MCP, REST API |
| **Логика** | Простая: одно-/многошаговые flows | Любая: ReAct, иерархии, делегирование, условная логика |
| **Модели** | Gemini (по умолчанию) | Любая LLM из Vertex AI Model Garden |
| **Память** | Ограниченная (в рамках сессии) | Полное управление состоянием и долгосрочной памятью |
| **БД** | Через предустановленные коннекторы | Прямое подключение (psycopg2, MCP Toolbox, Cloud SQL) |
| **Тестирование** | Интерактивный чат в UI | `adk web` + unit/integration/E2E тесты |
| **Развёртывание** | Один клик → Agent Gallery | `adk deploy` → Agent Engine → Agent Gallery |
| **CI/CD** | Нет | Cloud Build, GitHub Actions, GitLab CI |
| **On-premise** | Нет | Да (VPN, PSC, Hybrid NEG) |
| **Стоимость разработки** | Низкая | Высокая |
| **Время создания** | Минуты-часы | Дни-недели |
| **Масштабируемость** | Стандартная | Enterprise-grade (Agent Engine) |

## Когда что использовать

### Agent Designer — выбирайте, если:
- Нужен агент за часы, а не за недели
- Задача — автоматизация рутины (отчёты, FAQ, поиск по документам)
- Все нужные данные доступны через предустановленные коннекторы
- Нет разработчиков в команде или они заняты
- Прототипирование — нужно быстро проверить гипотезу

### ADK — выбирайте, если:
- Нужна интеграция с внутренними БД (PostgreSQL, Oracle) или on-premise системами
- Сложная бизнес-логика (fraud detection, credit scoring, AML/KYC)
- Требуется многоагентная архитектура с оркестрацией
- Агент работает в production с требованиями к SLA и масштабируемости
- Нужен полный контроль над безопасностью (VPC-SC, CMEK, IAM)

### Рекомендация для финтех-компаний

**Гибридный подход:**
1. **Agent Designer** — для бизнес-подразделений (compliance FAQ, отчёты, internal support)
2. **ADK** — для IT-команды (fraud detection, KYC automation, transaction analysis)
3. Оба типа агентов публикуются в единой **Agent Gallery** и доступны всей организации

---

# 7. Практические сценарии для финтеха

## Сценарий 1: KYC-проверка (Agent Designer)

**Создание через Agent Designer за 30 минут:**

**Инструкция агенту:**
> «Ты — ассистент по KYC-проверке. При получении имени клиента:
> 1. Найди документы клиента в Google Drive (папка /KYC_Documents/)
> 2. Сверь загруженные документы с чек-листом из Confluence
> 3. Проверь статус клиента в Salesforce
> 4. Сформируй отчёт: какие документы есть, каких не хватает, рекомендация (одобрить/запросить дополнительные)
> 5. Отправь результат в Slack-канал #kyc-reviews»

**Источники**: Google Drive, Confluence, Salesforce
**Действия**: поиск, анализ, отправка в Slack

## Сценарий 2: Анализ транзакций на fraud (ADK)

**Многоагентная система:**

```python
# Агент-скринер: быстрый анализ на Gemini 3 Flash
screener = LlmAgent(
    model="gemini-3-flash",
    instruction="Быстро классифицируй транзакцию как normal/suspicious/critical...",
    tools=[get_transaction_details, get_user_history]
)

# Агент-аналитик: глубокий анализ на Gemini 3.1 Pro
analyst = LlmAgent(
    model="gemini-3.1-pro",
    instruction="Проведи глубокий анализ подозрительной транзакции...",
    tools=[get_related_transactions, check_sanctions, get_geo_data]
)

# Оркестратор
fraud_detector = LlmAgent(
    model="gemini-3.1-pro",
    instruction="""
    1. Отправь транзакцию на скрининг → screener
    2. Если suspicious/critical → отправь на глубокий анализ → analyst
    3. Если critical → создай тикет в Jira + уведомление в Slack
    4. Сформируй отчёт для compliance-офицера
    """,
    sub_agents=[screener, analyst],
    tools=[create_jira_ticket, send_slack_notification]
)
```

## Сценарий 3: Генерация комплаенс-отчётов (Agent Designer)

**Агент, работающий по расписанию (каждый понедельник):**

> «Каждую неделю:
> 1. Собери результаты SonarQube-сканирования из Jira (все тикеты с лейблом "security")
> 2. Найди соответствующие стандарты в Confluence (страница "PCI DSS Requirements")
> 3. Сопоставь найденные уязвимости со стандартами
> 4. Создай отчёт в Google Docs с таблицей: уязвимость, критичность, стандарт, рекомендация
> 5. Отправь ссылку на отчёт compliance-офицеру в Gmail»

## Сценарий 4: Кастомный MCP-сервер для тестирования (ADK)

Кейс **Paysera** (литовский финтех):

- Создали кастомный MCP-сервер для генерации тест-кейсов из ТЗ в Confluence
- Серверы App-MCP работают **локально** на машине пользователя
- API-токены — только для чтения (read-only)
- Установка из внутренних репозиториев компании
- **Стоимость**: 6-7 центов за один файл с тест-кейсами
- **Принцип**: «AI делает — человек решает»

---

# 8. Безопасность агентов

## Принципы безопасности

| Принцип | Реализация |
|:--------|:-----------|
| **Permissions-aware** | Агент наследует права пользователя — видит только то, что видит пользователь |
| **Data isolation** | Данные клиента НЕ используются для обучения моделей (Business/Standard/Plus/Enterprise) |
| **No human review** | Промпты и ответы не просматриваются сотрудниками Google |
| **Least privilege** | Сервис-аккаунты с минимально необходимыми IAM-ролями |
| **Encryption** | CMEK — клиент управляет ключами шифрования |
| **Network isolation** | VPC Service Controls — предотвращение эксфильтрации данных |
| **Audit trail** | Полное логирование всех действий агентов |

## Governance для администраторов

- **Centralized Dashboard** — единая точка управления всеми агентами в организации
- **Agent approval workflow** — можно настроить процесс одобрения перед публикацией в Gallery
- **Usage quotas** — контроль расходов на compute через лимиты
- **Monitoring** — мониторинг токенов, запросов, ошибок
- **Model Armor** — защита от adversarial атак и prompt injection

## Рекомендации для финтеха

1. **Начинайте с Agent Designer** — для быстрых побед (FAQ-боты, отчёты)
2. **Переходите к ADK** — для production-critical агентов (fraud, KYC)
3. **VPC Service Controls** — обязательно для любых агентов, работающих с финансовыми данными
4. **Secret Manager** — никогда не храните credentials в коде агента
5. **Staging → Production** — тестируйте в изолированном окружении перед деплоем
6. **Audit logging** — включите для всех агентов для регуляторных проверок

---

## Источники

- [Gemini Enterprise — Main Page](https://cloud.google.com/gemini-enterprise)
- [Compare editions of Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/editions)
- [Integrate Gemini Enterprise Agents with Workspace (Codelab)](https://codelabs.developers.google.com/ge-gws-agents)
- [Gemini Code Assist overview](https://developers.google.com/gemini-code-assist/docs/overview)
- [Code Assist quotas and limits](https://developers.google.com/gemini-code-assist/resources/quotas)
- [Code Assist in GitHub for Enterprises](https://cloud.google.com/blog/products/ai-machine-learning/gemini-code-assist-in-github-for-enterprises/)
- [Connect your Google apps and third-party data](https://support.google.com/g/answer/16550932?hl=en)
- [Introduction to connectors and data stores](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores)
- [Example use cases](https://docs.cloud.google.com/gemini/enterprise/docs/example-use-cases)
- [Quotas and system limits](https://docs.cloud.google.com/gemini/enterprise/docs/quotas)
- [Gemini Enterprise (Devoteam)](https://www.devoteam.com/google-cloud-gemini-enterprise/)
- [Gemini API for Developers](https://ai.google.dev/gemini-api/docs)
