# coding=utf-8
""" global_ab.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def change_lines(lines,dtips):
 newlines = []
 nchg = 0
 def f(m):
  x = m.group(0)
  tip = m.group(1)
  abbrev = m.group(2)
  if abbrev in dtips:
   rec = dtips[abbrev]
   tip0 = rec.tip
   if tip == tip0:
    y = "<ab>%s</ab>" % abbrev
    rec.n = rec.n + 1
   else:
    y = x
  else:
   y = x
  return y
 for line in lines:
  newline = re.sub(r'<ab n="(.*?)">(.*?)</ab>',f,line)
  if newline != line:
   nchg = nchg + 1
  newlines.append(newline)
 print('change_lines: %s lines changed' %nchg)
 return newlines

class Tip(object):
 def __init__(self,line):
  self.abbrev,self.tip,self.count = line.split(':')
  self.count = int(self.count)
  self.n = 0  # observed
  
def init_abbrevs(filein):
 lines = read_lines(filein)
 recs = [Tip(line) for line in lines]
 print(len(recs),"abbreviations read from",filein)
 d = {}
 for rec in recs:
  abbrev = rec.abbrev
  if abbrev in d:
   print('init_abbrev: eunexpected duplicate',abbrev)
  d[abbrev] = rec
 return recs,d

def write_lines(fileout,lines):
 outarr = lines
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)

def check(recs):
 nprob = 0
 print('checking global abbreviations')
 for rec in recs:
  if rec.count != rec.n:
   print('Problem: %s:%s:%s:%s' %(rec.abbrev,rec.tip,rec.count,rec.n))
   nprob = nprob + 1
 print("  ",nprob,"problems with abbreviations")
 
if __name__=="__main__":
 filein = sys.argv[1] # temp_graab_OLD.txt
 filein1 = sys.argv[2] # extract_abbrev.txt
 fileout = sys.argv[3] # temp_graab_NEW.txt
 lines = read_lines(filein)
 print(len(lines),"from",filein)
 recs,recsd = init_abbrevs(filein1)
 newlines = change_lines(lines,recsd) #
 write_lines(fileout,newlines)
 check(recs)
 
