# **Архитектурная трансформация финансовых технологий: Экосистема Gemini Enterprise и Google Workspace в разработке ИТ-продуктов**

Современная индустрия финансовых технологий (финтех) находится в точке перегиба, где традиционные методы цифровизации уступают место агентским вычислениям и глубокой интеграции искусственного интеллекта в каждый этап создания стоимости. Платформа Gemini Enterprise от Google представляет собой не просто набор инструментов для повышения продуктивности, а комплексную среду, способную радикально изменить жизненный цикл разработки программного обеспечения (SDLC), процессы соблюдения регуляторных требований и методы анализа рыночных данных.1 Для корпоративного клиента в сфере финтеха переход на эту экосистему означает возможность автоматизации многоступенчатых рабочих процессов, которые ранее требовали значительного вовлечения квалифицированного персонала и несли в себе риски человеческой ошибки.3

## **Технологический фундамент: Архитектура моделей и возможности контекста**

В основе Gemini Enterprise лежат мультимодальные модели семейства Gemini, использующие инновационную архитектуру Mixture-of-Experts (MoE). Этот подход позволяет моделям быть более эффективными в обучении и обслуживании, обеспечивая при этом производительность, превосходящую предыдущие поколения тяжелых монолитных моделей.5 Для финтех-организаций это означает высокую скорость отклика систем ИИ при решении критически важных задач, таких как проверка транзакций в реальном времени или генерация кода для высоконагруженных систем.

### **Модели и их спецификации**

Экосистема предлагает доступ к различным вариантам моделей, оптимизированным под конкретные задачи. Модель **Gemini 3.1 Pro** является флагманским решением для сложных рассуждений (GA с 19 февраля 2026), в то время как **Gemini 3 Flash** обеспечивает frontier performance при высокой скорости.8 Также доступна **Gemini 3.1 Flash-Lite** (Preview с 3 марта 2026) — наиболее экономичная модель.

> **Примечание:** Серия Gemini 1.5 (Flash, Pro) retired и более недоступна. Все ссылки на 1.5 модели в исходных источниках устарели.

| Характеристика | Gemini 3 Flash | Gemini 3.1 Pro | Gemini 3.1 Flash-Lite (Preview) |
| :---- | :---- | :---- | :---- |
| **Базовая архитектура** | MoE + reasoning | Агентские рассуждения | MoE (cost-effective) |
| **Контекстное окно** | 1 миллион токенов | 1 миллион токенов | 1 миллион токенов |
| **Специализация** | Скорость + intelligence | Сложные мультимодальные задачи | Массовая обработка, low-cost |
| **Бенчмарки** | GPQA Diamond 90.4%, HLE 33.7% | ARC-AGI-2: 77.1% | $0.25/1M input tokens |
| **Применение в финтехе** | Чат-боты, первичный скоринг | Анализ кода, автономные агенты | Классификация, batch-обработка |

### **Значение расширенного контекстного окна**

Одной из самых значимых характеристик моделей Google является способность обрабатывать огромные объемы информации в рамках одного контекстного окна. Актуальные модели (Gemini 3.1 Pro, 3 Flash) поддерживают окно до **1 миллиона токенов**, что позволяет ИТ-командам загружать полные репозитории кода или многолетние архивы документации для анализа без потери связности.8 В контексте финтеха это обеспечивает беспрецедентную точность при поиске «иглы в стоге сена» (needle-in-a-haystack), будь то поиск конкретного условия в тысячах юридических контрактов или обнаружение тонких уязвимостей в распределенной архитектуре микросервисов.

## **Коммерческая структура и управление ресурсами**

Для корпоративных клиентов Google предлагает прозрачную, но многоуровневую систему подписок, которая разделяет возможности повседневного использования ИИ в Workspace и специализированную агентскую платформу Gemini Enterprise.1 Понимание различий между этими уровнями критично для оптимизации затрат ИТ-департамента финтех-компании.

### **Сравнение планов Gemini Enterprise**

Подписки Gemini Enterprise разработаны с учетом масштабируемости: от малых стартапов до глобальных финансовых институтов. Каждый уровень предлагает специфический набор инструментов управления и объемов хранения данных.2

