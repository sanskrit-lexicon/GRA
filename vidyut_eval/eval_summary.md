# H5147 eval summary — vidyut vs verbs01 (computed by compare.py)

## Slice A — 300-headword deterministic stride sample (every 39th of 11836 gra.txt headwords)

| metric | verbs01 | vidyut (kosha direct lookup) |
|---|---|---|
| any output (hit) | — (filter is verb-classifier) | 253/300 = 84.3% |
| verb identified | 30/300 = 10.0% | 11/300 = 3.7% |

Verb-classification confusion (vidyut Tinanta-hit vs verbs01 code=V):

| | vidyut verb | vidyut not-verb |
|---|---|---|
| verbs01 verb | 0 | 30 |
| verbs01 not-verb | 11 | 259 |

vidyut-as-verb-classifier on sample: precision 0.0%, recall 0.0% vs verbs01.

## Slice B — all 902 verbs01 GRA verbs, vidyut direct kosha lookup of the citation root

| metric | count | rate |
|---|---|---|
| kosha returns ANY entry | 325 | 36.0% |
| kosha returns Tinanta (verb) entry | 4 | 0.4% |
| Tinanta lemma == verbs01 mw root | 3 | 0.3% of all / 75.0% of verb-hits |

