#-*- coding:utf-8 -*-
"""H5147: run vidyut over the fixed sample.

Slice A (sample_headwords.tsv): direct kosha lookup of the headword form (SLP1).
  - fallback per official tutorial for visarga forms: bare query, then final H->s / H->r variants.
Slice B (verb_set.tsv): same direct lookup + generator round-trip:
  derive 3sg parasmaipada lat (Bavati-style form) from the GRA root with vidyut-prakriya,
  then kosha-lookup that form and check dhatu-lemma recovery (== GRA k1, or == verbs01 mw root).

Output: vidyut_sample.tsv, vidyut_verbs.tsv (committed).
"""
import codecs, os, sys
from vidyut.kosha import Kosha
import vidyut.prakriya as p

HERE = os.path.dirname(os.path.abspath(__file__))
KOSHA = os.environ.get('VIDYUT_KOSHA', '/tmp/opencode/vidyut-0.4.0/kosha')

def read_tsv(name):
    rows = []
    with codecs.open(os.path.join(HERE, name), encoding='utf-8', mode='r') as f:
        for line in f:
            line = line.rstrip('\r\n')
            if not line or line.startswith('#') or line.startswith('L\t'):
                continue
            rows.append(line.split('\t'))
    return rows

def kosha_analyze(kosha, form):
    """Return (n_entries, n_tinanta, lemmas_set, verb_lemmas_set, query_used)."""
    queries = [form]
    if form.endswith('H'):
        queries += [form[:-1] + 's', form[:-1] + 'r']
    for q in queries:
        es = list(kosha.get(q))
        if es:
            lemmas = {e.lemma for e in es}
            tins = [e for e in es if 'Tinanta' in type(e).__name__]
            verb_lemmas = {e.lemma for e in tins}
            return len(es), len(tins), lemmas, verb_lemmas, q
    return 0, 0, set(), set(), queries[0]

def main():
    kosha = Kosha(KOSHA)
    vy = p.Vyakarana()

    # Slice A
    out = codecs.open(os.path.join(HERE, 'vidyut_sample.tsv'), 'w', encoding='utf-8')
    out.write('L\tk1\tn_entries\tn_tinanta\tlemmas\tverb_lemmas\tquery_used\n')
    for (L, k1, k2, isv) in read_tsv('sample_headwords.tsv'):
        n, nt, lem, vlem, q = kosha_analyze(kosha, k1)
        out.write('%s\t%s\t%d\t%d\t%s\t%s\t%s\n' % (L, k1, n, nt,
            ','.join(sorted(lem)), ','.join(sorted(vlem)), q))
    out.close()

    # Slice B
    out = codecs.open(os.path.join(HERE, 'vidyut_verbs.tsv'), 'w', encoding='utf-8')
    out.write('L\tk1\tmw\tn_entries\tn_tinanta\tverb_lemmas\trt_derive_ok\trt_form\trt_lookup_entries\trt_lemma_match_k1\trt_lemma_match_mw\n')
    nd = nok = nlk = 0
    for (L, k1, k2, mw) in read_tsv('verb_set.tsv'):
        n, nt, lem, vlem, q = kosha_analyze(kosha, k1)
        rt_ok, rt_form, rt_n, rt_k1, rt_mw = 0, '', 0, 0, 0
        try:
            prs = vy.derive(p.Pada.Tinanta(dhatu=k1, lakara=p.Lakara.Lat,
                prayoga=p.Prayoga.Kartari, purusha=p.Purusha.Prathama, vacana=p.Vacana.Eka))
            if prs:
                rt_ok = 1
                nd += 1
                rt_form = prs[0].text
                # visarga-aware lookup of the generated form
                es = list(kosha.get(rt_form))
                if not es and rt_form.endswith('H'):
                    es = list(kosha.get(rt_form[:-1] + 's')) or list(kosha.get(rt_form[:-1] + 'r'))
                rt_n = len(es)
                if rt_n:
                    nlk += 1
                    dlemma = {e.lemma for e in es if 'Tinanta' in type(e).__name__}
                    if k1 in dlemma:
                        rt_k1 = 1
                    if mw and mw in dlemma:
                        rt_mw = 1
        except Exception:
            pass
        if rt_k1:
            nok += 1
        out.write('%s\t%s\t%s\t%d\t%d\t%s\t%d\t%s\t%d\t%d\t%d\n' % (L, k1, mw, n, nt,
            ','.join(sorted(vlem)), rt_ok, rt_form, rt_n, rt_k1, rt_mw))
    out.close()
    print('slice B: derive ok %d / kosha-hit %d / lemma==k1 %d' % (nd, nlk, nok))

if __name__ == '__main__':
    main()
