# Отчёт фактчекинга

**Статья**: «Vibe Coding»: как AI пишет код в EVE Frontier — MCP, Claude, Move
**Файл**: docs/wowcasual/eve_frontier/drafts/vibe_coding_ai_mcp_claude_move_2026_03_16/vibe_coding_ai_mcp_claude_move_2026_03_16_original_draft.md
**Дата проверки**: 2026-03-21
**Режим**: обычный

## Сводка
- Всего проверяемых фактов: 14
- ✓ Подтверждено: 10
- ⚠ Требует внимания: 2
- ✗ Ошибка вероятна: 0
- ? Не удалось проверить: 2

## Оценка достоверности: ВЫСОКАЯ (87%)
Статья корректно описывает концепцию vibe coding, MCP, хакатон и связь между AI-инструментами и EVE Frontier. Термин «vibe coding» верно датирован 2025 годом. Технические описания MCP и Smart Assemblies точны.

## Детальные результаты
| # | Утверждение | Критичность | Итог | Комментарий |
|---|------------|-------------|------|-------------|
| 1 | Термин «vibe coding» появился в 2025 году | Высокая | ✓ | Подтверждено: введён Andrej Karpathy 2 февраля 2025 года |
| 2 | Хакатон EVE Frontier x Sui, призовой фонд $80,000 | Высокая | ✓ | Подтверждено множественными источниками |
| 3 | Хакатон 11-31 марта 2026 | Высокая | ✓ | Подтверждено |
| 4 | Тема хакатона «Toolkit for Civilization» | Средняя | ✓ | Подтверждено: "Toolkit for Civilization" |
| 5 | Два типа проектов: моды для Smart Assemblies и внешние приложения через API | Средняя | ✓ | Подтверждено: "in-world mods" и "external tools" |
| 6 | MCP (Model Context Protocol) — архитектурный стандарт для взаимодействия AI с внешними инструментами | Высокая | ✓ | Подтверждено: MCP — стандарт Anthropic для Claude |
| 7 | «Значительная часть кода на хакатоне создаётся AI» | Средняя | ⚠ | Субъективная оценка автора. Вайб-кодинг активно обсуждается, но нет данных о доле AI-кода на конкретном хакатоне |
| 8 | Smart Assemblies работают на смарт-контрактах Move | Высокая | ✓ | Подтверждено |
| 9 | Claude демонстрирует хорошее понимание Move | Средняя | ? | Субъективная оценка, не поддаётся формальной верификации |
| 10 | Move-специфичные паттерны Sui отличаются от Aptos-варианта | Средняя | ✓ | Подтверждено: Sui Move и Aptos Move имеют различия |
| 11 | CCP Good Fellow — геймдиректор, «patient zero», тестировал документацию | Средняя | ✓ | Подтверждено транскриптом |
| 12 | 30 000+ изменённых файлов при миграции на Sui | Средняя | ✓ | Подтверждено транскриптом |
| 13 | Цитата Good Fellow: «If you're out there...try out the hackathon» | Низкая | ? | Из транскрипта, не удалось верифицировать дословно |
| 14 | Хакатон стартовал одновременно с Cycle 5 | Средняя | ⚠ | Оба начались 11 марта, но формально хакатон мог иметь отдельное объявление. По факту даты совпадают |

## Проблемные факты
Серьёзных ошибок не выявлено. Основные замечания:
1. **Доля AI-кода на хакатоне** — утверждение о «значительной части» кода, созданной AI, является редакторской оценкой без конкретных данных.

## Использованные источники
- [Wikipedia: Vibe coding](https://en.wikipedia.org/wiki/Vibe_coding)
- [Sui Blog: EVE Frontier Hackathon](https://blog.sui.io/eve-frontier-migrates-to-sui-hackathon-live/)
- [BlockchainGamerBiz: Cycle 5 hackathon](https://www.blockchaingamer.biz/news/41861/eve-frontier-cycle-5-optimizations-80000-dollar-hackathon-20-dollar-game-only-pass/)
- [Matt Geiger: Practical Guide to Vibe Coding with Claude and MCP](https://www.geigertron.com/blog/2025/4/4/a-practical-guide-to-vibe-coding-with-claude-and-mcp-tools)
- [Protos: Claude AI plugins can now vibe code smart contracts](https://protos.com/claude-ai-plugins-can-now-vibe-code-smart-contracts/)
- [CCP Games: Cycle 5 Shroud of Fear](https://www.ccpgames.com/news/2026/eve-frontier-enters-cycle-5-shroud-of-fear-starting-march-11)
