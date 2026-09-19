# -*- coding:utf-8 -*-
"""H5147 audit_misses.py -- classify lane-1 (sample.tsv) vidyut misses.

For each form vidyut missed: is the ref ROOT covered anywhere in the dump
(tolerant core match on any dhatu)?  Root-covered miss -> our Stamm+suffix
construction produced a non-form (reference flaw).  Root-not-covered ->
genuine vidyut inventory gap for that GRA verb.
"""
import io, csv, re, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from run_eval import vidyut_core, tolerant, VERBMAP, DUMP

def variants1(s):
    out = {s}
    for i in range(len(s) + 1):
        out.add(s[:i] + s[i+1:])
    return out

def main():
    roots = set()
    with io.open(VERBMAP, encoding='utf-8') as f:
        for line in f:
            m = re.search(r'k1=([^,]+),', line)
            if m:
                roots.add(m.group(1))
    # cores of all dhatus in dump
    cores = set()
    with io.open(DUMP, encoding='utf-8') as f:
        it = iter(f)
        for line in it:
            if line.startswith('padas,'):
                rdr = csv.DictReader(io.StringIO(line + ''.join(it)))
                break
        else:
            raise RuntimeError('no CSV header found in ' + DUMP)
        for row in rdr:
            cores.add(vidyut_core(row['dhatu']))
    print(len(cores), 'distinct dhatu cores in dump')
    covered = set()
    for k1 in roots:
        if any(tolerant(c, k1) for c in cores):
            covered.add(k1)
    print(len(covered), 'of', len(roots), 'GRA roots covered (tolerant)')

    misses = []
    with io.open(os.path.join(HERE, 'eval_results.tsv'), encoding='utf-8') as f:
        hdr = f.readline().rstrip('\n').split('\t')
        for line in f:
            r = dict(zip(hdr, line.rstrip('\n').split('\t')))
            if r['type'] == 'infl' and r['vidyut_hit'] == '0':
                misses.append(r)
    b_root, b_form, b_other = [], [], []
    for r in misses:
        ref = r['ref_lemma']
        if any(tolerant(c, ref) for c in cores):
            b_root.append(r)
        elif ref in covered:
            b_form.append(r)   # shouldn't happen
        else:
            b_other.append(r)
    print('misses:', len(misses),
          '| root covered (our construction flawed):', len(b_root),
          '| root not in vidyut inventory:', len(b_other))
    io.open(os.path.join(HERE, 'miss_audit.tsv'), 'w', encoding='utf-8').write(
        'bucket\tid\tform\tref\tstem\tsuffix\n' + ''.join(
        '%s\t%s\t%s\t%s\t%s\t%s\n' % (name, r['id'], r['form'], r['ref_lemma'],
                                      '', '')
        for name, bucket in (('form-flaw', b_root), ('root-absent', b_other))
        for r in bucket))

if __name__ == '__main__':
    main()
