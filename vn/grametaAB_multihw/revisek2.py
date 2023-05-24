#-*- coding:utf-8 -*-
"""revisek2.py
"""
from __future__ import print_function
import sys, re,codecs
import transcoder
transcoder.transcoder_set_dir('transcoder')

slp1chars = {}
def update_slp1chars(x,y,tranin,tranout):
 if not ((tranin == 'roman') and (tranout == 'slp1')):
  return
 m = re.search(r"^[a-zA-Z|~/\\^— √°'+.,;=?\[\]\(\)!‘’-]*$",y)
 if m == None:
  print('Unexpected character in line #%s' % (iline+1,))
  print(' x=',x)
  print(' y=',y)
 return
 
def convert(line,tranin,tranout):
 # convert text  in '<s>X</s>'
 tagname = 's'
 def f(m):
  x = m.group(1)
  parts = re.split(r'(<.*?>)',x)
  newparts = []
  for part in parts:
   if part == None:
    newpart = ''
   elif part.startswith('<'):
    newpart = part
   else:
    #newpart = transcoder.transcoder_processString(part,tranin,tranout)
    newpart = transcode(part,tranin,tranout)
   newparts.append(newpart)
  y = ''.join(newparts)
  return '<s>%s</s>' % y

 regex = '<s>(.*?)</s>'
 #lineout = transcoder.transcoder_processElements(line,tranin,tranout,tagname)
 lineout = re.sub(regex,f,line)
 return lineout

def print_unicode(x,u):
 """ Sample output:
x= a/MSa—BU/
0905 | अ | DEVANAGARI LETTER A
 """
 import unicodedata
 outarr = []
 for c in u:
  name = unicodedata.name(c)
  icode = ord(c)
  a = f"{icode:04X} | {c} | {name}"
  outarr.append(a)
 print('x=',x)
 for out in outarr:
  print(out)
 print()

def transcode(x,tranin,tranout):
 y = transcoder.transcoder_processString(x,tranin,tranout)
 #if True and (('|' in x) or ('Q' in x)):
 if False and ('~' in x):  # for debugging.
  print_unicode(x,y)
 update_slp1chars(x,y,tranin,tranout)
 return y

class Rec(object):
 def __init__(self,line):
  self.line = line
  self.meta,self.head = line.split('\t')
  self.bolds = re.findall(r'{@.*?@}',line)
  self.newmeta = None
  self.warning = False
  
newk2_replacements = [
  ('{@',''),
  ('@}',''),
  (',',''),
  ('.',''),
  ('√',''),
  ('(',''),
  (')',''),
  ('[',''),
  (']',''),
]
def make_newk2(x):
 for old,new in newk2_replacements:
  x = x.replace(old,new)
 # transcode
 y = transcoder.transcoder_processString(x,'roman1','slp1')
 return y

def insert_newk2s(oldmeta,allk2s):
 meta = oldmeta
 if '<h>' not in meta:
  # makes parsing easier. will remove <h>0 as last step
  meta = '%s<h>0' % oldmeta 
 m = re.search(r'<k2>(.*?)<h>',meta)
 oldk2 = m.group(1)
 meta1 = re.sub(r'<k2>(.*?)<h>','<k2><h>',meta)
 oldk2s = oldk2.split(', ') 
 if (allk2s[0] != oldk2s[0]):
  print('insert_newk2s warning',oldmeta)
  warning = True
 else:
  warning = False
 newk2 = ', '.join(allk2s)
 newmeta = meta1.replace('<k2><h>','<k2>%s<h>' % newk2)
 #newmeta = re.sub(r'<k2>(.*?)<','<k2>%s<' %newk2,meta)
 # remove <h>0 if present
 newmeta = newmeta.replace('<h>0','')
 return newmeta,warning

def make_newmeta(rec):
 if len(rec.bolds) == 1:
  return
 allk2s = []
 for bold in rec.bolds:
  allk2s.append(make_newk2(bold))
 rec.newmeta,rec.warning = insert_newk2s(rec.meta,allk2s)
 
def check_1(recs):
 d = {}
 for rec in recs:
  n = len(rec.bolds)
  if n not in d:
   d[n] = 0
  d[n] = d[n] + 1
 for n in d:
  print(n,d[n])

def write_changes(fileout,recs):
 outrecs = []
 nwarning = 0
 for irec,rec in enumerate(recs):
  if rec.newmeta == None:
   continue
  outarr = []
  lnum = irec+1
  old = rec.line
  new = '%s\t%s' %(rec.newmeta,rec.head)
  if rec.warning:
   outarr.append(';Warning please check')
   nwarning = nwarning + 1
  outarr.append('%s old %s' %(lnum,old))
  outarr.append('%s new %s' %(lnum,new))
  outarr.append(';')
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"changes written to file",fileout)
 print(nwarning,"warnings to check")
 
if __name__=="__main__":
 tranin = 'slp1'
 tranout = 'roman'
 filein = sys.argv[1] #  
 fileout = sys.argv[2] # 
 
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Rec(x.rstrip('\r\n')) for x in f]
 print(len(recs),"lines read from",filein)
 check_1(recs)
 for rec in recs:
  make_newmeta(rec)
 write_changes(fileout,recs)

