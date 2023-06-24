# coding=utf-8
""" ls_local_nonunique.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,abbrev,tip,lnum,line,metaline):
  self.abbrev = abbrev
  self.tip = tip
  self.lnum = lnum
  self.line = line
  self.metaline = metaline 

def init_abbrevs(filein):
 lines = read_lines(filein)
 regex = re.compile(r'<ls ab="(.*?)">(.*?)</ls>')
 d = {}
 metaline = None
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   continue
  for m in re.finditer(regex,line):
   tip,abbrev = m.group(1),m.group(2)
   lnum = iline+1
   if abbrev not in d:
    d[abbrev] = []
   rec = Tip(abbrev,tip,lnum,line,metaline)
   d[abbrev].append(rec)
 return d

def write_change_multitip(fileout,d):
 d1 = {}
 nchg = 0 # total number of change records written
 for abbrev in d:
  tiprecs = d[abbrev]  # list of Tip objects with given abbrev
  dtip = {}
  for tiprec in tiprecs:
   tip = tiprec.tip
   if tip not in dtip:
    dtip[tip] = []
   dtip[tip].append(tiprec)
  tipvals = list(dtip.keys())
  if len(tipvals) == 1:
   # only 1 tip value. not interested in this case
   continue
  d1[abbrev] = dtip
 #
 d1keys = sorted(d1.keys())
 # generate change transactions
 outrecs = []
 for abbrev in d1keys:
  outarr = []
  dtip = d1[abbrev]
  tipvals = list(dtip.keys())
  # 
  tipvals1 = sorted(tipvals,key = lambda tip: len(dtip[tip]), reverse=True)
  outarr.append('; ****************************************************')
  outarr.append('; abbrev=%s has %s tooltips' %(abbrev,len(tipvals1)))
  outarr.append('; ****************************************************')
  space = '&#xA0;'  # normal space, but in this 'htmlentity' form.
  spaceabbrev = ''
  for itip,tip in enumerate(tipvals1):
   outarr.append('; ----------------------------------------------------')
   tiprecs = dtip[tip]
   n = len(tiprecs)
   if itip != 0:
    spaceabbrev = spaceabbrev + space
   # print('%s::abbrev=%s::tip=%s' %(n,abbrev,tip))
   outarr.append('; %s instances of abbrev=%s, tooltip=%s' %(n,abbrev,tip))
   
   for tiprec in tiprecs:
    meta = re.sub(r'<k2>.*$','',tiprec.metaline)
    outarr.append('; %s' % meta)
    if itip == 0:
     outarr.append('; NO CHANGE at line %s' % tiprec.lnum)
    else:
     nchg = nchg + 1
     outarr.append('; old abbrev: %s' % abbrev)
     newabbrev = abbrev + spaceabbrev
     outarr.append('; new abbrev: %s' % newabbrev)
     lnum = tiprec.lnum
     old = tiprec.line
     new = old.replace('>%s<' % abbrev,'>%s<' %newabbrev)
     outarr.append('%s old %s' %(lnum,old))
     outarr.append(';')
     outarr.append('%s new %s' %(lnum,new))
  outrecs.append(outarr)
 #
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(nchg,"changes written to",fileout)


 exit(1)
 return d1

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
 fileout = sys.argv[2] # 
 d = init_abbrevs(filein)
 write_change_multitip(fileout,d)


