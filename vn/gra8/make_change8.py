#-*- coding:utf-8 -*-
"""make_change8.py
"""
from __future__ import print_function
import sys, re,codecs


class Correction(object):
 def __init__(self,line):
  self.line = line
  m = re.search(r'^<c ([0-9]+)> (<p>.*?): (.*?) +::AB:: +(.*)$',line)
  if m == None:
   print('make_dict2 skipping(1) %s' % line)
   self.status = False
   return
  
  self.cid = m.group(1)
  self.cwhere = m.group(2)
  self.new = m.group(3)
  old = m.group(4)
  if old.startswith('st. '):
   old1 = re.sub(r'^st\. +','',old)
  else:
   old1 = old
   print('no st.: %s old1=%s' %(self.cid,old1)) # dbg
  self.old = old1 
  self.status = True
  self.used = 0
  
def make_dict2(lines2):
 # <c 39> <p>101,10 v. u.: -ásā    ::AB:: st. -asā
 d = {}
 for iline,line in enumerate(lines2):
  if not line.startswith('<c '):
   continue
  correction = Correction(line)
  if not correction.status:
   continue
  d[correction.cid] = correction
 return d

def make_newline(line,d2):
 def changef(m):
  id = m.group(1)
  txt = m.group(2)
  old = txt
  if id in d2:
   tag = '<chg type="chg" n="%s" src="gra">' % id
   correction = d2[id]
   correction.used = correction.used + 1
   newelt = correction.new
   body = '<old>%s</old><new>%s</new>' %(old,newelt)
   new = '%s%s%s' %(tag,body,'</chg>')
   return new
 newline = re.sub(r'<c (.*?)>(.*?)</c>',changef,line)
 return newline 

def check_d2(d):
 # are any unused
 for id in d:
  correction = d[id]
  n = correction.used
  if n == 1:
   continue  # as expected
  print('check_d2: (%s) %s' %(n,correction.line))
  
def change_lines(lines1,lines2):
 ans = []
 d2 = make_dict2(lines2)
 for line1 in lines1:
  newline = make_newline(line1,d2)
  ans.append(newline)
 check_d2(d2)
 return ans

if __name__=="__main__": 
 filein1 = sys.argv[1] #  temp_gra_7
 filein2 = sys.argv[2] #  vn3_2
 fileout = sys.argv[3] # 

 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  lines1 = [line.rstrip('\r\n') for line in f]
 print(len(lines1),"read from",filein1)

 
 with codecs.open(filein2,encoding='utf-8',mode='r') as f:
  lines2 = [line.rstrip('\r\n') for line in f]
 print(len(lines2),"read from",filein2)
 
 newlines = change_lines(lines1,lines2)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for line in newlines:
   f.write(line + '\n')
 print(len(newlines),"written to",fileout)
 
