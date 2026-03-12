# Google Workspace + Gemini Enterprise: Полное исследование для финтеха

> Дата: 2026-03-12 | Фокус: корпоративное использование в IT-разработке финтех-продуктов

---

## Содержание

1. [Обзор продуктов и архитектура](#1-обзор-продуктов-и-архитектура)
2. [Тарифы и стоимость](#2-тарифы-и-стоимость)
3. [Модели и AI-возможности](#3-модели-и-ai-возможности)
4. [Рабочие процессы для финтех-компании](#4-рабочие-процессы-для-финтех-компании)
5. [Безопасность и комплаенс](#5-безопасность-и-комплаенс)
6. [Кейсы финтех-компаний](#6-кейсы-финтех-компаний)
7. [Источники](#7-источники)

---

# 1. Обзор продуктов и архитектура

## Два ключевых продукта Google

Google предлагает **два отдельных продукта** с AI-возможностями для корпоративных клиентов:

### 1.1 Google Workspace with Gemini

AI-ассистент, встроенный непосредственно в приложения Workspace:
- **Gmail** — Help me write, контекстные smart replies, AI side panel
- **Google Docs** — Help me write, суммаризация документов, генерация изображений
- **Google Sheets** — Enhanced smart fill, AI side panel для анализа данных
- **Google Slides** — генерация изображений, удаление фонов
- **Google Drive** — AI side panel, анализ PDF
- **Google Meet** — автоматические заметки, перевод субтитров (100+ языков), улучшение звука/изображения
- **Google Chat** — суммаризация разговоров, автоматический перевод

**Ключевая особенность**: С января 2025 года Gemini включён во ВСЕ тарифы Workspace (ранее был отдельным платным аддоном).

### 1.2 Gemini Enterprise (Google Cloud)

Отдельная платформа Google Cloud, запущенная **9 октября 2025 года**. Это НЕ аддон к Workspace, а самостоятельный продукт.

**5 основных компонентов:**

1. **Advanced Intelligence** — на базе моделей Gemini 2.5 Pro/Flash, Gemini 3 Pro/Flash, Gemini 3.1 Pro
2. **Pre-built Agents** (Made by Google):
   - **Deep Research** — исследует сотни сайтов, создаёт детальные отчёты
   - **NotebookLM Enterprise** — суммаризация PDF, Docs, Slides с enterprise-безопасностью
   - **Gemini Code Assist** — генерация и дебаг кода
3. **Agent Designer** — no-code инструмент для создания кастомных AI-агентов на естественном языке
4. **Data & App Connectivity** — интеграция с Google Workspace, Microsoft 365, Salesforce, SAP, ServiceNow, Atlassian
5. **Centralized Governance** — admin dashboard для управления безопасностью и мониторинга

### 1.3 Ключевые различия

| Аспект | Workspace with Gemini | Gemini Enterprise |
|--------|----------------------|-------------------|
| Тип | AI-ассистент в приложениях | Агентная платформа |
| Функция | Помогает пользователю (side panel) | Автоматизирует процессы |
| Данные | Workspace + интернет | Enterprise data + 3rd party connectors |
| Агенты | Нет | Pre-built + custom (no-code/full-code) |
| Платформа | Google Workspace | Google Cloud |
| Целевая аудитория | Все сотрудники | Knowledge workers, разработчики, power users |

### 1.4 NotebookLM Enterprise

Дополнительный продукт для работы с курированными источниками:
- Загружаете PDF, Google Docs, URL → NotebookLM становится экспертом по этим данным
- Ответы строго в рамках загруженных источников с цитатами
- Enterprise-версия с расширенной безопасностью
- Дополняет Gemini Enterprise: GE находит источники → NotebookLM глубоко анализирует

## Интеграции Gemini Enterprise

### Google-сервисы
Calendar, Chat, Drive, Gmail, BigQuery, Cloud Storage, Firestore, Spanner

### Enterprise-приложения
Confluence, Jira, Microsoft SharePoint, ServiceNow, Slack, Zendesk, Salesforce

### Дополнительные
Box, Dropbox, GitHub, HubSpot, Linear, Notion, Monday.com, Shopify

Поддерживаются также **custom connectors**.

---

# 2. Тарифы и стоимость

## Google Workspace (с включённым Gemini AI)

С января 2025 года Gemini включён во все тарифы. Ранее был аддоном за $20-30/user/mo.
Повышение цен на 17-22% с марта 2025.

### Бизнес-тарифы (до 300 пользователей)

| План | Месячная оплата | Годовая оплата | Storage |
|------|----------------|----------------|---------|
| Business Starter | $8.40/user/mo | $7/user/mo | 30 GB/user |
| Business Standard | $16.80/user/mo | $14/user/mo | 2 TB/user |
| Business Plus | $26.40/user/mo | $22/user/mo | 5 TB/user |

### Enterprise (300+ пользователей)
- **Custom pricing** — через отдел продаж Google или реселлеров
- Без ограничений по количеству пользователей
- Расширенное хранилище (as needed)

### AI-возможности по тарифам

| Функция | Starter | Standard | Plus | Enterprise |
|---------|---------|----------|------|------------|
| Gmail Help me write | ✓ | ✓ | ✓ | ✓ |
| Smart replies | ✓ | ✓ | ✓ | ✓ |
| Docs/Sheets/Slides AI | — | ✓ | ✓ | ✓ |
| Meet заметки | — | ✓ | ✓ | ✓ |
| Meet перевод субтитров | — | ✓ | ✓ | ✓ |
| Drive анализ PDF | — | ✓ | ✓ | ✓ |
| Chat суммаризация | — | ✓ | ✓ | ✓ |
| Meet watermarking | — | — | ✓ | ✓ |

## Add-on тарифы (расширенный AI)

### AI Expanded Access
- Повышенные лимиты AI-возможностей
- Доступ к Project Mariner, Whisk
- Flow Credits: 25,000/mo (vs. 50/mo в Starter)
- Workspace Studio: 10,000/mo
- NotebookLM Audio Overviews: 200/day

### AI Ultra Access
- Максимальные лимиты AI-возможностей
- Для специалистов: creative, coding, research

### Лимиты по тарифам (примеры)

| Функция | Starter | Standard/Plus | Enterprise | AI Expanded |
|---------|---------|---------------|------------|-------------|
| Avatar Gen (Vids) | 25/mo | 25/mo | 100/mo | 500/mo |
| Video Gen (Vids) | 50/mo | 50/mo | 200/mo | 500/mo |
| Image Gen (Nano Banana Pro) | 3/mo | 30/mo | 300/mo | 1,000/mo |
| Workspace Studio | 100/mo | 400/mo | 2,000/mo | 10,000/mo |
| Audio Overviews (PDFs) | — | 20/day | 40/day | 200/day |
| Flow Credits | 50/mo | — | — | 25,000/mo |

## Gemini Enterprise (Google Cloud) — Отдельный продукт

| План | Стоимость (annual) | Стоимость (monthly) | Для кого |
|------|-------------------|---------------------|----------|
| Business | $21/user/mo | — | Малый бизнес, стартапы |
| Standard | $30/user/mo | $35/user/mo | Knowledge workers |
| Plus | $50/user/mo | $60/user/mo | Разработчики, power users |
| Frontline | Ниже | — | Полевые работники (мин. 150 лиценций Standard/Plus) |

### Storage по изданиям Gemini Enterprise

| Издание | Storage |
|---------|---------|
| Business | 25 GiB/user/mo (pooled) |
| Standard | 30 GiB/user/mo (pooled) |
| Plus | 75 GiB/user/mo (pooled) |
| Frontline | 2 GiB/user/mo (pooled) |

**Важно**: Дополнительные расходы на compute (consumption charges) оплачиваются отдельно через привязанный Google Cloud аккаунт.

### Функции по изданиям Gemini Enterprise

| Функция | Business | Standard | Plus | Frontline |
|---------|----------|----------|------|-----------|
| Full connector ecosystem | ✓ | ✓ | ✓ | — |
| Enterprise search | ✓ | ✓ | ✓ | ✓ |
| Ground with Google Search | ✓ | ✓ | ✓ | — |
| Gemini Code Assist | ✓ | ✓ | — | — |
| NotebookLM Enterprise | ✓ | ✓ | — | — |
| Data Insights agent | ✓ | ✓ | — | — |
| Deep Research | ✓ | ✓ | ✓ | ✓ |
| Full-code custom agents | ✓ | ✓ | Limited | — |

## Расчёт стоимости для финтех-компании

### Пример: 200 сотрудников

**Вариант 1: Только Workspace Business Standard**
- 200 × $14/user/mo = **$2,800/mo** ($33,600/year)
- Включает базовый Gemini AI во всех приложениях

**Вариант 2: Workspace + Gemini Enterprise Standard**
- Workspace: 200 × $14 = $2,800/mo
- Gemini Enterprise: 200 × $30 = $6,000/mo
- **Итого: $8,800/mo** ($105,600/year) + compute charges
- Полная агентная платформа, enterprise search, кастомные агенты

**Вариант 3: Workspace Enterprise + Gemini Enterprise Plus (для IT-команды)**
- Workspace Enterprise: custom pricing (примерно $25-30/user)
- Gemini Enterprise Plus для 50 разработчиков: 50 × $50 = $2,500/mo
- Gemini Enterprise Standard для 150 остальных: 150 × $30 = $4,500/mo
- **Итого: ~$12,000-14,000/mo** + compute charges

## Образование

**Google AI Pro for Education**: $24/user/mo (monthly) или $20/user/mo (annual)

---

# 3. Модели и AI-возможности

## Доступные модели Gemini (март 2026)

### Gemini 3.1 Pro (Preview)
- **Статус**: Preview в Model Garden и Vertex AI
- **Назначение**: Самая продвинутая reasoning-модель Gemini
- **Контекстное окно**: 1M токенов
- **Возможности**: Решение сложных задач из разных источников — текст, аудио, изображения, видео, PDF, целые кодовые репозитории
- **Использование**: Enterprise через Vertex AI и Gemini Enterprise

### Gemini 3 Pro
- **Статус**: Generally Available
- **Назначение**: Глубокое рассуждение для сложных задач
- **Доступ**: Gemini app, Gemini Enterprise

### Gemini 3 Flash
- **Статус**: Public Preview
- **Назначение**: Лучшая модель для сложного мультимодального понимания
- **Бенчмарки**: GPQA Diamond 90.4%, Humanity's Last Exam 33.7% (без tools)
- **Особенность**: Frontier performance при высокой скорости — "speed and scale don't have to come at the cost of intelligence"
- **Доступ**: Vertex AI, Gemini Enterprise

### Gemini 3.1 Flash-Lite (Preview)
- **Статус**: Preview
- **Назначение**: Самая cost-effective модель
- **Доступ**: Gemini API, Google AI Studio, Vertex AI

### Gemini 2.5 Flash
- **Статус**: Available (superseded Gemini 3 серией)
- **Доступ**: Vertex AI

### Специализированные модели
- **Nano Banana Pro** — продвинутая генерация изображений
- **Veo 3.1** — генерация видео, AI-аватары в Vids и Gemini app

## AI-возможности в Workspace

### Gmail
- **Help me write**: Быстрое составление профессиональных email
- **Contextual smart replies**: Интеллектуальные предложения ответов
- **Side panel**: AI-ассистент в интерфейсе Gmail

### Google Docs
- **Help me write**: Создание и редактирование документов
- **Help me create an image**: Генерация изображений в документах
- **Summarize a document**: Автоматическая суммаризация
- **Side panel**: AI-ассистент для работы с документами

### Google Sheets
- **Enhanced smart fill**: Улучшенное автозаполнение данных
- **Side panel**: AI-анализ данных в таблицах
- **Trend identification**: Выявление скрытых трендов в данных (portfolio, рынки)

### Google Slides
- **Help me create an image**: Генерация графики для презентаций
- **Remove image backgrounds**: Автоматическое удаление фонов
- **Side panel**: AI-ассистент для презентаций

### Google Meet
- **Take notes for me**: Автоматические заметки по встречам
- **Translated captions**: Перевод в реальном времени (100+ языковых пар)
- **Studio features**: Улучшение звука, изображения, освещения
- **Generate background**: AI-генерация фонов
- **Watermarking**: Водяные знаки (Business Plus+)
- **Adaptive audio**: Управление фоновым шумом

### Google Drive
- **Analyze PDFs**: Извлечение и анализ содержимого документов
- **Side panel**: AI-ассистент для управления файлами

### Google Chat
- **Summarize conversations**: Суммаризация обсуждений
- **Automatic translation**: Автоматический перевод сообщений

## Агенты в Gemini Enterprise

### Pre-built (Made by Google)
1. **Deep Research** — автоматическое исследование сотен источников, создание детальных отчётов
2. **NotebookLM Enterprise** — глубокий анализ загруженных документов с цитатами
3. **Gemini Code Assist Standard** — помощь в написании и дебаге кода
4. **Data Insights Agent** — анализ данных

### Agent Gallery
- Готовые агенты от Google и партнёров
- Поддержка Dialogflow, A2A, ADK агентов
- Marketplace интеграция

### Custom Agents
- **Agent Designer** (no-code) — создание агентов на естественном языке
- **Full-code custom agents** — для разработчиков (Agent Development Kit — ADK)
- Поддержка мультишаговых workflow

## Vertex AI (для разработчиков)

Gemini Enterprise дополняется Vertex AI для backend-разработки:
- API доступ ко всем моделям Gemini
- Rate limits зависят от модели и региона
- Квоты: 500 data stores/project, 500 engines/project (увеличиваемые)
- Shared quotas с Vertex AI Search

---

# 4. Рабочие процессы для финтех-компании

## Использование Google Workspace + Gemini Enterprise в IT-разработке финтеха

### 4.1 Разработка продукта (Engineering)

#### Gemini Code Assist
- **Генерация кода**: автокомплит, генерация функций, рефакторинг
- **Code review**: анализ кода, выявление уязвимостей
- **Debugging**: автоматическая диагностика ошибок
- **Документация**: генерация docstrings, README, API docs
- **Оценка инструментов**: помощь в выборе и интеграции новых мониторинговых инструментов

#### Кастомные AI-агенты для разработки
- Автоматизация CI/CD pipeline мониторинга
- Агенты для анализа логов и incident response
- Интеграция с Jira/Linear для автоматического трекинга задач
- Агенты для автоматического тестирования и QA

#### Workspace для DevOps
- **Google Chat** — интеграция с alerting (PagerDuty, OpsGenie через коннекторы)
- **Google Meet** — post-mortem встречи с автоматическими заметками
- **Google Docs** — автогенерация runbooks и документации инцидентов

### 4.2 Аналитика и Data Science

#### Анализ финансовых данных
- **Sheets AI** — обнаружение скрытых трендов в портфолио
- **Predictive analytics** — прогнозирование рыночных трендов
- **BigQuery интеграция** — Gemini Enterprise подключается к BigQuery для анализа данных в natural language
- **Data Insights Agent** — автоматический анализ данных для бизнес-пользователей

#### Risk Management & Fraud Detection
- Идентификация аномалий и необычных паттернов в реальном времени
- AI-powered fraud detection — 40% сокращение ложноположительных срабатываний (кейс Macquarie Bank)
- Комплексная оценка рисков

### 4.3 Продуктовый менеджмент

#### Исследования и стратегия
- **Deep Research** — автоматическое исследование конкурентов, рыночных трендов
- **NotebookLM** — анализ рыночных отчётов, regulatory filings
- Суммаризация earnings reports и регуляторных изменений

#### Работа с требованиями
- **Docs AI** — быстрое составление PRD, user stories
- **Sheets AI** — приоритизация бэклога, анализ метрик
- **Slides AI** — подготовка презентаций для стейкхолдеров

### 4.4 Клиентский сервис

#### Customer Support Automation
- AI-чатботы на базе Gemini Enterprise для 24/7 поддержки
- Персонализированные ответы на основе профиля клиента
- 38% больше пользователей перенаправлено на self-service (кейс Macquarie)

#### Onboarding клиентов
- Автоматизация KYC/AML проверок
- Автоматическая регистрация клиентов через AppSheet
- Compliance approvals automation

### 4.5 Маркетинг и коммуникации

#### Контент-маркетинг
- **Docs Help me write** — быстрое создание маркетинговых материалов
- **Gmail AI** — персонализированные email-кампании (40% сокращение времени создания — кейс Virgin Voyages)
- **Vids** — создание видеоконтента с AI-аватарами
- **Slides** — презентации для инвесторов и клиентов

#### Перевод и локализация
- Автоматический перевод документов и email
- Real-time перевод на встречах (100+ языков)
- Глобальное масштабирование коммуникаций

### 4.6 Compliance и Legal

#### Регуляторный мониторинг
- **Deep Research** — отслеживание изменений в регуляторике
- **NotebookLM** — анализ нормативных документов с цитатами
- Автоматическая генерация compliance-отчётов

#### Документооборот
- Автоматизированное создание отчётов для регуляторов
- AI-powered Data Loss Prevention
- Client-side encryption для конфиденциальных документов

### 4.7 HR и внутренние процессы

- **Gmail AI** — ускорение внутренних коммуникаций на 20% (кейс FinQuery)
- **Chat AI** — суммаризация обсуждений в командах
- **Meet AI** — автозаметки с action items
- Агенты для HR (onboarding новых сотрудников, FAQ)
- Интеграция с ServiceNow для IT support

## Типовой стек для финтеха

```
┌─────────────────────────────────────────────┐
│            Google Workspace                  │
│  Gmail │ Docs │ Sheets │ Meet │ Drive │ Chat │
│         ↕ Gemini AI side panels ↕            │
├─────────────────────────────────────────────┤
│          Gemini Enterprise                   │
│  Deep Research │ NotebookLM │ Code Assist   │
│  Agent Designer │ Data Insights Agent        │
│  Custom Agents (ADK)                         │
├─────────────────────────────────────────────┤
│          Google Cloud / Vertex AI            │
│  BigQuery │ Cloud Storage │ Spanner         │
│  Vertex AI (Gemini API) │ Firestore         │
├─────────────────────────────────────────────┤
│          Интеграции                          │
│  Jira │ Salesforce │ ServiceNow │ Slack     │
│  GitHub │ Confluence │ SAP                   │
└─────────────────────────────────────────────┘
```

---

# 5. Безопасность и комплаенс

## Google Workspace — Сертификации

### Международные стандарты
- **ISO 27001** — управление информационной безопасностью
- **SOC 2 и SOC 3** — контроли безопасности и конфиденциальности
- **FedRAMP High** — федеральный стандарт безопасности (США)

### Финансовые регуляторы
- **FINRA** — Financial Industry Regulatory Authority (США)
- **SEC Rule 17a-4** — хранение электронных записей (США)
- **CFTC** — Commodity Futures Trading Commission (США)
- **DORA** — Digital Operational Resilience Act (ЕС)
- **OSFI** — Office of the Superintendent of Financial Institutions (Канада)
- Регуляторные требования Австралии, Индии, Сингапура, UK

### Доступность
- **99.99% uptime** через Business Continuity environment

## Gemini Enterprise — Безопасность

### Управление доступом
- **SSO интеграция** — единый вход через корпоративные IdP
- **Permission-aware search** — результаты поиска соответствуют правам пользователя
- Все данные доступны только при наличии соответствующих прав

### Шифрование
- **Client-side encryption** — шифрование на стороне клиента
- **Customer-Managed Encryption Keys (CMEK)** — клиент управляет ключами шифрования
- Шифрование данных at rest и in transit

### Защита данных
- **VPC Service Controls** — предотвращение утечки данных
- **Model Armor** — защита от adversarial атак на модели
- **AI-powered Data Loss Prevention (DLP)** — автоматическая классификация и защита конфиденциальных файлов
- **Private UI access** — доступ через приватный интерфейс

### Аудит и мониторинг
- **Audit logging** — полное логирование действий
- **Admin dashboard** — централизованное управление агентами и безопасностью
- Мониторинг использования AI на уровне организации

### Данные и обучение моделей
- **Enterprise данные НЕ используются для обучения моделей** (кроме Starter edition)
- Данные остаются в контроле организации

### Assured Controls (аддон)
- **Data sovereignty** — управление местоположением данных
- Контроль над геолокацией обработки данных

## Ключевые метрики безопасности

- 33% пользователей Workspace сообщают о снижении инцидентов безопасности (vs 22% у Microsoft 365)
- Автоматическая классификация и маркировка конфиденциальных файлов
- Privacy-preserving AI модели для отраслевых нужд

## Рекомендации для финтеха

### Минимальный набор для соответствия регуляциям:
1. **Google Workspace Enterprise** (не Business) — полный набор compliance features
2. **Client-side encryption** — для данных клиентов и финансовых транзакций
3. **CMEK** — собственное управление ключами шифрования
4. **VPC Service Controls** — изоляция данных
5. **Assured Controls** — если требуется data sovereignty (GDPR, локальные регуляции)
6. **DLP policies** — автоматическое предотвращение утечки персональных и финансовых данных
7. **Audit logging** — для регуляторных проверок и внутреннего аудита

### Ограничения для финтеха:
- Не все модели прошли отраслевую сертификацию
- Для обработки платёжных данных (PCI DSS) могут потребоваться дополнительные меры
- Рекомендуется phased rollout с пилотной группой

---

# 6. Кейсы финтех-компаний

## Финансовые организации, использующие Google Workspace + Gemini

### FinQuery (финтех, SaaS для бухгалтерии)
- **Продукт**: Google Workspace with Gemini
- **Использование**:
  - VP of Infrastructure экономит 20% времени на email
  - Инженерные команды используют Gemini для дебага и troubleshooting кода
  - Brainstorming и планирование проектов
  - Помощь в онбординге — вопросы по новым системам и интеграциям
  - Оценка и внедрение новых мониторинговых инструментов

### Grasshopper Bank (цифровой банк, $1.4B активов)
- **Продукт**: Gemini Enterprise
- **Специфика**: Полностью цифровой банк без филиалов, обслуживает стартапы и fintech
- **Использование**:
  - Разработка agent-based системы для natural language доступа к банковским данным
  - Интеграция Google Drive документов с core banking системой через BigQuery
  - Безопасный доступ сотрудников к данным на естественном языке

### ATB Financial (финансовый институт, Канада)
- **Продукт**: Google Workspace with Gemini
- **Масштаб**: 5,000+ сотрудников
- **Результаты**:
  - Автоматизация рутинных задач
  - Быстрый доступ к информации
  - Повышение эффективности коллаборации

### Macquarie Bank (глобальный инвестбанк)
- **Продукт**: Gemini Enterprise
- **Результаты**:
  - 38% больше пользователей перенаправлено на self-service решения
  - 40% снижение ложноположительных fraud alerts
  - Значительное улучшение клиентского опыта

### Equifax (кредитное бюро)
- **Продукт**: Google Workspace with Gemini
- **Результаты**:
  - 90% участников пилотного проекта отметили повышение качества и количества работы
  - Усиление security posture при росте продуктивности

### Banestes (бразильский банк)
- **Продукт**: Google Workspace with Gemini
- **Использование**:
  - Ускорение кредитного анализа
  - Повышение продуктивности юридического и маркетингового отделов

### Nu Bank (цифровой банк, Бразилия)
- **Продукт**: Google Workspace
- **Статус**: Noted as adopter (детали не раскрыты)

### Robinhood (финтех-брокер)
- **Продукт**: Google Workspace
- **Статус**: Noted as adopter (детали не раскрыты)

### BBVA (международный банк)
- **Продукт**: Google Workspace
- **Статус**: Noted as adopter (детали не раскрыты)

### Pennymac (ипотечная компания)
- **Продукт**: Google Workspace
- **Статус**: Noted as adopter (детали не раскрыты)

## Другие индустрии (релевантные паттерны)

### Virgin Voyages (travel)
- Создали AI-агента "Email Ellie"
- 40% сокращение времени создания email-кампаний
- 28% рост продаж year-over-year

### Gordon Food Service (12,000 сотрудников)
- Агенты подключают ServiceNow и Jira для customer insights
- HR-коммуникации через AI

### Banesco USA (банк)
- 10-15% рост продуктивности

### Seguros Bolivar (страхование)
- 20-30% снижение затрат

### WEX (финтех, платёжные решения)
- 63,000 часов экономии ежемесячно

## Ключевые выводы для финтеха

1. **Быстрый ROI** — большинство компаний видят 10-20% рост продуктивности
2. **Fraud detection** — AI значительно снижает false positives (до 40%)
3. **Customer service** — до 38% больше запросов решается через self-service
4. **Email/Comms** — 20-40% экономии времени на коммуникациях
5. **Масштабируемость** — от 200 до 60,000+ сотрудников
6. **Security first** — финансовые компании подтверждают достаточность security controls

---

# 7. Источники

## Официальные страницы Google

### Pricing & Plans
- [Google Workspace Pricing](https://workspace.google.com/pricing) — официальная страница тарифов
- [Compare Google AI expansion add-ons](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-google-ai-expansion-add-ons) — сравнение AI-аддонов
- [How Google Workspace with Gemini billing works](https://support.google.com/a/answer/13969047?hl=en) — биллинг Workspace+Gemini
- [AI Ultra Access](https://support.google.com/a/answer/16345165?hl=en) — описание ультра-тарифа

### Gemini Enterprise (Google Cloud)
- [Gemini Enterprise — Main Page](https://cloud.google.com/gemini-enterprise) — главная страница продукта
- [What is Gemini Enterprise?](https://docs.cloud.google.com/gemini/enterprise/docs) — документация
- [Compare editions of Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/editions) — сравнение изданий
- [Gemini Enterprise FAQ](https://cloud.google.com/gemini-enterprise/faq) — FAQ
- [NotebookLM Enterprise vs Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/choose-product) — выбор продукта
- [Introducing Gemini Enterprise (Blog)](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise) — анонс продукта
- [Quotas and system limits](https://docs.cloud.google.com/gemini/enterprise/docs/quotas) — квоты и лимиты

### Gemini AI Features in Workspace
- [Gemini AI features in Workspace subscriptions](https://knowledge.workspace.google.com/admin/gemini/gemini-ai-features-now-included-in-google-workspace-subscriptions) — полный список AI-фич
- [AI Tools for Business](https://workspace.google.com/solutions/ai/) — AI-инструменты для бизнеса
- [Workspace Updates: Higher AI access (Feb 2026)](https://workspaceupdates.googleblog.com/2026/02/google-workspace-ai-expanded-access.html) — обновления февраля 2026
- [Gemini Workspace updates (March 2026)](https://blog.google/products-and-platforms/products/workspace/gemini-workspace-updates-march-2026/) — обновления марта 2026

### Модели Gemini
- [Gemini 3.1 Pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/) — анонс модели
- [Gemini 3 Flash](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash) — документация
- [Gemini 3 Pro](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro) — документация
- [Gemini 3.1 Flash-Lite](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/) — cost-effective модель
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) — цены на API
- [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) — лимиты API

### Финансовые сервисы
- [Google Workspace for Finance](https://workspace.google.com/industries/finance/) — отраслевая страница
- [Financial Services on Google Cloud](https://cloud.google.com/solutions/financial-services) — Google Cloud для финансов
- [Integrate Gemini Enterprise Agents with Workspace (Codelab)](https://codelabs.developers.google.com/ge-gws-agents) — tutorial по агентам

## Кейсы и аналитика

### Финтех-кейсы
- [FinQuery case study](https://workspace.google.com/blog/customer-stories/finquery-innovates-gemini-google-workspace) — FinQuery + Gemini
- [Grasshopper Bank case study](https://workspace.google.com/customers/grasshopper-bank/) — Grasshopper Bank
- [128 ways customers use AI](https://workspace.google.com/blog/ai-and-machine-learning/how-our-customers-transform-work-with-ai) — 128 кейсов использования
- [101 real-world gen AI use cases](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders) — 101 кейс от лидеров индустрии
- [Gemini at Work 2024](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work-ai-agents/) — AI-агенты на практике

### Аналитические статьи
- [Google Workspace Pricing 2026 (Name.com)](https://www.name.com/blog/google-workspace-pricing) — обзор цен
- [Google Workspace Pricing 2026 (Lineserve)](https://www.lineserve.net/blog/google-workspace-pricing-2026) — обзор цен
- [Gemini Pricing 2026 (Finout)](https://www.finout.io/blog/gemini-pricing-in-2026) — обзор цен Gemini
- [Gemini Workspace pricing guide (eesel.ai)](https://www.eesel.ai/blog/gemini-workspace-pricing) — гайд по ценам
- [Workspace Gemini pricing changes (Cumulus Global)](https://www.cumulusglobal.com/google-workspace-gemini-ai-features-and-pricing-changes/) — изменения цен
- [Gemini for Business plans (IntuitionLabs)](https://intuitionlabs.ai/articles/gemini-business-pricing-plans) — обзор планов
- [Gemini Enterprise guide (Revolgy)](https://www.revolgy.com/insights/blog/guide-to-gemini-enterprise-features-pricing-and-implementation) — полный гайд
- [Gemini Enterprise vs Workspace (Premier Cloud)](https://premiercloud.com/blog/gemini-enterprise-how-is-it-different-from-gemini-in-workspace-and-notebooklm/) — сравнение
- [Gemini for Financial Services (Promevo)](https://promevo.com/blog/gemini-for-financial-services) — для финансов
- [Top 6 Gemini Use Cases (Cloudfresh)](https://cloudfresh.com/en/blog/gemini-google-workspace/) — топ кейсы
- [Google Workspace price increase (9to5Google)](https://9to5google.com/2025/01/15/google-workspace-gemini-price-increase/) — повышение цен
- [Workspace drops Gemini add-on (Constellation Research)](https://www.constellationr.com/blog-news/insights/google-workspace-drops-gemini-add-charge-raises-business-enterprise-plan-prices) — отмена аддона
