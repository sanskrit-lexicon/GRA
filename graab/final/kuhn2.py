# coding=utf-8
""" kuhn2.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Tip(object):
 def __init__(self,line):
  self.line = line
  self.abbrev,self.tip = line.split('\t')

class Kuhn(object):
 def __init__(self,line):
  self.line = line
  parts = line.split('|')
  assert len(parts) == 3
  self.lsbase = parts[0].strip()
  self.lsparm = parts[1].strip()
  self.article = parts[2].strip()
  
def generate_basegroups(lines):
 for iline,line in enumerate(lines):
  m = re.search(r'^([0-9][0-9]) (.*?)$',line)
  if m:
   if iline != 0:
    yield group
   group = []
  else:
   group.append(line)
 yield group
 
def init_ktips(filein):
 lines = read_lines(filein)
 basegroups = generate_basegroups(lines)
 basegroups = list(basegroups)
 print(len(basegroups),'base groups from',filein)
 return basegroups

def grouptips(group):
 recs = [Kuhn(line) for line in group]
 # check lsbase same for all recs
 lsbaseset = set([rec.lsbase for rec in recs])
 assert len(lsbaseset) == 1
 lsbases = list(lsbaseset)
 lsbase = lsbases[0]
 # print('grouptips check',lsbase)
 articleset = set([rec.article for rec in recs])
 if len(articleset) == 1:
  articles = list(articleset)
  article = articles[0]
  abbrev = lsbase
  article1 = article.replace('—','&#10;—')
  tipline = '%s\t%s' % (abbrev,article1)
  tip = Tip(tipline)
  tips = [tip]
 else:
  tips = []
  for rec in recs:
   lsparm = rec.lsparm
   article = rec.article
   lsparm1 = re.sub(r'[〔〕]','',lsparm)
   abbrev = '%s %s' %(lsbase,lsparm1)
   article1 = article.replace('—','&#10;—')
   tipline = '%s\t%s' % (abbrev,article1)
   tip = Tip(tipline)
   tips.append(tip)
 print('%s tips for base=%s' %(len(tips),lsbase))
 return tips

def write_tips(fileout,tips):
 #tips1 = sorted(tips,key = lambda tip: tip.ls)
 with codecs.open(fileout,"w","utf-8") as f:
  nout = 0
  for gtips in tips:
   for tip in gtips:
    out = tip.line
    f.write(out+'\n')
    nout = nout + 1
 print(nout,"records written to",fileout)



if __name__=="__main__":
 filein = sys.argv[1]  # kuhn1a file
 fileout = sys.argv[2] # new tooltip_1_ku file
 basegroups = init_ktips(filein)
 tips = [grouptips(group) for group in basegroups]
 write_tips(fileout,tips)

 


