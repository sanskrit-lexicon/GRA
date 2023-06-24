# coding=utf-8
""" check_ls_global_local.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,abbrev,tip):
  self.abbrev = abbrev
  self.tip = tip
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

class TipRead(object):
 def __init__(self,line):
  try:
   (self.abbrev,self.tip,self.count) = line.split('\t:')
  except:
   print('TipRead error')
   print(line)
   exit(1)
  self.count = int(self.count)
 
def init_tipread(filein):
 lines = read_lines(filein)
 recs = [TipRead(line) for line in lines if not line.startswith(';')]
 print(len(recs),"TipRead records from",filein)
 return recs

def check_tipread_dups(recs,name):
 d = {}
 ndup = 0
 for rec in recs:
  abbrev = rec.abbrev
  if abbrev in d:
   print('WARNING: %s: dup=%s' %(name,abbrev))
   ndup = ndup + 1
   prevrec = d[abbrev]
   print('prev tip: (%s) %s' % (prevrec.count,prevrec.tip))
   print('cur  tip: (%s) %s' % (rec.count,rec.tip))
   print()
  else:
   d[abbrev] = rec
 print('%s abbrev dups %s' %(ndup,name))

def globals_count_from_graab(filein):
 lines = read_lines(filein)
 d = {}
 for line in lines:
  for m in re.finditer(r'<ls>(.*?)</ls>',line):
   abbrev = m.group(1)
   if abbrev.startswith('AV.'):
    abbrev = 'AV.'
   if abbrev not in d:
    d[abbrev] = 0 # count
   d[abbrev] = d[abbrev] + 1
 return d

def check_global(dglobals,globals):
 # compare d[abbrev] with count of globals
 for tipread in globals:
  gcount = tipread.count
  abbrev = tipread.abbrev
  if abbrev not in dglobals:
   print('WARNING: global abbrev not used: %s' % abbrev)
  else:
   count = dglobals[abbrev]
   if count != gcount:
    print('WARNING: abbrev: %s readcount count %s != tipread count %s' %(abbrev,count,gcount))
 # check same sets of abbreviations
 set1 = set(dglobals.keys())
 set2 = set([tipread.abbrev for tipread in globals])
 print(set1 == set2," compare set1 and set2")
 print("set1 - set2 = ",set1.difference(set2))
 print("set2 - set1 = ",set2.difference(set1))
 for abbrev in set1.difference(set2):
  tip = '?'
  count = dglobals[abbrev]
  out = '\t:'.join([abbrev,tip,str(count)])
  print(out)
  
if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 filein1 = sys.argv[2] # local ls tooltip file 
 filein2 = sys.argv[3] # global ls tooltip file
 locals = init_tipread(filein1)
 globals = init_tipread(filein2)
 check_tipread_dups(locals,'local')
 check_tipread_dups(globals,'global')
 all = locals + globals
 check_tipread_dups(all,'local+global')
 #
 global_count_d = globals_count_from_graab(filein)
 check_global(global_count_d,globals)
 exit(1)
 d = init_abbrevs(filein)
 
 write_abbrevs(fileout,d)
 write_dups(d)

