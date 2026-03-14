# Newsroom — Claude Code Guide

## Project Overview

Python framework for news aggregation, LLM-powered style rewriting, and multi-platform publishing.
Two domains: **wowcasual** (gaming) and **technocrats** (techno-futurology).

## Quick Reference

```bash
# Run the pipeline
python -m newsroom --topic "AI" --format markdown

# Rewriter management
python -m newsroom rewriter-setup -d wowcasual import export.xml
python -m newsroom rewriter-setup -d wowcasual analyze
python -m newsroom rewriter-setup -d wowcasual stats

# Google Drive auth
python -m newsroom gdrive-auth login

# Publisher (multi-platform)
python -m newsroom publisher

# Agency (multi-agent, CrewAI)
python -m newsroom agency
```

## Architecture

Pipeline: **Sources → Processors → Formatters → Exporters**

- `newsroom/sources/` — data source plugins (rss, web, newsapi, obsidian, gdrive)
- `newsroom/processors/` — filter → dedup → llm → rewriter
- `newsroom/formatters/` — markdown, json, html, plaintext
- `newsroom/exporters/` — obsidian, gdrive
- `newsroom/publisher/` — wordpress, telegram, discord, twitter, linkedin, facebook, instagram, reddit
- `newsroom/agency/` — CrewAI multi-agent system
- `newsroom/rewriter/` — LLM style transfer engine (Anthropic API, TF-IDF, SQLite corpus)

All layers are extensible via base classes + registry pattern (`SOURCE_REGISTRY`, `PROCESSOR_REGISTRY`, etc.).

## Configuration

- `config.yaml` (from `config.example.yaml`) — main config
- `.env` (from `.env.example`) — API keys and publisher credentials
- `sources/` — 793 YAML files organized by domain/topic

## Key Conventions

- Language: Python 3, no type checker configured yet
- Config: PyYAML for all configuration
- LLM: Anthropic API via `newsroom/rewriter/llm_client.py`
- Data: SQLite for rewriter corpus (`rewriter/corpus/store.py`)
- All source YAML files: one source per file (type at top level) or multiple under `sources:` key
- Documentation and comments are in Russian

## Dependencies

Core: feedparser, requests, beautifulsoup4, lxml, pyyaml, python-dateutil, jinja2
Optional: anthropic, openai, scikit-learn, pydantic, crewai, google-api-python-client, python-dotenv
