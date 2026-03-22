# EVE Frontier Cycle 5: Shroud of Fear — Raw Patch Notes Data

Источник: https://evefrontier.com/en/news
Дата сбора: 2026-03-22

---

## Анонс: Cycle 5 is Starting March 11 (2026-03-10)

URL: https://evefrontier.com/en/news/cycle-5-arrives-11-march

### Shell Industry & Identity System
- Manufacturing clone bodies через Shell industry
- Nursery — производственный модуль для Shells
- Nest — хранилище для Shells
- Crowns — специализированные memory constructs, определяют capabilities
- При уничтожении Shell — все skills и memory permanently lost

### Galaxy Evolution
- Orbital Zones заменяют dungeons — persistent ecosystems в солнечных системах
- Feral AI патрулирует динамически, реагирует на окружение
- Два новых типа рифтов + crude matter в почти каждой системе
- Ранний доступ к crude industry

### Base Building Expansion
- Construction Sites на owned Network Nodes — коллективная доставка материалов
- L-Points поддерживают несколько баз одновременно
- Три типа турелей:
  - Autocannon Turret (small ships)
  - Plasma Turret (mid-sized threats)
  - Railgun Turret (larger vessels)

### Combat & Traversal
- Light hulls: быстрое ускорение, тесные траектории, активная защита
- Heavy ships: больше массы, выше top speed, пассивная прочность
- Новый фрегат Exclave — high-mobility, precision-focused
- Fuel с новыми свойствами, влияющими на потребление и travel
- Passive scanning — обнаружение сигнатур перед движением/боем

### Blockchain & Dev
- Миграция с Ethereum на Sui blockchain
- Хакатон 2026: $80,000 призовой фонд

---

## Patch Notes 0.5.1 (2026-03-11) — Основной патч Cycle 5

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-1-shroud-of-fear

### Signatures & Scanning System
- Градиентная видимость вместо бинарной (видно/не видно)
- Пассивное обнаружение ambient signatures от ближайших объектов
- Resolution зависит от: signal strength, distance, environmental interference, observation stability
- Информация улучшается со временем, деградирует при потере контакта
- Asymmetric gameplay: игроки выбирают, когда себя раскрыть

### Shell Industry
- **Nursery**: 20 Building Foam, 3.2 минуты build time
  - Три варианта Shell: Reaping, Aggressive, Rugged
  - Каждый даёт 10% capacity reduction для specific modules
- **Nest**: 20 Building Foam, 48 минут на постройку
- **Memories** → fuel Pathway growth
- **Crowns** — imprinting memories в active shells каждые 30 минут
- Character Sheet redesigned

### Camera
- Новая undock animation
- Chase camera (C) — soft re-center
- Track mode — soft target following
- Enhanced Telescope — stable orbit pipeline
- Improved idle animations

### Base Building
- **Construction Sites**: материалы не в ship inventory, а доставляются на площадку
  - Любой игрок может доставлять материалы
  - Все construction times уменьшены на 20%
- **Building Foam Rebalancing**:
  - 1 → 10 units per item
  - Volume: 470 → 47
  - Mass: 470,000 → 147,980 kg
  - Quantity per run: 1 → 10
  - Max runs (Printer S): 1 → 3
- **Турели**: Smart Turret → три специализированных:
  - Mini Turret (small targets)
  - Turret (medium targets)
  - Heavy Turret (large targets)
  - Уникальное оружие, недоступное игрокам — преимущество защитникам
- **L-points**: 5–20 anchor points per location
- Убраны лимиты на количество gate и turret
- Убраны минимальные дистанции между турелями
- Ренейминг: "Hangar M" → "Shelter"

### Orbital Zones (заменяют Landscapes)
- 15 вариаций зон, permanently populate systems
- Зоны не деспаунятся: "anything you leave or hide there should still be there when you return"
- **NPC Overhaul**: Feral drones redesigned
  - Новые scaling paradigms и reactive behaviors
  - Перемещаются между Orbital Zones, Lagrange Points, Celestials
  - Анализируют и реагируют на environmental conditions
  - NPCs не дропают лут — игроки находят wrecks и storage containers
