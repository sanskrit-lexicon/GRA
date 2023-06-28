# coding=utf-8
""" apply_reform.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Rvlink(object):
 def __init__(self,line):
  parts = line.split('\t')
  self.count,self.tag = parts[0].split(',')
  self.old = parts[1]
  if len(parts) == 3:
   self.new = parts[2]
  else:
   self.new = '?_%s' % self.old
   assert self.tag == '?'
  self.used = 0
  
def init_rvlinks(filein):
 lines = read_lines(filein)
 recs = [Rvlink(line) for line in lines]
 print('%s non-standard rvlinks read from %s' % (len(recs),filein))
 return recs

def init_rvlinks_dict(recs):
 d = {}
 for rec in recs:
  old = rec.old
  if old in d:
   print('unexpected duplicate rvlink:',old)
  d[old] = rec
 return d

def apply_reform(lines,dref):
 regex = re.compile(r'{[0-9].*?}')
 d = dref
 n = 0  # changed lines
 ans = []  # array of lines
 for iline,line in enumerate(lines):
  rvlinks = re.findall(regex,line)
  rvlinks_set = set(rvlinks)  # remove duplicates
  newline = line
  for rvlink in rvlinks_set:
   if rvlink in d:
    rec = d[rvlink]
    assert rec.old == rvlink
    new = rec.new
    # this rvlink could appear multiple times.
    newline1 = newline.replace(rvlink,new)
    if newline == newline1:
     print('anomaly. rvlink = %s, new = %s' % (rvlink,new))
     print(iline+1,' newline=',newline)
     exit(1)
    newline = newline1
    rec.used = rec.used + 1
  ans.append(newline)
  if newline != line:
   n = n + 1
 print('apply_reform changes %s lines' % n)
 return ans

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)

def check_used(rvlinks):
 n = 0
 for rec in rvlinks:
  if rec.used == 0:
   print('WARNING rvlink unused:',rec.old)
   n = n + 1
 print(n,'unused rvlinks')
 
if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 filein1 = sys.argv[2] # reform_1
 fileout = sys.argv[3] # non-standard links
 lines = read_lines(filein)
 print(len(lines),"read from",filein)
 rvlinks = init_rvlinks(filein1)
 d = init_rvlinks_dict(rvlinks)
 newlines = apply_reform(lines,d)
 
 write_lines(fileout,newlines)
 check_used(rvlinks)
