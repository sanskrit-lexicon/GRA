# coding=utf-8
""" kuhn1.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Kuhn(object):
 def __init__(self,line):
  self.line = line
  try:
   self.ident,self.ls,self.article = line.split('\t')
  except:
   print('Kuhn format error',line)
   exit(1)
  
def init_kuhn(filein):
 lines = read_lines(filein)
 recs = [Kuhn(line) for line in lines]
 print(len(recs),"Kuhn records read from",filein)
 return recs




def write_recs(fileout,recs):
 d = {} # aggregate by article
 for rec in recs:
  a = rec.article
  if a not in d:
   d[a] = []
  d[a].append(rec)
 articles = list(d.keys())
 articles = sorted(articles)
 # -------------------
 outrecs = []
 for i,article in enumerate(articles):
  arecs = d[article]
  outarr = []
  outarr.append('%02d %s' %(i+1,article))
  arecs1 = sorted(arecs,key = lambda rec: rec.ls)
  for rec in arecs1:
   ls = rec.ls
   ls1 = re.sub(r'<ls n="(.*?)">',r'<ls>\1',ls)
   if ls1 == ls:
    outarr.append('  %s' % ls)
   else:
    outarr.append('  %s === %s' %(ls1,ls))
  outrecs.append(outarr)
 # --------------------
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print("records written to",fileout)


if __name__=="__main__":
 filein = sys.argv[1]  # kuhn articles
 fileout = sys.argv[2] #
 recs = init_kuhn(filein)
 
 write_recs(fileout,recs)
 exit(1)
 lines = read_lines(filein)
 instancesd = find_instances(lines)
 write_instances(fileout,instancesd)
 


