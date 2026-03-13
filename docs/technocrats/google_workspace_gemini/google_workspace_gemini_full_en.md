
# Google Workspace + Gemini Enterprise: Complete Research for Fintech

> Date: 2026-03-12 | Focus: corporate use in IT development of fintech products

---

## Table of Contents

1. [Product Overview and Architecture](#1-product-overview-and-architecture)
2. [Plans and Pricing](#2-plans-and-pricing)
3. [Models and AI Capabilities](#3-models-and-ai-capabilities)
4. [Workflows for a Fintech Company](#4-workflows-for-a-fintech-company)
5. [Security and Compliance](#5-security-and-compliance)
6. [Fintech Case Studies](#6-fintech-case-studies)
7. [Strategic Implementation: From Pilot to Production](#7-strategic-implementation-from-pilot-to-production)
8. [Sources](#8-sources)

---

# 1. Product Overview and Architecture

## Two Key Google Products

Google offers **two separate products** with AI capabilities for enterprise customers:

### 1.1 Google Workspace with Gemini

An AI assistant built directly into Workspace applications:
- **Gmail** — Help me write, contextual smart replies, AI side panel
- **Google Docs** — Help me write, document summarization, image generation
- **Google Sheets** — Enhanced smart fill, AI side panel for data analysis
- **Google Slides** — image generation, background removal
- **Google Drive** — AI side panel, PDF analysis
- **Google Meet** — automatic notes, translated captions (100+ languages), audio/video enhancement
- **Google Chat** — conversation summarization, automatic translation

**Key Feature**: Since January 2025, Gemini has been included in all Workspace plans (previously a separate paid add-on). However, the scope of AI features varies significantly by plan: Business Starter receives only a minimal set (Vids, Workspace Studio), while full AI features (Help me write, side panels, Meet notes) start with Business Standard.

### 1.2 Gemini Enterprise (Google Cloud)

A separate Google Cloud platform, launched **October 9, 2025**. This is NOT an add-on to Workspace, but a standalone product.

**5 Core Components:**

1. **Advanced Intelligence** — powered by Gemini 3 Pro/Flash, Gemini 3.1 Pro (as well as Gemini 2.5 Pro/Flash via Vertex AI)
2. **Pre-built Agents** (Made by Google):
   - **Deep Research** — explores hundreds of websites, creates detailed reports
   - **NotebookLM Enterprise** — summarization of PDFs, Docs, Slides with enterprise security
   - **Gemini Code Assist** — code generation and debugging
3. **Agent Designer** — no-code tool for creating custom AI agents using natural language
4. **Data & App Connectivity** — integration with Google Workspace, Microsoft 365, Salesforce, SAP, ServiceNow, Atlassian
5. **Centralized Governance** — admin dashboard for security management and monitoring

### 1.3 Key Differences

| Aspect | Workspace with Gemini | Gemini Enterprise |
|--------|----------------------|-------------------|
| Type | AI assistant in applications | Agent platform |
| Function | Assists the user (side panel) | Automates processes |
| Data | Workspace + internet | Enterprise data + 3rd party connectors |
| Agents | No | Pre-built + custom (no-code/full-code) |
| Platform | Google Workspace | Google Cloud |
| Target audience | All employees | Knowledge workers, developers, power users |

### 1.4 NotebookLM Enterprise

An additional product for working with curated sources:
- Upload PDFs, Google Docs, URLs — NotebookLM becomes an expert on that data
- Answers strictly within the scope of uploaded sources with citations to specific pages and paragraphs — eliminates hallucinations
- Enterprise version with enhanced security
- Complements Gemini Enterprise: GE finds sources → NotebookLM deeply analyzes them

### 1.5 Agent Platform Architecture

Gemini Enterprise is not just a set of AI tools, but a full-fledged **agent platform** that enables creating autonomous or semi-autonomous assistants that reason, plan, and execute actions across various business systems.

#### Key Architectural Concepts

**Grounding**

The key concept of Gemini Enterprise is **Grounding**: an agent connects to corporate data through connectors (Google Drive, Salesforce, SAP, BigQuery) and responds strictly based on that data, rather than generating answers "from scratch." This is critically important for fintech, where data accuracy and absence of hallucinations are mandatory requirements.

Three types of grounding:
1. **Ground with Google Search** — extending responses with up-to-date information from the internet
2. **Ground with enterprise data** — binding to corporate sources through connectors
3. **Ground with uploaded sources** — binding to specific uploaded documents (NotebookLM)

**Model Context Protocol (MCP)**

**MCP** is a standardized protocol for connecting AI to specific APIs and databases. It provides a secure interface between the model and external tools (banking APIs, CRM, document management systems). It allows developers to define custom functions (e.g., `check_credit_limit`, `verify_kyc_status`) that the Gemini model calls as needed.

Key MCP capabilities:
- Standardized tool description format
- Secure database access through parameterized SQL queries
- Local deployment of MCP servers on the user's machine (data does not leave the perimeter)
- Support for read-only tokens to prevent unwanted writes

**Agent-to-Agent Protocol (A2A)**

An open protocol for interaction between agents on different platforms. Enables integrating agents created on external platforms (Dialogflow, LangChain, CrewAI) into the Gemini Enterprise ecosystem.

**Vertex AI Agent Engine**

A managed execution environment for pro-code agents:
- Enterprise-grade scalability and security
- Automatic session, state, and monitoring management
- Integration with IAM roles (e.g., `Discovery Engine Editor`)
- Deployment via `adk deploy agent-engine`
- Containerization, auto-scaling, observability out of the box

## Gemini Enterprise Integrations

### Google Services
Calendar, Chat, Drive, Gmail, BigQuery, Cloud Storage, Firestore, Spanner

### Enterprise Applications
Confluence, Jira, Microsoft SharePoint, ServiceNow, Slack, Zendesk, Salesforce

### Additional
Box, Dropbox, GitHub, HubSpot, Linear, Notion, Monday.com, Shopify

**Custom connectors** are also supported.

### Connector Architecture (Permissions-Aware)

Gemini Enterprise connectors operate with access rights awareness — they are **permissions-aware**. Two users will receive different answers to the same query in accordance with their permissions in the source system.

**Technical Mechanism:**

1. **Fetch**: collecting content and metadata from the external system
2. **Transform**: converting to Document format for Discovery Engine, including **access control lists (ACL)**
3. **Sync**: uploading and updating data in the Data Store

**Access Rights Enforcement:**
- **Direct ACLs**: for each document, lists of users/groups with viewing rights are specified
- **Identity Mapping**: mapping external identifiers (Active Directory, Jira) to Google Workspace accounts via the Identity Mapping Store API

**Two Data Access Modes:**
- **Federated search** — real-time query without copying data. Guarantees freshness but may affect speed
- **Data ingestion** (indexing) — copying and indexing into the Data Store. Faster and deeper analysis, but requires a sync schedule

For fintech, the choice between modes allows flexible balancing between performance and data localization requirements.

**Authentication Protocols:**
- **OAuth 2.0** — standard for cloud services (Jira Cloud, Confluence Cloud). The administrator creates an OAuth 2.0 application, configures scopes, obtains Client ID/Secret
- **SAML 2.0** — for identity federation with corporate IdP (Okta, Azure AD)
- **On-premise**: hybrid connection via Hybrid Network Endpoint Group (NEG) + internal load balancer, authentication via API keys or Kerberos

---

# 2. Plans and Pricing

## Google Workspace (with Included Gemini AI)

Since January 2025, Gemini has been included in all plans. Previously it was an add-on at $20-30/user/mo.
Price increase of 17-22% from March 2025.

### Business Plans (up to 300 users)

| Plan | Monthly Billing | Annual Billing | Storage |
|------|----------------|----------------|---------|
| Business Starter | $8.40/user/mo | $7/user/mo | 30 GB/user |
| Business Standard | $16.80/user/mo | $14/user/mo | 2 TB/user |
| Business Plus | $26.40/user/mo | $22/user/mo | 5 TB/user |

### Enterprise (no user limit)
- **Custom pricing** — through Google sales or resellers
- 5 TB/user by default (expandable through Google Sales for organizations with 5+ users)

### AI Capabilities by Plan

| Feature | Starter | Standard | Plus | Enterprise |
|---------|---------|----------|------|------------|
| Gmail Help me write | — | ✓ | ✓ | ✓ |
| Smart replies | — | ✓ | ✓ | ✓ |
| Docs/Sheets/Slides AI | — | ✓ | ✓ | ✓ |
| Meet notes | — | ✓ | ✓ | ✓ |
| Meet translated captions | — | ✓ | ✓ | ✓ |
| Drive PDF analysis | — | ✓ | ✓ | ✓ |
| Chat summarization | — | ✓ | ✓ | ✓ |
| Image Gen (Nano Banana Pro) | ✓ ¹ | ✓ | ✓ | ✓ |
| Vids (avatars, video) | ✓ ¹ | ✓ | ✓ | ✓ |
| NotebookLM Audio Overviews | — | ✓ | ✓ | ✓ |
| Meet watermarking | — | — | ✓ | ✓ |

> ¹ Available in all plans but with significantly lower limits (see limits table below).

## Add-on Plans (Extended AI)

### AI Expanded Access
- Increased AI capability limits
- Access to Project Mariner, Whisk
- Flow Credits: 25,000/mo (vs. 50/mo in Starter)
- Workspace Studio: 10,000/mo
- NotebookLM Audio Overviews: 200/day

### AI Ultra Access
- Maximum AI capability limits
- For specialists: creative, coding, research

### Limits by Plan (Examples)

| Feature | Starter | Standard/Plus | Enterprise | AI Expanded |
|---------|---------|---------------|------------|-------------|
| Avatar Gen (Vids) | 25/mo | 25/mo | 100/mo | 500/mo |
| Video Gen (Vids) | 50/mo | 50/mo | 200/mo | 500/mo |
| Image Gen (Nano Banana Pro) | 3/mo | 30/mo | 300/mo | 1,000/mo |
| Workspace Studio | 100/mo | 400/mo | 2,000/mo | 10,000/mo |
| Audio Overviews (PDFs) | — | 20/day | 40/day | 200/day |
| Flow Credits | 50/mo | — ² | — ² | 25,000/mo |

> ² Flow Credits for Standard/Plus/Enterprise without the add-on are not available — the feature is only available in Starter (base limit) and through the AI Expanded Access add-on.

## Gemini Enterprise (Google Cloud) — Separate Product

| Plan | Cost (annual) | Cost (monthly) | Target Audience |
|------|-------------------|---------------------|----------|
| Business | $21/user/mo | — | Small business, startups |
| Standard | $30/user/mo | $35/user/mo | Knowledge workers |
| Plus | $50/user/mo | $60/user/mo | Developers, power users |
| Frontline | Lower | — | Field workers (available with 150+ Standard/Plus users in the organization) |

### Storage by Gemini Enterprise Edition

| Edition | Storage |
|---------|---------|
| Business | 25 GiB/user/mo (pooled) |
| Standard | 30 GiB/user/mo (pooled) |
| Plus | 75 GiB/user/mo (pooled) |
| Frontline | 2 GiB/user/mo (pooled) |

**Important**: Additional compute expenses (consumption charges) are billed separately through a linked Google Cloud account.

### Features by Gemini Enterprise Edition

| Feature | Business | Standard | Plus | Frontline |
|---------|----------|----------|------|-----------|
| Full connector ecosystem | ✓ | ✓ | ✓ | — |
| Enterprise search | ✓ | ✓ | ✓ | ✓ |
| Ground with Google Search | ✓ | ✓ | ✓ | — |
| Gemini Code Assist | — | ✓ | ✓ | — |
| NotebookLM Enterprise (chat) | ✓ | ✓ | ✓ | ✓ |
| NotebookLM Enterprise (creation) | ✓ | — | ✓ | — |
| Data Insights agent | ✓ | ✓ | — | — |
| Deep Research | ✓ | ✓ | ✓ | ✓ |
| Full-code custom agents | ✓ | ✓ | Limited | — |

### Quotas and Request Limits

| Resource | Limit |
|--------|-------|
| **Code Assist Enterprise** | 2,000 RPD / 120 RPM per user |
| **Code Assist Standard** | 1,500 RPD / 120 RPM per user |
| **Deep Research (Workspace Enterprise)** | 10 reports per 30-day period ³ |
| **Veo 3 Fast (Workspace Enterprise)** | 3 videos/day |
| **Data stores/project** | 500 (expandable) |
| **Engines/project** | 500 (expandable) |
| **Docs AI** | up to 500,000 characters |
| **Sheets AI** | up to 50,000 rows |

> ³ 20 reports/day is the limit for consumer AI Pro, not the enterprise plan. A single prompt in agent mode can result in multiple model requests.

## Cost Calculation for a Fintech Company

### Example: 200 Employees

**Option 1: Workspace Business Standard Only**
- 200 × $14/user/mo = **$2,800/mo** ($33,600/year)
- Includes basic Gemini AI across all applications

**Option 2: Workspace + Gemini Enterprise Standard**
- Workspace: 200 × $14 = $2,800/mo
- Gemini Enterprise: 200 × $30 = $6,000/mo
- **Total: $8,800/mo** ($105,600/year) + compute charges
- Full agent platform, enterprise search, custom agents

**Option 3: Workspace Enterprise + Gemini Enterprise Plus (for IT team)**
- Workspace Enterprise: custom pricing (approximately $25-30/user)
- Gemini Enterprise Plus for 50 developers: 50 × $50 = $2,500/mo
- Gemini Enterprise Standard for 150 others: 150 × $30 = $4,500/mo
- **Total: ~$12,000-14,000/mo** + compute charges

## Education

**Google AI Pro for Education**: pricing TBD (previously Gemini Education — $20/user/mo, Gemini Education Premium — $30/user/mo). Launched September 2025, replacing previous AI add-ons for education.

---

# 3. Models and AI Capabilities

## Model Architecture

At the core of Gemini Enterprise are multimodal models from the Gemini family, using the **Mixture-of-Experts (MoE)** architecture. This approach allows models to be more efficient in training and serving, delivering performance that surpasses previous generations of monolithic models. For fintech, this means high response speed for critical tasks — real-time transaction verification, code generation for high-load systems.

## Available Gemini Models (March 2026)

### Gemini 3.1 Pro (Preview)
- **Status**: Preview in Model Garden and Vertex AI (GA since February 19, 2026)
- **Purpose**: The most advanced Gemini reasoning model
- **Context window**: 1M tokens
- **Benchmarks**: ARC-AGI-2: 77.1%
- **Capabilities**: Solving complex tasks from diverse sources — text, audio, images, video, PDFs, entire code repositories
- **Usage**: Enterprise via Vertex AI and Gemini Enterprise

### Gemini 3 Pro
- **Status**: Deprecated since March 9, 2026 — migration to Gemini 3.1 Pro underway
- **Purpose**: Deep reasoning for complex tasks
- **Access**: Gemini app, Gemini Enterprise (migration to 3.1 Pro recommended)

### Gemini 3 Flash
- **Status**: Public Preview
- **Purpose**: Best model for complex multimodal understanding
- **Benchmarks**: GPQA Diamond 90.4%, Humanity's Last Exam 33.7% (without tools)
- **Distinction**: Frontier performance at high speed — "speed and scale don't have to come at the cost of intelligence"
- **Access**: Vertex AI, Gemini Enterprise

### Gemini 3.1 Flash-Lite (Preview)
- **Status**: Preview (since March 3, 2026)
- **Purpose**: Most cost-effective model
- **Access**: Gemini API, Google AI Studio, Vertex AI

### Gemini 2.5 Flash
- **Status**: Available (superseded by Gemini 3 series)
- **Access**: Vertex AI

### Specialized Models
- **Nano Banana Pro** — advanced image generation
- **Veo 3.1** — video generation, AI avatars in Vids and Gemini app

## Summary Model Table with Fintech Mapping

| Characteristic | Gemini 3 Flash | Gemini 3.1 Pro | Gemini 3.1 Flash-Lite |
|:---|:---|:---|:---|
| **Architecture** | MoE + reasoning | Agentic reasoning | MoE (cost-effective) |
| **Context window** | 1M tokens | 1M tokens | 1M tokens |
| **Specialization** | Speed + intelligence | Complex multimodal tasks | Bulk processing, low-cost |
| **Benchmarks** | GPQA Diamond 90.4%, HLE 33.7% | ARC-AGI-2: 77.1% | $0.25/1M input tokens |
| **Fintech application** | Chatbots, initial scoring | Code analysis, autonomous agents | Classification, batch processing |

## Significance of Extended Context Window

All current models (Gemini 3.1 Pro, 3 Flash, 3.1 Flash-Lite) support a window of up to **1 million tokens**, enabling loading of complete code repositories or multi-year documentation archives for analysis without losing coherence. In the fintech context, this provides unprecedented accuracy for needle-in-a-haystack tasks — whether searching for a specific clause in thousands of legal contracts or detecting vulnerabilities in a distributed microservices architecture.

## AI Capabilities in Workspace

### Gmail
- **Help me write**: Rapid composition of professional emails
- **Contextual smart replies**: Intelligent response suggestions
- **Side panel**: AI assistant in the Gmail interface

### Google Docs
- **Help me write**: Document creation and editing
- **Help me create an image**: Image generation within documents
- **Summarize a document**: Automatic summarization
- **Side panel**: AI assistant for working with documents

### Google Sheets
- **Enhanced smart fill**: Improved data autofill
- **Side panel**: AI data analysis in spreadsheets
- **Trend identification**: Discovering hidden trends in data (portfolio, markets)

### Google Slides
- **Help me create an image**: Graphics generation for presentations
- **Remove image backgrounds**: Automatic background removal
- **Side panel**: AI assistant for presentations

### Google Meet
- **Take notes for me**: Automatic meeting notes
- **Translated captions**: Real-time translation (100+ language pairs)
- **Studio features**: Audio, video, and lighting enhancement
- **Generate background**: AI background generation
- **Watermarking**: Watermarks (Business Plus+)
- **Adaptive audio**: Background noise management

### Google Drive
- **Analyze PDFs**: Document content extraction and analysis
- **Side panel**: AI assistant for file management

### Google Chat
- **Summarize conversations**: Discussion summarization
- **Automatic translation**: Automatic message translation

## Agents in Gemini Enterprise

### Pre-built (Made by Google)
1. **Deep Research** — automatic research across hundreds of sources, creating detailed reports
2. **NotebookLM Enterprise** — deep analysis of uploaded documents with citations
3. **Gemini Code Assist Standard** — assistance with writing and debugging code
4. **Data Insights Agent** — data analysis
5. **Idea Generation** — tournament-style brainstorming and idea generation

### Agent Gallery
- Ready-made agents from Google and partners
- Support for Dialogflow, A2A, ADK agents
- Marketplace integration

### Custom Agents
- **Agent Designer** (no-code) — creating agents using natural language
- **Full-code custom agents** — for developers (Agent Development Kit — ADK)
- Support for multi-step workflows

## Vertex AI (for Developers)

Gemini Enterprise is complemented by Vertex AI for backend development:
- API access to all Gemini models
- Rate limits depend on model and region
- Quotas: 500 data stores/project, 500 engines/project (expandable)
- Shared quotas with Vertex AI Search

---

# 4. Workflows for a Fintech Company

## Using Google Workspace + Gemini Enterprise in Fintech IT Development

### 4.1 Product Development (Engineering)

#### Gemini Code Assist

**Core Capabilities:**
- **Code generation**: autocomplete, function generation, refactoring
- **Code review**: code analysis, vulnerability detection
- **Debugging**: automatic error diagnosis
- **Documentation**: docstring, README, API docs generation
- **Tool evaluation**: assistance in selecting and integrating new monitoring tools

**Advanced Code Assist Capabilities:**
- **Agent Mode** — multi-step tasks: refactoring an entire module, updating dependencies across the project
- **Gemini CLI** — access to Code Assist from the developer's terminal
- **Local codebase awareness** — generating suggestions that account for company-specific internal libraries and coding standards
- **Automatic test generation** — creating unit tests to ensure high code coverage

**IDE Integrations:** VS Code, JetBrains, Android Studio

#### Integration with GitHub and DevOps

Gemini Code Assist on GitHub acts as an intelligent reviewer with issue severity classification:

| Integration Scenario | Description | Result |
|:---|:---|:---|
| **GitHub PR Review** | Automatic summarization and code review with severity levels (Critical, High, Medium, Low) | Faster reviews |
| **Jira Issue Creation** | Ticket creation from Gemini Enterprise chat | Reduced administrative overhead |
| **Confluence Wiki Sync** | Documentation generation from code and logs | Up-to-date technical documentation |
| **Firebase App Quality** | Crash analysis and fix suggestions | Improved mobile app stability |

**Style Guides ("golden paths"):** Platform administrators can define centralized Style Guides at the organization level. This ensures that AI suggests solutions that comply with internal quality and security standards — critically important for fintech.

#### Automatic Gherkin Test Case Generation

A QA engineer can use Gemini to generate BDD scenarios based on technical specifications from Confluence:

1. **Spec preparation** in Confluence with business rules and acceptance criteria
2. **Gemini prompt**: "Analyze the spec and create a set of test cases in Gherkin format. Include positive scenarios, negative scenarios, and edge cases"
3. **Permissions-aware connector** ensures access to the document based on the QA engineer's permissions
4. **Result**: Gherkin scenarios (Given-When-Then) for import into TestRail or Jira (X-Ray/Zephyr)

#### Automatic OpenAPI Documentation Generation

1. Developer documents REST controllers (Spring Boot) with Javadoc comments
2. Gemini Code Assist generates an OpenAPI 3.0 specification in YAML via prompt
3. CI/CD pipeline validates the specification (`swagger-cli`), generates client SDKs (`openapi-generator-cli`)
4. Artifact is published on the internal developer portal

#### Automated Code Compliance Checking (SonarQube + Gemini)

Integration of Gemini with SonarQube and Confluence for automatic code compliance report generation:

1. **Confluence connector** indexes pages with internal security standards
2. **Custom SonarQube connector** extracts SAST scan results
3. **Prompt**: "Create a code compliance report for the project, map vulnerabilities from SonarQube to internal standards from Confluence, classify by risk level"
4. **Result**: Structured report in Google Docs — summary, details, standards mapping, remediation recommendations

#### Custom AI Agents for Development
- CI/CD pipeline monitoring automation
- Agents for log analysis and incident response
- Integration with Jira/Linear for automatic task tracking
- Agents for automated testing and QA
- **Compliance Evidence** — automatic collection of proof that all checks passed for audits

#### Workspace for DevOps
- **Google Chat** — integration with alerting (PagerDuty, OpsGenie via connectors)
- **Google Meet** — post-mortem meetings with automatic notes
- **Google Docs** — auto-generation of runbooks and incident documentation

### 4.2 Analytics and Data Science

#### Financial Data Analysis
- **Sheets AI** — discovering hidden trends in portfolios
- **Predictive analytics** — market trend forecasting
- **BigQuery integration** — Gemini Enterprise connects to BigQuery for natural language data analysis
- **Data Insights Agent** — automatic data analysis for business users

#### Financial Analytics and KPI Calculation in Sheets

Gemini in Google Sheets allows analysts to move from manual formula entry to natural language queries. To calculate liquidity or profitability ratios, it is sufficient to ask the AI to analyze an uploaded balance sheet. The model can not only provide the result but also explain the reasons behind changes in metrics.

**Sample Prompts for a Product Analyst:**

1. **Conversion funnel**: "Analyze the data. Build a conversion funnel: view → cart → purchase. Identify the top 5 products with low conversion"
2. **A/B test hypotheses**: "Suggest 3 hypotheses for an A/B test to increase average order value. For each: hypothesis, primary metric, potential risks"
3. **Anomaly detection**: "Find the 5 most significant anomalies in transactions for the last month by amount. For each, indicate user_id and date"
4. **Segmentation**: "Segment users into 3 groups by purchasing behavior. Create a pivot table with average order value by segment and region"

**Limitations:** Sheets AI is effective for tens of thousands of rows. For millions of records — pre-aggregate in BigQuery, then import results into Sheets for visualization.

#### Risk Management & Fraud Detection
- Real-time identification of anomalies and unusual patterns
- AI-powered fraud detection — 40% reduction in false positives (Macquarie Bank case)
- Comprehensive risk assessment

### 4.3 Product Management

#### Research and Strategy
- **Deep Research** — automatic competitor research, market trend analysis
- **NotebookLM** — analysis of market reports, regulatory filings
- Summarization of earnings reports and regulatory changes

#### NotebookLM for Compliance and Due Diligence

NotebookLM becomes a central hub for working with large knowledge bases:
- **Knowledge synthesis**: upload directives (GDPR, EBA) → instant answers about new feature compliance
- **Earnings Calls analysis**: upload competitor investor call transcripts to highlight key trends and threats
- **Source of truth**: references to specific pages and paragraphs of uploaded documents — eliminates hallucinations and ensures verifiability

#### Requirements Management
- **Docs AI** — rapid PRD and user story drafting
- **Sheets AI** — backlog prioritization, metrics analysis
- **Slides AI** — preparing presentations for stakeholders

### 4.4 Automated Financial Document Processing

Fintech products often require processing large volumes of incoming documents (invoices, statements, ID cards). With Gemini and Google Cloud, an automated pipeline can be built:

1. **Next-generation OCR** — Gemini understands the context and semantic structure of a document, accurately extracting data even from unstructured files
2. **Intelligent categorization** — automatic mapping of extracted data to accounting codes or expense categories
3. **Anomaly analysis** — comparing data from new documents with historical patterns, instantly flagging suspicious transactions

### 4.5 Customer Service

#### Customer Support Automation
- AI chatbots powered by Gemini Enterprise for 24/7 support
- Personalized responses based on customer profiles
- 38% more users redirected to self-service (Macquarie case)

#### Client Onboarding
- KYC/AML verification automation
- Automatic client registration via AppSheet
- Compliance approvals automation

### 4.6 Marketing and Communications

#### Content Marketing
- **Docs Help me write** — rapid creation of marketing materials
- **Gmail AI** — personalized email campaigns (40% reduction in creation time — Virgin Voyages case)
- **Vids** — video content creation with AI avatars
- **Slides** — presentations for investors and clients

#### Translation and Localization
- Automatic document and email translation
- Real-time translation in meetings (100+ languages)
- Global communication scaling

### 4.7 Compliance and Legal

#### Regulatory Monitoring
- **Deep Research** — tracking regulatory changes
- **NotebookLM** — analysis of regulatory documents with citations
- Automatic compliance report generation

#### Document Management
- Automated report creation for regulators
- AI-powered Data Loss Prevention
- Client-side encryption for confidential documents

### 4.8 HR and Internal Processes

- **Gmail AI** — 20% faster internal communications (FinQuery case)
- **Chat AI** — team discussion summarization
- **Meet AI** — auto-notes with action items
- Agents for HR (new employee onboarding, FAQ)
- Integration with ServiceNow for IT support

## Typical Fintech Stack

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
│          Integrations                        │
│  Jira │ Salesforce │ ServiceNow │ Slack     │
│  GitHub │ Confluence │ SAP │ SonarQube      │
└─────────────────────────────────────────────┘
```

---

# 5. Security and Compliance

## Google Workspace — Certifications

### International Standards
- **ISO/IEC 27001** — information security management
- **ISO/IEC 27017** — cloud security
- **ISO/IEC 27018** — protection of personal data in the cloud
- **ISO/IEC 27701** — privacy information management
- **ISO/IEC 42001** — AI management systems (world's first AIMS certification)
- **SOC 1, 2, and 3** — security, financial reporting, and privacy controls
- **FedRAMP High** — federal security standard (USA)
- **HIPAA** — for processing health-related data
- **PCI DSS 4.0.1** — certified for **Google Cloud Platform** (NOT for Google Workspace). GCP must be used for processing payment card data

### Financial Regulators

| Regulator / Standard | Scope | Support Status |
|:---|:---|:---|
| **DORA (EU)** | Operational resilience | Supported through contract mappings and Business Continuity (SLA 99.9%) |
| **EBA Guidelines** | Bank outsourcing in the EU | Compliance with audit rights |
| **FINRA / SEC 17a-4** | Record retention in the US | Supported through Cohasset Attestation |
| **CFTC** | Commodity Futures Trading Commission (US) | Supported |
| **OSFI** | Canadian financial regulator | Supported |

**DORA**: Google introduced specialized Business Continuity plans — a separate standby product that maintains access to critical Workspace tools during major infrastructure outages (a direct response to DORA's ICT system resilience requirements).

### Availability
- **99.9% uptime** — guaranteed SLA ([Google Workspace SLA](https://workspace.google.com/terms/sla/))
- **Business Continuity** — a separate standby product for organizations using non-Google tools as primary

## Gemini Enterprise — Security

### Access Management
- **SSO integration** — single sign-on through corporate IdPs (SAML 2.0, OIDC)
- Supported providers: Okta, Azure AD (Microsoft Entra ID), Ping Identity
- **Permission-aware search** — search results correspond to user permissions
- **RBAC** — role-based model (super admins, admins, users)
- **Granular management**: enabling/disabling Gemini at the organizational unit (OU) and configuration group levels (group settings take priority over OU)
- All data is accessible only with appropriate permissions

### Encryption
- **Client-side encryption** — encryption on the client side
- **Customer-Managed Encryption Keys (CMEK)** — the client manages encryption keys
- Data encryption at rest and in transit

### Data Residency
- Administrators can specify the storage region: multi-region **US**, **EU**, or global location
- Settings are applied at the organization or individual OU level
- CMEK usage requires selecting the `us` or `eu` multi-region
- Gemini Enterprise Plus supports **Sovereignty Controls** for sovereign data boundaries

### Data Protection
- **VPC Service Controls** — data exfiltration prevention
- **Model Armor** — protection against adversarial model attacks
- **AI-powered Data Loss Prevention (DLP)** — automatic classification and protection of confidential files
- **Information Rights Management (IRM)** — if a document has a "top secret" label and IRM prohibits downloading, Gemini respects these restrictions
- **Private UI access** — access through a private interface

### Audit and Monitoring
- **Audit logging** — complete action logging
- **Admin dashboard** — centralized agent and security management
- Organization-level AI usage monitoring
- Gemini activity data export for audit purposes

### Data and Model Training
- **Enterprise data is NOT used for model training** (Business, Standard, Plus, Enterprise)
- **Information is not subject to human review** by Google specialists — eliminates risks of confidential financial information leakage
- **Starter edition**: data may be used for service improvement and model training; human reviewers may read content. Opt-out is available. Google recommends not sending confidential data through Starter
- Data remains under the organization's control

### Assured Controls (add-on)
- **Data sovereignty** — data location management
- Control over data processing geolocation

## Google Vault — Information Governance and eDiscovery

Google Vault is a key tool for fintech companies, providing retention, search, and export of all electronic communications, including AI-generated content.

### Integration with Gemini

- **Meet transcripts and summaries**: meeting summary documents are saved in Google Drive → subject to Vault policies
- **Chat summaries**: Gemini-generated summaries are saved in Chat spaces → managed by Vault
- **Prompts and responses in the Gemini app**: Vault supports search and export of conversations from the Gemini application (web and mobile)

### Configuration for FINRA / SEC Rule 17a-4

SEC 17a-4 requires record retention in an immutable **WORM** (Write Once, Read Many) format:

1. **Retention Rules**: the administrator creates rules for Google Drive and Chat (e.g., 7 years or indefinite). Rules can be applied to the entire organization or individual OUs
2. **Vault Lock**: retention rule lock — a locked rule cannot be modified or deleted even by super admins. Guarantees data immutability (WORM requirement)
3. **Legal Holds (deletion prohibition)**: during litigation or regulatory requests — data lock for specific users. Takes priority over any retention rules
4. **eDiscovery**: creating a "Matter," searching by keywords/users/dates, export in standard formats (MBOX, CSV, XML) with metadata
5. **FINRA export**: with Enterprise Plus + Assured Controls subscription → export to customer's GCS bucket → archiving via **AODocs** to immutable GCS buckets

### Cohasset Attestation
Google Workspace received **Cohasset Attestation** — an independent assessment of compliance with FINRA/SEC record retention requirements. This simplifies the process of proving compliance to regulators.

## Key Security Metrics

- 33% of Workspace users report reduced security incidents (vs 22% for Microsoft 365) — according to [Google-commissioned survey, October 2025](https://services.google.com/fh/files/misc/google_workspace_v_microsoft_365_final_report_101525.pdf)
- Automatic classification and labeling of confidential files
- Privacy-preserving AI models for industry needs

## Recommendations for Fintech

### Minimum Set for Regulatory Compliance:
1. **Google Workspace Enterprise** (not Business) — full set of compliance features
2. **Client-side encryption** — for customer data and financial transactions
3. **CMEK** — self-managed encryption keys
4. **VPC Service Controls** — data isolation
5. **Assured Controls** — if data sovereignty is required (GDPR, local regulations)
6. **DLP policies** — automatic prevention of personal and financial data leakage
7. **Audit logging** — for regulatory inspections and internal audits
8. **Google Vault** — with configured retention rules and Vault Lock for WORM compatibility

### Limitations for Fintech:
- PCI DSS is certified for GCP, NOT for Google Workspace — GCP infrastructure is required for payment data processing
- Not all models have received industry certification
- Phased rollout with a pilot group is recommended

---

# 6. Fintech Case Studies

## Financial Organizations Using Google Workspace + Gemini

### FinQuery (fintech, SaaS for accounting)
- **Product**: Google Workspace with Gemini
- **Usage**:
  - VP of Infrastructure saves 20% of time on email
  - Engineering teams use Gemini for debugging and troubleshooting code
  - Brainstorming and project planning
  - Onboarding assistance — questions about new systems and integrations
  - Evaluation and adoption of new monitoring tools

### Grasshopper Bank (digital bank, $1.4B in assets)
- **Product**: Gemini Enterprise
- **Specifics**: Fully digital bank without branches, serving startups and fintech
- **Usage**:
  - Developing an agent-based system for natural language access to banking data
  - Integrating Google Drive documents with core banking system via BigQuery
  - Secure natural language data access for employees

### ATB Financial (financial institution, Canada)
- **Product**: Google Workspace with Gemini
- **Scale**: 5,000+ employees
- **Results**:
  - Routine task automation
  - Quick access to information
  - Improved collaboration efficiency

### Macquarie Bank (Australian diversified financial group, retail banking)
- **Product**: Gemini Enterprise
- **Results**:
  - 38% more users redirected to self-service solutions
  - 40% reduction in false positive fraud alerts
  - Significant improvement in customer experience

### Equifax (credit bureau)
- **Product**: Google Workspace with Gemini
- **Results**:
  - 90% of pilot project participants noted improved quality and volume of work
  - Enhanced security posture alongside productivity growth

### Banestes (Brazilian bank)
- **Product**: Google Workspace with Gemini
- **Usage**:
  - Accelerated credit analysis
  - Improved legal and marketing department productivity

### Banco BV (Brazilian bank)
- **Product**: Gemini Enterprise
- **Usage**:
  - Analytics automation for client relationship managers
  - Managers previously spent hours on independent data analysis — now Gemini handles this work, freeing time for acquiring new clients

### Nu Bank (digital bank, Brazil)
- **Product**: Google Workspace (basic tools)
- **Status**: Uses Workspace for productivity, but AI strategy is built on a partnership with OpenAI, not Google Gemini

### Robinhood (fintech broker)
- **Product**: Google Workspace
- **Status**: Noted as adopter (details not disclosed)

### BBVA (international bank)
- **Product**: Google Workspace
- **Status**: Noted as adopter (details not disclosed)

### Pennymac (mortgage company)
- **Product**: Google Workspace
- **Status**: Noted as adopter (details not disclosed)

### Paysera (Lithuanian fintech, payment solutions)
- **Product**: Gemini Enterprise + internal App-MCP framework
- **Usage**:
  - Custom MCP server for automatic test case generation (cost per file: 6-7 cents)
  - AI Code Review in CI/CD pipeline (GitLab)
  - Automatic Compliance Evidence collection for audits
  - Jira + Confluence + GitLab integration via permissions-aware connectors
- **Principle**: "AI does — human decides"

## Other Industries (Relevant Patterns)

### Virgin Voyages (travel)
- Created AI agent "Email Ellie"
- 40% reduction in email campaign creation time
- 28% year-over-year sales growth

### Gordon Food Service (12,000 employees)
- Agents connect ServiceNow and Jira for customer insights
- HR communications through AI

### Banesco USA (bank)
- 10-15% productivity increase

### Seguros Bolivar (insurance)
- 20-30% cost reduction

### WEX (fintech, payment solutions)
- 63,000 hours saved monthly

## Key Takeaways for Fintech

1. **Quick ROI** — most companies see 10-20% productivity increase
2. **Fraud detection** — AI significantly reduces false positives (up to 40%)
3. **Customer service** — up to 38% more queries resolved via self-service
4. **Email/Comms** — 20-40% time savings on communications
5. **Scalability** — from 200 to 60,000+ employees
6. **Security first** — financial companies confirm adequacy of security controls

---

# 7. Strategic Implementation: From Pilot to Production

Transitioning to Gemini Enterprise requires a structured approach. The experience of ATB Financial, Equifax, and other companies shows that success depends on proper change management setup.

## 4-Phase Implementation Plan

### Phase 1: Infrastructure
- Setting up **VPC Service Controls** and **CMEK** in Google Cloud Console for a secure perimeter
- Assigning IAM roles (e.g., `Discovery Engine Editor`) to responsible personnel
- Configuring **DLP policies** and **Vault** with retention rules
- Setting up SSO (SAML 2.0 / OIDC) and Identity Mapping

### Phase 2: Integration
- Connecting key data sources (Jira, GitHub, Drive, Confluence)
- Setting up permissions-aware connectors with OAuth 2.0
- Configuring quotas and limits to prevent uncontrolled cost growth
- Setting up Style Guides (golden paths) for Code Assist

### Phase 3: Piloting
- Launching focus groups:
  - **Developers** — Code Assist (Agent Mode, auto-generated tests, PR review)
  - **Financial analysts** — NotebookLM, AI in Sheets, Data Insights Agent
  - **Compliance officers** — Google Vault, Deep Research for regulatory monitoring
- Collecting metrics: Lead Time for Changes, Code Coverage, Time-to-Market, False Positive Rate
- Evaluating and adjusting Style Guides based on feedback

### Phase 4: Scaling
- Deploying custom agents for specific processes:
  - KYC/AML onboarding automation
  - Compliance control in CI/CD (SonarQube + Gemini)
  - Financial document processing pipeline
- Consolidating AI subscriptions into a single platform — reducing "AI technical debt"
- Publishing internal agents in the Agent Gallery for the organization

## Reducing AI Technical Debt

Implementing Gemini Enterprise enables consolidation of disparate generative AI tool subscriptions into a single, secure, and managed platform. This not only optimizes the budget but also creates a unified standard for data security and quality across the entire organization.

---

# 8. Sources

## Official Google Pages

### Pricing & Plans
- [Google Workspace Pricing](https://workspace.google.com/pricing) — official pricing page
- [Compare Google AI expansion add-ons](https://knowledge.workspace.google.com/admin/getting-started/editions/compare-google-ai-expansion-add-ons) — AI add-on comparison
- [How Google Workspace with Gemini billing works](https://knowledge.workspace.google.com/admin/gemini/how-google-workspace-with-gemini-billing-works) — Workspace+Gemini billing
- [AI Ultra Access](https://knowledge.workspace.google.com/admin/gemini/ai-ultra-access) — ultra plan description

### Gemini Enterprise (Google Cloud)
- [Gemini Enterprise — Main Page](https://cloud.google.com/gemini-enterprise) — main product page
- [What is Gemini Enterprise?](https://docs.cloud.google.com/gemini/enterprise/docs) — documentation
- [Compare editions of Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/editions) — edition comparison
- [Gemini Enterprise FAQ](https://cloud.google.com/gemini-enterprise/faq) — FAQ
- [NotebookLM Enterprise vs Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/choose-product) — product selection
- [Introducing Gemini Enterprise (Blog)](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise) — product announcement
- [Quotas and system limits](https://docs.cloud.google.com/gemini/enterprise/docs/quotas) — quotas and limits
- [Choose your edition](https://support.google.com/g/answer/16547364?hl=en) — edition selection
- [Compliance certifications and security controls](https://docs.cloud.google.com/gemini/enterprise/docs/compliance-security-controls) — certifications
- [Example use cases](https://docs.cloud.google.com/gemini/enterprise/docs/example-use-cases) — use case examples
- [Introduction to connectors and data stores](https://docs.google.com/gemini/enterprise/docs/connectors/introduction-to-connectors-and-data-stores) — connectors

### Gemini AI Features in Workspace
- [Gemini AI features in Workspace subscriptions](https://knowledge.workspace.google.com/admin/gemini/gemini-ai-features-now-included-in-google-workspace-subscriptions) — full AI feature list
- [AI Tools for Business](https://workspace.google.com/solutions/ai/) — AI tools for business
- [Workspace Updates: Higher AI access (Feb 2026)](https://workspaceupdates.googleblog.com/2026/02/google-workspace-ai-expanded-access.html) — February 2026 updates
- [Gemini Workspace updates (March 2026)](https://blog.google/products-and-platforms/products/workspace/gemini-workspace-updates-march-2026/) — March 2026 updates
- [Gemini for Google Workspace FAQ](https://knowledge.workspace.google.com/admin/gemini/gemini-for-google-workspace-faq) — FAQ

### Gemini Models
- [Gemini 3.1 Pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/) — model announcement
- [Gemini 3.1 Pro on CLI, Enterprise, Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-3-1-pro-on-gemini-cli-gemini-enterprise-and-vertex-ai) — technical description
- [Gemini 3 Flash](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-flash) — documentation
- [Gemini 3 Pro](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro) — documentation
- [Gemini 3.1 Flash-Lite](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/) — cost-effective model
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing) — API pricing
- [Gemini API Rate Limits](https://ai.google.dev/gemini-api/docs/rate-limits) — API limits

### Code Assist & SDLC
- [Gemini Code Assist overview](https://developers.google.com/gemini-code-assist/docs/overview) — overview
- [Code Assist for teams and businesses](https://codeassist.google/products/business) — for business
- [Code Assist Standard and Enterprise overview](https://docs.cloud.google.com/gemini/docs/codeassist/overview) — Standard and Enterprise
- [Code Assist quotas and limits](https://developers.google.com/gemini-code-assist/resources/quotas) — quotas
- [Review GitHub code using Code Assist](https://developers.google.com/gemini-code-assist/docs/review-github-code) — GitHub PR review
- [Code Assist in GitHub for Enterprises](https://cloud.google.com/blog/products/ai-machine-learning/gemini-code-assist-in-github-for-enterprises/) — Style Guides, golden paths
- [Gemini for end-to-end SDLC](https://www.skills.google/paths/236/course_templates/885) — course

### Connectors & Data Integration
- [Connect your Google apps and third-party data](https://support.google.com/g/answer/16550932?hl=en) — data connection
- [Connect a third-party data source](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/connect-third-party-data-source) — third-party sources
- [Set up a Jira Cloud data store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/jira-cloud/set-up-data-store) — Jira
- [Set up a Confluence Cloud data store](https://docs.cloud.google.com/gemini/enterprise/docs/connectors/confluence-cloud/set-up-data-store) — Confluence

### Agents & ADK
- [Integrate Gemini Enterprise Agents with Workspace (Codelab)](https://codelabs.developers.google.com/ge-gws-agents) — agent tutorial
- [Gemini API for Developers](https://ai.google.dev/gemini-api/docs) — API

### Financial Services
- [Google Workspace for Finance](https://workspace.google.com/industries/finance/) — industry page
- [Financial Services on Google Cloud](https://cloud.google.com/solutions/financial-services) — Google Cloud for finance
- [Transform Financial Services with AI (UK)](https://workspace.google.com/intl/en_uk/industries/finance/) — EBA Guidelines
- [AI for Finance — Gemini](https://workspace.google.com/solutions/ai/finance/) — AI for finance
- [Analyze financial statements (use case)](https://docs.cloud.google.com/gemini/enterprise/docs/use-case-analyze-financial-statements) — financial statement analysis
- [Expanding commitments for Financial Services](https://workspace.google.com/blog/product-announcements/expanding-commitments-to-help-global-financial-services-customers) — DORA, BC

### Security and Compliance
- [Cloud Security](https://workspace.google.com/security/) — security
- [Generative AI Privacy Hub](https://knowledge.workspace.google.com/admin/gemini/generative-ai-in-google-workspace-privacy-hub) — AI privacy
- [Gemini Security Privacy Compliance Whitepaper](https://workspace.google.com/learning/content/gemini-privacy-security-compliance-whitepaper) — whitepaper
- [EBA Outsourcing Guidelines Mapping](https://services.google.com/fh/files/misc/eba_outsourcing_guidelines_googleworkspace_compliance_mapping.pdf) — EBA mapping
- [Google Workspace SLA](https://workspace.google.com/terms/sla/) — SLA

## Case Studies and Analytics

### Fintech Cases
- [FinQuery case study](https://workspace.google.com/blog/customer-stories/finquery-innovates-gemini-google-workspace) — FinQuery + Gemini
- [Grasshopper Bank case study](https://workspace.google.com/customers/grasshopper-bank/) — Grasshopper Bank
- [128 ways customers use AI](https://workspace.google.com/blog/ai-and-machine-learning/how-our-customers-transform-work-with-ai) — 128 AI use cases
- [101 real-world gen AI use cases](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders) — 101 cases from industry leaders
- [Gemini at Work 2024](https://blog.google/innovation-and-ai/infrastructure-and-cloud/google-cloud/gemini-at-work-ai-agents/) — AI agents in practice

### Analytical Articles
- [Google Workspace Pricing 2026 (Name.com)](https://www.name.com/blog/google-workspace-pricing) — pricing overview
- [Google Workspace Pricing 2026 (Lineserve)](https://www.lineserve.net/blog/google-workspace-pricing-2026) — pricing overview
- [Gemini Pricing 2026 (Finout)](https://www.finout.io/blog/gemini-pricing-in-2026) — Gemini pricing overview
- [Gemini Workspace pricing guide (eesel.ai)](https://www.eesel.ai/blog/gemini-workspace-pricing) — pricing guide
- [Workspace Gemini pricing changes (Cumulus Global)](https://www.cumulusglobal.com/google-workspace-gemini-ai-features-and-pricing-changes/) — pricing changes
- [Gemini for Business plans (IntuitionLabs)](https://intuitionlabs.ai/articles/gemini-business-pricing-plans) — plan overview
- [Gemini Enterprise guide (Revolgy)](https://www.revolgy.com/insights/blog/guide-to-gemini-enterprise-features-pricing-and-implementation) — complete guide
- [Gemini Enterprise vs Workspace (Premier Cloud)](https://premiercloud.com/blog/gemini-enterprise-how-is-it-different-from-gemini-in-workspace-and-notebooklm/) — comparison
- [Gemini for Financial Services (Promevo)](https://promevo.com/blog/gemini-for-financial-services) — for finance
- ~~[Top 6 Gemini Use Cases (Cloudfresh)](https://cloudfresh.com/en/blog/gemini-google-workspace/)~~ — link unavailable (403 Cloudflare)
- [Google Workspace price increase (9to5Google)](https://9to5google.com/2025/01/15/google-workspace-gemini-price-increase/) — price increase
- [Workspace drops Gemini add-on (Constellation Research)](https://www.constellationr.com/insights/news/google-workspace-drops-gemini-add-charge-raises-business-enterprise-plan-prices) — add-on removal
- [Google AI Guide: Enterprise vs Vertex vs Workspace (ByteeIT)](https://byteeit.com/blog/google-ai-comparison-gemini-enterprise-vertex-ai-workspace) — comparison
- [Gemini Enterprise (Devoteam)](https://www.devoteam.com/google-cloud-gemini-enterprise/) — overview
- [10 Differences: Workspace with Gemini vs Enterprise (Devoteam)](https://www.devoteam.com/expert-view/google-workspace-with-gemini-vs-gemini-enterprise-10-differences-you-should-know/) — differences
- [Gemini for Financial Services (Evonence)](https://www.evonence.com/blog/gemini-for-enterprise-in-financial-services-the-new-era-of-intelligent-finance) — for finance
- [TEI of Google Workspace with Gemini (Forrester)](https://tei.forrester.com/go/Google/WorkspaceWithGemini/index.html) — Forrester report
- [Google Workspace vs Microsoft 365 Survey](https://services.google.com/fh/files/misc/google_workspace_v_microsoft_365_final_report_101525.pdf) — security research
