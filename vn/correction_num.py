#-*- coding:utf-8 -*-
"""correction_num.py
"""
from __future__ import print_function
import sys, re,codecs

def add_correction_nums(lines):
 N = 0  # sequence number of matched lines
 nchg = 0
 regex = re.compile(r'^<p>[0-9]+,[0-9]+')
 ans = []
 for line in lines:
  if re.search(regex,line):
   nchg = nchg + 1
   label = '<c %s>' % nchg
   newline = '%s %s' % (label,line)
  else:
   newline = line
  ans.append(newline)
 print(nchg,'lines labeled')
 return ans

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 fileout = sys.argv[2] # 

 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"read from",filein)
 newlines = add_correction_nums(lines)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for line in newlines:
   f.write(line + '\n')
 print(len(newlines),"written to",fileout)
 
