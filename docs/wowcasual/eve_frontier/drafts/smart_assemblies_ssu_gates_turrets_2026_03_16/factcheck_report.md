# Отчёт фактчекинга

**Статья**: Smart Assemblies: программируй вселенную — SSU, Gates, Turrets
**Файл**: docs/wowcasual/eve_frontier/drafts/smart_assemblies_ssu_gates_turrets_2026_03_16/smart_assemblies_ssu_gates_turrets_2026_03_16_original_draft.md
**Дата проверки**: 2026-03-21
**Режим**: обычный

## Сводка
- Всего проверяемых фактов: 18
- ✓ Подтверждено: 12
- ⚠ Требует внимания: 3
- ✗ Ошибка вероятна: 2
- ? Не удалось проверить: 1

## Оценка достоверности: СРЕДНЯЯ (75%)
Статья хорошо описывает концепцию Smart Assemblies и их типы. Основные проблемы: несоответствие в описании типов турелей (Mini/Standard/Heavy вместо Autocannon/Plasma/Railgun), неверное утверждение о предыдущем лимите в 6 турелей (было 3 на Smart Assembly).

## Детальные результаты
| # | Утверждение | Критичность | Итог | Комментарий |
|---|------------|-------------|------|-------------|
| 1 | Smart Assembly — программируемый объект на блокчейне Sui, управляемый смарт-контрактом Move | Высокая | ✓ | Подтверждено документацией |
| 2 | Три типа: SSU, Smart Gate, Smart Turret | Высокая | ✓ | Подтверждено |
| 3 | SSU — хранилище с активным инвентарём в фиксированной точке | Высокая | ✓ | Подтверждено: "deployed to a fixed location in space with an active inventory" |
| 4 | SSU может быть торговым терминалом, квестовым NPC, системой баунти и т.д. | Средняя | ✓ | Подтверждено — SSU программируется произвольной логикой |
| 5 | Smart Gate — игрок-созданные врата между системами | Высокая | ✓ | Подтверждено: "allows ships to jump from one star system to another" |
| 6 | Настраиваемая логика допуска (открытые, племенные, платные и т.д.) | Средняя | ✓ | Подтверждено документацией |
| 7 | Smart Turret устанавливается в радиусе 25 км от другой Smart Assembly | Средняя | ? | Не удалось верифицировать конкретный радиус 25 км |
| 8 | Турель автоматически прикрепляется к Smart Assembly | Средняя | ✓ | Подтверждено: турели "attach to existing Smart Assemblies" |
| 9 | Предыдущая система: максимум 6 турелей на локацию | Высокая | ✗ | По документации, лимит был 3 турели на Smart Assembly, а не 6 |
| 10 | Ранее нужно было вручную устанавливать корабельные орудия на турели | Средняя | ✓ | Подтверждено транскриптом разработчиков |
| 11 | Новая система: оружие встроено (embedded) в каждый тип турели | Высокая | ✓ | Подтверждено: три специализированных типа с встроенным вооружением |
| 12 | Лимит в 6 турелей полностью убран — теперь ограничение по энергосети (power-based) | Высокая | ⚠ | Убрание фиксированного лимита подтверждено транскриптом, но исходный лимит был 3, а не 6 |
| 13 | Типы: Mini Turret, Turret (стандартная), Heavy Turret | Высокая | ✗ | Официальные названия в Cycle 5: **Autocannon Turret** (малые цели), **Plasma Turret** (средние), **Railgun Turret** (крупные). Названия Mini/Standard/Heavy не совпадают |
| 14 | Логика наведения программируется: приоритеты, белый список, зона контроля | Средняя | ✓ | Подтверждено: "build custom logic for targeting systems" |
| 15 | Система блюпринтов — готовые пакеты Move | Средняя | ✓ | Подтверждено: builder-examples на GitHub |
| 16 | EVE Frontier x Sui Hackathon 2026, 11-31 марта, $80,000 | Высокая | ✓ | Подтверждено |
| 17 | Обфускация локаций — координаты как хэш | Высокая | ✓ | Подтверждено |
| 18 | Добровольный broadcasting в ближайшем point release | Средняя | ⚠ | Подтверждено транскриптом, но статус реализации на 21 марта неизвестен |

## Проблемные факты
1. **Названия турелей** — статья использует Mini Turret / Turret / Heavy Turret, но официальные названия в Cycle 5: Autocannon Turret, Plasma Turret, Railgun Turret. Рекомендуется исправить.
2. **Предыдущий лимит турелей** — указано «максимум 6 турелей», но по документации лимит был 3 турели на Smart Assembly. Рекомендуется уточнить.

## Использованные источники
- [EVE Frontier Docs: Smart Assemblies](https://docs.evefrontier.com/SmartAssemblies)
- [EVE Frontier Support: Smart Turret](https://support.evefrontier.com/hc/en-us/articles/20197323010076-Smart-Turret)
- [EVE Frontier Support: Smart Assembly](https://support.evefrontier.com/hc/en-us/articles/19355304547228-Smart-Assembly)
- [CCP Games: Cycle 5 Shroud of Fear](https://www.ccpgames.com/news/2026/eve-frontier-enters-cycle-5-shroud-of-fear-starting-march-11)
- [Pool Party Nodes: Smart Assemblies Guide](https://poolpartynodes.com/eve-frontier-smart-assemblies-a-beginners-guide/)
- [GitHub: builder-examples](https://github.com/projectawakening/builder-examples)
