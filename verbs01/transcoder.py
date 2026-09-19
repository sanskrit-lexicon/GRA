#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""H5148: bootstrap stub — engine migrated to indic_transliteration.

The self-written FSM transcoder that lived here was retired 2026-09-19 and
replaced by the canonical library-backed engine in
indic_translit_migration/transcoder_engine.py (single copy, no per-dir
duplicates). XML transliteration tables in ./transcoder/ are UNCHANGED —
they remain the data source. The public API is identical; callers
(preverb0.py, preverb1.py, ...) need no changes.

NOTE: the legacy default table dir (../data/transcoder) was never used by
any caller in this repo — every caller calls transcoder_set_dir() first.
Requires: indic-transliteration == 2.3.82.
Verification: indic_translit_migration/difftest.py (429,977 cases,
byte-identical to the retired copy at git HEAD).
"""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_engine_dir = None
_walk = _here
for _ in range(5):  # pipeline dirs sit at depth 1 (verbs01) or 2 (vn/...)
    _cand = os.path.join(_walk, 'indic_translit_migration')
    if os.path.isfile(os.path.join(_cand, 'transcoder_engine.py')):
        _engine_dir = _cand
        break
    _walk = os.path.dirname(_walk)
if _engine_dir is None:  # pipeline dir used stand-alone
    _engine_dir = os.path.join(_here, 'indic_translit_migration')
if _engine_dir not in sys.path:
    sys.path.insert(0, _engine_dir)

from transcoder_engine import (  # noqa: E402,F401
    transcoder_set_dir,
    transcoder_get_dir,
    transcoder_processString,
    transcoder_processElements,
)
