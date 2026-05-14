# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GRA is a corrections and enhancements repository for the Cologne digitization of Grassmann's *Wörterbuch zum Rig-Veda* (Leipzig, 1873). The canonical source data lives in `csl-orig/v02/gra/gra.txt`. This repo holds tooling, issue-specific correction workflows, and derived files.

The assumed local directory layout (adjust `$BASE` to your installation):
```
$BASE/sanskrit-lexicon/
  GRA/          ← this repo
$BASE/cologne/
  csl-orig/     ← source data (gra.txt lives at v02/gra/gra.txt)
  csl-pywork/   ← build tools
```

## Architecture

| Directory | Purpose |
|---|---|
| `forward/` | German foreword PDF and English translation drafts |
| `verbs01/` | GRA verb identification: `gra_verb_filter.py`, preverb mapping, MW correlation |
| `vn/` | VN supplement integration — Grassmann's changes/deletions/additions; `gra-dev/` for gra9 display |
| `graab/` | CDSL display adaptation for the Andhrabharati version of `gra.txt` |
| `issues/` | Per-issue correction workflows (`issueNNN/` pattern) |

### Issue correction pattern (`issues/issueNNN/`)

Each issue folder follows the same workflow:
1. Copy current `gra.txt` to a local `temp_gra_0.txt` (not tracked by git)
2. Apply corrections incrementally as `temp_gra_1.txt`, `temp_gra_2.txt`, etc.
3. Rebuild XML with `generate_dict.sh` and validate with `xmlchk_xampp.sh`
4. Commit the corrected file to `csl-orig`, then sync to Cologne
5. Commit issue documentation files back here

### AB version pipeline (`graab/`)

The Andhrabharati (AB) version of `gra.txt` provides an alternate digitization for display comparison. Pipeline:
- `change_*.txt` files record corrections applied via `updateByLine.py`
- `abbrevs/` and `abbrevs1/` contain abbreviation markup work
- `althws/` contains alternate headword data

## Common Commands

### Apply line-level corrections
```bash
python updateByLine.py <input_file> <changein_file> <output_file>
```
Change file format: paired lines `NNN old <original>` / `NNN new <replacement>`. Lines starting with `;` are comments.

### Rebuild and validate XML (from `csl-pywork/v02/`)
```bash
cp temp_gra_N.txt $BASE/cologne/csl-orig/v02/gra/gra.txt
cd $BASE/cologne/csl-pywork/v02
sh generate_dict.sh gra  ../../gra
sh xmlchk_xampp.sh gra
```

### Verb pipeline (from `verbs01/`)
```bash
python gra_verb_filter.py gra.txt gra_verb_filter.txt
python changes.py gra_verb_filter.txt gra_preverb0.txt gra_upasarga_map.txt
```

## Dependencies

- **Python 3**
- **lxml** — XML parsing (`pip install lxml`)
- **gra.txt** — in `$BASE/cologne/csl-orig/v02/gra/gra.txt`

