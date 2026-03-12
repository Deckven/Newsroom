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
- **Trend identification**: Выявление скрытых трендов в данных (порт folio, рынки)

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
