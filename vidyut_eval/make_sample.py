#-*- coding:utf-8 -*-
"""H5147: fix the eval sample.

Inputs (read-only):
  /Users/mac/Documents/GitHub/csl-orig/v02/gra/gra.txt            (csl-orig, fenced — never committed)
  verbs01/gra_verb_filter_map.txt                                  (verbs01 ground truth: code=V + mw root)

Outputs (committed artifacts):
  sample_headwords.tsv  — deterministic stride sample of 300 GRA headwords (L, k1, k2, sliceA flag)
  verb_set.tsv          — all verbs01-identified GRA verbs (L, k1, k2, mw)

Reproducible: pure deterministic parsing + fixed stride, no RNG.
"""
import codecs, re, sys, os

GRA = os.environ.get('GRA_TXT', '/Users/mac/Documents/GitHub/csl-orig/v02/gra/gra.txt')
HERE = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HERE, '..', 'verbs01', 'gra_verb_filter_map.txt')
N_SAMPLE = 300

meta_re = re.compile(r'^<L>(\d+)<pc>.*?<k1>([^<]*)<k2>([^<]*)')

def init_headwords(filein):
    out = []
    with codecs.open(filein, encoding='utf-8', mode='r') as f:
        for line in f:
            line = line.rstrip('\r\n')  # codecs reader leaves trailing \r on CRLF lines
            m = meta_re.match(line)
            if m:
                out.append((m.group(1), m.group(2), m.group(3)))
    return out

def init_verb_map(filein):
    case_re = re.compile(r'^;; Case \d+: L=(\d+), k1=([^,]*), k2=([^,]*), code=V(?:, mw=(.*))?$')
    out = []
    with codecs.open(filein, encoding='utf-8', mode='r') as f:
        for line in f:
            m = case_re.match(line.rstrip('\r\n'))
            if m:
                out.append((m.group(1), m.group(2), m.group(3), (m.group(4) or '').strip()))
    return out

def main():
    hw = init_headwords(GRA)
    vm = init_verb_map(MAP)
    print('headwords parsed:', len(hw))
    print('verbs01 verb cases parsed:', len(vm))
    verbLs = {L for (L, k1, k2, mw) in vm}

    stride = max(1, len(hw) // N_SAMPLE)
    sample = hw[::stride][:N_SAMPLE]
    print('stride:', stride, 'sample size:', len(sample))

    with codecs.open(os.path.join(HERE, 'sample_headwords.tsv'), 'w', encoding='utf-8') as f:
        f.write('# H5147 slice A: deterministic stride sample, every %dth headword of %d (gra.txt), first %d rows\n' % (stride, len(hw), len(sample)))
        f.write('L\tk1\tk2\tis_verbs01_verb\n')
        for (L, k1, k2) in sample:
            f.write('%s\t%s\t%s\t%s\n' % (L, k1, k2, 'V' if L in verbLs else '-'))

    with codecs.open(os.path.join(HERE, 'verb_set.tsv'), 'w', encoding='utf-8') as f:
        f.write('# H5147 slice B: all verbs01-identified GRA verbs (gra_verb_filter_map.txt, code=V)\n')
        f.write('L\tk1\tk2\tmw\n')
        for (L, k1, k2, mw) in vm:
            f.write('%s\t%s\t%s\t%s\n' % (L, k1, k2, mw))

    n_in_sample = sum(1 for (L, k1, k2, mw) in vm if any(L == sL for (sL, _, _) in sample))
    print('verbs01 verbs inside slice-A sample:', n_in_sample)

if __name__ == '__main__':
    main()
