# coding=utf-8
""" metak1.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines


def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')
 print(len(lines),"lines written to",fileout)

def get_metak1(lines):
 ans = []
 for line in lines:
  if line.startswith('<L>'):
   m = re.search(r'^<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>',line)
   L = m.group(1)
   k1 = m.group(3)
   metak1 = '<L>%s<k1>%s' %(L,k1)
   ans.append(metak1)
 return ans
if __name__=="__main__":
 filein = sys.argv[1] # version of metaline xxx.txt
 fileout = sys.argv[2] # 
 lines = read_lines(filein)
 metak1s = get_metak1(lines)
 write_lines(fileout,metak1s)
