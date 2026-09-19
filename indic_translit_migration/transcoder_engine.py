#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""H5148 — indic_transliteration-backed transcoder engine (canonical, single copy).

Replaces the two byte-identical self-written FSM copies
(verbs01/transcoder.py, vn/grametaAB_multihw/transcoder.py, both retired
2026-09-19). Public API is preserved 1:1:

  transcoder_set_dir(dir) / transcoder_get_dir()
  transcoder_processString(line, from1, to)
  transcoder_processElements(line, from1, to, tagname)

Engine:
  * Single-state XML tables (<from>_<to>.xml: slp1_roman, slp_roman1,
    roman_slp1, roman1_slp1) are converted once into indic_transliteration
    SchemeMaps and transliterated by the library (indic-transliteration
    2.3.82). The neutral group name 'transcoder' keeps the mapper in pure
    longest-match/passthrough mode (no brahmic virama/om/digit side
    effects), so output stays byte-identical to the legacy FSM.
  * The stateful table slp1_deva (INIT/SKT schwa states, 3-way state lists)
    is served by a compact port of the legacy FSM runner — a stateless
    SchemeMap cannot express look-behind context, and the library built-in
    SLP1->DEVANAGARI changes bytes (digits, om-fix, accent order).
    Byte-identity is proven by indic_translit_migration/difftest.py against
    the retired copies at git HEAD.

Legacy semantics preserved exactly:
  from == to            -> line unchanged
  missing table file    -> line unchanged (silent passthrough)
  unmapped character    -> passthrough, state reset
  longest match wins; on equal length the EARLIEST table entry wins
