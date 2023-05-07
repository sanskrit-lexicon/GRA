# coding=utf-8
""" make_meta_vn_cd.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def make_entry_dict(entries):
 d = {}
 for entry in entries:
  for iline,line in enumerate(entry.datalines):
   for m in re.finditer(r'<chg type="(.*?)" n="(.*?)" src="gra">',line):
    ctype = m.group(1)
    cid = m.group(2)
    key = (ctype,cid)
    #if key == ('chg','10'): print('dbg:',key,entry.metaline)
    if key in d:
     preventry = d[key]
     if preventry != entry:
      print('make_entry_dict duplicate:',key)
      print('  old = %s' % preventry.metaline)
      print('  cur = %s' % entry.metaline)
      continue
    d[key] = entry
 keys = d.keys()
 print('make_entry_dict has %s keys' % len(keys))
 return d

def make_outrec(line,chgd,page,lnum_old):
 # return array of strings
 m = re.search(r'<info vn="(chg|del) (.*?) gra"/>',line)
 if m == None:
  return [line],lnum_old
 ctype = m.group(1)
 cid = m.group(2)
 key = (ctype,cid)
 if key not in chgd:
  print('make_outrec: (%s,%s) not found' % (ctype,cid))
  return [line],lnum_old
 entry = chgd[key]
 metaline = entry.metaline
 lnum = lnum_old + 1
 newmeta = re.sub(r'<L>(.*?)<pc>(.*?)<','<L>%s<pc>%s<' % (lnum,page),metaline)
 outarr = []
 outarr.append(newmeta)
 newline = line
 outarr.append(newline)
 outarr.append('<LEND>')
 return outarr,lnum

def write_vn(fileout,lines2,chgd):
 outrecs = []
 page = None
 lnum0 = 11000
 lnum = lnum0
 for line in lines2:
  outarr = []
  if line.startswith('[Page'):
   m = re.search(r'\[Page(.*?)\]',line)
   page = m.group(1)
   outarr.append(line)
  elif line.startswith(';'):
   outarr.append(line)
  else:
   outarr,lnum1 = make_outrec(line,chgd,page,lnum)
   lnum = lnum1
  outrecs.append(outarr)
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')
 print(len(outrecs),"records written to",fileout)
  
if __name__=="__main__":
 filein1 = sys.argv[1] # temp_gra_8b
 filein2 = sys.argv[2] # vn4.txt
 fileout = sys.argv[3] # vn5.txt - metalines added
 entries = digentry.init(filein1)
 chgd = make_entry_dict(entries)
 
 lines2 = read_lines(filein2)
 write_vn(fileout,lines2,chgd)
