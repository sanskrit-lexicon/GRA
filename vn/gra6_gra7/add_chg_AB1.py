#-*- coding:utf-8 -*-
""" add_chg_AB1.py
"""
from __future__ import print_function
import sys, re,codecs


def make_changes(lines1,lines2):
 # replaces line2 with line1, for certain line1
 ans = [] 
 for i,line1 in enumerate(lines1):
  if '<c ' not in line1:
   continue
  line2 = lines2[i]
  lnum = i+1
  old = line2
  new = line1
  # remove <lbinfo from new
  new = re.sub(r' <lbinfo.*?/>','',new)

  change = (lnum,old,new)
  ans.append(change)
 return ans

def write_changes(fileout,changes):
 outrecs = []
 for change in changes:
  lnum,x1,x2 = change
  outarr = []
  outarr.append('%s old %s' %(lnum,x1))
  outarr.append('%s new %s' %(lnum,x2))
  outarr.append(';')
  outrecs.append(outarr)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out + '\n')
 print(len(outrecs),"changes written to",fileout)


if __name__=="__main__": 
 filein1 = sys.argv[1] #  temp_gra_6
 filein2 = sys.argv[2] #  temp_gra_.CSL._.AB1.txt
 fileout1 = sys.argv[3] # changes

 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  lines1 = [line.rstrip('\r\n') for line in f]
 print(len(lines1),"read from",filein1)

 with codecs.open(filein2,encoding='utf-8',mode='r') as f:
  lines2 = [line.rstrip('\r\n') for line in f]
 print(len(lines2),"read from",filein2)
 changes = make_changes(lines1,lines2)
 write_changes(fileout1,changes)
 
