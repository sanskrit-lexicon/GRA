#-*- coding:utf-8 -*-
"""H5147: compare vidyut vs verbs01 on the fixed sample. Emits eval_summary.md + discrepancy TSVs."""
import codecs, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))

def read_tsv(name):
    rows = []
    with codecs.open(os.path.join(HERE, name), encoding='utf-8', mode='r') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#') or line.startswith('L\t'):
                continue
            rows.append(line.split('\t'))
    return rows

def main():
    # Slice A: 300-headword stride sample
    sample = read_tsv('sample_headwords.tsv')      # L k1 k2 is_verbs01_verb
    vids = {r[0]: r for r in read_tsv('vidyut_sample.tsv')}  # L k1 n_entries n_tinanta lemmas verb_lemmas query_used

    n = len(sample)
    v01_verb = [r for r in sample if r[3] == 'V']
    vid_any = [r for r in sample if int(vids[r[0]][2]) > 0]
    vid_verb = [r for r in sample if int(vids[r[0]][3]) > 0]
    v01set = {r[0] for r in v01_verb}
    vidvset = {r[0] for r in vid_verb}

    conf = Counter()
    for r in sample:
        L = r[0]
        conf[(L in v01set, L in vidvset)] += 1

    # lemma agreement on both-verb rows (vidyut tinanta lemmas vs verbs01 mw root)
    vm = {r[0]: r[3] for r in read_tsv('verb_set.tsv')}
    both = [r for r in sample if r[0] in v01set and r[0] in vidvset]
    agree_k1 = agree_mw = 0
    dis_rows = []
    for r in both:
        L, k1 = r[0], r[1]
        vlem = set(filter(None, vids[L][5].split(',')))
        mw = vm.get(L, '')
        m1, m2 = k1 in vlem, (mw in vlem)
        agree_k1 += m1
        agree_mw += m2
        if not (m1 or m2):
            dis_rows.append((L, k1, mw, ','.join(sorted(vlem))))

    # Slice B: all 902 verbs01 verbs
    vb = read_tsv('vidyut_verbs.tsv')  # L k1 mw n_entries n_tinanta verb_lemmas rt...
    nB = len(vb)
    B_any = [r for r in vb if int(r[3]) > 0]
    B_verb = [r for r in vb if int(r[4]) > 0]
    B_agree = []
    B_dis = []
    for r in vb:
        vlem = set(filter(None, r[5].split(',')))
        if r[2] and r[2] in vlem:
            B_agree.append(r)
        elif r[4] != '0':
            B_dis.append(r)

    lines = []
    add = lines.append
    add('# H5147 eval summary — vidyut vs verbs01 (computed by compare.py)\n')
    add('## Slice A — 300-headword deterministic stride sample (every 39th of 11836 gra.txt headwords)\n')
    add('| metric | verbs01 | vidyut (kosha direct lookup) |')
    add('|---|---|---|')
    add('| any output (hit) | — (filter is verb-classifier) | %d/%d = %.1f%% |' % (len(vid_any), n, 100.0*len(vid_any)/n))
    add('| verb identified | %d/%d = %.1f%% | %d/%d = %.1f%% |' % (len(v01_verb), n, 100.0*len(v01_verb)/n, len(vid_verb), n, 100.0*len(vid_verb)/n))
    add('')
    add('Verb-classification confusion (vidyut Tinanta-hit vs verbs01 code=V):')
    add('')
    add('| | vidyut verb | vidyut not-verb |')
    add('|---|---|---|')
    add('| verbs01 verb | %d | %d |' % (conf[(True, True)], conf[(True, False)]))
    add('| verbs01 not-verb | %d | %d |' % (conf[(False, True)], conf[(False, False)]))
    prec = conf[(True,True)] / max(1, conf[(True,True)] + conf[(False,True)])
    rec = conf[(True,True)] / max(1, conf[(True,True)] + conf[(True,False)])
    add('')
    add('vidyut-as-verb-classifier on sample: precision %.1f%%, recall %.1f%% vs verbs01.' % (100*prec, 100*rec))
    if both:
        add('')
        add('Lemma agreement on %d both-verb rows: dhatu == GRA k1 %d (%.0f%%); dhatu == verbs01 mw root %d (%.0f%%).' % (
            len(both), agree_k1, 100.0*agree_k1/len(both), agree_mw, 100.0*agree_mw/len(both)))
    add('')
    add('## Slice B — all %d verbs01 GRA verbs, vidyut direct kosha lookup of the citation root\n' % nB)
    add('| metric | count | rate |')
    add('|---|---|---|')
    add('| kosha returns ANY entry | %d | %.1f%% |' % (len(B_any), 100.0*len(B_any)/nB))
    add('| kosha returns Tinanta (verb) entry | %d | %.1f%% |' % (len(B_verb), 100.0*len(B_verb)/nB))
    if nB:
        add('| Tinanta lemma == verbs01 mw root | %d | %.1f%% of all / %.1f%% of verb-hits |' % (
            len(B_agree), 100.0*len(B_agree)/nB, 100.0*len(B_agree)/max(1,len(B_verb))))
    add('')
    with codecs.open(os.path.join(HERE, 'eval_summary.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    with codecs.open(os.path.join(HERE, 'discrepancies_sliceA.tsv'), 'w', encoding='utf-8') as f:
        f.write('L\tk1\tmw\tnot_in_vidyut_verb_lemmas\n')
        for row in dis_rows:
            f.write('\t'.join(row) + '\n')
    with codecs.open(os.path.join(HERE, 'discrepancies_sliceB.tsv'), 'w', encoding='utf-8') as f:
        f.write('L\tk1\tmw\tn_entries\tn_tinanta\tverb_lemmas\n')
        for r in B_dis[:100]:
            f.write('\t'.join(r[:6]) + '\n')
    print('\n'.join(lines))

if __name__ == '__main__':
    main()
