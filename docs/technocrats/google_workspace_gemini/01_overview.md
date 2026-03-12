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