| Параметр | Business | Standard | Plus |
| :---- | :---- | :---- | :---- |
| **Стоимость (от, annual)** | $21 / пользователь / месяц | $30 / пользователь / месяц | $50 / пользователь / месяц ($60 monthly) |
| **Целевой сегмент** | Стартапы, малые команды | Крупные компании | Регулируемые организации |
| **Объем хранилища (pooled)** | 25 ГиБ на пользователя | 30 ГиБ на пользователя | 75 ГиБ на пользователя |
| **Доступ к коннекторам** | Базовый набор | Полная экосистема | Полная экосистема \+ VPC-SC |
| **Управление данными** | Стандартное | Расширенное | CMEK, Sovereignty Controls |

Редакция Gemini Enterprise Plus является наиболее востребованной в финтехе из\-за поддержки функций контроля суверенитета данных и использования ключей шифрования, управляемых клиентом (CMEK), что позволяет соответствовать жестким требованиям безопасности при работе с облачными провайдерами.2

### **Квоты и лимиты запросов**

Эффективность разработки ИТ-продуктов напрямую зависит от доступности ресурсов ИИ. Google устанавливает дифференцированные квоты на количество запросов в минуту (RPM) и в день (RPD).11

* **Gemini Code Assist Enterprise:** Обеспечивает до 120 запросов в минуту и до 2000 запросов в день на одного пользователя. Это покрывает потребности даже самых активных инженеров, занимающихся непрерывным рефакторингом и написанием тестов.11  
* **Deep Research:** Для пользователей Google Workspace Enterprise — **10 отчётов за 30-дневный период** (20/день — лимит consumer AI Pro, не корпоративного тарифа). Тем не менее, это значительно ускоряет этап сбора требований и анализа конкурентов.13  
* **Генерация мультимедиа:** До 3 видео через Veo 3 Fast в день для Workspace Enterprise. Лимиты на изображения зависят от тарифа и аддона AI Expanded Access (конкретные числа для Enterprise не публикуются). Для расширенного доступа рекомендуется AI Expanded Access аддон.13

## **Безопасность, конфиденциальность и регуляторный комплаенс**

Для финтех-компаний вопрос доверия к облачному ИИ является экзистенциальным. Google выстраивает архитектуру Gemini Enterprise вокруг принципа «безопасность по умолчанию», гарантируя, что корпоративные данные остаются собственностью клиента.2

### **Принципы обработки данных**

Ключевым отличием корпоративных версий от потребительских является полная изоляция данных. В рамках Gemini Enterprise:

* Данные клиента, включая промпты и сгенерированный контент, не используются для обучения глобальных моделей Google без явного согласия.15  
* Информация не подвергается человеческому просмотру специалистами Google, что устраняет риски утечки конфиденциальной финансовой информации.15  
* Существующие настройки безопасности Google Workspace (такие как политики регионов данных и DLP) автоматически распространяются на все взаимодействия с ИИ.15

### **Соответствие финансовым регламентам (DORA, EBA, FINRA)**

Разработка финансовых продуктов требует соблюдения множества международных стандартов. Google Workspace и Gemini Enterprise сертифицированы по наиболее строгим из них.16

| Регулятор / Стандарт | Область применения | Статус поддержки |
| :---- | :---- | :---- |
| **DORA (EU)** | Операционная устойчивость | Поддержка через contract mappings и Business Continuity (отдельный standby-продукт, SLA 99.9%) 18 |
| **EBA Guidelines** | Аутсорсинг в банках ЕС | Соответствие правам на аудит 19 |
| **FINRA / SEC** | Хранение записей в США | Поддержка через Cohasset Attestation 18 |
| **SOC 1/2/3** | Финансовый и ИТ-контроль | Ежегодные аудиты пройдены 10 |
| **ISO 42001** | Системы управления ИИ | Первая в мире сертификация AIMS 16 |

Особое внимание стоит уделить закону ЕС DORA (Digital Operational Resilience Act). Google представил специализированные планы Business Continuity, которые позволяют финансовым организациям сохранять доступ к критически важным инструментам Workspace даже в случае масштабных сбоев инфраструктуры, что является прямым ответом на требования регулятора к устойчивости ИКТ-систем.18

## **Интеграция в жизненный цикл разработки (SDLC) финтех-продуктов**

