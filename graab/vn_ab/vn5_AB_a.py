# coding=utf-8
""" vn5_AB_a.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def change_lines(lines):
 newlines = []
 replacements = [
  (' st. ', ' <ab n="statt">st.</ab> '),
  (' v. u.:', ' <ab n="von unten">v. u.</ab>:'),
  ]
 counts = []
 for _ in replacements:
  counts.append(0)
 for line in lines:
  newline = line
  for i,replacement in enumerate(replacements):
   old,new = replacement
   newline1 = newline.replace(old,new)
   if newline1 != newline:
    counts[i] = counts[i] + 1
   newline = newline1
  newlines.append(newline)
 for i,replacement in enumerate(replacements):
  old,new = replacement
  n = counts[i]
  print("%s '%s' -> '%s'" % (n,old,new))
 return newlines

def write_lines(fileout,lines):
 outarr = lines
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1] # 
 fileout = sys.argv[2] # 
 lines = read_lines(filein)
 newlines = change_lines(lines) # 
 write_lines(fileout,newlines)
 
