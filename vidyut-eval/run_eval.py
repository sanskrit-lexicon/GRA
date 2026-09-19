# -*- coding:utf-8 -*-
"""H5147 run_eval.py -- vidyut vs verbs01 lemmatization eval over sample.tsv.

Lane 1 (vidyut): form -> lemma via vidyut-prakriya's generated tiNanta dump
  (tinantas_slp1.csv, produced by create_all_tinantas --output-scheme=Slp1).
  The dump maps every conjugated form to its dhatu (SLP1).  A form is a HIT
  if it occurs in the dump (any root); AGREEMENT if the sample's reference
  lemma (gra.txt entry k1) is among the roots returned, raw or
  marker-normalized (vidyut dhatu strings carry seT/indicatory markers
  like '~', '\\', '/').

Lane 2 (verbs01): form -> lemma modeled from verbs01's own committed
  artifacts, because verbs01 is a headword classifier, not a lemmatizer.
  Its lemma resources are (a) the 905 verb roots (gra_verb_filter_map.txt),
  (b) the prefixed-form table (gra_preverb1.txt: upasarga+root -> form),
  (c) the upasarga list (gra_upasarga_map.txt).  Lookup order: raw form in
  (a) U (b); then upasarga-stripped form in (a); then naive longest-suffix
  strip in (a).  HIT = any root found; AGREEMENT = found root == ref lemma.

Usage:  python run_eval.py [path/to/tinantas_slp1.csv] [--sample sample.tsv]
Writes: eval_results.tsv (or eval_results_<samplename>.tsv), report_fragments.tsv (per-type numbers).
"""
import csv, io, os, re, sys, hashlib
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, 'sample.tsv')
GRA_ROOT_DIR = r'C:\Users\user\Documents\GitHub\GRA'
VERBMAP = os.path.join(GRA_ROOT_DIR, 'verbs01', 'gra_verb_filter_map.txt')
PREVERB1 = os.path.join(GRA_ROOT_DIR, 'verbs01', 'gra_preverb1.txt')
UPASARGA = os.path.join(GRA_ROOT_DIR, 'verbs01', 'gra_upasarga_map.txt')
DUMP = os.path.join(HERE, 'tinantas_slp1.csv')
ARGS = sys.argv[1:]
if '--sample' in ARGS:
    i = ARGS.index('--sample')
    SAMPLE = ARGS[i + 1]
    ARGS = ARGS[:i] + ARGS[i + 2:]
else:
    SAMPLE = os.path.join(HERE, 'sample.tsv')
DUMP = ARGS[0] if ARGS else DUMP
_tag = os.path.splitext(os.path.basename(SAMPLE))[0]
OUT = os.path.join(HERE, ('eval_results.tsv' if _tag == 'sample'
                          else 'eval_results_%s.tsv' % _tag))

MARKERS = re.compile(r'[~\\/^]+')          # vidyut seT/indicatory markers
def norm_root(x):
    return MARKERS.sub('', x)

def vidyut_core(d):
    """Strip vidyut dhatu-string conventions down to a bare-root sketch.

    vidyut's upadesha = root + (internal \\, /, ^ it-flags) + indicatory
    vowel (seT roots only, marked with a trailing ~ flag) + suffix flags
    (Y, w, ...).  qu/ru are It-prefixes.  Examples: BU->BU, zu\\Y->zu,
    qudA\\Y->dA, va\\ha~^->vah, Ra\\ma~->Ram, puwi~->pu, kfpU~\\->kfp,
    De\\w->de.
    """
    flag_set = '~' in d
    if d.startswith('qu'): d = d[2:]
    elif d.startswith('ru'): d = d[2:]
    d = norm_root(d)                     # strip ~ \ / ^ anywhere
    d = d.rstrip('YwR')                  # trailing it-flags
    if flag_set:                         # seT: final vowel is indicatory
        d = d.rstrip('aiuU')             # (short a/i/u and long U; A/I kept)
    return d

def lev(a, b):
    """Edit distance (small strings)."""
    if abs(len(a) - len(b)) > 2:
        return 99
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j-1] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]

def tolerant(a, b):
    """Convention-tolerant lemma match: equal, or edit distance <= 1
    (covers su/zu, vand/vad, arz/arS style drift)."""
    if not a or not b:
        return False
    return a == b or lev(a, b) <= 1

# ---------------------------------------------------------------- vidyut lane
def load_dump(path):
    forms = defaultdict(set)   # form -> set(dhatu raw)
    with io.open(path, encoding='utf-8', mode='r') as f:
        # the exe logs a '.git directory found at:' notice on stdout before
        # the CSV header; skip everything up to the 'padas,...' header line.
        lines = iter(f)
        for line in lines:
            if line.startswith('padas,'):
                rdr = csv.DictReader(io.StringIO(line + ''.join(lines)))
                break
        else:
            raise RuntimeError('no CSV header found in ' + path)
        for row in rdr:
            for pada in row['padas'].split('|'):
                if pada:
                    forms[pada].add(row['dhatu'])
    return forms

