# GRA Sub-Workflow Manual

_Created: 11-07-2026 · Last updated: 11-07-2026_

The consolidated operator manual for GRA's distinct sub-workflows: `verbs01`
(verb identification against MW), `vn` (integrating Grassmann's own
*Nachträge* supplement, pp. 1741–1776), `graab` (adapting the Andhrabharati
re-digitization for CDSL display), plus the standard per-issue correction
pattern and the prefaces OCR. The per-directory `readme.txt` files are
working *logs* written during the work — this manual is the runbook layer
above them: what each workflow does, what it consumes and produces, and what
an operator actually runs.

Companion metadoc: [docs/SUBWORKFLOW_MANUAL.meta.md](https://github.com/sanskrit-lexicon/GRA/blob/main/docs/SUBWORKFLOW_MANUAL.meta.md).

---

## 1. Cheat-sheet

```bash
# verbs01 — regenerate the verb identification (needs sibling MWS checkout, §3.1)
cd verbs01 && sh redo.sh

# vn — the numbering/transcoding chain is script + manual hybrid (§3.2);
#      the two mechanical steps:
python correction_num.py orig/vn0.txt orig/vn1.txt     # label the 364 corrections <c N>
python addition_num.py  orig/vn1.txt orig/vn2.txt      # label the 636 additions  <a N>
# …and the exporter that turns a hand-edited text pair into a change file:
python diff_to_changes_dict.py temp_gra_0.txt temp_gra_1.txt change_gra_1.txt

# any correction, all workflows — the one shared applier:
python updateByLine.py <input> <change_file> <output>

# rebuild + validate display XML (from csl-pywork/v02/, not this repo):
sh generate_dict.sh gra ../../gra
sh xmlchk_xampp.sh gra
```

**Delivery rule (all workflows):** the canonical text is
[csl-orig/v02/gra/gra.txt](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/gra/gra.txt).
Changes are expressed as `NNN old` / `NNN new` change files and reach csl-orig
via the canonical
[correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
— org agents queue change files for the batched PR; the direct
`cp … csl-orig/...` lines in the old readmes/redo scripts are the
upstream-maintainer (XAMPP-layout) pattern.

## 2. Data-flow diagram

```
csl-orig/v02/gra/gra.txt  (canonical, SLP1 keys, German glosses)
│
├── verbs01/  — WHICH ENTRIES ARE VERBS, MAPPED TO MW
│     gra.txt ──gra_verb_filter.py──► gra_verb_filter.txt  (907 verbs;
│        exclusion patterns + hand lists gra_verb_{exclude,include}.txt)
│     + ../../MWS/mwverbs/mwverbs1.txt   ◄── SIBLING-REPO DEPENDENCY
│        ──gra_verb_filter_map.py──► gra_verb_filter_map.txt (GRA↔MW spellings)
│        ──preverb0.py / preverb1.py (slp1, deva)──► gra_preverb1{,_deva}.txt
│        (upasarga parsing via gra_upasarga_map.txt)
│
├── vn/  — GRASSMANN'S OWN SUPPLEMENT (Nachträge, print pp. 1741–1776)
│     orig/grassmann_Nachtraege_utf8.txt  (OCR)
│       → vn0 (manual page breaks) → vn1 (correction_num: <c 1>…<c 364>)
│       → vn2 (addition_num: <a N> ×636; deletion block relabeled <d 273>–<d 364>)
│       → vn3 (transcoding to gra.txt IAST: Grassmann's ē/ō/roof-accent
│              conventions normalized — the table in vn/readme.txt)
│       → vn3_1…vn3_3 (Andhrabharati review rounds, '::AB::' notes)
│       → hand-applied to a pinned temp_gra_0.txt
│       → diff_to_changes_dict.py ──► change_gra_1..6.txt ──► gra.txt
│     gra-dev/  = the gra9 display prototype (pywork + web copies) that
│                 pioneered the supplement's display; later merged upstream
│
├── graab/  — ANDHRABHARATI RE-DIGITIZATION → CDSL DISPLAY (issues #29–#32)
│     temp_graab_0.txt (AB's file, issue #29 attachment)
│       → change_1 (XML well-formedness) → +vn_ab (AB's own VN block)
│       → change_3…change_9h_9gAB — one numbered change file per repair topic,
│         with per-topic workspaces: abbrevs/, abbrevs1/ (<ab> markup),
│         litsrc/ litsrc1/ litsrc2/ (<ls> citations), althws/ (alternate
│         headwords), meta_compare/ (metalines vs gra9), mischg/, final/
│         (9g ↔ 9g_AB reconciliation: 89,186 → 89,074 lines)
│       → redo.sh: deploy temp_graab_10.txt + gra_hwextra.txt to csl-orig
│         and regenerate display via csl-pywork (maintainer step)
│
├── issues/issue34/  — grahwextra → Lbody structural markup (per-issue pattern)
├── prefaces/        — front-matter OCR + EN/RU translations (§3.5)
└── forward/         — the 2018-era foreword translation drafts (superseded
                       by prefaces/ for the foreword text itself)
```

## 3. The sub-workflows

### 3.1 verbs01 — verb identification and MW correlation

**Question it answers:** which of GRA's entries are verbs, and which MW root
does each correspond to (including prefixed/upasarga forms)?

Run: `cd verbs01 && sh redo.sh`. The script:

1. `gra_verb_filter.py` scans each entry's first line with exclusion
   patterns, then applies the hand-kept `gra_verb_exclude.txt` /
   `gra_verb_include.txt` overrides → `gra_verb_filter.txt` (historic
   count: 995 candidates → **907 verbs**).
2. `gra_verb_filter_map.py` aligns GRA verb spellings with MW's, reading
   **`../../MWS/mwverbs/mwverbs1.txt`** — a sibling
   [MWS](https://github.com/sanskrit-lexicon/MWS) checkout is required (the
   `mwverb.py`/`mwverbs1.py` generation steps are commented out in
   `redo.sh`; MWS owns them now).
3. `preverb0.py` + `preverb1.py` (run twice: `slp1`, `deva`) parse
   upasarga-prefixed forms via `gra_upasarga_map.txt` →
   `gra_preverb1.txt` / `gra_preverb1_deva.txt`, the final correlation
   tables. Open enhancement: [issue #11](https://github.com/sanskrit-lexicon/GRA/issues/11).

### 3.2 vn — the Nachträge supplement

**What it is:** Grassmann's own corrections/deletions/additions, printed as
pp. 1741–1776 of the 1873 edition, brought into `gra.txt` — the scholarly
heart of the repo. The chain
([vn/readme.txt](https://github.com/sanskrit-lexicon/GRA/blob/main/vn/readme.txt)
is the detailed log):

1. **OCR → vn0**: `orig/grassmann_Nachtraege_utf8.txt` hand-edited to put
   every `[pageNNNN]` break on its own line.
2. **Numbering**: `correction_num.py` labels the 364 page,line-keyed
   corrections `<c N>`; `addition_num.py` labels the 636 headword-keyed
   supplement entries `<a N>`; the "Zu streichen" (to-delete) block is
   relabeled `<d 273>`–`<d 364>` by hand. Corrections cite
   `page,line` (with `v. u.` = counted from the bottom); additions carry
   `<p><b>headword:</b>`.
3. **Transcoding → vn3**: Grassmann's idiosyncratic transcription (his
   foreword defends it — see
   [prefaces](https://github.com/sanskrit-lexicon/GRA/blob/main/prefaces/grapref_all.en.md)):
   `ē`→`ai`, `ō`→`au`, roof = accented long vowel (`â`→`ā́`), svarita marked
   on the preceding semivowel — all normalized to gra.txt's IAST
   conventions; the full substitution table with per-rule counts is in the
   readme (e.g. `â→ā́` ×525, `ṅs→ṃs` ×20).
4. **AB review → vn3_1…vn3_3**: Andhrabharati's line-by-line review
   (`vn3.1_AB.txt`, notes joined with `::AB::`), plus 3-column page-break
   disambiguation (`[PageN-a]`/`[PageN-b]`).
5. **Application**: the reviewed supplement is worked into a **pinned**
   `temp_gra_0.txt` (`git show <commit>:v02/gra/gra.txt` — the readme
   records the exact hash), and `diff_to_changes_dict.py` exports each
   round as `change_gra_1..6.txt` for `updateByLine.py`.
6. **Display**: `gra-dev/` holds the *gra9* prototype (its `pywork/` +
   `web/` files were later copied into csl-pywork/csl-websanlexicon —
   the graab readme documents that hand-off). NB
   [vn/redo.sh](https://github.com/sanskrit-lexicon/GRA/blob/main/vn/redo.sh)
   is **empty** — there is no one-shot rerun; the chain is deliberately
   manual + reviewed.

### 3.3 graab — the Andhrabharati version for CDSL display

**What it is:** Nagabhushana Rao (Andhrabharati) re-digitized Grassmann
independently; `graab/` is the long reconciliation that made his version
CDSL-displayable and cross-checked it against Cologne's
([issues #29](https://github.com/sanskrit-lexicon/GRA/issues/29)–[#32](https://github.com/sanskrit-lexicon/GRA/issues/32)).
Shape: a numbered change-file chain (`change_1.txt` … `change_9h_9gAB.txt`)
over `temp_graab_N.txt` snapshots (~89k lines), each number paired with a
topic workspace:

| Workspace | Topic |
|---|---|
| `abbrevs/`, `abbrevs1/` | `<ab>` abbreviation markup + tooltips |
| `litsrc/`, `litsrc1/`, `litsrc2/` | `<ls>` literary-source (Rig-Veda citation) markup |
| `althws/` | alternate headwords → `gra_hwextra.txt` |
| `meta_compare/`, `meta2/` | metaline reconciliation against the gra9 text |
| `vn_ab/` | AB's own rendering of the VN block, merged in at `temp_graab_2` |
| `mischg/` | miscellaneous print-change notes |
| `final/` | the 9g ↔ 9g_AB line-count reconciliation (89,186 → 89,074) + the commented 66-change `change_9h_9gAB.txt` |

[graab/redo.sh](https://github.com/sanskrit-lexicon/GRA/blob/main/graab/redo.sh)
is the maintainer deploy step: copy `temp_graab_10.txt` → csl-orig's
`gra.txt` (+ `gra_hwextra.txt`), then `generate_dict.sh gra` into a `devN/`
tree for inspection — absolute XAMPP paths, upstream-only (§1's delivery
rule for everyone else). The `temp_graab_N.txt` snapshots themselves are
gitignored; the change files + readmes are the durable record.

### 3.4 Per-issue corrections (`issues/issueNNN/`)

The standard Cologne pattern (detailed in
[CLAUDE.md](https://github.com/sanskrit-lexicon/GRA/blob/main/CLAUDE.md)):
pin `temp_gra_0.txt` from csl-orig, transform incrementally, rebuild
(`generate_dict.sh gra` + `xmlchk_xampp.sh gra`), deliver per the correction
workflow, commit the documentation here. Current example:
[issues/issue34/](https://github.com/sanskrit-lexicon/GRA/tree/main/issues/issue34)
(the `grahwextra` → Lbody structural markup change).

### 3.5 Prefaces and forward

[prefaces/](https://github.com/sanskrit-lexicon/GRA/tree/main/prefaces) —
per-scan-page OCR of the 1873 front matter (faithful 19th-c. orthography)
with English (foreword: Dr. Felix Rau, 2018) and Russian (new, pre-1918
orthography) translations, consolidated per-language editions built by
`build_combined.py`. Grassmann's romanization is kept **verbatim** — it is
the key to §3.2's transcoding table. `forward/` holds the earlier
foreword-translation drafts; for the foreword text itself, `prefaces/` is
the current home.

## 4. Environment & prerequisites

- **Python 3** (+ `lxml` for XML checks: `pip install lxml`); `sh` via Git
  Bash on Windows.
- **Sibling checkouts:** `csl-orig` (canonical `gra.txt`), `csl-pywork`
  (display build), **`MWS`** (for `verbs01`'s `mwverbs1.txt`). The scripts
  assume the maintainer layout `$BASE/sanskrit-lexicon/GRA` +
  `$BASE/cologne/csl-orig` (relative `../../../cologne/csl-orig` in
  `verbs01/redo.sh`) — adjust the variables at the top of each script for
  your clone layout.
- Scans: [sanskrit-lexicon-scans/gra](https://github.com/sanskrit-lexicon-scans/gra)
  (note the pg_1769 mix-up was fixed there; the correct supplement pages are
  also in [vn/gra_bayer_nachtraege_pp1741-1776.pdf](https://github.com/sanskrit-lexicon/GRA/blob/main/vn/gra_bayer_nachtraege_pp1741-1776.pdf)).

## 5. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| `verbs01/redo.sh`: "No such file … MWS/mwverbs/mwverbs1.txt" | The MW verb tables now live in the sibling MWS repo (generation steps are commented out here) | Clone MWS beside GRA, or point `mwverbs1=` at your copy |
| `vn/redo.sh` does nothing | It is **empty** — the vn chain is manual + reviewed by design | Follow §3.2; the numbered scripts are the only mechanical steps |
| Supplement text looks mis-transliterated (`ē`, `ō`, roof accents) | That's Grassmann's own convention, pre-normalization | Apply/consult the §3.2 transcoding table before comparing with gra.txt |
| A vn correction's `page,line` doesn't match the scan | `v. u.` lines count from the *bottom* of the page; 3-column print pages carry two page numbers (`[PageN-a]/[PageN-b]`) | See the vn readme's numbering notes |
| Scan page pg_1769 shows pages 1761–2 | Historic scan mix-up, already fixed at Cologne + sanskrit-lexicon-scans | Use the repo's Bayer PDF if in doubt |
| `updateByLine.py` line-count mismatch | Change file built against a different `gra.txt` state than the input | Re-pin the input (`git show <hash>:v02/gra/gra.txt`) to the state the change file names; the canonical workflow doc covers this class |
| Tempted to run `graab/redo.sh` | It copies files straight into csl-orig and expects `/c/xampp/...` | Upstream-maintainer step only; org agents deliver via the correction queue (§1) |
| `temp_graab_N.txt` / `temp_gra_N.txt` missing after clone | The big snapshots are gitignored working files | Rebuild from the pinned base + the numbered change files (that's what they exist for) |
| Which of `forward/` vs `prefaces/` is current for the foreword | `forward/` = 2018 drafts; `prefaces/` = the finished per-page OCR + translations | Use `prefaces/`; keep `forward/` as history |

## 6. Glossary

| Term | Meaning |
|---|---|
| VN / Nachträge | Grassmann's own supplement (corrections + additions + deletions), print pp. 1741–1776 |
| `<c N>` / `<a N>` / `<d N>` | vn-chain labels: correction / addition / deletion items |
| `v. u.` | *von unten* — line counted from the bottom of the page in VN correction addresses |
| AB / Andhrabharati | Nagabhushana Rao's independent re-digitization of Grassmann (the graab source) |
| gra9 | The vn-era display prototype (`vn/gra-dev/`) whose pywork/web changes were upstreamed |
| grahwextra / Lbody | Alternate-headword side file → its successor structural markup (issue #34) |
| upasarga | Verbal prefix; `verbs01` parses prefixed verbs via `gra_upasarga_map.txt` |
| svarita | The dependent accent — Grassmann marks it on the preceding semivowel (normalized in vn3) |
| roof (ˆ) | Grassmann's mark for an *accented* long vowel (`â` = ā́); plain macron = unaccented long |
| metaline | `<L>…<pc>…<k1>…<k2>…` — entry id, page ref, headword, sort key (with accent, e.g. `a/MSa`) |
| `updateByLine.py` | The shared line-keyed change-file applier used by every workflow here |

## 7. Maintainer appendix

- **Live vs finished:** `verbs01` is rerunnable (and has an open issue,
  #11); `issues/issueNNN` + prefaces are the ongoing patterns; the `vn`
  chain and `graab` chain are **completed campaigns** — their value now is
  provenance (every change to gra.txt from the supplement and the AB
  reconciliation is replayable from the numbered change files). Don't
  "clean up" the numbered snapshots' readmes; they are the audit trail.
- **Observed quirks** (11-07-2026, while writing this manual): (1)
  `vn/redo.sh` is an empty file — misleading next to the real redo scripts;
  (2) `verbs01/redo.sh` half-commented header (the MWS-owned steps) makes
  the sibling-repo dependency easy to miss; (3) `graab/redo.sh` hardcodes
  `/c/xampp/htdocs/...` absolute paths; (4) the per-directory readmes mix
  log narrative with instructions — this manual is the runbook layer, the
  readmes stay the provenance layer.
- **Cross-repo edges:** MWS (`mwverbs1.txt` input), csl-orig (canonical
  text + `gra_hwextra.txt`), csl-pywork/csl-websanlexicon (display build;
  gra9's `basicadjust.php`/`basicdisplay.php` originated here),
  sanskrit-lexicon-scans/gra (page images), VedaWeb crosswalk queued as
  [issue #52](https://github.com/sanskrit-lexicon/GRA/issues/52).
- **Issue taxonomy:** dictionary-repo taxonomy (type / severity /
  milestone) — see
  [CLAUDE.md](https://github.com/sanskrit-lexicon/GRA/blob/main/CLAUDE.md)
  and the README's typology tables.

---

_Dr. Mārcis Gasūns_
