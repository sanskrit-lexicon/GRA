#-*- coding:utf-8 -*-
"""quote_counts.py
"""
from __future__ import print_function
import sys, re,codecs

DLQM = u'„' # DOUBLE LOW-9 QUOTATION MARK
LDQM = u'“' # LEFT DOUBLE QUOTATION MARK

class Count(object):
 def __init__(self,iline,line):
  self.lnum = iline+1
  a = re.findall(DLQM,line)
  b = re.findall(LDQM,line)
  self.DLQM = len(a)
  self.LDQM = len(b)
  self.equal = (self.DLQM == self.LDQM)

def count_quotes(lines):
 counts = []
 for iline,line in enumerate(lines):
  count = Count(iline,line)
  if count.equal:
   continue
  else:
   counts.append(count)
 print(len(counts),'quote character mismatches')
 return counts

if __name__=="__main__": 
 filein = sys.argv[1] # 
 fileout = sys.argv[2] # 

 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 print(len(lines),"read from",filein)
 counts = count_quotes(lines)

 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for count in counts:
   out = '%s: %s %s != %s %s' %(count.lnum,DLQM,count.DLQM,LDQM,count.LDQM)
   f.write(out + '\n')
 print(len(counts),"written to",fileout)
 
