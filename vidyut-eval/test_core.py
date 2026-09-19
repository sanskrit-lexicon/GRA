# -*- coding:utf-8 -*-
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
from run_eval import vidyut_core

BS = chr(92)
cases = [
    ('BU', 'BU'),
    ('zu' + BS + 'Y', 'zu'),
    ('qudA' + BS + 'Y', 'dA'),
    ('va' + BS + 'ha~^', 'vah'),
    ('Ra' + BS + 'ma~', 'Ram'),
    ('puwi~', 'puw'),
    ('kfpU~' + BS, 'kfp'),
    ('De' + BS + 'w', 'De'),
    ('asa~', 'as'),
    ('tusa~', 'tus'),
    ('vadi~' + BS, 'vad'),
    ('syandU~' + BS, 'syand'),
    ('DmA' + BS, 'DmA'),
    ('eDa~' + BS, 'eD'),
    ('qukf~Y', 'kf'),
    ('sPura~', 'sPur'),
]
bad = 0
for d, want in cases:
    got = vidyut_core(d)
    ok = got == want
    bad += not ok
    print(('OK ' if ok else 'BAD'), repr(d), '->', got, '(want %s)' % want)
print('FAILURES:', bad)
