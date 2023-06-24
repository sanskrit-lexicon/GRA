# coding=utf-8
""" make_graauth_tooltip_2.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,line):
  parts = line.split('\t:')
  if len(parts) != 3:
   print('error: line\n',parts)
   exit(1)
  self.abbrev,self.tip,self.count = parts
  self.count = int(self.count)
 
def init_abbrevs(filein):
 lines = read_lines(filein)
 recs = [Tip(line) for line in lines if not line.startswith(';')]
 print(len(recs),"abbreviations read from",filein)
 d = {}
 for rec in recs:
  abbrev = rec.abbrev
  if abbrev in d:
   print('init_abbrev: unexpected duplicate',abbrev)
  d[abbrev] = rec
 return recs,d

def write_abbrevs(fileout,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []
 for abbrev in abbrevs:
  rec = d[abbrev]
  tip = rec.tip
  if tip == '':
   tip = '?'
  # format of CDSL auth tooltip file
  # X\tTIP
  out = '%s\t%s' %(abbrev,tip)
  outarr.append(out)

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1]  # ls abbreviations with tooltips and counts
 fileout = sys.argv[2] # tooltip file for csl-pywork
 recs,d = init_abbrevs(filein)
 write_abbrevs(fileout,d)
 
