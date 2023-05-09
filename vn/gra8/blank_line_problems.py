#-*- coding:utf-8 -*-
"""blank_line_problems.py
"""
from __future__ import print_function
import sys, re,codecs

def nonblank_outside_lend(lines):
 inentry = None
 first = True
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   inentry = True
   first = False
  elif line.startswith('<LEND>'):
   inentry = False
   nblank = 0 
  elif line.strip() == '':
   if first:
    continue
   # blank line.
   if not inentry:
    nblank = nblank + 1
    if nblank > 1:
     print(iline+1)
     
if __name__=="__main__": 
 filein = sys.argv[1] #  temp_gra_9
 #fileout = sys.argv[2] # 

 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"read from",filein)

 nonblank_outside_lend(lines)
 exit(1)
 
 newlines = change_lines(lines1,lines2)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for line in newlines:
   f.write(line + '\n')
 print(len(newlines),"written to",fileout)
 
