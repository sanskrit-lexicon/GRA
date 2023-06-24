# coding=utf-8
""" make_change_bollensen.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Change(object):
 def __init__(self,lnum,line,metaline,newline,replaced):
  self.lnum = lnum
  self.line = line
  self.metaline = metaline 
  self.newline = newline
  self.replaced = replaced

replacements = [
  ('<ls>Bollensen</ls>',
   '<ls ab="Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident">Bollensen</ls>'),
  ('<ls ab="Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident">Bollensen&#xA0;</ls>',
   '<ls ab="Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident">Bollensen</ls>'),
 ('<ls>Bollens.</ls>',
   '<ls ab="Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident">Bollens.</ls>'),
 ('<ls>Boll.</ls>',
   '<ls ab="Zur Herstellung des Veda.— Bollensenʼs Article in Orient und Occident">Boll.</ls>'),

 ('<ls>Ku. in Zeitschr.</ls>',
  '<ls ab="Ueber des alte S und einige damit verbundene lautentwicklungen (5ter artikel)— Kuhnʼs Article in Kuhnʼs Zeitschrift">Ku. in Zeitschr.</ls>'),

 ('in  JRAS', # extra space
  'in JRAS'),

 ('<ls>Iliad, Homer</ls>',
  '<ls>Iliad— Homer</ls>'),

 
  ]

def get_newline(line):
 newline = line
 replaced = []
 for a,b in replacements:
  newline1 = newline.replace(a,b)
  if newline1 != newline:
   replaced.append((a,b))
  newline = newline1
 return newline,replaced

def init_changes(filein):
 lines = read_lines(filein)
 changes = []
 metaline = None
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   continue
  newline,replaced = get_newline(line)
  if newline != line:
   lnum = iline+1
   change = Change(lnum,line,metaline,newline,replaced)
   changes.append(change)
 return changes

def write_changes(fileout,changes):
 # generate change transactions
 outrecs = []
 outarr = [] # title
 outarr.append('; ************************************************')
 outarr.append('; Bollensen local abbreviation. (%s changes)' % len(changes))
 outarr.append('; ************************************************')
 outrecs.append(outarr)
 for change in changes:
  outarr = []
  outarr.append('; ----------------------------------------------------')
  meta = re.sub(r'<k2>.*$','',change.metaline)
  outarr.append('; %s' % meta)
  replaced = change.replaced
  for i,replacement in enumerate(replaced):
   a,b = replacement
   outarr.append('; Replacement %s of %s' %(i+1,len(replaced)))
   outarr.append(';   old: %s' % a)
   outarr.append(';   new: %s' % b)
  lnum = change.lnum
  old = change.line
  new = change.newline
  outarr.append('%s old %s' %(lnum,old))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,new))
  outrecs.append(outarr)
 #
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),"changes written to",fileout)

    
if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 fileout = sys.argv[2] # 
 changes = init_changes(filein)
 write_changes(fileout,changes)


