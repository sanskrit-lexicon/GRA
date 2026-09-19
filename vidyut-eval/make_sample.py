# -*- coding:utf-8 -*-
"""H5147 make_sample.py -- freeze the evaluation sample for vidyut-vs-verbs01.

Draws 200-500 word forms from gra.txt (forms of Grassmann's headwords),
biased toward verb forms the verbs01 pipeline already processes:

  type=infl : inflected form mechanically derived from a sampled VERB entry
              (stem from the entry's own `Stamm {@X:@}` line, suffix from one
              of its `<div n="TS">-suffix` lines). Reference lemma = entry k1
              (valid by construction).
  type=cite : the citation form (k1) itself, for a seeded 1-in-4 subset.
              Shows what each system does with bare roots.
  type=ctrl : same derivation over NON-verb entries (seeded controls); these
              are mostly noun forms, so they measure precision on non-verbs.

Deterministic: fixed seed 5147, entries sorted by numeric L.
Output: sample.tsv (frozen, committed). Re-runnable.
"""
import re, sys, unicodedata, codecs
from random import Random

SEED = 5147
N_VERB_ENTRIES = 250     # infl forms drawn from these (up to 2 each)
N_CTRL_ENTRIES = 50
MAX_FORMS_PER_ENTRY = 1
GRA = r"C:\Users\user\Documents\GitHub\csl-orig\v02\gra\gra.txt"
VERBMAP = r"C:\Users\user\Documents\GitHub\GRA\verbs01\gra_verb_filter_map.txt"
OUT = r"C:\Users\user\Documents\GitHub\GRA\vidyut-eval\sample.tsv"

# ---------------------------------------------------------------------------
# Grassmann transliteration -> SLP1
# ---------------------------------------------------------------------------
# Digraphs first, then single chars.  Diacritics resolved mark-by-mark:
#   dot-below = retroflex/vocalic class, macron = long vowel, tilde = ñ,
#   acute/grave = accent (stripped).  SLP1 has no accents, so stripping is right.
DIGRAPHS = {
    'kh':'K','gh':'G','ch':'C','jh':'J','ṭh':'W','ḍh':'Q','Th':'W','Dh':'Q',
    'th':'T','dh':'D','ph':'P','bh':'B','ai':'E','au':'O',
}
DOT_BELOW = {'r':'ṛ','l':'ḷ','t':'ṭ','d':'ḍ','n':'ṇ','s':'ṣ','h':'ḥ','m':'ṃ'}
MACRON = {'a':'ā','i':'ī','u':'ū','ṛ':'ṝ'}
DOT_ABOVE = {'n':'ṅ','m':'ṃ'}
TILDE = {'n':'ñ'}
SINGLES = {
    'a':'a','ā':'A','i':'i','ī':'I','u':'u','ū':'U',
    'ṛ':'f','ṝ':'F','ḷ':'x','ḹ':'X','e':'e','o':'o',
    'ṃ':'M','ṁ':'M','ḥ':'H',
    'k':'k','g':'g','ṅ':'N','c':'c','j':'j','ñ':'Y',
    'ṭ':'w','ḍ':'q','ṇ':'R','t':'t','d':'d','n':'n',
    'p':'p','b':'b','m':'m','y':'y','r':'r','l':'l','v':'v',
    'ś':'z','ṣ':'S','s':'s','h':'h',
}
def _base_char(ch):
    """Resolve one (possibly precomposed/decomposed) char to bare IAST."""
    d = unicodedata.normalize('NFD', ch)
    base, marks = d[0], d[1:]
    if '\u0323' in marks:  base = DOT_BELOW.get(base, base)
    if '\u0304' in marks:  base = MACRON.get(base, base)
    if '\u0307' in marks:  base = DOT_ABOVE.get(base, base)
    if '\u0303' in marks:  base = TILDE.get(base, base)
    # acute U+0301 / grave U+0300 = accent: dropped (SLP1 is accentless)
    return base

def to_slp1(s):
    s = s.rstrip(':.')  # Grassmann stem markers like 'aca:'
    out = []
    i = 0
    while i < len(s):
        two = s[i:i+2]
        if two in DIGRAPHS:
            out.append(DIGRAPHS[two]); i += 2; continue
        ch = _base_char(s[i])
        if ch in SINGLES:
            out.append(SINGLES[ch]); i += 1; continue
        return None  # not Sanskrit translit (German etc.)
    return ''.join(out)

# ---------------------------------------------------------------------------
# gra.txt entry parsing (same <L>...<LEND> discipline as verbs01)
# ---------------------------------------------------------------------------
def init_entries(filein):
    with codecs.open(filein, encoding='utf-8', mode='r') as f:
        lines = [line.rstrip('\r\n') for line in f]
    recs = []
    idx1 = None
    for idx, line in enumerate(lines):
        if line.startswith('<L>'):
            if idx1 is None:
                idx1 = idx
        elif line.startswith('<LEND>'):
            if idx1 is not None:
                recs.append((lines[idx1:idx+1], idx1 + 1))
                idx1 = None
    return recs

def parse_meta(metaline):
    d = {}
    m = re.search(r'<L>([^<]*)', metaline); d['L'] = m.group(1) if m else '?'
    m = re.search(r'<k1>([^<]*)', metaline); d['k1'] = m.group(1) if m else '?'
    return d

STEM_RE = re.compile(r'Stamm.*?{@([^:@]+):?@}')
SUFFIX_RE = re.compile(r'<div n="TS">-([^<\s]+)')

