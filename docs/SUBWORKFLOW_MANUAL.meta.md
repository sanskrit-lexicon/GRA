# SUBWORKFLOW_MANUAL.md — metadoc

_Created: 11-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/SUBWORKFLOW_MANUAL.md](https://github.com/sanskrit-lexicon/GRA/blob/main/docs/SUBWORKFLOW_MANUAL.md).

## Purpose

The runbook layer over GRA's per-directory working logs: one section per
sub-workflow (verbs01 verb identification, the vn Nachträge chain, the graab
Andhrabharati reconciliation, per-issue corrections, prefaces OCR), each
with commands, I/O, and the live-vs-completed-campaign distinction.

## Audience

- An operator rerunning `verbs01` or starting a new `issues/issueNNN/` fix.
- A scholar tracing how a supplement (VN) or AB reading entered `gra.txt`
  (the numbered change files are replayable provenance).
- A maintainer touching the display side (gra9 lineage into
  csl-pywork/csl-websanlexicon).

## Provenance

Authored 11-07-2026 by Fable 5 (`claude-fable-5`) under handoff
[H512-Fable_GRA_sub_workflow_manual_10.07.26](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H512-Fable_GRA_sub_workflow_manual_10.07.26.md)
(the H501–H531 per-repo manuals programme, Litpam-Indexator MANUAL.md gold
standard). Content read from the actual redo scripts and the
`verbs01`/`vn`/`graab` readme logs (incl. the vn transcoding table and the
graab change-chain), plus README/CLAUDE.md/prefaces — none invented.

## Ranked improvement backlog

| # | Item | Status |
|---|---|---|
| 1 | Delete or populate the empty [vn/redo.sh](https://github.com/sanskrit-lexicon/GRA/blob/main/vn/redo.sh) (misleading next to real redo scripts) | open |
| 2 | Parameterize `graab/redo.sh`'s hardcoded `/c/xampp/htdocs/...` paths (a `$BASE` variable like CLAUDE.md describes) | open |
| 3 | Make `verbs01/redo.sh`'s MWS dependency explicit (echo + existence check for `../../MWS/mwverbs/mwverbs1.txt`) | open |
| 4 | An index table in `graab/readme.txt` mapping each `change_N` to its topic workspace (currently reconstructed by reading the log) | open |
| 5 | Close the loop on VN display: [issue #33](https://github.com/sanskrit-lexicon/GRA/issues/33) (supplemental-list display) is the open successor to the vn campaign | open (owned by issue) |

## Known limitations

- The vn and graab campaigns are documented at replay/provenance level, not
  keystroke level — their readme logs remain the primary record of each
  manual decision.
- `preverb0.py`/`preverb1.py` parsing internals and the gra9 PHP display
  changes are not decoded; scripts and the graab readme hand-off notes are
  the reference.
- Scholarly adjudications (which AB reading wins, `arvācīná` vs `avācīná`
  class questions) are outside scope.

## Related documents

- [README.md](https://github.com/sanskrit-lexicon/GRA/blob/main/README.md) — repo overview, timeline, issue typology
- [CLAUDE.md](https://github.com/sanskrit-lexicon/GRA/blob/main/CLAUDE.md) — layout assumptions + per-issue pattern
- [DATA_DICTIONARY.md](https://github.com/sanskrit-lexicon/GRA/blob/main/DATA_DICTIONARY.md) — markup tag reference
- Working logs: [verbs01/readme.txt](https://github.com/sanskrit-lexicon/GRA/blob/main/verbs01/readme.txt) · [vn/readme.txt](https://github.com/sanskrit-lexicon/GRA/blob/main/vn/readme.txt) · [graab/readme.txt](https://github.com/sanskrit-lexicon/GRA/blob/main/graab/readme.txt)
- [csl-corrections correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) — canonical delivery path
- [prefaces/README.md](https://github.com/sanskrit-lexicon/GRA/blob/main/prefaces/README.md) — front-matter conventions

## Revision history

| Date | Change | By |
|---|---|---|
| 11-07-2026 | Initial version (H512) | Fable 5 (`claude-fable-5`) |

---

_Dr. Mārcis Gasūns_