Использование Gemini Enterprise в разработке ИТ-продуктов позволяет сократить время вывода на рынок (Time-to-Market) за счет автоматизации рутинных операций на каждом этапе SDLC: от проектирования архитектуры до мониторинга в промышленной эксплуатации.2

### **Инструменты для инженеров: Gemini Code Assist**

Gemini Code Assist предоставляет интеллектуальную поддержку непосредственно в IDE (VS Code, JetBrains, Android Studio) и терминале разработчика через Gemini CLI.23 В финтехе, где код должен быть не только функциональным, но и максимально защищенным, ИИ помогает выявлять антипаттерны и предлагать безопасные методы обработки данных.

* **Анализ локального кода:** Благодаря локальной осведомленности (local codebase awareness), Gemini генерирует предложения, учитывающие специфические внутренние библиотеки и стандарты кодирования компании.11  
* **Генерация тестов:** Автоматическое создание модульных тестов позволяет обеспечить высокое покрытие кода (code coverage) без значительных временных затрат со стороны разработчиков.23  
* **Агентский режим:** Новая функция Agent Mode позволяет ИИ выполнять многоступенчатые задачи, такие как рефакторинг целого модуля или обновление зависимостей во всем проекте.23

### **Оптимизация процессов на GitHub и Jira**

Интеграция Gemini с системами управления кодом и задачами создает бесшовную среду для командной работы.27 Корпоративная версия Gemini Code Assist на GitHub действует как интеллектуальный рецензент, предоставляя обратную связь по пулл-реквестам с учетом серьезности проблем (Critical, High, Medium, Low).27

| Интеграционный сценарий | Описание действия | Результат для продукта |
| :---- | :---- | :---- |
| **GitHub PR Review** | Автоматическое резюмирование и проверка кода | Ускорение ревью (конкретные метрики зависят от организации) 27 |
| **Jira Issue Creation** | Создание тикетов из чата Gemini Enterprise | Снижение административной нагрузки 30 |
| **Confluence Wiki Sync** | Генерация документации из кода и логов | Актуальность тех. документации 30 |
| **Firebase App Quality** | Анализ крашей и предложение фиксов | Повышение стабильности мобильных приложений 23 |

Для платформенных администраторов финтех-компаний важным инструментом является возможность определения «золотых путей» (golden paths) через централизованные Style Guides на уровне организации. Это гарантирует, что ИИ будет предлагать решения, соответствующие внутренним стандартам качества и безопасности.28

## **Агентская платформа: Создание кастомных финансовых помощников**

Gemini Enterprise позиционируется как агентская платформа, позволяющая создавать автономных или полуавтономных помощников, которые могут рассуждать, планировать и выполнять действия в различных бизнес-системах.1

### **No-code разработка через Agent Designer**

Сотрудники бизнес-подразделений (аналитики, риск-менеджеры, юристы) могут использовать Agent Designer для создания агентов без написания кода.34

1. **Заземление на данных (Grounding):** Агент подключается к корпоративным данным через коннекторы (Google Drive, Salesforce, SAP, BigQuery).2  
2. **Инструкции:** Пользователь описывает роль агента (например, «Ты — ассистент по проверке KYC-документации») и логику его действий.4  
3. **Интеграция действий:** Агент может не только искать информацию, но и инициировать процессы, такие как отправка уведомления в Slack или обновление статуса клиента в CRM.4

### **Профессиональная разработка с Agent Development Kit (ADK)**

Для глубокой интеграции в ИТ-ландшафт финтеха используется ADK. Это позволяет разработчикам создавать сложные агентские архитектуры.34

* **Model Context Protocol (MCP):** Обеспечивает стандартизированный интерфейс для подключения ИИ к специфическим банковским API и базам данных.24  
* **Vertex AI Agent Engine:** Служит средой исполнения для про-код агентов, обеспечивая масштабируемость и безопасность корпоративного уровня.34  
* **Функциональные инструменты:** Разработчики могут определять кастомные функции (например, check\_credit\_limit), которые модель Gemini будет вызывать по мере необходимости в процессе решения задачи пользователя.34

## **Специфические финтех-сценарии использования**

Интеграция Gemini Enterprise в повседневную деятельность финтех-компании выходит далеко за рамки написания кода, охватывая аналитику, аудит и клиентский сервис.3

### **Автоматизированная обработка финансовых документов**

