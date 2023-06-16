# coding=utf-8
""" prepare_ls_tags.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_ls(fileout,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []

 for abbrev in abbrevs:
  count = d[abbrev]
  tip=""
  # repla
  out = '%s:%s:%s' %(abbrev,tip,count)
  outarr.append(out)
  
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)
 
def count_ls(lines):
 d = {}
 n = 0
 for iline,line in enumerate(lines):
  # 
  for m in re.finditer(r'<ls>(.*?)</ls>',line):
   abbrev = m.group(1)
   if abbrev not in d:
    d[abbrev] = 0
   d[abbrev] = d[abbrev] + 1
   n = n + 1
 abbrevs = list(d.keys())
 print(len(abbrevs),"global lang tags")
 print(n,'lang tag instances found')
 return d


def count_ls1(lines):
 d = {}
 n = 0
 for iline,line in enumerate(lines):
  # 
  for m in re.finditer(r'<ls n="(.*?)">(.*?)</ls>',line):
   abbrev = m.group(2)
   tip = m.group(1)
   if abbrev in d:
    rec = d[abbrev]
    rec.count = rec.count + 1
    if tip != rec.tip:
     print('count_ls1: warning',abbrev)
   else:
    rec = LS(abbrev,tip)
    rec.count = rec.count + 1
    d[abbrev] = rec
   n = n + 1
 abbrevs = list(d.keys())
 print(len(abbrevs),"local lang tags")
 print(n,'local lang tag instances found')
 return d

class LS(object):
 def __init__(self,abbrev,tip):
  self.abbrev = abbrev
  self.tip = tip
  self.count = 0  # filled in later

def write_ls1(fileout,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []

 for abbrev in abbrevs:
  rec = d[abbrev]
  tip = rec.tip
  count = rec.count
  out = '%s:%s:%s' %(abbrev,tip,count)
  outarr.append(out)
  
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] # temp_graab
 fileout = sys.argv[2] # <ls>X</ls>
 fileout1 = sys.argv[3] # <ls n="Y">x</ls>
 lines = read_lines(filein)
 print(len(lines),"lines from",filein)
 d = count_ls(lines)
 write_ls(fileout,d)
 d1 = count_ls1(lines)
 write_ls1(fileout1,d1)
 
