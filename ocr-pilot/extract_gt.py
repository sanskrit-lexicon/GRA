# H5146 OCR pilot — ground-truth extraction for ONE gra page.
# Page assignment: entry starts at metaline <pc>NNNN; body text belongs to
# the current page until a [PageMMMM] marker flips the current page.
# Devanagari asserted by gra.txt: k1 headwords (SLP1) + {@...@} spans (IAST-ish).
import codecs, re, sys, unicodedata
from indic_transliteration import sanscript

GRA = '/Users/mac/Documents/GitHub/csl-orig/v02/gra/gra.txt'
PAGE = sys.argv[1] if len(sys.argv) > 1 else '0955'
DENSITY = '--density' in sys.argv

txt = codecs.open(GRA, 'r', 'utf-8').read()
entries = re.split(r'(?=^<L>)', txt, flags=re.M)

chunks = {}  # page -> list of body text chunks assigned to it
head = {}    # page -> headwords starting on it (order)
for e in entries:
    m = re.match(r'<L>\d+<pc>(\d+)<k1>(.*?)<k2>.*?<h>', e)
    if not m:
        continue
    cur = m.group(1)
    head.setdefault(cur, []).append(m.group(2))
    body = e[m.end():]
    for part in re.split(r'\[Page(\d+)\]', body):
        pm = re.fullmatch(r'\d{4}', part)
        if pm:
            cur = part
        elif part:
            chunks.setdefault(cur, []).append(part)

if DENSITY:
    dens = []
    for p, cs in chunks.items():
        if int(p) % 2 == 1:
            n = sum(len(re.findall(r'\{@.*?@\}', c, re.S)) for c in cs)
            dens.append((n, p))
    dens.sort(reverse=True)
    for n, p in dens[:12]:
        print(p, n)
    sys.exit(0)

def clean_span(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\{[^}]*\}', '', s)
    return unicodedata.normalize('NFC', s.strip())

pieces = []
for k1 in head.get(PAGE, []):
    if k1:
        pieces.append(sanscript.transliterate(k1, sanscript.SLP1, sanscript.DEVANAGARI))
for c in chunks.get(PAGE, []):
    for sp in re.findall(r'\{@(.*?)@\}', c, re.S):
        pieces.append(clean_span(sp))

gt = unicodedata.normalize('NFC', ' '.join(p for p in pieces if p))
out = ' '.join(gt.split())
codecs.open('gt_page%s.txt' % PAGE, 'w', 'utf-8').write(out + '\n')
print('GT pieces:', len(pieces), '| GT chars:', len(out))
print(out[:500])
