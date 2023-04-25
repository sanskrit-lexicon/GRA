#-*- coding:utf-8 -*-
"""diffexamine2.py
"""
from __future__ import print_function
import sys, re,codecs


def adjustlines1(lines1):
 ans = []
 for line in lines1:
  x = line
  # one space around '::AB::'
  x = re.sub(r' +::AB:: +', ' ::AB:: ',x)
  ans.append(x)
 return ans

def adjustlines2(lines2):
 ans = []
 for line in lines2:
  x = line
  # one space around '::AB::'
  x = re.sub(r' +::AB:: +', ' ::AB:: ',x)
  # remove {} around numbers
  x = re.sub(r'\{([0-9])',r'\1',x)
  x = re.sub(r'([0-9])\}',r'\1',x)
  # {@X@} -> <b>X</b>
  x = x.replace('{@','<b>')
  x = x.replace('@}','</b>')
  # {%X%} -> <i>X</i>
  x = x.replace('{%','<i>')
  x = x.replace('%}','</i>')
  ans.append(x)
 return ans

def write(fileout,lines1a,lines2a):
 outrecs = []
 for i,x1 in enumerate(lines1a):
  x2 = lines2a[i]
  x2 = x2.replace(' ::AB:: ',' ')
  if x1 == x2:
   continue
  outarr = []
  lnum = i+1
  outarr = []
  outarr.append('%s old %s' %(lnum,x1))
  outarr.append('%s new %s' %(lnum,x2))
  outarr.append('')
  outrecs.append(outarr)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out + '\n')
 print(len(outrecs),"remaining differences written to",fileout)
 

if __name__=="__main__": 
 filein1 = sys.argv[1] #  vn3_1.txt
 filein2 = sys.argv[2] #  vn3.1_AB.updated_ejf.txt
 fileout = sys.argv[3] # 

 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  lines1 = [line.rstrip('\r\n') for line in f]
 print(len(lines1),"read from",filein1)

 with codecs.open(filein2,encoding='utf-8',mode='r') as f:
  lines2 = [line.rstrip('\r\n') for line in f]
 print(len(lines2),"read from",filein2)
 
 lines2a = adjustlines2(lines2)
 lines1a = adjustlines1(lines1)
 write(fileout,lines1a,lines2a)
