# Сводный отчёт фактчекинга: 16 черновиков Diablo IV

**Дата проверки:** 2026-03-22
**Режим:** обычный (параллельный, 4 пачки по 4 файла)

---

## Сводная таблица

| # | Файл | Оценка | Критичные проблемы |
|---|------|--------|--------------------|
| 1 | diablo_iv_2026_stoit_li_pokupat | **ВЫСОКАЯ** | VoH «смешанные отзывы» — преувеличение (OpenCritic 86/100) |
| 2 | doom_diablo_kollaboraciya | **ВЫСОКАЯ** | Ошибок нет |
| 3 | lord_of_hatred_obzor | **СРЕДНЯЯ** | Juggernaught→Juggernaut, Ae'gron→Ae'grom, неточность сюжета VoH |
| 4 | ostrova_skovos | **ВЫСОКАЯ** | Ошибок нет |
| 5 | paladin_sistema_klyatv | **ВЫСОКАЯ** | 1 неточность (формулировка «лжепророк Акарата») |
| 6 | rasplata_mefisto | **СРЕДНЯЯ** | Акарат/Эру/Нейрель неточности, Ae'gron→Ae'grom, пропущен Ritualist, дата 1996→1997 |
| 7 | rogue_specializations | **СРЕДНЯЯ** | Механика Preparation описана неверно (выдуманная система зарядок) |
| 8 | rybalka_v_sanktuarii | **ВЫСОКАЯ** | Минимальные замечания, спекуляции честно маркированы |
| 9 | sezon_boini_killstreak | **СРЕДНЯЯ** | Паладин в мете S12 (его ещё нет!), Hunger-аффиксы неверно |
| 10 | skill_tree_2_0 | **СРЕДНЯЯ** | Матрица 3x2x2 не подтверждена, примеры навыков спекулятивные |
| 11 | sorcerer_enchantments | **НИЗКАЯ** | Интеллект (8→10), Teleport CD (17с→5с), Hydra (300→200 маны) |
| 12 | spiritborn_dukhi | **СРЕДНЯЯ** | Primary/secondary бонусы Орла перепутаны, Ягуар устаревшие числа |
| 13 | stan_myasnikom | **СРЕДНЯЯ** | Пропущен Ceremony of Slaughter (3-й способ трансформации) |
| 14 | varlok_soul_shard | **ВЫСОКАЯ** | 1 опечатка: Ae'gron→Ae'grom |
| 15 | vse_unikalnye_predmety | **НИЗКАЯ** | ВСЕ 5 НАЗВАНИЙ ПРЕДМЕТОВ ВЫМЫШЛЕНЫ, слоты и аффиксы неверны |
| 16 | war_plans_echoing_hatred | **СРЕДНЯЯ** | Неполный список активностей, спекуляции поданы как факты |

---

## Распределение по оценкам

- **ВЫСОКАЯ** (5): stoit_li_pokupat, doom_kollaboraciya, ostrova_skovos, paladin, rybalka, varlok_soul_shard
- **СРЕДНЯЯ** (8): lord_of_hatred, rasplata_mefisto, rogue, sezon_boini, skill_tree_2_0, spiritborn, stan_myasnikom, war_plans
- **НИЗКАЯ** (2): sorcerer_enchantments, vse_unikalnye_predmety
- **КРИТИЧЕСКАЯ** (0)

---

## Приоритет исправлений

### СРОЧНО (полная переработка)

**1. vse_unikalnye_predmety_sezona_12** — все 5 названий предметов галлюцинированы:
- «Тесак Мясника» → **Blood-Mad Idol** (амулет, все классы)
- «Фартук Мясника» → **Wendigo Brand** (кольцо, все классы)
- «Цепь Мясника» → **Wyrdskin** (перчатки, все классы)
- «Крюк Палача» → **Rustbitten Dirk** (кинжал; Чародей, Друид, Разбойник, Некромант)
- «Маска Свежей Крови» → **Thousand-Eye Reaver** (одноручный топор; Варвар, Друид, Некромант, Паладин)
- Слоты, классы и аффиксы тоже все неверны

**2. sorcerer_enchantments** — три числовые ошибки:
- Интеллект: +1% за **10** единиц (не 8)
- Teleport enchantment CD: **5 секунд** (не 17)
- Hydra enchantment: порог **200 маны** (не 300)

### ВАЖНО (точечные исправления)

**3. rogue_specializations** — Preparation описан неверно:
- НЕТ системы «зарядок» (1 зарядка за 100 энергии, нужно 2)
- Реально: каждые 100 энергии = -5 сек кулдауна ульты; использование ульты = сброс остальных кулдаунов

**4. sezon_boini_killstreak** — два исправления:
- Убрать Паладина из билдов Сезона 12 (его ещё нет в игре)
- Hunger-аффикс: улучшает **награды/лут**, не боевую мощь

### МИНОРНЫЕ (опечатки и уточнения)

**5. Повторяющаяся ошибка Ae'gron→Ae'grom** — в файлах: lord_of_hatred, rasplata_mefisto, varlok_soul_shard
**6. Juggernaught→Juggernaut** — в lord_of_hatred
**7. «Лжепророк Акарата»** — в paladin, rasplata_mefisto: Мефисто вселился в тело настоящего пророка Акарата, предательство совершил Эру
**8. Пропущен Ritualist** — в rasplata_mefisto (упомянуты 3 из 4 специализаций Варлока)
**9. Diablo 1** — дата 1996→январь 1997 (в rasplata_mefisto, stan_myasnikom)
**10. stan_myasnikom** — добавить Ceremony of Slaughter как 3-й способ трансформации
**11. spiritborn** — уточнить primary/secondary бонусы Орла
**12. skill_tree_2_0** — пометить матрицу 3x2x2 как авторскую интерпретацию
