# coding=utf-8
""" vn6_add_1.py
"""
from __future__ import print_function
import sys, re,codecs

class AddEntry(object):
 def __init__(self,isentry,lines):
  self.isentry = isentry
  self.entrylines = lines
  # attributes set elsewhere, for some, but not all, entries
  self.Ladd = None
  self.add_page = None
  self.add_id = None
  self.add_hom = ''
  self.add_k1iast = None
  self.oldmeta = None
  self.isnew = None
  self.newmeta = None
  self.L_body = None  #info from gra.txt metaline
  self.pc_body = None
  self.k1_body = None
  self.k2_body = None

def generate_add_entry(lines):
 nlines = len(lines)
 page = None
 iline = 0
 Lnew = 0
 while (iline < nlines):
  line = lines[iline]
  if not line.startswith(';'):
   isentry = False
   entrylines = [line]
   add_entry = AddEntry(isentry,entrylines)
   iline = iline + 1
   yield add_entry
   continue
  # line starts with semicolon
  # get entrylines (current line and all lines until next line empty
  entrylines = []
  while(line != ''):
   entrylines.append(line)
   iline = iline + 1
   line = lines[iline]
  isentry = True
  add_entry = AddEntry(isentry,entrylines)
  yield add_entry
 return
 
def generate_add_entries(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines read from",filein)
 recs = []
 i = 0
 for rec in generate_add_entry(lines):
  recs.append(rec)
 return recs

def parse_firstline(add_entries):
 Ladd = 12000
 for rec in add_entries:
  if not rec.isentry:
   continue
  # add various attributes
  Ladd = Ladd + 1
  rec.Ladd = Ladd
  firstline = rec.entrylines[0]
  parts = firstline[1:].split(':')
  # page,add_id,hom,k1iast,meta = 
  rec.add_page = parts[0]
  rec.add_id = parts[1]
  rec.add_hom = parts[2]
  rec.add_k1iast = parts[3]
  rec.oldmeta = parts[4]

def make_meta(add_entries):
 for rec in add_entries:
  if not rec.isentry:
   continue
  L = rec.Ladd
  pc = rec.add_page
  # brand new headwords cannot be completed at this point
  rec.isnew =  rec.oldmeta.startswith('NEW')
  if not rec.isnew:
   # construct newmeta
   m = re.search(r'<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>([^<]*)',rec.oldmeta)
   L_body = m.group(1)
   pc_body = m.group(2)
   k1_body = m.group(3)
   k2_body = m.group(4)
   k1 = k1_body
   k2 = k2_body
   newmeta = '<L>%s<pc>%s<k1>%s<k2>%s' %(L,pc,k1,k2)
   if rec.add_hom != '':
    h = rec.add_hom
    newmeta = '%s<h>%s' % (newmeta,h)
   rec.newmeta = newmeta
  else:
   rec.newmeta = get_newmeta(L)
   """
   # newmeta is None, by AddEntry constructor
   k1 = ''
   k2 = ''
   newmeta = '<L>%s<pc>%s<k1>%s<k2>%s' %(L,pc,k1,k2)
   rec.newmeta = newmeta
   print(newmeta)
   """

def get_newmeta(L):
 manual_lines = """
<L>12004<pc>1749<k1>aMhoyu<k2>aMhoyu/
<L>12005<pc>1749<k1>akarman<k2>a-karma/n
<L>12039<pc>1750<k1>aDapriya<k2>aDa-priya
<L>12048<pc>1750<k1>anApta<k2>a/n-Apta
<L>12049<pc>1750<k1>anABayin<k2>an-ABayin
<L>12050<pc>1750<k1>anAyata<k2>a/n-Ayata
<L>12073<pc>1751<k1>apratIta<k2>a/-pratIta
<L>12081<pc>1751<k1>aBivlaNGa<k2>aBivlaNGa/
<L>12083<pc>1751<k1>aBrAtfvya<k2>a-BrAtfvya/
<L>12099<pc>1751<k1>aramati<k2>a-ra/mati
<L>12109<pc>1751<k1>arDadeva<k2>arDa-deva/
<L>12112<pc>1751<k1>aryayA<k2>arya-yA/
<L>12124<pc>1751<k1>avyanat<k2>a/-vyanat
<L>12125<pc>1751<k1>avyaTya<k2>a/-vyaTya
<L>12129<pc>1751<k1>aSAy<k2>aSAy
<L>12147<pc>1751<k1>ahaMsana<k2>ahaM-sana
<L>12174<pc>1754<k1>iq<k2>iq
<L>12213<pc>1754<k1>upavid<k2>upavi/d
<L>12227<pc>1757<k1>usri<k2>u/sri
<L>12235<pc>1757<k1>fjIyas<k2>f/jIyas
<L>12262<pc>1757<k1>Eyes<k2>E/yes
<L>12272<pc>1757<k1>kadarTa<k2>ka/d-arTa
<L>12286<pc>1757<k1>kuhacidvid<k2>kuhacid-vi/d
<L>12313<pc>1760<k1>gATAnI<k2>gATA-nI/
<L>12357<pc>1761<k1>jAvat<k2>jA/vat
<L>12371<pc>1761<k1>tadbanDu<k2>ta/d-banDu
<L>12407<pc>1763<k1>tvoti<k2>tvo/ti
<L>12425<pc>1763<k1>BUtAMSa<k2>BUtA/MSa
<L>12460<pc>1766<k1>mahimaGa<k2>ma/hi-maGa
<L>12465<pc>1766<k1>mADyaMdina<k2>mA/DyaMdina
<L>12494<pc>1766<k1>yAtujU<k2>yAtu-jU/
<L>12517<pc>1768<k1>rAjayakzma<k2>rAjayakzma/
<L>12540<pc>1768<k1>vayoDeya<k2>vayo-De/ya
<L>12543<pc>1768<k1>varAhayu<k2>varAhayu/
<L>12565<pc>1769<k1>vicayizWa<k2>vi/cayizWa
<L>12605<pc>1771<k1>Sagmya<k2>Sagmya^
<L>12608<pc>1771<k1>Satamanyu<k2>Sata/-manyu
<L>12687<pc>1773<k1>sArasvata<k2>sArasvata/
""".splitlines()
 Lstart = '<L>%s<pc>' %L
 for line in manual_lines:
  if line.startswith(Lstart):
   return line.strip('\r\n')
 print('get_newmeta error for L=',L)
 exit(1)
  
def info(add_entries):
 # for entry, change <a N> X¦c  => X¦c <info vn="add N gra"/>
 for rec in add_entries:
  if not rec.isentry:
   continue
  iline = 1 # second line of vn6_add
  line = rec.entrylines[iline] 
  assert '¦' in line
  infoelt = '<info vn="add %s gra"/>' % rec.add_id
  newline = re.sub(r'^<a [^>]*> (.*?¦.)',r'\1' + infoelt + ' ',line)
  newline = re.sub(r'  +',' ',newline)
  rec.entrylines[iline] = newline

def bold_italic(add_entries):
 # use {@X@} for <b>X</b>, and {%X%} for <i>X</i>
 # for consistency with gra.txt markup convention
 replacements = [
   ('<b>', '{@'),
   ('</b>', '@}'),
   ('<i>', '{%'),
   ('</i>', '%}'),
  ]
 for rec in add_entries:
  newlines = []
  oldlines = rec.entrylines
  for line in oldlines:
   newline = line
   for old,new in replacements:
    newline = newline.replace(old,new)
   newlines.append(newline)
  rec.entrylines = newlines

def misc1(add_entries):
 replacements = [
   ('<p>', '<div n="P">'),
   ('<P1>', '<div n="H">'),
   ('</h>', '')
   #('', ''),
  ]
 for rec in add_entries:
  if not rec.isentry:
   continue
  newlines = []
  oldlines = rec.entrylines
  for line in oldlines:
   newline = line
   if '</h>' in line:
    print('misc1: </h>: ',line)
   for old,new in replacements:
    newline = newline.replace(old,new)
   newlines.append(newline)
  rec.entrylines = newlines

def rv(add_entries):
 # ' A,B' -> ' {A,B}', where A and B are sequences of digits
 # This will mark most of the Rgveda references 
 for rec in add_entries:
  if not rec.isentry:
   continue
  newlines = []
  oldlines = rec.entrylines
  for line in oldlines:
   newline = re.sub(r' ([0-9]+,[0-9]+)',r' {\1}',line)
   newlines.append(newline)
  rec.entrylines = newlines
 
def write_vn(fileout,add_entries):
 nout = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(add_entries):
   outarr = rec.entrylines
   if rec.isentry:
    outarr1 = []
    # outarr1.append(outarr[0]) # metaline comment  for debugging
    outarr1.append(rec.newmeta)
    for out in outarr[1:]:
     outarr1.append(out)
    outarr = outarr1
   for out in outarr:
    try:
     f.write(out+'\n')
    except:
     print('write_vn error at irec=',irec)
     exit(1)
    nout = nout + 1
 print(len(add_entries),"records (%s lines) written to %s" %(nout,fileout))

if __name__=="__main__":
 filein = sys.argv[1] # vn6_add.txt
 fileout = sys.argv[2] # vn6_add_1.txt 

 add_entries = generate_add_entries(filein)
 parse_firstline(add_entries)
 make_meta(add_entries)
 info(add_entries)
 bold_italic(add_entries)
 misc1(add_entries)
 rv(add_entries)
 
 n = len([x for x in add_entries if x.isentry])
 print(n,"entries")
 
 write_vn(fileout,add_entries)
 
