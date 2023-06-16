# coding=utf-8
""" extract_lang.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_abbrevs(fileout,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []

 for abbrev in abbrevs:
  rec = d[abbrev]
  # repla
  out = '%s:%s:%s' %(abbrev,rec.tip,rec.count)
  outarr.append(out)
  
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)
 
def count_lang(lines,d):
 # updates d
 n = 0
 for iline,line in enumerate(lines):
  # 
  for m in re.finditer(r'<lang>(.*?)</lang>',line):
   abbrev = m.group(1)
   if abbrev not in d:
    print('count_lang: abbrev not found:%s at line %s' % (abbrev,iline+1))
   else:
    rec = d[abbrev]
    rec.count = rec.count + 1
    n = n + 1
 print(n,'lang tags found')
 
class Lang(object):
 def __init__(self,line):
  m =re.search('^<lang>(.*?)</lang>\t(.*)$',line)
  if m == None:
   print('Lang error:',line)
   exit(1)
  self.abbrev = m.group(1)
  self.tip = m.group(2)
  self.count = 0  # filled in later
  
def read_lang_tags(filein):
 lines = read_lines(filein)
 recs = [Lang(line) for line in lines]
 print(len(recs),"records parsed from",filein)
 d = {}
 for rec in recs:
  abbrev = rec.abbrev
  if abbrev in d:
   print('unexpected duplicate lang',abbrev)
   exit(1)
  d[abbrev] = rec
 return recs,d

if __name__=="__main__":
 filein = sys.argv[1] # temp_graab
 filein1 = sys.argv[2] # GRA.lang.tags...txt
 fileout = sys.argv[3] # abbreviations with tooltips and counts
 lines = read_lines(filein)
 print(len(lines),"lines from",filein)
 recs,dlang = read_lang_tags(filein1)
 count_lang(lines,dlang)
 write_abbrevs(fileout,dlang)
 