# --------------------------------------------------------------- verbs01 lane
def load_verbs01():
    roots = set()
    with io.open(VERBMAP, encoding='utf-8') as f:
        for line in f:
            m = re.search(r'k1=([^,]+),', line)
            if m:
                roots.add(m.group(1))
    prefixed = {}              # prefixed form -> root (k1 spelling)
    with io.open(PREVERB1, encoding='utf-8') as f:
        for line in f:
            if line.startswith(';'):
                continue
            fields = line.strip().split()
            if len(fields) >= 4:
                prefixed[fields[3]] = fields[2]
    upasargas = set()
    with io.open(UPASARGA, encoding='utf-8') as f:
        for line in f:
            if line.startswith(';'):
                continue
            # format: <count>\t<translit text>\t<SLP1 transcode>  (field 3 is SLP1)
            parts = line.split('\t')
            if len(parts) >= 3 and parts[2].strip():
                upasargas.add(parts[2].strip())
    # naive tiNanta endings for the fallback stripper (longest first)
    endings = ['anta', 'Ami', 'asi', 'ati', 'Ate', 'ante', 'Anti', 'ata',
               'anti', 'tAti', 'tAte', 'Dvam', 'ire', 'are', 'ira', 're',
               'ti', 'ta', 'te', 'as', 'Am']
    return roots, prefixed, sorted(upasargas), endings

def verbs01_lookup(form, roots, prefixed, upasargas, endings):
    """Return the root verbs01-style resources yield, or None."""
    if form in roots:
        return form
    if form in prefixed:
        return prefixed[form]
    for upa in upasargas:
        if upa and form.startswith(upa) and len(form) > len(upa) + 1:
            stripped = form[len(upa):]
            if stripped in roots:
                return stripped
            if stripped in prefixed:
                return prefixed[stripped]
    for e in endings:
        if form.endswith(e) and len(form) > len(e) + 1:
            stem = form[:-len(e)]
            if stem in roots:
                return stem
    return None

# ------------------------------------------------------------------ scoring
def main():
    print('loading vidyut dump ...')
    dump = load_dump(DUMP)
    print(' ', len(dump), 'distinct forms in dump')
    roots, prefixed, upasargas, endings = load_verbs01()
    print(' ', len(roots), 'verbs01 roots,', len(prefixed), 'prefixed forms,',
          len(upasargas), 'upasargas')

    stats = defaultdict(lambda: [0, 0, 0, 0])  # type -> [n, vhit, vagree, lhit]
    with io.open(SAMPLE, encoding='utf-8') as f, io.open(OUT, 'w', encoding='utf-8', newline='') as out:
        out.write('id\tform\ttype\tref_lemma\tvidyut_roots\tvidyut_hit\t'
                  'vidyut_exact_agree\tvidyut_norm_agree\tvidyut_variant_hit\t'
                  'verbs01_root\tverbs01_hit\tverbs01_agree\n')
        for line in f:
            if line.startswith('id\t'):
                continue
            c = line.rstrip('\n').split('\t')
            _id, L, k1, mw, typ, ref, stem, sfx, form, variants = c
            vr = dump.get(form, set())
            vhit = bool(vr)
            vex = bool(vr and ref in vr)
            vnorm = bool(vr and any(tolerant(vidyut_core(x), ref) for x in vr))
            vvar = False
            if not vhit:
                for alt in variants.split('|'):
                    if alt != form and dump.get(alt):
                        vvar = True
                        break
            lroot = verbs01_lookup(form, roots, prefixed, upasargas, endings)
            lhit = lroot is not None
            lagree = bool(lroot and tolerant(lroot, ref))
            s = stats[typ]
            s[0] += 1
            s[1] += vhit
            s[2] += vnorm
            s[3] += lhit
            out.write('\t'.join([_id, form, typ, ref,
                                 '|'.join(sorted(vr)) if vr else '-',
                                 '1' if vhit else '0',
                                 '1' if vex else '0',
                                 '1' if vnorm else '0',
                                 '1' if vvar else '0',
                                 lroot if lroot else '-',
                                 '1' if lhit else '0',
                                 '1' if lagree else '0']) + '\n')

    print('\n%-6s %5s %9s %11s %9s' % ('type', 'n', 'vid_hit', 'vid_agreeN', 'v01_hit'))
    tot = [0, 0, 0, 0, 0]
    for typ in ('infl', 'cite', 'ctrl'):
        n, vhit, vnorm, lhit = stats[typ]
        if not n:
            continue
        print('%-6s %5d %8.1f%% %10.1f%% %8.1f%%' %
              (typ, n, 100.0 * vhit / n, 100.0 * vnorm / n, 100.0 * lhit / n))
        for i, v in enumerate((n, vhit, vnorm, lhit)):
            tot[i] += v
    print('%-6s %5d %8.1f%% %10.1f%% %8.1f%%' %
          ('ALL', tot[0], 100.0 * tot[1] / tot[0], 100.0 * tot[2] / tot[0],
           100.0 * tot[3] / tot[0]))

if __name__ == '__main__':
    main()