Финтех-продукты часто требуют обработки огромного количества входящих документов (счета, выписки, ID-карты). С помощью Gemini и Google Cloud можно построить автоматизированный конвейер.40

* **OCR нового поколения:** В отличие от традиционных систем распознавания, Gemini понимает контекст и семантическую структуру документа, что позволяет безошибочно извлекать данные даже из неструктурированных файлов.13  
* **Интеллектуальная категоризация:** Система автоматически сопоставляет извлеченные данные с бухгалтерскими кодами или категориями расходов организации.13  
* **Анализ аномалий:** ИИ может сравнивать данные из новых документов с историческими паттернами, мгновенно помечая подозрительные транзакции для проверки отделом безопасности.3

### **Финансовая аналитика и расчет KPI**

Использование Gemini в Google Sheets позволяет аналитикам переходить от ручного ввода формул к запросам на естественном языке.42 Например, для расчета коэффициентов ликвидности или рентабельности достаточно попросить ИИ проанализировать загруженный балансовый отчет. Математические операции выполняются моделью с высокой точностью, например:

![][image1]  
Модель способна не только выдать результат, но и объяснить причины изменения показателей, синтезируя данные из новостей рынка и внутренних отчетов.38

### **NotebookLM для комплаенса и Due Diligence**

Инструмент NotebookLM (входящий в состав Gemini Enterprise) становится центральным хабом для работы с большими массивами знаний.38

* **Синтез знаний:** Юридические отделы могут загружать в блокнот все актуальные директивы (например, обновленные требования GDPR или EBA) и мгновенно получать ответы на вопросы о соответствии новых функций продукта этим нормам.38  
* **АнализEarnings Calls:** Аналитики могут загружать транскрипты звонков инвесторов конкурентов для быстрого выделения ключевых рыночных трендов и угроз.26  
* **Источник правды:** Важнейшим преимуществом является то, что NotebookLM предоставляет ссылки на конкретные страницы и абзацы загруженных документов, исключая галлюцинации и обеспечивая проверяемость данных.44

## **Экосистема коннекторов и интеграция данных**

Ценность Gemini Enterprise для финтеха заключается в способности объединять разрозненные «острова» данных. Коннекторы позволяют ИИ видеть полную картину бизнеса.2

| Тип источника | Примеры систем | Механизм доступа | Значимость для финтеха |
| :---- | :---- | :---- | :---- |
| **Productivity** | Google Workspace, Microsoft 365 | Интеграция API | Поиск по письмам, встречам, документам 2 |
| **Development** | Jira, Confluence, GitHub | Вебхуки, OAuth 2.0 | Связь задач с кодом и документацией 30 |
| **Business Ops** | Salesforce, SAP, ServiceNow | Data Ingestion | Анализ клиентских путей и опер. рисков 2 |
| **Data Lakes** | BigQuery, Vertex AI Search | Federated Search | Прямые запросы к транзакционным БД 2 |

Процесс синхронизации данных может выполняться как в режиме федеративного поиска (без копирования данных в Google), так и в режиме индексации (для более быстрого и глубокого анализа). Для финтеха возможность выбора между этими режимами позволяет гибко балансировать между производительностью и требованиями к локализации данных.31

## **Стратегическое внедрение: От пилота к эксплуатации**

Переход на Gemini Enterprise требует структурированного подхода. Опыт таких компаний, как ATB Financial и Equifax, показывает, что успех зависит от правильной настройки управления изменениями (Change Management).21

1. **Этап инфраструктуры:** Настройка VPC Service Controls и CMEK в Google Cloud Console для обеспечения безопасного периметра. Назначение ролей IAM (например, Discovery Engine Editor) ответственным сотрудникам.10  
2. **Этап интеграции:** Подключение ключевых источников данных (Jira, GitHub, Drive). Настройка квот и лимитов для предотвращения неконтролируемого роста затрат.11  
3. **Этап пилотирования:** Запуск фокус-групп среди разработчиков (использование Code Assist) и финансовых аналитиков (использование NotebookLM и AI в Sheets). Сбор метрик, таких как сокращение Lead Time for Changes.4  
4. **Масштабирование:** Развертывание кастомных агентов для автоматизации специфических процессов онбординга клиентов или комплаенс-контроля.2

