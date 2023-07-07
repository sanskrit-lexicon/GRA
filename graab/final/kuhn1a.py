# coding=utf-8
""" kuhn1a.py
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
   self.ident,self.lsraw,self.article = line.split('\t')
  except:
   print('Kuhn format error',line)
   exit(1)
  self.ls = re.sub(r'<ls n="(.*?)">',r'<ls>\1',self.lsraw)
  ls = self.ls
  m = re.search(r'^<ls>(.*?)</ls>$',self.ls)
  lsdata = m.group(1)
  self.lsdata = lsdata
  ## lsbase and param so ls = '<ls>B P</ls>'
  ## one kind: P = [X]  (twice)
  ## the other: P = 〔.*?〕
  m = re.search(r'^(.*) (\[.*\])$',lsdata)
  if m == None:
   m = re.search(r'<ls>(.*?) (〔.*?〕)',ls)
  if m != None:
   self.lsbase,self.lsparm = (m.group(1),m.group(2))
   self.lsparm = self.lsparm.replace('%%','')
  else:
   print('Kuhn rec cannot find lsbase, lsparm\nline=',self.line)

  
def init_kuhn(filein):
 lines = read_lines(filein)
 recs = [Kuhn(line) for line in lines]
 print(len(recs),"Kuhn records read from",filein)
 return recs

def write_recs(fileout,recs):
 # alphabetical by base
 dbase = {}
 for rec in recs:
  lsbase = rec.lsbase
  article = rec.article
  if lsbase not in dbase:
   dbase[lsbase] = []
  dbase[lsbase].append(rec)
 lsbases = list(dbase.keys())
 lsbases = sorted(lsbases)
 # prepare outrecs, one per lsbase
 outrecs = []
 for i,lsbase in enumerate(lsbases):  
  arecs = dbase[lsbase]
  outarr = []
  outarr.append('%02d %s' %(i+1,lsbase))
  arecs1 = sorted(arecs,key = lambda rec: rec.article)
  for rec in arecs1:
   lsbase = rec.lsbase
   lsparm = rec.lsparm
   article = rec.article
   lsbase1 = lsbase.ljust(25)
   lsparm1 = lsparm.ljust(15)
   out = '   %s | %s | %s' % (lsbase1,lsparm1,article)
   outarr.append(out)
  outrecs.append(outarr)
 # --------------------
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print("records written to",fileout)
 
def unused_write_recs(fileout,recs):
 d = {} # aggregate by article

 for rec in recs:
  a = rec.article
  if a not in d:
   d[a] = []
  d[a].append(rec)
 articles = list(d.keys())
 articles = sorted(articles)
 print(len(articles),"distinct articles")
 # associate a number with an article
 darticlenum = {}  
 for i,article in  enumerate(articles):
  darticlenum[article] = i+1
 #
 # aggregate recs by lsbase
 d1 = {}
 for rec in recs:
  lsbase = rec.lsbase
  article = rec.article
  if lsbase not in d1:
   d1[lsbase] = []
  articlenum = darticlenum[article]
  if articlenum not in d1[lsbase]:
   d1[lsbase].append(articlenum)
 ##
 lsbases = list(d1.keys())
 lsbases = sorted(lsbases)
 print(len(lsbases),'bases')
 print('BASES WITH ONE ARTICLE')
 for lsbase in lsbases:
  basearticlenums = d1[lsbase]
  if len(basearticlenums) == 1:
   print("%s : %s" %(lsbase,d1[lsbase]))
 print()
 print('BASES WITH MANY ARTICLES')
 for lsbase in lsbases:
  basearticlenums = d1[lsbase]
  if len(basearticlenums) != 1:
   print("%s : %s" %(lsbase,d1[lsbase]))

 exit(1)
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

 


