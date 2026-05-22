### Location

Counterpart of https://github.com/sanskrit-lexicon/PWG/issues/175 (PWG) and https://github.com/sanskrit-lexicon/PWK/issues/113 (PWK) for `gra.txt`.

I ran the same two-job recipe over `csl-orig/v02/gra/gra.txt`: auto-fix the few things with a single safe resolution; audit everything else with line refs. Added `08_markup_fix.py` plus outputs to a new `issues/markup_fix/` folder on the branch `markup-fix-audit`.

@funderburkjim @Andhrabharati — please review the findings listed below.

## Markup fixer + audit for `gra.txt`

### What it auto-fixes

| Pattern | Result |
|---|---|
| `<ab><ab>X</ab> Y</ab>` | `<ab>X Y</ab>` |
| `<ab> word </ab>` | `<ab>word</ab>` |
| `<ls> word </ls>` | `<ls>word</ls>` |
| `<per> word </per>` | `<per>word</per>` |

Whitespace trimming applies to all 11 paired tag(s) in `gra.txt`: `<ab>`, `<ls>`, `<per>`, `<hom>`, `<lang>`, `<old>`, `<chg>`, `<new>`, `<gk>`, `<F>`, `<heb>`. The original file is never modified — output goes to `gra_fixed.txt`, with the full diff in `markup_fix_changes.txt` (updateByLine format). 60 line(s) changed.

### Closing-tag inventory in current `gra.txt`

| Tag | Count |
|---|---:|
| `</ab>` | 45 |
| `</726)>` | ? |
| `</ls>` | 2 |
| `</341)>` | ? |
| `</per>` | 1 |
| `</815)>` | ? |
| `</hom>` | 1 |
| `</643)>` | ? |
| `</lang>` | 481 |
| `</old>` | 380 |
| `</chg>` | 380 |
| `</new>` | 280 |
| `</gk>` | 229 |
| `</F>` | 1 |
| `</heb>` | 1 |

### What it found in current `gra.txt`

- 60 whitespace trims applied: 60 leading spaces in `<old>` + 1 trailing in `<old>` + 6 leading in `<new>`.
- 1 `<ab n="?">` placeholder: needs expansion lookup.
- 1,126 within-line `<ab n="…">` non-standard expansion matches — German words ("siehe" ×677, "mit" ×259, "Vers" ×59, etc.). These are intentional German expansions; confirm format is consistent.
- 5,759 within-line adjacent `</ab> <ab>` pairs for verification.
- 4 empty content tags — listed in `markup_audit.txt` with line refs.
- 44 `{{old → new || …}}` correction records present.

### Usage

```
cd issues/markup_fix
python 08_markup_fix.py                        # uses csl-orig/v02/gra/gra.txt by default
python 08_markup_fix.py IN.txt OUT.txt         # custom paths
```

Outputs: `gra_fixed.txt`, `markup_fix_changes.txt`, `markup_audit.txt`.

### Summary

German dictionary; <ab n> uses German descriptive words. <old>/<chg>/<new> tags for corrections.

### Severity

`minor`
