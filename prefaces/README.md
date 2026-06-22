# GRA — Front Matter (Title Page, Foreword)

OCR transcriptions **and English + Russian translations** of the front matter of the **Wörterbuch zum Rig-Veda** (*Dictionary to the Rig-Veda*) by **Hermann Grassmann**, Leipzig: F. A. Brockhaus, 1873.

Source: the Cologne digitization scan pages under
[grapref.html](https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces/grapref.html).

For each scan page there are three files:

| suffix | language | content |
|---|---|---|
| `graprefNN.md` | German | faithful OCR transcription (original 19th-c. orthography) |
| `graprefNN.en.md` | English | translation of the German |
| `graprefNN.ru.md` | Russian | translation of the German |

Files carry a YAML header (source scan, section, volume, source URL). Sanskrit appears in Grassmann's own romanization as printed (ṙ, ē, ō, accents by macron/circumflex, etc.) and is left **verbatim** in the translations; personal names, work titles, and bibliographic abbreviations are likewise kept as printed. Uncertain readings are marked `[?]`. The original PNGs are kept under [scans/](scans/).

The English foreword translation is courtesy of **Dr. Felix Rau** (University of Cologne, 2018); page `grapref06` on the Cologne site is itself that English translation page. The Russian translation here is new and uses pre-1918 (dореформенная) orthography to match the period of the original.

## Consolidated single-file editions

The complete front matter is also assembled into one file per language (all 6 pages in order, with a table of contents):

| language | file |
|---|---|
| German (Deutsch) | [grapref_all.de.md](grapref_all.de.md) |
| English | [grapref_all.en.md](grapref_all.en.md) |
| Russian (русский) | [grapref_all.ru.md](grapref_all.ru.md) |

These are generated from the per-page files by [build_combined.py](build_combined.py) (`python build_combined.py`); edit the per-page files and re-run to regenerate.

## Contents

| # | Section | Vol. | German | English | Russian |
|---|---------|------|--------|---------|---------|
| 1 | Title page (1873) | 1 | [de](grapref01.md) | [en](grapref01.en.md) | [ru](grapref01.ru.md) |
| 2 | Foreword, 1 | 1 | [de](grapref02.md) | [en](grapref02.en.md) | [ru](grapref02.ru.md) |
| 3 | Foreword, 2 | 1 | [de](grapref03.md) | [en](grapref03.en.md) | [ru](grapref03.ru.md) |
| 4 | Foreword, 3 | 1 | [de](grapref04.md) | [en](grapref04.en.md) | [ru](grapref04.ru.md) |
| 5 | Foreword, 4 | 1 | [de](grapref05.md) | [en](grapref05.en.md) | [ru](grapref05.ru.md) |
| 6 | English translation (F. Rau, 2018) | 1 | [de](grapref06.md) | [en](grapref06.en.md) | [ru](grapref06.ru.md) |

## About the dictionary

Hermann Grassmann (1809–1877) — better known to mathematicians for his *Ausdehnungslehre* — compiled this complete glossary to the Rig-Veda over the years preceding 1873. It cites every form occurring in the Rig-Veda by Aufrecht's continuous hymn numbering (1–1028, including the Vālakhilya), with all attestations, and gives comparative etymologies (Curtius, Fick, Kuhn, Böhtlingk–Roth, Benfey). The foreword (Stettin, 10 August 1872) sets out Grassmann's stem-form conventions, his transcription (ṙ, ē, ō; svarita on the preceding semivowel), his removal of sandhi for lexical transparency, and the concordance between continuous and ten-book numbering.

<details>
<summary>Run notes (provenance &amp; cost)</summary>

- **Pages:** 6 (title page + 4 foreword pages + the site's English-translation page).
- **Languages:** German source (`*.md`), English (`*.en.md`), Russian (`*.ru.md`), plus consolidated `grapref_all.{de,en,ru}.md`.
- **OCR method:** PIL native-resolution column/band crops of the Cologne scan PNGs (`scans/gra_Page_009/011/012/013/014`); no full-page downsampled reads. The title page and the four foreword pages were transcribed directly; `grapref06` is the Cologne site's own transcribed English-translation page (no scan), reproduced verbatim.
- **English foreword:** Dr. Felix Rau, University of Cologne, 2018 (as published on the Cologne site).
- **Russian:** newly produced for this edition, pre-1918 orthography.
- **Builder:** [build_combined.py](build_combined.py), adapted from the canonical `PWG/prefaces/build_combined.py`.
- All files are UTF-8 **without BOM** (verified), matching the csl-orig convention.
</details>
