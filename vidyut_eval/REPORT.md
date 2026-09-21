# H5147 — vidyut оценка vs verbs01 (лемматизация Грассмана): отчёт

_Created: 19-09-2026 · Last updated: 19-09-2026_

**Tier:** OxAlpha (opencode/z-ai/glm-5.3-flash) · **Handoff:** [H5147](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5147-OxAlpha_GRA_vidyut-vs-verbs01-eval_18.09.26.md) · **Worktree:** GRA-h5147-drain (off origin/main)

## Mission

Оценить vidyut 0.4.0 (ambuda-org/vidyut — Python-биндинг `pip install vidyut` + kosha `data-0.4.0`) как лемматизатор против самописного verbs01-фильтра GRA на выборке 200–500 словоформ из gra.txt (формы головных слов Грассмана, SLP1). Вердикт по цифрам: брать только при сопоставимом качестве.

## Методология (воспроизводимо скриптами)

1. **Выборка зафиксирована файлом.** `vidyut_eval/make_sample.py` парсит `csl-orig/v02/gra/gra.txt` (11836 головных слов) и фиксирует **slice A: 300 головных слов** детерминированным шагом (каждое 39-е) → `sample_headwords.tsv`. Срез **slice B: все 902 глагола verbs01** (`gra_verb_filter_map.txt`, code=V, с эталонным корнем mw=) → `verb_set.tsv`. Без ГСЧ — полная воспроизводимость.
2. **Прогон vidyut** — `vidyut_eval/run_vidyut.py`: прямой lookup головного слова в kosha (`Kosha.get`, SLP1, с visarga-фолбэком H→s/r по официальному tutorial). Оба прогона перезапускаются скриптом.
3. **Прогон verbs01** — эталон из `verbs01/gra_verb_filter_map.txt` (902 code=V + mw-корень).
4. **Сравнение** — `vidyut_eval/compare.py` → `eval_summary.md` + два TSV расхождений.

## Результаты (`eval_summary.md`, вычислен compare.py)

### Slice A — 300 головных слов

| метрика | verbs01 | vidyut (kosha direct) |
|---|---|---|
| любой вывод (hit) | — | 253/300 = 84.3% |
| определён глагол | 30/300 = 10.0% | 11/300 = 3.7% |

Путаница «глагол/не-глагол» (vidyut Tinanta-hit vs verbs01 code=V): verbs01-глаголы, пойманные vidyut как глаголы — **0 из 30**; все 11 «глаголов» vidyut — verbs01-не-глаголы. Precision/recall vidyut как классификатора глагола: **0.0% / 0.0%**.

### Slice B — все 902 глагола verbs01 (корни-цитации)

| метрика | count | rate |
|---|---|---|
| kosha возвращает любую запись | 325 | 36.0% |
| kosha возвращает Tinanta (глагол) | 4 | 0.4% |
| Tinanta-лемма == mw-корень verbs01 | 3 | 0.3% всех / 75% verb-hits |

### Примеры расхождений

- `akz` (verbs01 V, mw=akz) — kosha: 0 записей. Глагольные корни-цитации kosha в основном не находит (paradigma: kosha индексирует **словоформы**, а не корни-цитации).
- `zAs` — 15 записей, все Subanta с леммой `za` (существительное): прямое цитирование корня даёт **ложную именную лемму**.
- Единственные Tinanta-хиты slice B: `jYA→jYA`, `pAtu→pA`, `SrA→SrA` (верно), `Ar→f` (неверно).

## Вердикт (по цифрам)

**vidyut НЕ брать** для этой задачи: качество несопоставимо с verbs01. Причина — парадигмальная, а не поверхностная: kosha — это FST-индекс **словоформ** (строится из словоизменений MW), а формы головных слов GRA — **корни-цитации**; прямой lookup ловит их случайно (совпадение с inflected-формой) или даёт именную омонимию. verbs01 решает свою задачу (идентификация глагола по разметке статьи + MW-корреляция) на этих же данных с ~100% покрытием. Вторичное подтверждение: generator→kosha round-trip (генерация 3sg из корня prakriya-генератором, обратный lookup) заблокирован API 0.4.0: `Pada.Tinanta(dhatu=…)` требует объект `Dhatu`, а dhatupatha ключуется аупадешевскими акцентированными формами (`BU`, `eDa~\`), не GRA/MW guna-формами (`Bav`, `gam`) — мост потребовал бы отдельного слоя нормализации, т.е. adoption-cost сам по себе значим.

## Доставка (пять полей)

- **Changed:** новый каталог `vidyut_eval/` (5 скриптов + зафиксированные выборки + результаты + 2 TSV расхождений) в GRA.
- **Unchanged:** `verbs01/`, `csl-orig/` (только чтение), canonical gra.txt.
- **Checks:** `make_sample.py → run_vidyut.py → compare.py` — воспроизводятся; `eval_summary.md` — PASS (числа выше).
- **Risks:** kosha data-0.4.0 построена из MW, не из GRA; версия vidyut запинена 0.4.0; round-trip-метрика отсутствует (API 0.4.0, см. выше).
- **Inspect:** открыть `vidyut_eval/eval_summary.md`, затем `discrepancies_sliceB.tsv`.

_Гасунс_
