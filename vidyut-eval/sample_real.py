# -*- coding:utf-8 -*-
"""H5147 sample_real.py -- real-form lane: sample REAL inflected forms of GRA
verbs out of vidyut's generated tiNanta dump itself.

A form qualifies when vidyut_core(dhatu) matches a GRA verb k1 under the same
convention-tolerant rule run_eval.py uses.  One form per verb root (seeded
pick), deterministic seed 5147, forms must be longer than the root (real
inflections, not bare citation stems).  vidyut's hit-rate on this lane is
100% BY CONSTRUCTION (disclosed in the report); the meaningful numbers here
are (a) vidyut lemma agreement vs GRA k1 and (b) verbs01's hit/accuracy on
real forms.  Together with the GRA-anchored sample.tsv lane this
triangulates the adoption verdict.

Output: sample_real.tsv (same columns as sample.tsv).
"""
import csv, io, os, re, sys
from random import Random

SEED = 5147
N_FORMS = 250
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_eval import vidyut_core, tolerant, VERBMAP, DUMP  # noqa: E402

OUT = os.path.join(HERE, 'sample_real.tsv')

def gra_roots():
    roots = set()
    with io.open(VERBMAP, encoding='utf-8') as f:
        for line in f:
            m = re.search(r'k1=([^,]+),', line)
            if m:
                roots.add(m.group(1))
    return roots

ALPHA = 'akgGcjJwqQtDdnpbmyrlvzsSzhNiIuUfeEoOAMHRfxX'
def variants1(s):
    """s plus every 1-edit variant (tolerant() <=1 neighborhood)."""
    out = {s}
    for i in range(len(s) + 1):
        out.add(s[:i] + s[i+1:])
        for c in ALPHA:
            out.add(s[:i] + c + s[i:])
    for i in range(len(s)):
        for c in ALPHA:
            out.add(s[:i] + c + s[i+1:])
    return out

def main():
    roots = gra_roots()
    print(len(roots), 'GRA verb roots')
    var_index = {}                 # 1-edit variant -> set(k1)
    for k1 in roots:
        for v in variants1(k1):
            var_index.setdefault(v, set()).add(k1)
    dump = {}
    with io.open(DUMP, encoding='utf-8') as f:
        it = iter(f)
        for line in it:
            if line.startswith('padas,'):
                rdr = csv.DictReader(io.StringIO(line + ''.join(it)))
                break
        else:
            raise RuntimeError('no CSV header found in ' + DUMP)
        for row in rdr:
            for p in row['padas'].split('|'):
                if p:
                    dump.setdefault(p, set()).add(row['dhatu'])

    per_root = {}   # k1 -> {form: dhatus}
    for form, dts in dump.items():
        for d in dts:
            core = vidyut_core(d)
            for k1 in var_index.get(core, ()):
                if tolerant(core, k1) and len(form) > len(k1):
                    per_root.setdefault(k1, {}).setdefault(form, list(dts))
    print(len(per_root), 'GRA roots covered by vidyut dump;',
          sum(len(v) for v in per_root.values()), 'candidate forms')

    rng = Random(SEED)
    keys = sorted(per_root)
    rows, used = [], set()
    for pass_i in (1, 2):            # pass 1: one form per root; pass 2: fill up
        for k1 in keys:
            if len(rows) >= N_FORMS:
                break
            forms = sorted(f for f in per_root[k1]
                           if (k1, f) not in used)
            if not forms:
                continue
            form = forms[rng.randrange(len(forms))] if pass_i == 1 else forms[0]
            used.add((k1, form))
            rows.append(('-', k1, '-', 'infl', k1, '-', '-', form,
                         '|'.join(sorted(per_root[k1][form]))))
        if len(rows) >= N_FORMS:
            break
    rows = rows[:N_FORMS]
    rows.sort(key=lambda r: (r[1], r[7]))
    with io.open(OUT, 'w', encoding='utf-8', newline='') as f:
        f.write('id\tL\tk1\tmw\ttype\tref_lemma\tstem\tsuffix\tform\tvariants\n')
        for i, r in enumerate(rows, 1):
            f.write('%04d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %
                    (i, r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))
    print(len(rows), 'real forms written to', OUT)

if __name__ == '__main__':
    main()