Внедрение Gemini Enterprise позволяет финтех-организациям значительно снизить «технический долг ИИ», консолидируя разрозненные подписки на инструменты генеративного ИИ в единую, защищенную и управляемую платформу. Это не только оптимизирует бюджет, но и создает единый стандарт безопасности и качества данных во всей организации.48

## **Выводы**

Google Workspace в сочетании с Gemini Enterprise представляет собой наиболее зрелую экосистему для финтех-компаний, стремящихся к лидерству в эпоху ИИ. Платформа успешно решает триединую задачу: радикальное повышение продуктивности ИТ-разработки, обеспечение высочайшего уровня регуляторного комплаенса и предоставление инструментов для глубокой финансовой аналитики. Для корпоративного клиента переход на эту платформу является инвестицией в агентское будущее, где ИИ-ассистенты берут на себя сложность операционного управления, позволяя людям сосредоточиться на инновациях и стратегическом росте. Благодаря глубокой интеграции с инструментами Google Cloud, такими как BigQuery и Vertex AI, Gemini Enterprise становится центральным звеном в стратегии обработки данных современного цифрового банка или платежной системы. При соблюдении рекомендаций по настройке безопасности и поэтапному внедрению, организация может достичь значительного конкурентного преимущества, сохраняя при этом полное доверие клиентов и регуляторов.

#### **Works cited**