def entry_data(entrylines):
    meta = parse_meta(entrylines[0])
    body = entrylines[1:-1]
    stem = None
    for ln in body:
        m = STEM_RE.search(ln)
        if m:
            stem = m.group(1)
            break
    suffixes = []
    for ln in body:
        for m in SUFFIX_RE.finditer(ln):
            sfx = m.group(1).rstrip(',.')
            if sfx and re.fullmatch(r'[āīūṛṝḷaAiIuUeEoOMḥkgGṅcjJñYṭḍṇtdnpbmyrlvśṣsh]+', sfx):
                suffixes.append(sfx)
    return meta, stem, suffixes

# Surface-form construction: minimal verb sandhi.
# Vowel-initial endings: lopa (elision) of a stem-final simple vowel, except
# a + Ami which lengthens (Bav + a + Ami -> BavAmi).  Consonant-initial
# endings: direct concat, plus duplicate-stop elision and final-stop devoicing
# alternates (kept in the `variants` column for reference only).
DEVOICE = {'g':'k','G':'K','j':'c','J':'C','d':'t','D':'T','b':'p','B':'P'}
VOWELS = set('aiufxFeEoOAiIuU')
def sandhi(stem_slp1, suffix_slp1):
    """Return (primary_form, [alternate_forms]) for stem + ending."""
    s, t = stem_slp1, suffix_slp1
    alts = []
    if t and t[0] in VOWELS:
        if s and s[-1] == t[0] and s[-1] in 'aA':
            return s + t[1:], alts                # same-vowel collapse: dA+as -> dAs
        if s and s[-1] in 'aiufxX':
            if s[-1] == 'a' and t.startswith('Ami'):
                return s[:-1] + 'Ami', alts       # BavAmi (lengthening)
            return s[:-1] + t, alts               # lopa: nama+ati -> namati
        return s + t, alts
    if s and t and s[-1] == t[0]:
        alts.append(s[:-1] + t)                   # sat + ta -> sata / sta
    if s and t and s[-1] in DEVOICE and t[0] in 'tTsScC':
        alts.append(s[:-1] + DEVOICE[s[-1]] + t)  # vah + ti -> vahati / vakti
    return s + t, alts

def main():
    rng = Random(SEED)
    recs = init_entries(GRA)
    print(len(recs), 'entries from gra.txt')

    verbs = {}  # L -> (k1, mw)
    with codecs.open(VERBMAP, encoding='utf-8', mode='r') as f:
        for line in f:
            m = re.search(r'L=([^,]+), k1=([^,]+), .* mw=(\S+)', line)
            if m:
                verbs[m.group(1)] = (m.group(2), m.group(3))
    print(len(verbs), 'verbs01 verb entries')

    # split entries, numeric-L sort for stable sampling
    verb_ents, other_ents = [], []
    for entrylines, ln in recs:
        meta, stem, suffixes = entry_data(entrylines)
        if not suffixes or meta['k1'] == '?':
            continue
        key = float(meta['L']) if re.fullmatch(r'[\d.]+', meta['L']) else 10**9
        item = (key, meta['L'], meta['k1'], stem, suffixes)
        if meta['L'] in verbs:
            verb_ents.append(item)
        else:
            other_ents.append(item)
    verb_ents.sort(); other_ents.sort()
    print(len(verb_ents), 'verb entries with derivable forms;',
          len(other_ents), 'non-verb entries with forms')

    rows = []
    def emit(L, k1, mw, typ, stem_src, suffix):
        # stem_src is Grassmann translit, or plain SLP1 when it equals k1
        stem_slp1 = k1 if stem_src == k1 else to_slp1(stem_src)
        suffix_slp1 = to_slp1(suffix)
        if stem_slp1 is None or suffix_slp1 is None or not suffix_slp1:
            return
        form, alts = sandhi(stem_slp1, suffix_slp1)
        rows.append((L, k1, mw, typ, k1, stem_slp1, suffix_slp1,
                     form, '|'.join([form] + alts)))

    sampled_verbs = rng.sample(verb_ents, N_VERB_ENTRIES)
    for key, L, k1, stem, suffixes in sampled_verbs:
        stem0 = stem if stem else k1  # fallback: k1 is already SLP1-compatible
        for sfx in suffixes[:MAX_FORMS_PER_ENTRY]:
            emit(L, k1, verbs[L][1], 'infl', stem0, sfx)
        if rng.random() < 0.25:  # seeded 1-in-4 citation-form subset
            rows.append((L, k1, verbs[L][1], 'cite', k1, '-', '-', k1, k1))

    sampled_ctrl = rng.sample(other_ents, N_CTRL_ENTRIES)
    for key, L, k1, stem, suffixes in sampled_ctrl:
        stem0 = stem if stem else k1
        emit(L, k1, '-', 'ctrl', stem0, suffixes[0])

    # dedup exact (type,form) duplicates, cap total at 500
    seen, final = set(), []
    for r in rows:
        keyf = (r[3], r[7])
        if keyf in seen:
            continue
        seen.add(keyf)
        final.append(r)
    final = final[:500]

    with codecs.open(OUT, 'w', encoding='utf-8') as f:
        f.write('id\tL\tk1\tmw\ttype\tref_lemma\tstem\tsuffix\tform\tvariants\n')
        for i, r in enumerate(final, 1):
            L, k1, mw, typ, k1slp1, stem, sfx, form, vars_ = r
            f.write('%04d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' %
                    (i, L, k1, mw, typ, k1slp1, stem, sfx, form, vars_))
    from collections import Counter
    print(len(final), 'forms written to', OUT)
    for t, c in sorted(Counter(r[3] for r in final).items()):
        print(' ', t, c)

if __name__ == '__main__':
    main()
