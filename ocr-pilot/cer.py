# H5146 CER: Devanagari-only Levenshtein, NFC, whitespace/danda/roman stripped.
# Usage: python3 cer.py <gt_file> <ocr_run1> [ocr_run2]
import re, sys, unicodedata, codecs

def deva(s):
    s = unicodedata.normalize('NFC', s)
    s = re.sub(r'[०-९0-9।॥\s.,:;!?()\-–—√/*""\'\'»«]+', '', s)
    s = re.sub(r'[A-Za-zāīūṛṝḷḹēōṃḥáàâìûṭḍñśṣṅ]+', '', s)
    return s

def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

gt = deva(codecs.open(sys.argv[1], encoding='utf-8').read())
runs = [deva(codecs.open(f, encoding='utf-8').read()) for f in sys.argv[2:]]
for n, o in enumerate(runs, 1):
    d = lev(gt, o)
    print('run%d: chars=%d lev=%d CER=%.3f (GT chars=%d)' % (n, len(o), d, d / len(gt), len(gt)))
if len(runs) == 2:
    st = lev(runs[0], runs[1])
    print('stability run1-vs-run2: lev=%d CER=%.3f (run1 chars=%d)' % (st, st / max(1, len(runs[0])), len(runs[0])))
