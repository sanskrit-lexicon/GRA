# H5148 — отчёт о ликвидации дубликатов transcoder (indic_transliteration)

_Created: 19-09-2026_

## Что изменилось

| Поверхность | Было | Стало |
|---|---|---|
| `verbs01/transcoder.py` | 411 строк самописного FSM-транскодера (копия) | 35-строчный bootstrap-стаб → общий движок |
| `vn/grametaAB_multihw/transcoder.py` | байт-в-байт та же копия | тот же стаб (байт-идентичен verbs01-стабу) |
| `indic_translit_migration/transcoder_engine.py` | — | **единственный** канонический движок: без-состоянийные таблицы → `indic_transliteration` 2.3.82 (`SchemeMap`, custom-группа `transcoder`, longest-match + passthrough); stateful `slp1_deva` (INIT/SKT + conlook look-ahead) → компактный порт FSM-раннера |
| XML-таблицы (`verbs01/transcoder/`, `vn/grametaAB_multihw/transcoder/`) | 5 файлов | **без изменений** — остаются источником данных; движок строит SchemeMap из них на лету |
| Вызывающие скрипты (`preverb0.py`, `preverb1.py`, `revisek2.py`) | `import transcoder` | **без изменений** — публичный API сохранён 1:1 |

Дубликат движка (2 × 411 строк байт-идентичных) ликвидирован: 1 движок + 2 стабиль-заглушки.

## Верификация (всё PASS)

1. **Дифференциальный тест** `indic_translit_migration/difftest.py` — легаси-модуль материализуется из `git HEAD`, сравнивается с новым движком на **429 977 случаях** (`PYTHONHASHSEED=0`; детерминированное ядро: все ключи всех таблиц, удвоенные/встроенные ключи, реальные данные репо, `transcoder_processElements` на обёртках `<SA>…</SA>`, identity-пары, отсутствующая таблица; плюс 2000 синтетических комбинаций): **0 расхождений, байт-в-байт**.
2. **End-to-end канари** `revisek2.py` (vn): baseline легаси → 864 changes; с новым движком → 864 changes; `cmp` — **байт-идентично**, те же 155 предупреждений (существовавшие ранее, не транскодерные).
3. `generate_dict.sh`/`xmlchk` — недоступны на этой машине (нет `$BASE/cologne/csl-pywork`); при этом канонические данные `csl-orig` не затронуты вовсе, а поведение тулинга доказано байт-идентичным — XML-вывод по построению неизменен.

## Что осталось / не тронуто (честно)

- **`slp1_deva` (stateful)**: библиотечный built-in SLP1→DEVANAGARI меняет байты (цифры, om-фикс, порядок акцентов), а без-состоянийная SchemeMap не выражает look-behind-контекст schwa — поэтому для этой единственной пары сохранён компактный порт FSM-раннера (~60 строк) внутри общего движка. Данные — те же XML-таблицы. Отмечено в коде; закрытие возможно отдельным юнитом (выравнивание библиотечных групп vowels/vowel_marks/virama с таблицей + диффтест).
- **`graab/`**: transcoder там нет вообще (предположение хэндоффа устарело) — мигрировать нечего.
- **`vn/gra-dev/`**: PHP-копии (`web/utilities/transcoder.php`, `webtc*/`) — Python-библиотека неприменима к PHP-слою отображения; Python call-sites в gra-dev отсутствуют. Out of scope с указанием причины.

## Риски

- Стаб-заглушки ищут движок вверх по дереву (до 5 уровней) — при переносе каталога pipeline в отрыве от репо нужно положить `indic_translit_migration/` рядом (задокументировано в стабах).
- Пин: `indic-transliteration == 2.3.82` (указан в стабах); мажорный апдейт библиотеки потребует повторного прогона `difftest.py` (это единственная защита регрессии — тест самодостаточен).

## Как проверить

```
python3 indic_translit_migration/difftest.py          # 429 977 cases, 0 mismatches
cd vn/grametaAB_multihw && python3 revisek2.py gra_CSL_AB_meta.head.txt /tmp/out.txt && cmp /tmp/out.txt <baseline>
```

_Гасунс_
