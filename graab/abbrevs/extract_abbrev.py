# coding=utf-8
""" extract_abbrev.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_abbrevs_v1(fileout,d):
 abbrevs = sorted(d.keys())
 outarr = []
 ndup = 0
 for abbrev in d:
  da = d[abbrev]
  tips = list(da.keys())
  arr = []
  arr.append(abbrev)
  if len(tips) == 1:
   tip = tips[0]
   ntip = da[tip]
   arr.append(tip)
   arr.append('%s' % ntip)
  elif len(tips) == 2:
   ndup = ndup + 1
   # make first one more common
   if da[tips[0]] < da[tips[1]]:
    newtips = [tips[1],tips[0]]
    tips = newtips
   arr.append(tips[0])
   arr.append('%s' % da[tips[0]])
   arr.append('DUP: %s, %s' % (tips[1],da[tips[1]]))
  else:
   print('write_abbrevs UNEXPECTED: ',abbrev)
   arr.append('UNEXPECTED')
  out = '\t'.join(arr)
  outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)
 print(ndup,"abbrevs with 2 tooltips found. Marked 'DUP'")

def write_abbrevs_2(fileout,d):
 abbrevs = sorted(d.keys())
 outarr = []
 ndup = 0
 for abbrev in d:
  da = d[abbrev]
  tips = list(da.keys())
  arr = []
  arr.append(abbrev)
  tips = sorted(tips,key = lambda tip : da[tip],reverse=True)
  for itip,tip in enumerate(tips):
   ntip = da[tip]
   if itip == 0:
    arr.append(tip)
    arr.append('%s' % ntip)
   else:
    arr.append('(DUP)%s' %tip)
    arr.append('%s' % ntip)
  out = '\t'.join(arr)
  outarr.append(out)
  if len(tips) > 1:
   ndup = ndup + 1
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)
 print(ndup,"abbrevs with 2 tooltips found. Marked 'DUP'")

def write_abbrevs(fileout,filedup,d):
 abbrevs = sorted(d.keys(),key = lambda abbrev : abbrev.lower())
 outarr = []
 duparr = []
 ndup = 0
 for abbrev in abbrevs:
  da = d[abbrev]
  tips = list(da.keys())
  #arr = []
  #arr.append(abbrev)
  tips = sorted(tips,key = lambda tip : da[tip],reverse=True)
  for itip,tip in enumerate(tips):
   ntip = da[tip]
   out = '%s:%s:%s' %(abbrev,tip,ntip)
   if itip == 0:
    outarr.append(out)
   else:
    duparr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(abbrevs),"lines written to",fileout)
 with codecs.open(filedup,"w","utf-8") as f:
  for out in duparr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)
 print(len(duparr),"local abbrevs written to",filedup)

def get_abbrev_info(lines):
 d = {}
 for line in lines:
  # <ab n="T">A</ab>
  for m in re.finditer(r'<ab n="(.*?)">(.*?)</ab>',line):
   tip = m.group(1)
   abbrev = m.group(2)
   if abbrev not in d:
    d[abbrev] = {}  # another map
   da = d[abbrev]
   if tip not in da:
    da[tip] = 0
   da[tip] = da[tip] + 1
 return d
if __name__=="__main__":
 filein = sys.argv[1] # graab_input
 fileout = sys.argv[2] # abbreviations with tooltips and counts
 filedup = sys.argv[3] # local abbreviations
 lines = read_lines(filein)
 d = get_abbrev_info(lines) # dictionary
 write_abbrevs(fileout,filedup,d)
 
