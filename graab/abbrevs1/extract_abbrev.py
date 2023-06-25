# coding=utf-8
""" extract_abbrev.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Glab(object):
 def __init__(self,line):
  abbrev,data = line.split('\t')
  m = re.search(r'^<id>(.*?)</id> <disp>(.*?)</disp>$',data)
  if m == None:
   print('Glab: cannot parse',line)
  self.abbrev = abbrev
  assert self.abbrev == m.group(1)
  self.tip = m.group(2)
  
def init_global_abbrevs(filein):
 lines = read_lines(filein)
 recs = []
 d = {}
 ndup = 0
 for iline,line in enumerate(lines):
  if line.startswith(';'):
   continue # skip comment line
  rec = Glab(line)
  if rec.abbrev in d:
   print('WARNING: global duplicate at line %s in %s',(iline+1,filein))
   ndup = ndup + 1
  else:
   d[rec.abbrev] = rec
   recs.append(rec)
 s = '  (%s duplicates)' % ndup
 print(len(recs),"global abbreviations read from",filein,s)
 return d

def update_dall(line,regex,tag,abtype,d,dglab):
 # update dictionary d
 noglob = 0  # number of global abbreviations not in dglab
 for m in re.finditer(regex,line):
  if abtype == 'global':
   abbrev = m.group(1)
   if abbrev not in dglab:
    noglob = noglob + 1
    tip = 'NO TIP??'
   else:
    glab = dglab[abbrev]
    tip = glab.tip
  elif abtype == 'local':
   tip = m.group(1)
   abbrev = m.group(2)
  else:
   print('ERROR update_dall',abtype)
   exit(1)
  instance = (abbrev,tip,tag,abtype)
  if instance not in d:
   d[instance] = 0
  d[instance] = d[instance] + 1

def get_regex(tab,abtype):
 if abtype == 'local':
  attrib = ' n="(.*?)"'
 else:
  attrib = ''
 regex = r'<%s%s>(.*?)</%s>' %(tag,attrib,tag)
 #print(tag,abtype,regex)
 return regex

def write(fileout,d):
 # sort on abbreviation, case-insensitive
 instances = sorted(d.keys(),key = lambda instance : instance[0].lower())
 outarr = []
 for instance in instances:
  count = d[instance]
  (abbrev,tip,tag,abtype) = instance
  a = (tag,abtype,abbrev,str(count),tip)
  out = '\t' . join(a)
  outarr.append(out)

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(instances),"lines written to",fileout)

def note(dall,tags,abtypes):
 instances = dall.keys()
 for tag0 in tags:
  for abtype0 in abtypes:
   d = {}
   for instance in instances:
    (abbrev,tip,tag,abtype) = instance
    if (tag == tag0) and (abtype == abtype0):
     if abbrev not in d:
      d[abbrev] = True
   abbrevs = d.keys()
   print("%03d %s,%s" % (len(abbrevs),tag0,abtype0))
 
if __name__=="__main__":
 filein = sys.argv[1] # temp_graab_x.txt
 filein1 = sys.argv[2] # graab_input (global abbreviation tips)
 fileout = sys.argv[3] # abbreviations with tooltips and counts
 lines = read_lines(filein)
 dglab = init_global_abbrevs(filein1)
 tags = ('ab','pe','lang')
 abtypes = ('local','global')
 dall = {}
 for tag in tags:
  for abtype in abtypes:
   regex = get_regex(tag,abtype)
   for line in lines:
    update_dall(line,regex,tag,abtype,dall,dglab)
 write(fileout,dall)
 note(dall,tags,abtypes)

 
 
