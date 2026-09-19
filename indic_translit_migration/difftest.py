#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""H5148 differential test: retired legacy transcoder vs library-backed engine.

For every XML table in both pipeline dirs (verbs01/, vn/grametaAB_multihw/)
and every corpus input (table keys, real repo data, synthetic combos),
legacy transcoder (materialized from the last pre-migration commit) and the new engine
(indic_translit_migration/transcoder_engine.py) must produce BYTE-IDENTICAL
output. Exit 1 on any mismatch.

Usage: python3 indic_translit_migration/difftest.py
"""
import glob
import importlib.util
import os
import random
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import transcoder_engine as new  # noqa: E402

TABLE_DIRS = {
    'verbs01': os.path.join(REPO, 'verbs01', 'transcoder'),
    'vn': os.path.join(REPO, 'vn', 'grametaAB_multihw', 'transcoder'),
}
CORPUS_FILES = {
    'vn': [os.path.join(REPO, 'vn', 'grametaAB_multihw',
                        'gra_CSL_AB_meta.head.txt')],
    'verbs01': [os.path.join(REPO, 'verbs01', 'gra_verb_filter.txt'),
                os.path.join(REPO, 'verbs01', 'gra_verb_filter_map.txt')],
}


def load_legacy():
    # Walk back past any post-migration commits until the blob is the real
    # legacy FSM (H4235 verifier finding: HEAD may already be the stub,
    # which would make this test self-referential).
    blob = None
    for depth in range(1, 50):
        rev = 'HEAD~%d' % depth
        try:
            cand = subprocess.check_output(
                ['git', '-C', REPO, 'show', '%s:verbs01/transcoder.py' % rev],
                stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            break
        if b'transcoder_engine' not in cand:
            blob = cand
            print('legacy materialized from %s' % rev)
            break
    if blob is None:
        raise SystemExit('no pre-migration legacy blob found')
    tmp = tempfile.mkdtemp(prefix='legacy_transcoder_')
    path = os.path.join(tmp, 'legacy_transcoder.py')
    with open(path, 'wb') as f:
        f.write(blob)
    spec = importlib.util.spec_from_file_location('legacy_transcoder', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def table_inputs(table_dir):
    """{fromto: [raw <in> values]} parsed straight from the XML tables."""
    import xml.etree.ElementTree as ET
    out = {}
    for f in sorted(glob.glob(os.path.join(table_dir, '*.xml'))):
        fromto = os.path.splitext(os.path.basename(f))[0]
        vals = []
        for e in ET.parse(f).getroot():
            if e.tag == 'e':
                x = e.find('in')
                vals.append(x.text if x is not None and x.text else '')
        out[fromto] = vals
    return out


def corpus(table_dir_key, tables):
    """Every input string we dare throw at both engines."""
    items = set()
    for fromto, vals in tables.items():
        items.update(v for v in vals if v)  # raw keys
        items.update(v + v for v in vals if v)  # doubled keys
        items.update('x' + v + 'y' for v in vals if v)  # embedded
    for cf in CORPUS_FILES[table_dir_key]:
        if os.path.exists(cf):
            with open(cf, encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\r\n')
                    items.update(line.split('\t'))
                    items.update(re.split(r'[^A-Za-z/a-z^\\\\~@#{}._0-9]+',
                                          line))
    items.add('')
    items.add('{#zAstra#} 123 <h>7</h> sarvam')
    items.add('k/^')
    rng = random.Random(42)
    pool = [i for i in items if i]
    for _ in range(2000):
        items.add(''.join(rng.choice(pool) for _ in range(3)))
    return sorted(items)


def main():
    legacy = load_legacy()
    failures = 0
    total = 0
    for key, tdir in sorted(TABLE_DIRS.items()):
        tables = table_inputs(tdir)
        pairs = list(tables.keys()) + ['slp1_slp1', 'roman_slp1_ghost',
                                       'roman1_slp1_ghost']
        inputs = corpus(key, tables)
        for pair in pairs:
            sfrom, sto = pair.split('_', 1)
            # each engine gets its own directory context
            legacy.transcoder_set_dir(tdir)
            new.transcoder_set_dir(tdir)
            for item in inputs:
                total += 1
                a = legacy.transcoder_processString(item, sfrom, sto)
                b = new.transcoder_processString(item, sfrom, sto)
                if a != b:
                    failures += 1
                    if failures <= 20:
                        print('MISMATCH %s %r\n  legacy=%r\n  new   =%r'
                              % (pair, item, a, b))
        # processElements spot-check (tag-wrapped segments)
        legacy.transcoder_set_dir(tdir)
        new.transcoder_set_dir(tdir)
        for pair in tables:
            sfrom, sto = pair.split('_', 1)
            for item in inputs[:500]:
                if not item or re.search(r'[<>]', item):
                    continue
                wrapped = '<SA>%s</SA>' % item
                total += 1
                a = legacy.transcoder_processElements(wrapped, sfrom, sto,
                                                      'SA')
                b = new.transcoder_processElements(wrapped, sfrom, sto, 'SA')
                if a != b:
                    failures += 1
                    if failures <= 20:
                        print('MISMATCH-ELEM %s %r\n  legacy=%r\n  new   =%r'
                              % (pair, wrapped, a, b))
    # cache-scoping: missing table in dir A, present in dir B — legacy
    # re-attempts after set_dir, so the new engine must too (H4235 finding).
    for sfrom, sto in [('roman', 'slp1'), ('roman1', 'slp1')]:
        legacy.transcoder_set_dir(TABLE_DIRS['verbs01'])
        new.transcoder_set_dir(TABLE_DIRS['verbs01'])
        a1 = legacy.transcoder_processString('kh', sfrom, sto)
        b1 = new.transcoder_processString('kh', sfrom, sto)
        legacy.transcoder_set_dir(TABLE_DIRS['vn'])
        new.transcoder_set_dir(TABLE_DIRS['vn'])
        for item in ['kh', 'ai', 'a/ M zAstra']:
            total += 2
            a = legacy.transcoder_processString(item, sfrom, sto)
            b = new.transcoder_processString(item, sfrom, sto)
            if a != b:
                failures += 1
                print('MISMATCH-CACHE %s %r legacy=%r new=%r'
                      % (sfrom + '_' + sto, item, a, b))
        if a1 != b1:
            failures += 1
            print('MISMATCH-CACHE pre-phase %s' % sfrom)

    print('compared %d cases, %d mismatches' % (total, failures))
    if failures:
        sys.exit(1)
    print('DIFTEST PASS: new engine byte-identical to legacy on all pairs')


if __name__ == '__main__':
    main()
