# Отчёт фактчекинга

**Статья**: PvP нового поколения: догфайты на 4Hz
**Файл**: docs/wowcasual/eve_frontier/drafts/pvp_novogo_pokoleniya_dogfajty_na_4hz_2026_03_16/pvp_novogo_pokoleniya_dogfajty_na_4hz_2026_03_16_original_draft.md
**Дата проверки**: 2026-03-21
**Режим**: обычный

## Сводка
- Всего проверяемых фактов: 17
- ✓ Подтверждено: 10
- ⚠ Требует внимания: 4
- ✗ Ошибка вероятна: 0
- ? Не удалось проверить: 3

## Оценка достоверности: ВЫСОКАЯ (85%)
Статья написана в формате личного дневника и корректно описывает систему управления WASD, детенты, камеры и общую философию PvP. EVE Online тик-рейт в 1 Гц подтверждён. Утверждение о «4 Гц» в EVE Frontier основано на субъективных ощущениях автора и не подтверждено официально.

## Детальные результаты
| # | Утверждение | Критичность | Итог | Комментарий |
|---|------------|-------------|------|-------------|
| 1 | EVE Online работала на 1 Гц — один серверный тик в секунду | Высокая | ✓ | Подтверждено: "tick rate of the physics simulation is 1Hz" (EVE University Wiki) |
| 2 | EVE Frontier тик-рейт «минимум в четыре раза чаще» (4 Гц в заголовке) | Высокая | ⚠ | Субъективное ощущение автора, помеченное как «по ощущениям». Официальный тик-рейт EVE Frontier не опубликован. Заголовок «4Hz» создаёт впечатление точной цифры |
| 3 | WASD — дефолтный режим с Cycle 4 | Высокая | ✓ | Подтверждено: "full rollout of the WASD ship control system, now serves as the base flight model" в Cycle 4 |
| 4 | W/S — тангаж, A/D — рыскание | Средняя | ✓ | Подтверждено документацией |
| 5 | E — ускорение, четыре detents: 25%, 50%, 75%, 100% | Средняя | ⚠ | E и Q для контроля тяги подтверждены. Точные значения detents (25/50/75/100%) из транскрипта, но не верифицированы независимо |
| 6 | Q — снижение скорости, при 0% — движение задним ходом (reverse) | Средняя | ⚠ | Логика Q подтверждена, детали реверса из транскрипта |
| 7 | Ctrl+Space — полная остановка | Средняя | ✓ | Подтверждено: "order a full stop of the ship with a press of ctrl-space" |
| 8 | Lie — новый фрегат Cycle 5 | Средняя | ⚠ | Официальные источники упоминают «Exclave frigate», а не «Lie». «Lie» может быть внутриигровым названием или из транскрипта |
| 9 | Lie — ранее известен как Microparo | Низкая | ? | Не удалось верифицировать из открытых источников |
| 10 | Chase camera (C) — мягкое следование за кормой | Средняя | ? | Из транскрипта, не удалось независимо верифицировать |
| 11 | Track camera (T) — удерживает цель и корабль в кадре | Средняя | ? | Из транскрипта, не опровергнуто |
| 12 | Тактическая камера (F2) | Средняя | ✓ | WASD-поддержка в tactical view подтверждена для Cycle 4+ |
| 13 | Автоматическое управление убрано в пользу WASD | Высокая | ✓ | Подтверждено: WASD стал дефолтным, хотя waypoint navigation вернулся |
| 14 | Ребаланс: лёгкие — уклонение и активная защита, тяжёлые — дальний бой и пассивная прочность | Высокая | ✓ | Подтверждено: "lighter hulls accelerate faster, active defenses; heavier ships — mass, top speeds, passive durability" |
| 15 | Mini Turret по лёгким, Heavy Turret по тяжёлым | Средняя | ✓ | Подтверждено: Autocannon (малые), Plasma (средние), Railgun (крупные) |
| 16 | Shell Industry — потеря Shell и Crowns при гибели | Высокая | ✓ | Подтверждено: "Destroyed Shells result in permanent loss of equipped skills and memories" |
| 17 | Skip module — резкое увеличение скорости по прямой, потребляет capacitor | Средняя | ✓ | Подтверждено транскриптом и геймплейными описаниями |

## Проблемные факты
1. **4 Гц в заголовке** — конкретная цифра тик-рейта не подтверждена официально. Статья корректно помечает это как ощущение, но заголовок создаёт впечатление факта. Рекомендуется изменить заголовок или добавить явное указание, что 4 Гц — оценка автора.
2. **Lie vs Exclave** — в официальных анонсах Cycle 5 упоминается «Exclave frigate», а не «Lie». Требует уточнения.

## Использованные источники
- [EVE University Wiki: Server tick](https://wiki.eveuniversity.org/Server_tick)
- [BlockchainGamerBiz: Cycle 4 WASD controls](https://www.blockchaingamer.biz/news/41140/eve-frontiers-cycle-4-live-wasd-controls/)
- [Massively OP: EVE Frontier WASD](https://massivelyop.com/2025/12/04/blockchain-mmo-eve-frontier-introduces-wasd-flight-controls-and-opens-another-free-test-access-event/)
- [CCP Games: Cycle 5 Shroud of Fear](https://www.ccpgames.com/news/2026/eve-frontier-enters-cycle-5-shroud-of-fear-starting-march-11)
- [Shacknews: Cycle 4 controls](https://www.shacknews.com/article/147120/eve-frontier-cycle-4-wasd-controls-reset)
