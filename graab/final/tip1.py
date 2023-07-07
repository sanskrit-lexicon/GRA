# coding=utf-8
""" tip1.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,line):
  self.line = line
  self.ls,self.tip = line.split('\t')
  self.type = None
  
def init_tips(filein):
 lines = read_lines(filein)
 recs = [Tip(line) for line in lines]
 print(len(recs),"Tip records read from",filein)
 return recs

def write_tips(fileout,tips):
 tips1 = sorted(tips,key = lambda tip: tip.ls)
 with codecs.open(fileout,"w","utf-8") as f:
  for tip in tips1:
   out = tip.line
   f.write(out+'\n')
 print(len(tips),"records written to",fileout)

def tiptype(tips):
 for tip in tips:
  if 'Ku' in tip.ls:
   tip.type = 0
  elif 'Zeitschr.' == tip.ls:
   tip.type = 0
  else:
   tip.type = 1

def init_ktips(filein):
 # kuhn1a
 lines = read_lines(filein)
 lsbases = []
 for line in lines:
  m = re.search(r'^([0-9][0-9]) (.*)$',line)
  if m:
   lsbases.append(m.group(2))
 return lsbases

def compare(tipbases,ktipbases):
 print("bases from tips SAME AS bases from kuhn file? ",(tipbases == ktipbases))
 print('%s tipbases, %s ktipbases' % (len(tipbases), len(ktipbases)))
 a = set(tipbases)
 b = set(ktipbases)
 c = a.intersection(b)
 print('%s tip bases match' % len(c))
 for x in a.difference(b):
  print('%s in tipbases only' % x)

 for x in b.difference(a):
  print('%s in kuhn1a bases only' % x)

if __name__=="__main__":
 filein = sys.argv[1]  # tooltip file
 filein1 = sys.argv[2] # kuhn1a file
 tips = init_tips(filein)
 tipbases = [rec.ls for rec in tips]
 ktipbases = init_ktips(filein1)

 compare(tipbases,ktipbases)

 


