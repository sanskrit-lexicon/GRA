# coding=utf-8
""" make_5a.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_5a(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')
 print(len(lines),"lines written to",fileout)
 
def make_5a(lines):
 newlines = []
 n = 0
 for iline,line in enumerate(lines):
  newline = re.sub(r'<ls n="(.*?)">(.*?)</ls>',r'<ls>\2</ls>',line)
  newlines.append(newline)
 return newlines

if __name__=="__main__":
 filein = sys.argv[1] # temp_graab
 fileout = sys.argv[2] # revised temp_graab
 lines = read_lines(filein)
 print(len(lines),"lines from",filein)
 newlines = make_5a(lines)
 write_5a(fileout,newlines)
 