"""
from __future__ import print_function

__program_name__ = 'transcoder.py (indic_translit_migration engine)'
__license__ = 'GPL http://www.gnu.org/licenses/gpl.txt'

import os
import re
import xml.etree.ElementTree as ET

from indic_transliteration.sanscript import Scheme, SchemeMap, transliterate

_transcoder_dir = None
_tables = {}   # fromto -> ('stateless', SchemeMap) | ('stateful', fsm_dict)


def transcoder_set_dir(dir):
    """Mirror legacy: absolute path recorded only if it exists; returned."""
    global _transcoder_dir
    path = os.path.abspath(dir)
    if os.path.exists(path):
        _transcoder_dir = path
    return _transcoder_dir


def transcoder_get_dir():
    return _transcoder_dir


def _to_unicode(x):
    """Decode \\uxxxx escapes exactly like the legacy loader."""
    if x is None:
        return ''
    if x == r"\u":
        return x
    if not re.match(r'\\u', x):
        return x
    ans = ''
    for z in re.split(r'\\u', x):
        if z == '':
            continue
        z1, z2 = z, ''
        if len(z) > 4:
            z1, z2 = z[:4], z[4:]
        ans += chr(int(z1, 16)) + z2
    return ans


def _parse_entries(path):
    """Return (start_state, [(in, out, startStates, nextState), ...]).

    nextState=None means "no <next> element" (legacy: stay in startStates[0]).
    """
    xml = ET.parse(path).getroot()
    start_state = xml.attrib['start']  # required, as in legacy
    entries = []
    for e in xml:
        if e.tag != 'e':
            continue  # xml comments
        x_in = e.find("in")
        inval = x_in.text if x_in is not None else ''
        if not inval:
            inval = ''
        s_el = e.find("s")
        sval = s_el.text if (s_el is not None and s_el.text) else 'INIT'
        start_states = re.split(",", sval)
        x_out = e.find("out")
        outval = x_out.text if x_out is not None else ''
        if outval is None:
            outval = ''
        x_next = e.find("next")
        next_state = x_next.text if x_next is not None else start_states[0]
        entries.append((_to_unicode(inval), _to_unicode(outval),
                        start_states, next_state))
    return start_state, entries


def _make_scheme(pairs, name):
    """Custom roman Scheme holding the table under a neutral group.

    Group name 'transcoder' deliberately avoids the 'consonants'/'virama'/
    'accents' suffixes so the library mapper applies plain longest-match +
    passthrough with no brahmic context logic. 'vowels' carries identity
    entries only to satisfy Scheme's long_vowels construction; the resulting
    identity maps are transliteration no-ops.
    """
    data = {'vowels': {v: v for v in 'आईऊॠएऐओऔ'},
            'transcoder': dict(pairs)}
    return Scheme(data=data, is_roman=True, name=name)


def _build_stateless(entries, fromto):
    first = entries[0][2]
    for _, _, starts, _ in entries:
        if starts != first:
            raise ValueError('%s: mixed states without <next>; not stateless'
                             % fromto)
    pairs = {}
    for inval, outval, _, _ in entries:
        if inval == '':
            continue
        if inval not in pairs:  # earliest entry wins (legacy tie-break)
            pairs[inval] = outval
    s_in = _make_scheme({k: k for k in pairs}, fromto + '.in')
    s_out = _make_scheme(pairs, fromto + '.out')
    return SchemeMap(s_in, s_out)


def _translit_stateless(line, smap):
    return transliterate(line, scheme_map=smap)


def _load(fromto):
    if fromto in _tables:
        return _tables[fromto]
    result = None
    if _transcoder_dir:
        path = os.path.join(_transcoder_dir, fromto + '.xml')
        if os.path.exists(path):
            start_state, entries = _parse_entries(path)
            try:
                result = ('stateless', _build_stateless(entries, fromto))
            except ValueError:
                result = ('stateful', _build_fsm(start_state, entries,
                                                 fromto))
    _tables[fromto] = result
    return result


# ---------------------------------------------------------------------------
# Stateful tables (slp1_deva): compact port of the legacy FSM runner
# (transcoder_fsm + transcoder_processString + transcoder_processString_match
# from the retired copies, minus debug output). Includes the consonant
# look-ahead ('regex') entries used by slp1_deva. Byte-identity is verified
# by difftest.py.
# ---------------------------------------------------------------------------

_CONLOOK_PAIRS = (('slp1', 'deva'), ('deva', 'slp1'), ('hkt', 'tamil'))
_CONLOOK_VOWELS = re.compile(r'[^aAiIuUfFxXeEoO^/\\]')


def _regex_code(fromto):
    sfrom, _, to = fromto.partition('_')
    if sfrom.startswith('slp1') and to.startswith('deva'):
        return 'slp1_deva'
    if sfrom.startswith('deva') and to.startswith('slp1'):
        return 'deva_slp1'
    if sfrom.startswith('hkt') and to.startswith('tamil'):
        return 'hkt_tamil'
    return None


def _build_fsm(start_state, entries, fromto):
    regex_code = _regex_code(fromto)
    fsm_entries = []
    states = {}
    for i, (inval, outval, start_states, next_state) in enumerate(entries):
        fe = {'starts': start_states, 'in': inval, 'out': outval,
              'next': next_state}
        # legacy conlook: <in>k/^([^aAiIuU...])</in> marks a look-ahead entry;
        # the prefix before '/^' is the matched edge, the class after it is
        # the "is the next char a non-vowel" test.
        m = re.match(r'^([^/]+)/\^', inval)
        if m:
            if not regex_code:
                continue  # legacy: entry skipped entirely
            fe['in'] = m.group(1)
            fe['regex'] = regex_code
        fsm_entries.append(fe)
        edge = fe['in']
        c = edge[0] if edge else edge
        states.setdefault(c, []).append(i)
    return {'start': start_state, 'fsm': fsm_entries, 'states': states}


def _match_len(line, n, m, fe):
    """Return length of the matched input at n, 0 if the rule fails.

    Port of transcoder_processString_match (no-virama variant: the
    deva_slp1/hkt_tamil vowel-sign branches are not reachable for the
    tables in this repo and are omitted; difftest.py guards this).
    """
    edge = fe['in']
    if line[n:n + len(edge)] != edge:
        return 0
    if 'regex' not in fe:
        return len(edge)
    n1 = n + len(edge)
    if n1 == m:
        return len(edge)
    if _CONLOOK_VOWELS.match(line[n1]):
        return len(edge)  # next char is a non-vowel: rule applies
    return 0


def _translit_stateful(line, fsm):
    current = fsm['start']
    fsm_entries = fsm['fsm']
    states = fsm['states']
    n = 0
    result = ''
    m = len(line)
    while n < m:
        c = line[n]
        if c not in states:
            result += c
            current = fsm['start']
            n += 1
            continue
        nbest = 0
        best_fe = None
        for isub in states[c]:
            fe = fsm_entries[isub]
            if current not in fe['starts']:
                continue
            nmatch = _match_len(line, n, m, fe)
            if nmatch > nbest:  # strictly greater: earliest entry wins ties
                nbest = nmatch
                best_fe = fe
        if best_fe is not None:
            result += best_fe['out']
            n += nbest
            current = best_fe['next']
        else:
            result += c
            current = fsm['start']
            n += 1
    return result


def transcoder_processString(line, from1, to):
    if from1 == to:
        return line
    loaded = _load(from1 + '_' + to)
    if loaded is None:
        return line  # legacy: missing table -> silent passthrough
    kind, obj = loaded
    if kind == 'stateless':
        return _translit_stateless(line, obj)
    return _translit_stateful(line, obj)


_transcoder_from = None
_transcoder_to = None


def _elements_callback(match):
    return transcoder_processString(match.group(1), _transcoder_from,
                                    _transcoder_to)


def transcoder_processElements(line, from1, to, tagname):
    global _transcoder_from, _transcoder_to
    _transcoder_from = from1
    _transcoder_to = to
    regex = '<%s>(.*?)</%s>' % (tagname, tagname)
    return re.sub(regex, _elements_callback, line)