1. Choose your edition \- Gemini Enterprise – Business Edition Help \- Google Help, accessed on March 12, 2026, [https://support.google.com/g/answer/16547364?hl=en](https://support.google.com/g/answer/16547364?hl=en)  
2. Gemini Enterprise: Best of Google AI for Business, accessed on March 12, 2026, [https://cloud.google.com/gemini-enterprise](https://cloud.google.com/gemini-enterprise)  
3. Gemini for Enterprise in Financial Services | AI-Driven Finance Transformation — Evonence | Google Cloud Partner, accessed on March 12, 2026, [https://www.evonence.com/blog/gemini-for-enterprise-in-financial-services-the-new-era-of-intelligent-finance](https://www.evonence.com/blog/gemini-for-enterprise-in-financial-services-the-new-era-of-intelligent-finance)  
4. Gemini Enterprise \- Devoteam, accessed on March 12, 2026, [https://www.devoteam.com/google-cloud-gemini-enterprise/](https://www.devoteam.com/google-cloud-gemini-enterprise/)  
5. Our next-generation model: Gemini 1.5 \- Google Blog, accessed on March 12, 2026, [https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/](https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/)  
6. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context \- arXiv, accessed on March 12, 2026, [https://arxiv.org/pdf/2403.05530](https://arxiv.org/pdf/2403.05530)  
7. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context \- Googleapis.com, accessed on March 12, 2026, [https://storage.googleapis.com/deepmind-media/gemini/gemini\_v1\_5\_report.pdf](https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf)  
8. Gemini 3.1 Pro on Gemini CLI, Gemini Enterprise, and Vertex AI | Google Cloud Blog, accessed on March 12, 2026, [https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-pro-on-gemini-cli-gemini-enterprise-and-vertex-ai](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-pro-on-gemini-cli-gemini-enterprise-and-vertex-ai)  
9. Gemini 3.1 Pro: A smarter model for your most complex tasks \- Google Blog, accessed on March 12, 2026, [https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/)  
10. Compliance certifications and security controls | Gemini Enterprise, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/compliance-security-controls](https://docs.cloud.google.com/gemini/enterprise/docs/compliance-security-controls)  
11. Quotas and limits | Gemini Code Assist \- Google for Developers, accessed on March 12, 2026, [https://developers.google.com/gemini-code-assist/resources/quotas](https://developers.google.com/gemini-code-assist/resources/quotas)  
12. Quotas and limits | Gemini for Google Cloud, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/docs/quotas](https://docs.cloud.google.com/gemini/docs/quotas)  
13. Gemini AI features now included in Google Workspace subscriptions ..., accessed on March 12, 2026, [https://knowledge.workspace.google.com/admin/gemini/gemini-ai-features-now-included-in-google-workspace-subscriptions](https://knowledge.workspace.google.com/admin/gemini/gemini-ai-features-now-included-in-google-workspace-subscriptions)  
14. Gemini Apps limits & upgrades for Google AI subscribers, accessed on March 12, 2026, [https://support.google.com/gemini/answer/16275805?hl=en](https://support.google.com/gemini/answer/16275805?hl=en)  
15. Gemini for Google Workspace FAQ, accessed on March 12, 2026, [https://knowledge.workspace.google.com/admin/gemini/gemini-for-google-workspace-faq](https://knowledge.workspace.google.com/admin/gemini/gemini-for-google-workspace-faq)  
16. Generative AI in Google Workspace Privacy Hub | Google ..., accessed on March 12, 2026, [https://knowledge.workspace.google.com/admin/gemini/generative-ai-in-google-workspace-privacy-hub](https://knowledge.workspace.google.com/admin/gemini/generative-ai-in-google-workspace-privacy-hub)  
17. Gemini security privacy compliance Whitepaper \- Google Workspace, accessed on March 12, 2026, [https://workspace.google.com/learning/content/gemini-privacy-security-compliance-whitepaper](https://workspace.google.com/learning/content/gemini-privacy-security-compliance-whitepaper)  
18. Expanding commitments to help global Financial Services customers compliantly adopt the latest agentic AI tools \- Google Workspace, accessed on March 12, 2026, [https://workspace.google.com/blog/product-announcements/expanding-commitments-to-help-global-financial-services-customers](https://workspace.google.com/blog/product-announcements/expanding-commitments-to-help-global-financial-services-customers)  
19. Transform financial services with AI | Google Workspace with Gemini, accessed on March 12, 2026, [https://workspace.google.com/intl/en\_uk/industries/finance/](https://workspace.google.com/intl/en_uk/industries/finance/)  
20. EBA Outsourcing Guidelines \- Google, accessed on March 12, 2026, [https://services.google.com/fh/files/misc/eba\_outsourcing\_guidelines\_googleworkspace\_compliance\_mapping.pdf](https://services.google.com/fh/files/misc/eba_outsourcing_guidelines_googleworkspace_compliance_mapping.pdf)  
21. Cloud Security and Data Protection Services | Google Workspace, accessed on March 12, 2026, [https://workspace.google.com/security/](https://workspace.google.com/security/)  
22. Gemini for end-to-end SDLC \- Google Skills, accessed on March 12, 2026, [https://www.skills.google/paths/236/course\_templates/885](https://www.skills.google/paths/236/course_templates/885)  
23. Gemini Code Assist overview \- Google for Developers, accessed on March 12, 2026, [https://developers.google.com/gemini-code-assist/docs/overview](https://developers.google.com/gemini-code-assist/docs/overview)  
24. Gemini Code Assist for teams and businesses, accessed on March 12, 2026, [https://codeassist.google/products/business](https://codeassist.google/products/business)  
25. Gemini Code Assist Standard and Enterprise overview \- Google Cloud Documentation, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/docs/codeassist/overview](https://docs.cloud.google.com/gemini/docs/codeassist/overview)  
26. Example use cases | Gemini Enterprise \- Google Cloud Documentation, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/example-use-cases](https://docs.cloud.google.com/gemini/enterprise/docs/example-use-cases)  
27. Review GitHub code using Gemini Code Assist \- Google for Developers, accessed on March 12, 2026, [https://developers.google.com/gemini-code-assist/docs/review-github-code](https://developers.google.com/gemini-code-assist/docs/review-github-code)  
28. Gemini Code Assist in GitHub for Enterprises | Google Cloud Blog, accessed on March 12, 2026, [https://cloud.google.com/blog/products/ai-machine-learning/gemini-code-assist-in-github-for-enterprises/](https://cloud.google.com/blog/products/ai-machine-learning/gemini-code-assist-in-github-for-enterprises/)  
29. Use Gemini Code Assist on GitHub \- Google for Developers, accessed on March 12, 2026, [https://developers.google.com/gemini-code-assist/docs/use-code-assist-github](https://developers.google.com/gemini-code-assist/docs/use-code-assist-github)  
30. Connect your Google apps and third-party data \- Gemini Enterprise – Business Edition Help, accessed on March 12, 2026, [https://support.google.com/g/answer/16550932?hl=en](https://support.google.com/g/answer/16550932?hl=en)  
31. Set up a Jira Cloud data store | Gemini Enterprise, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/connectors/jira-cloud/set-up-data-store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/jira-cloud/set-up-data-store)  
32. Set up a Confluence Cloud data store | Gemini Enterprise, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/connectors/confluence-cloud/set-up-data-store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/confluence-cloud/set-up-data-store)  
33. Google AI Guide: Gemini Enterprise vs. Vertex vs. Workspace \- ByteeIT, accessed on March 12, 2026, [https://byteeit.com/blog/google-ai-comparison-gemini-enterprise-vertex-ai-workspace](https://byteeit.com/blog/google-ai-comparison-gemini-enterprise-vertex-ai-workspace)  
34. Integrate Gemini Enterprise Agents with Google Workspace, accessed on March 12, 2026, [https://codelabs.developers.google.com/ge-gws-agents](https://codelabs.developers.google.com/ge-gws-agents)  
35. Introduction to connectors and data stores | Gemini Enterprise, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores)  
36. Connect a third-party data source | Gemini Enterprise \- Google Cloud Documentation, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/connectors/connect-third-party-data-source](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/connect-third-party-data-source)  
37. Gemini API | Google AI for Developers, accessed on March 12, 2026, [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)  
38. Transform Financial Services with AI | Google Workspace with Gemini, accessed on March 12, 2026, [https://workspace.google.com/industries/finance/](https://workspace.google.com/industries/finance/)  
39. 128 ways our customers are using AI for business | Google Workspace Blog, accessed on March 12, 2026, [https://workspace.google.com/blog/ai-and-machine-learning/how-our-customers-transform-work-with-ai](https://workspace.google.com/blog/ai-and-machine-learning/how-our-customers-transform-work-with-ai)  
40. Automated financial document processing with Google Gemini OCR | n8n workflow template, accessed on March 12, 2026, [https://n8n.io/workflows/9054-automated-financial-document-processing-with-google-gemini-ocr/](https://n8n.io/workflows/9054-automated-financial-document-processing-with-google-gemini-ocr/)  
41. Google Workspace with Gemini, accessed on March 12, 2026, [https://knowledge.workspace.google.com/admin/gemini/google-workspace-with-gemini](https://knowledge.workspace.google.com/admin/gemini/google-workspace-with-gemini)  
42. Use case: Analyze financial statements and calculate ratios | Gemini Enterprise, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/use-case-analyze-financial-statements](https://docs.cloud.google.com/gemini/enterprise/docs/use-case-analyze-financial-statements)  
43. AI for Finance \- Gemini \- Google Workspace, accessed on March 12, 2026, [https://workspace.google.com/solutions/ai/finance/](https://workspace.google.com/solutions/ai/finance/)  
44. The Total Economic Impact™ Of Google Workspace With Gemini \- Forrester, accessed on March 12, 2026, [https://tei.forrester.com/go/Google/WorkspaceWithGemini/index.html](https://tei.forrester.com/go/Google/WorkspaceWithGemini/index.html)  
45. Gemini Enterprise: How is it Different from Gemini in Workspace and NotebookLM?, accessed on March 12, 2026, [https://premiercloud.com/blog/gemini-enterprise-how-is-it-different-from-gemini-in-workspace-and-notebooklm/](https://premiercloud.com/blog/gemini-enterprise-how-is-it-different-from-gemini-in-workspace-and-notebooklm/)  
46. Quotas and system limits | Gemini Enterprise \- Google Cloud Documentation, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/enterprise/docs/quotas](https://docs.cloud.google.com/gemini/enterprise/docs/quotas)  
47. Set up Gemini Code Assist Standard and Enterprise \- Google Cloud Documentation, accessed on March 12, 2026, [https://docs.cloud.google.com/gemini/docs/codeassist/set-up-gemini](https://docs.cloud.google.com/gemini/docs/codeassist/set-up-gemini)  
48. Google Workspace with Gemini vs. Gemini Enterprise: 10 Differences You Should Know, accessed on March 12, 2026, [https://www.devoteam.com/expert-view/google-workspace-with-gemini-vs-gemini-enterprise-10-differences-you-should-know/](https://www.devoteam.com/expert-view/google-workspace-with-gemini-vs-gemini-enterprise-10-differences-you-should-know/)

[image1]: <data:image/png;base64,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>