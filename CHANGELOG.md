_Created: 13-06-2026 · Last updated: 05-09-2026_

# Changelog

All notable changes to GRA are documented here.

This repository does not currently publish versioned release notes. Entries use
dated maintenance snapshots; keep upcoming work under [Unreleased] until it is
ready for a dated entry.

## [Unreleased]

### Added
- 2026-09-19 ocr-pilot/ — H5146 OCR-пилот страницы 0587 Cologne-скана gra:
  пайплайн Хелльвига не существует (проверка web+GitHub; единственная
  публикация OCRopus-2009 без кода), заменён Sanskrit fine-tuned
  Qwen2.5-VL (GGUF Q4_K_M); CER 0.986 page-level (GT 506 симв., распознано
  16), run1↔run2 байт-идентичны; вердикт — OCR не заменяет ручную
  транскрипцию; систематика + дифф в [ocr-pilot/README.md](ocr-pilot/README.md).
- 2026-09-18 docs/KASSA_TOCHKA_VS_PARTNER_TCO_COMPARE_18-09-2026.md — TCO-сравнение
  онлайн-кассы 54-ФЗ: банк Точка (покупка комплекта / облачная подписка) против
  партнёрской аренды («Специальный тариф №1»); облачная подписка Точки исключена —
  факт 5 000–15 000 ₽/мес против заявленных «от 1 350». Конкурентный анализ 18-09:
  новый лидер DigitalKassa — 63 670 ₽/36 мес = 1 769 ₽/мес (−28% к аренде),
  нативная интеграция с Точкой; партнёрская аренда (2 457 ₽/мес) — запасной
  вариант (единственный письменный фикс цены 36 мес и безлимит чеков).
- 2026-09-18 tools/recall_vector.py + tools/recall_index.py (коммит 7ba6d566b) —
  починка гонки vec-БД: WAL + busy_timeout на подключении, деградация в BM25
  вместо «database is locked» при недоступности векторного тира.

## [1.0.0] - 2026-06-13

### Added
- Added this changelog so repository-level changes have a stable home.
- Recorded the current repository purpose: Grassmann, Hermann; Wörterbuch zum Rig-Veda.

### Recent Git History
- 2026-05-29 ai-wip: add .pre-commit-config.yaml (yaml-only)
- 2026-05-29 ai-wip: add CodeQL SAST workflow (php)
- 2026-05-29 ai-wip: add .github/dependabot.yml for GitHub Actions auto-updates
- 2026-05-29 fix(ci): smarter change-file validator + per-repo excludes

_Dr. Mārcis Gasūns_
