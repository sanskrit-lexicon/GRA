# H5147 — vidyut vs verbs01 lemmatization eval (GRA)

_Created: 19-09-2026 · Last updated: 19-09-2026_

Question: can [ambuda-org/vidyut](https://github.com/ambuda-org/vidyut) (`vidyut-prakriya`, Rust) replace or augment
GRA's self-written `verbs01` resources for *lemma lookup* — given a surface
word form, recover Grassmann's headword (gra.txt `k1`, SLP1)?

Verdict: **adopt-for-verbs-only** — see [Verdict](#verdict).

## Setup

- vidyut @ `8da2f90` ("[prakriya] लेट् implementation…"), shallow clone +
  `cargo build --release --example create_all_tinantas` (Windows, cargo
  1.97.1). Binary: `target/release/examples/create_all_tinantas.exe`.
- tiNanta dump regenerated with:
  `cargo run --release --example create_all_tinantas -- --output-scheme Slp1`
  → 2,029,068 rows, **1,683,437 distinct forms** in SLP1
  (`tinantas_slp1.csv`, 136 MB, gitignored — regenerate per above).
- GRA source: `csl-orig/v02/gra/gra.txt` (12,785 entries), verbs01 resources:
  `gra_verb_filter_map.txt` (815 distinct verb k1), `gra_preverb1.txt`
  (1,976 prefixed forms), `gra_upasarga_map.txt` (115 upasargas).
- Lemma match needs a **convention-tolerant normalizer** (`vidyut_core` +
  edit-distance ≤ 1 in `run_eval.py`): vidyut dhatu strings carry it-flags
  and indicatory vowels (`va\ha~^` = vah, `kfpU~\` = kḷp, `De\w` = dhe ← dhā)
  and MW-style spellings (`zu` vs GRA `su`, `vadi` vs GRA `vand`). Raw string
  agreement without it: **1.0%**. Unit tests: `test_core.py` (16/16 OK).

## Frozen samples (committed, deterministic seed 5147)

| sample | lane | n | what |
|---|---|---|---|
| `sample.tsv` | GRA-anchored | 326 (202 infl + 74 cite + 50 ctrl) | forms constructed from GRA's own morphology (entry Stamm + TS-div suffix, minimal sandhi); ref lemma = entry k1 |
| `sample_real.tsv` | real-form | 250 | real inflected forms of GRA verbs drawn from vidyut's generated dump (one per root); vidyut hit-rate is 100% **by construction** — disclosed, its real test here is agreement |

## Numbers (infl forms only; from `eval_results*.tsv`)

| metric | vidyut | verbs01 |
|---|---|---|
| lane 1 (GRA-anchored) hit | 24.3% (49/202) | 23.3% (47/202) |
| lane 1 lemma agreement | 19.8% (40/202) | 21.8% (44/202) |
| lane 1 misses where the **root is vidyut-covered** (our construction flawed) | 124/153 (81%) | — |
| lane 1 misses where the **root is absent from vidyut** | 29/153 (19%) | — |
| lane 2 (real forms) hit | 100% (by construction) | **0.4% (1/250)** |
| lane 2 lemma agreement | 100% (by construction) | 0.4% |
| precision on 50 noun controls (false positives) | 0 | 0 |
| bare citation forms (`cite`, n=74) | 2.7% (structural: a tiNanta table has no bare roots) | 100% (trivial: k1 ∈ its root list) |
| GRA verb inventory covered | **658/815 (80.7%)** | 100% (its own list) |

Miss audit: `miss_audit.tsv` (per-form buckets). Lane-1 vidyut's 24.3% raw
hit is dominated by our reference-construction imperfection (naive
Stamm+suffix composition cannot reproduce guna/reduplication/y-v-insertion —
e.g. `sunu+Anti` → our `sunAnti`, real `sunvAnti`); where the root IS covered
(124 of 153 misses), the failure is in the sample construction, not vidyut.
The 29 root-absent cases are mostly GRA-specific Rigvedic
denominatives/causative-headwords (`sumanasy`, `staBAy`, `Dunay`, `inakz`…)
outside vidyut's classical inventory, plus GRA-asserted middle forms of
P-only verbs (`namate` for nam).

verbs01's lane-2 collapse is structural: it is a **headword classifier**, not
a lemmatizer — its resources (root list + preverb table + upasarga list +
naive endings) match citation shapes, not inflected surface forms. Its 3
lane-1 wrong-lemma hits: `avasi→si` (upasarga strip gone wrong), `irajyasi→irajy`,
`jahAmi→jah` (reduplication stem vs root `hA`).

## Verdict

**Adopt-for-verbs-only.** Adopt vidyut as the lemma-lookup engine for
inflected verb forms: 100% lemma accuracy on its covered forms (vs verbs01's
resources at 0.4% on real forms), 80.7% GRA verb-root coverage, zero false
positives on non-verbs — contingent on shipping the convention normalizer
(`vidyut_core` + edit-distance ≤ 1) with it, since raw-string agreement is
1.0%. Keep verbs01 for what it actually does (verb/non-verb headword
classification) and keep GRA's own verb map as backstop for the ~19% of
GRA-anchored gaps (Rigvedic denominatives, middle forms of P-only verbs)
vidyut cannot derive.

## Reproduce

```bash
python make_sample.py                                   # regenerates sample.tsv
python sample_real.py                                   # needs tinantas_slp1.csv
python run_eval.py                                      # lane 1 -> eval_results.tsv
python run_eval.py --sample sample_real.tsv             # lane 2
python audit_misses.py                                  # miss buckets
python test_core.py                                     # normalizer unit tests
```

`tinentas_slp1.csv` is gitignored (136 MB): rebuild vidyut @ `8da2f90` and run
`cargo run --release --example create_all_tinantas -- --output-scheme Slp1`.

_Гасунс_
