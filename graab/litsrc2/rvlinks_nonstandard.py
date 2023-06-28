# coding=utf-8
""" rvlinks_nonstandard.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,abbrev,tip,lnum,line):
  self.abbrev = abbrev
  self.alltips = []
  self.alltips.append(tip)
  self.tip = tip
  self.lnum = lnum
  self.count = 0
 

def init_rvlinks(filein):
 lines = read_lines(filein)
 regex = re.compile(r'{[0-9].*?}')
 d = {}
 n = 0  # number of standard links {N,N}
 n1 = 0
 for iline,line in enumerate(lines):
  rvlinks = re.findall(regex,line)
  for rvlink in rvlinks:
   if re.search(r'^{[0-9]+,[0-9]+}$',rvlink):
    # standard
    n = n + 1
   else:
    # non-standard
    n1 = n1 + 1
    if rvlink not in d:
     d[rvlink] = 0
    d[rvlink] = d[rvlink] + 1
 print('%s standard rvlinks, %s non-standard' %(n,n1))
 n2 = len(list(d.keys()))
 print('%s distinct non-standard' % n2)
 return d

def write_rvlinks(fileout,d):
 rvlinks = sorted(d.keys())
 outarr = []
 for rvlink in rvlinks:
  n = d[rvlink]
  out = '%02d\t%s' %(n,rvlink)
  outarr.append(out)

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(rvlinks),"lines written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 fileout = sys.argv[2] # non-standard links
 d = init_rvlinks(filein)
 write_rvlinks(fileout,d)

