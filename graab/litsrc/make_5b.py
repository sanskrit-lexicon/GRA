# coding=utf-8
""" make_5b.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_5b(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')
 print(len(lines),"lines written to",fileout)
 
def make_5b(lines):
 newlines = []
 n = 0
 for iline,line in enumerate(lines):
  newline = re.sub(r'<ls>AV.</ls> {([0-9]+,[0-9]+,[0-9]+)}',r'<ls>AV. \1</ls>',line)
  newlines.append(newline)
 return newlines

if __name__=="__main__":
 filein = sys.argv[1] # temp_graab
 fileout = sys.argv[2] # revised temp_graab
 lines = read_lines(filein)
 print(len(lines),"lines from",filein)
 newlines = make_5b(lines)
 write_5b(fileout,newlines)
 
