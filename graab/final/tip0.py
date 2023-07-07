# coding=utf-8
""" tip0.py
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
   if tip.ls in ['Kuhn in Haupt Zeitschr.', 'Ku. Beitr.']:
    tip.type = 1
   else:
    tip.type = 0
  elif tip.ls in ['Zeitschr.', 'J. Grimm', 'Lottner']:
   tip.type = 0
  else:
   tip.type = 1
   
if __name__=="__main__":
 filein = sys.argv[1]  # tooltip file
 fileout = sys.argv[2] # tooltip file
 fileout1 = sys.argv[3] # tooltip file

 tips = init_tips(filein)
 tiptype(tips)
 write_tips(fileout,[tip for tip in tips if tip.type == 0])
 write_tips(fileout1,[tip for tip in tips if tip.type == 1])

 


