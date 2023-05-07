# coding=utf-8
""" make_meta_vn_a.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

class AddEntry(object):
 def __init__(self,iline,page,isentry):
  # etype: hw/nonhw
  self.iline = iline
  self.page = page
  self.isentry = isentry
  # attributes set elsewhere, for some, but not all, entries
  self.entrylines = []
  self.hdata = None  # characters before �
  self.adata = None  # <a X>
  self.adata1 = None # <a X> Y� = hdata
  self.hom = None # <a x> h.
  self.bdata = None # <b>X</b>
  
def generate_add_entry(lines):
 nlines = len(lines)
 page = None
 iline = 0
 while (iline < nlines):
  line = lines[iline]
  m = re.search(r'^(.*)¦',line)
  if m != None:
   #
   add_entry = AddEntry(iline,page,True)   
   hdata = m.group(1)
   add_entry.hdata = hdata;
   m1 = re.search(r'<a ([^>]+)> (.*)$',hdata)
   if m1 != None:
    # the usual case.
    adata = m1.group(1)
    adata1 = m1.group(2)
    add_entry.adata = adata
    add_entry.adata1 = adata1
    m2 = re.search(r'^([0-9])\.',adata1)
    if m2 != None:
     hom = m2.group(1)
     add_entry.hom = hom
    m3 = re.search(r'<b>(.*)</b>',adata1)
    if m3 != None:
     # should always be there
     bdata = m3.group(1)
     bdata = re.sub(r',.*$','',bdata) # <b>étaśa, etaśá</b> -> <b>étaśa</b>
     add_entry.bdata = bdata
    else:
     print('NO bdata for',adata1)
   # get entrylines
   entrylines = []
   while(line != ''):
    entrylines.append(line)
    iline = iline + 1
    line = lines[iline]
   add_entry.entrylines = entrylines
   yield add_entry
  else: # no ¦
   m = re.search(r'^\[Page(.*?)\]$',line)
   if m != None:
    page = m.group(1)
   add_entry = AddEntry(iline,page,False)
   add_entry.entrylines = [line]
   iline = iline + 1
   yield add_entry
 return
 
def generate_add_entries(filein):
 # part
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 recs = []
 i = 0
 for rec in generate_add_entry(lines):
  recs.append(rec)
 return recs

def make_entry_dict(entries):
 d = {}
 d1 = {}
 ndup = 0
 ndup1 = 0
 for entry in entries:
  line = entry.datalines[0] # first line
  # exclude entries of chg and deletion vn
  if '<info vn="del' in line:
   continue
  if '<info vn="chg' in line:
   continue
  m = re.search(r'^(.*)¦',line)
  if m == None:
   print('make_entry_dict: no ¦',entry.metaline)
   continue
  hdata = m.group(1)
  # remove chg markup, if any. Example L=1726 indravAyu
  if '<chg type="chg"' in hdata:
   hdata = re.sub(r'<chg type="chg.*<old>','',hdata)
   hdata = re.sub(r'</old>.*</chg>','',hdata)
  adata1 = hdata
  # do some tidying
  adata1 = adata1.replace('(','')
  adata1 = adata1.replace(')','')
  adata1 = adata1.replace('[','')
  #adata1 = adata1.replace(']','')
  adata1 = adata1.replace(',@}','@}')
  adata1 = re.sub(r', .*@','@',adata1) # {@átya, átia,@} -> {@átya@}
  adata1 = adata1.replace('.@}','@}')
  adata1 = adata1.replace('-','')
  m2 =  re.search(r'^([0-9])\.',adata1)
  if m2 == None:
   hom = ''
  else:
   hom = m2.group(1)
  m3 = re.search(r'{@(.*)@}',adata1)
  if m3 == None:
   print('make_entry_dict: no {@X@}',entry.metaline)
   continue
  bdata = m3.group(1)
  key = '%s,%s' % (hom,bdata)
  if key in d:
   preventry = d[key]
   prevmeta = re.sub(r'<k2>.*$','',preventry.metaline)
   meta = re.sub(r'<k2>.*$','',entry.metaline)
   if False: print('duplicate key "%s": %s   %s' %(key,prevmeta,meta))
   ndup = ndup + 1
  else:
   d[key] = entry
  # also keep dictionary of adjusted keys
  adjkey = adjust_key(key)
  if adjkey in d1:
   preventry = d1[adjkey]
   prevmeta = re.sub(r'<k2>.*$','',preventry.metaline)
   meta = re.sub(r'<k2>.*$','',entry.metaline)
   if False: print('duplicate ADJ key "%s": %s   %s' %(adjkey,prevmeta,meta))
   ndup1 = ndup1 + 1
  else:
   d1[adjkey] = entry
  if False: # dbg
   L = entry.metad['L']
   if L in ['1398']:
    print('dict dbg',L,key,adjkey)
    
 keys = d.keys()
 print('make_entry_dict has %s keys' % len(keys))
 print('  %s duplicate keys' % ndup)
 adjkeys = d1.keys()
 print('make_entry_dict has %s adjusted keys' % len(adjkeys))
 print('  %s duplicate adjusted keys' % ndup1)
 return d,d1

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

def  write_vn_chk1(fileout,add_entries):
 outarr = []
 for rec in add_entries:
  if rec.isentry:
   hom = rec.hom
   if hom == None:
    hom = ''
   out = '%s,%s,%s,%s' %(rec.iline+1,rec.adata,hom,rec.bdata)
   outarr.append(out)
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')
 print(len(outarr),"records written to",fileout)

adjust_key_specific = {
 'jiéṣṭha' : 'jyéṣṭha',
 'jiók' : 'jyók',
 'váreṇia' : 'váreṇya',
 'vā́dhriaśva' : 'vā́dhryaśva',
 'vīría' : 'vīryà',
 'śamiā́' : 'śamyā́',
 'sā́mrājia' : 'sā́mrājya',
 'gúhia' : 'gúhya',
 'vṛ́t' : 'vṛt',
 'śávistha' : 'śáviṣṭha',
 'sádhrī' : 'sádhri',
 'sasthā́van' : 'saṃsthā́van',
 'sóma' : 'soma',
 }

def adjust_key(keyfull):
 if keyfull == '1,áha':
  return ',aha'
 if keyfull == '1,u':
  return ',u'
 if keyfull == '1,ṛdh':
  return ',ṛdh'
 key1 = keyfull[1:]  # remove initial comma
 if key1 in adjust_key_specific:
  key = adjust_key_specific[key1]
  key2 = ',' + key
 else:
  key2 = keyfull
 key = key2
 key = key.replace('-','')
 key = key.replace('í','i')
 key = key.replace('á','a')
 key = key.replace('ú','u')
 key = key.replace('ā́','ā')
 return key

def  outarr_vn_chk2(add_entries,chgd,chgd1):
 outarr = []
 for rec in add_entries:
  if not rec.isentry:
   assert len(rec.entrylines) == 1
   outarr.append(rec.entrylines[0])
   continue
  if rec.isentry:
   hom = rec.hom
   if hom == None:
    hom = ''
   if rec.adata1 == None:
    print('dbg: adata1 is None ',rec.hdata)
   bdata = rec.bdata
   key = '%s,%s' %(hom,rec.bdata)
   adjkey = adjust_key(key)
   if False: # dbg
    if key in [',váreṇia', ',sā́mrājia',]:
     print('chk2dbg:',key,adjkey)
   if key in chgd:
    entry = chgd[key]
    meta = entry.metaline
   elif '*' in rec.adata1:
    meta = 'NEW headword in vn'    
   elif adjkey in chgd1:
    entry = chgd1[adjkey]
    #meta = 'ADJKEY' + entry.metaline
    meta = entry.metaline
   else:
    meta = '  KEY "%s" not found in gra.txt' % key
   out = ';%s:%s:%s:%s:%s' %(rec.page,rec.adata,hom,rec.bdata,meta)
   outarr.append(out)
   # also get all the entrylines
   for line in rec.entrylines:
    outarr.append(line)
   # and the <LEND> line
   outarr.append('<LEND>')
 return outarr

def write_vn_chk2(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"records written to",fileout)

if __name__=="__main__":
 filein1 = sys.argv[1] # temp_gra_8b
 filein2 = sys.argv[2] # vn3add_`.txt
 fileout = sys.argv[3] # vn6_add.txt - metalines added
 entries = digentry.init(filein1)
 chgd,chgd1 = make_entry_dict(entries)

 add_entries = generate_add_entries(filein2)

 #write_vn_chk1(fileout,add_entries)
 outarr = outarr_vn_chk2(add_entries,chgd,chgd1)
 write_vn_chk2(fileout,outarr)
 exit(1)
