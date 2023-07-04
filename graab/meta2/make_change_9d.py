# coding=utf-8
""" make_change_9d.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Change(object):
 def __init__(self,lnum,line,metaline,newline):
  self.lnum = lnum
  self.line = line
  self.metaline = metaline 
  self.newline = newline
  #self.replaced = replaced

def get_newline(line):
 #newline = re.sub(r'<ls>([^<]*)</ls> (〔.*?〕)',r'<ls>\1 \2</ls>',line)
 newline = re.sub(r'</ls> (〔.*?〕)',  r' \1</ls>',line)
 # a few remain
 # newline = re.sub(r'〕([^<])',r'〕_\1',newline)
 return newline

def init_changes(lines):
 changes = []
 newlines = []
 metaline = None
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   newlines.append(line)
   continue
  newline = get_newline(line)
  if newline != line:
   lnum = iline+1
   change = Change(lnum,line,metaline,newline)
   changes.append(change)
  newlines.append(newline)
 return changes,newlines

def get_newline_1(line):
 newline = re.sub(r'〕([^<])',r'〕_\1',line)
 return newline

def init_changes_1(lines):
 changes = []
 newlines = []
 metaline = None
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   newlines.append(line)
   continue
  newline = get_newline_1(line)
  if newline != line:
   lnum = iline+1
   change = Change(lnum,line,metaline,newline)
   changes.append(change)
  newlines.append(newline)
 return changes,newlines

def title_rec(changes):
 outarr = [] # title
 outarr.append('; ************************************************')
 outarr.append('; PART ONE "<ls>X></ls> 〔N〕"  -> "<ls>X 〔N〕</ls>"' )
 outarr.append('; %s changes' % len(changes))
 outarr.append('; ************************************************')
 return outarr

def title_rec_1(changes):
 outarr = [] # title
 outarr.append('; ************************************************')
 outarr.append('; PART TWO: ? 〔N〕, where ? is not >' )
 outarr.append('; %s changes' % len(changes))
 outarr.append('; ************************************************')
 return outarr

def change_rec(change):
  outarr = []
  outarr.append('; ----------------------------------------------------')
  meta = re.sub(r'<k2>.*$','',change.metaline)
  outarr.append('; %s' % meta)
  lnum = change.lnum
  old = change.line
  new = change.newline
  outarr.append('%s old %s' %(lnum,old))
  outarr.append(';')
  outarr.append('%s new %s' %(lnum,new))
  return outarr
 
def write_changes(fileout,changes,changesa):
 # generate change transactions
 outrecs = []
 outrecs.append(title_rec(changes))
 for change in changes:
  outrecs.append(change_rec(change))
 #
 outrecs.append(title_rec_1(changesa))
 for change in changesa:
  outrecs.append(change_rec(change))
 
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(changes),"changes written to",fileout)

    
if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 fileout = sys.argv[2] # 
 lines = read_lines(filein)
 changes,newlines = init_changes(lines)
 changes1,newlines1 = init_changes_1(newlines)
 write_changes(fileout,changes,changes1)