- Asteroids, crude, loot, NPCs — redistributed по orbital zones

### Crude, Fuel & Travel
- Два новых типа micro rift + два новых crude matter
- В почти каждой системе
- Fuel properties влияют на consumption и travel efficiency
- **4 новых Leap Drive** для разных классов кораблей (craftable)
- Starting regions consolidated — больше взаимодействия

### Ship Balance
- Light combat: mobility + active defenses (tight curves, faster acceleration)
- Heavy combat: top speed + passive defenses (higher mass, lower angular agility)
- **Новый корабль: LAI**
  - HP: 2100
  - Fuel Capacity: 2400
  - Capacitor: 40
  - Power Grid: 100 / CPU: 40
  - Slots: 2/2/2 (high/medium/low)
  - Max Velocity: 440
  - Agility: 0.2
  - Angular Agility: 0.65
  - Cargo: 1,040 m³

---

## Patch Notes 0.5.2 (2026-03-12)

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-2-shroud-of-fear

### Features & Changes
- **Experience progression**: tweaks для более consistent Memory acquisition
- **Pathway bonus**: adjustments для greater variation в Memories
- **Crowns**: enhanced information о contained memories
- **Character progression UI polish**
- **Signatures/Scanning**: smoothed удаление items/signatures при потере line of sight
- **Mission Hub**: opens full-screen (adjustable), external URLs через system browser

### Defect Fixes
- Heavy turret работает в пределах 160km range
- Турели надёжнее реагируют на угрозы
- **Турели больше не стреляют в владельца** при посадке на корабль
- Combat music реже триггерится, только в active engagement
- Фикс: большинство wrecks не имели signature → исправлено
- Corpse visibility restored in death scene
- **Camera polish** (множество улучшений):
  - Stability fixes (flickering, frame rate fluctuations)
  - Smoother response during movement
  - Natural acceleration/slowdown
  - Fixed rare twitches during tracking loss
  - Improved vertical smoothing while moving
  - Fixed camera pops when switching modes
  - Improved trailing behavior for turns
- Crowns: unstackable singleton objects
- Crowns useable from non-ship storage
- Ascendable skills listed at top of Ascension screen
- Shell Memories protected from deletion during Ascension
- Wrecks given resolvable signatures
- Default Region Spawns now named and varied

### Known Issues
- Heavy Turret can shoot players before passive scanning detects it

---

## Patch Notes 0.5.3 (2026-03-16)

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-3-shroud-of-fear

### Defect Fixes
- Fixed: игроки теряли line of sight к своим структурам → структуры исчезали, вызывая base building проблемы
- Fixed: industry facility details не загружались при открытии окна

---

## Patch Notes 0.5.4 (2026-03-17)

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-4-shroud-of-fear

### Features & Changes — Ascension QoL
- Новая кнопка "Move All" для Ascension protocol
- "Ascend with selected memories" отключается если нет transferred memories
- Улучшенные описания в интерфейсе
- Отображение Incarnation name и level
- Warning popup при non-Crown memories на Shell во время Ascension

### Defect Fixes
- Fixed: fuel loss при deposit в Network Nodes, которые не создались on-chain
- Fixed: asteroids spawning с minimal ore quantities
- Fixed: NPC, loot, salvage distribution problems
  - **Решает проблему Kadian11C**: Ferals внезапно уходили и возвращались en masse
- Adjusted asteroid distributions across orbital zones
- Fixed: wallet initialization failures для structures

---

## Patch Notes 0.5.5 (2026-03-18)

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-5-shroud-of-fear

### Defect Fixes
- Server memory leak improvements

---

## Patch Notes 0.5.6 (2026-03-20)

URL: https://evefrontier.com/en/news/patch-notes-founder-access-0-5-6-shroud-of-fear

### Defect Fixes
- Fixed: asteroids spawning on top of each other
- Fixed: NPCs remaining in game world after resource redistribution
- Fixed: Stillness system excessive memory consumption
- Fixed: passive scanner malfunction after docking at station
