# coding=utf-8
""" extract_ls_local.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,abbrev,tip,lnum,line):
  self.abbrev = abbrev
  self.alltips = []
  self.alltips.append(tip)
  self.tip = tip
  self.lnum = lnum
  self.count = 0
 

def init_abbrevs(filein):
 lines = read_lines(filein)
 regex = re.compile(r'<ls ab="(.*?)">(.*?)</ls>')
 d = {}
 for iline,line in enumerate(lines):
  for m in re.finditer(regex,line):
   tip,abbrev = m.group(1),m.group(2)
   lnum = iline+1
   if abbrev not in d:
    rec = Tip(abbrev,tip,lnum,line)
    d[abbrev] = rec
   rec = d[abbrev]
   if tip != rec.tip:
    print("tip inconsistency abbrev=",abbrev)
   rec.count = rec.count + 1
   if "'" in tip:  # should not happen:
    print("\nWARNING: line %s has apostrophe in tip at abbrev '%s'\n"% (lnum,abbrev))
 return d

def write_abbrevs(fileout,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []
 for abbrev in abbrevs:
  rec = d[abbrev]
  tip = rec.tip
  if tip == '':
   tip = '?'
   print('WARNING: abbrev=%s  No tooltip' % abbrev)
  count = rec.count
  # format of extract_ls1_AB.txt
  #out = '%s\t%s' %(abbrev,tip)
  out = '\t:' .join([abbrev,tip,str(count)])
  outarr.append(out)

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)

def write_dups(d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []
 for abbrev in abbrevs:
  rec = d[abbrev]
  alltips = rec.alltips
  if len(alltips) == 1:
   continue
  print("%s : abbreviation has %s tips" %(rec.abbrev,len(alltips)))
  alltips = sorted(alltips)
  for tip in alltips:
   print("  tip:",tip)
  print()
    
if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 fileout = sys.argv[2] # local tooltip file for csl-pywork
 d = init_abbrevs(filein)
 write_abbrevs(fileout,d)
 write_dups(d)

