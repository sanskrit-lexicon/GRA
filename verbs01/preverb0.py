#-*- coding:utf-8 -*-
"""preverb0.py for gra
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
import transcoder
transcoder.transcoder_set_dir('transcoder')

class Entry(object):
 Ldict = {}
 def __init__(self,lines,linenum1,linenum2):
  # linenum1,2 are int
  self.metaline = lines[0]
  self.lend = lines[-1]  # the <LEND> line
  self.datalines = lines[1:-1]  # the non-meta lines
  # parse the meta line into a dictionary
  #self.meta = Hwmeta(self.metaline)
  self.metad = parseheadline(self.metaline)
  self.linenum1 = linenum1
  self.linenum2 = linenum2
  #L = self.meta.L
  L = self.metad['L']
  if L in self.Ldict:
   print("Entry init error: duplicate L",L,linenum1)
   exit(1)
  self.Ldict[L] = self
  #  extra attributes
  self.marked = False # from a filter of markup associated with verbs
  self.marks = []  # verb markup markers, in order found, if any
  
def init_entries(filein):
 # slurp lines
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [line.rstrip('\r\n') for line in f]
 recs=[]  # list of Entry objects
 inentry = False  
 idx1 = None
 idx2 = None
 for idx,line in enumerate(lines):
  if inentry:
   if line.startswith('<LEND>'):
    idx2 = idx
    entrylines = lines[idx1:idx2+1]
    linenum1 = idx1 + 1
    linenum2 = idx2 + 1
    entry = Entry(entrylines,linenum1,linenum2)
    recs.append(entry)
    # prepare for next entry
    idx1 = None
    idx2 = None
    inentry = False
   elif line.startswith('<L>'):  # error
    print('init_entries Error 1. Not expecting <L>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <LEND>
    continue
  else:
   # inentry = False. Looking for '<L>'
   if line.startswith('<L>'):
    idx1 = idx
    inentry = True
   elif line.startswith('<LEND>'): # error
    print('init_entries Error 2. Not expecting <LEND>')
    print("line # ",idx+1)
    print(line.encode('utf-8'))
    exit(1)
   else: 
    # keep looking for <L>
    continue
 # when all lines are read, we should have inentry = False
 if inentry:
  print('init_entries Error 3. Last entry not closed')
  print('Open entry starts at line',idx1+1)
  exit(1)

 print(len(lines),"lines read from",filein)
 print(len(recs),"entries found")
 return recs

def dump_entry(entry):
 outarr = [entry.metaline] 
 for x in  entry.datalines:
  x = re.sub(r'({@.*?@})',r'   \1   ',x)
  x = re.sub(r'{%(.*?)%}',r'\1',x)
  outarr.append(x)
 outarr = outarr + [';']
 return '\n'.join(outarr)
 
def dump_entry1(entry):
 outarr = [entry.metaline] 
 for x in  entry.datalines:
  parts = re.split(r'({@.*?@})',x)
  newparts = []
  for part in parts:
   if part.startswith('{@'):
    newparts.append(part)
  if len(newparts) > 0:
   y = '  '.join(newparts)
   outarr.append(y)
  #x = re.sub(r'({@.*?@})',r'   \1   ',x)
  #x = re.sub(r'{%(.*?)%}',r'\1',x)
  #outarr.append(x)
 outarr = outarr + [';']
 return '\n'.join(outarr)
 
def write(fileout,recs,tranout='slp1'):
 tranin = 'slp1'
 def transcode(x):
  return transcoder.transcoder_processString(x,tranin,tranout)
 n = 0
 nyes = 0
 nno = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for irec,rec in enumerate(recs):
   entry = rec.entry
   upasargas = rec.upasargas
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   ustring = ','.join(upasargas)
   out1 = ';; Case %04d: L=%s, k1=%s, #upasargas=%s, upasargas=%s' %(
    irec+1,L,transcode(k1),len(upasargas),ustring)
   f.write(out1+'\n')
   if False:  # for debugging
    s = dump_entry1(entry)
    print(s)
    print('upas=',ustring)
    print()
   n = n + 1
 print(n,"records written to",fileout)
 if False: # dbg
  d = {}
  for rec in recs:
   for upa in rec.upasargas:
    if upa not in d:
     d[upa] = 0
    d[upa] = d[upa] + 1
  keys = sorted(d.keys())
  for upa in keys:
   print("'%s' %d" %(upa,d[upa]))
class Ccsverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*), mw=(.*)$',line)
  self.L,self.k1,self.k2,self.code,self.mw = m.group(1),m.group(2),m.group(3),m.group(4),m.group(5)
  self.upasargas = []
  self.entry = None
  self.preverbs = []
  self.mwpreverbs = []
  self.mwpreverbs_found = []
  self.mwpreverbs_parse = []

def init_ccsverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Ccsverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

def find_entries(recs,entries):
 # dictionary for entries
 d = {}
 for entry in entries:
  d[entry.metad['L']]= entry
 # 
 for irec,rec in enumerate(recs):
  L = rec.L
  try:
   entry = d[L]
   rec.entry = entry
   entry.marked = True
  except:
   print('find_entries. bad L=',rec.L)
   print('record # ',irec+1)
   print('  line = ',rec.line)
   exit(1)

def parse_sanskrit_string(x):
 # SLP1 coding of Sanskrit
 # remove accents 
 x0 = x # for debugging
 x = re.sub(r'[/\^]','',x)
 # remove 'missing' character
 x = re.sub(r'°','',x)
 # remove page breaks
 x = re.sub(r'\[Page.*?\]',' ',x)
 # remove long dash
 x = re.sub(r'—','',x)
 # remove hyphen
 x = re.sub(r'-','',x)
 # return strings of alphabetical characters
 x = re.sub(u'‡','',x)
 x = re.sub(u'á','a',x) # remove accent. it generates several false posisitives
 #a = re.findall(r'\w+',x)
 # next does NOT work !
 # a = re.findall(u'[a-zA-Zā]+',x)
 # nor does this
 # a = re.findall(r'[a-zA-Z\\u0101]+',x)
 # Temporarily change ā to 0
 y = transcoder.transcoder_processString(x,'roman','slp1')
 a = re.findall(r'\w+',y)
 #if x0.startswith('acchā'): print('parse_sanskrit_string:',x0,x,y,a)
 return a
 if re.search(r'[ā]',x):
  x0 = x
  x = re.sub('ā','Z',x)
  if False:
   print('chka: %s -> %s'%(x0,x))
  b =  re.findall(r'\w+',x)
  a = [y.replace('Z','ā') for y in b]
 else:
  a = re.findall(r'\w+',x)
 return a

def find_sanskrit_words(text,L):
 a = []
 # skip headword and first inflected form
 
 x = re.sub(r'^.*¦','',text)
 """
 if x == text:
  print('chk:\nx=%s\ntext=%s'%(x,text))
  exit(1)
 else:
  print('chk1:\nx=%s\nx=%s'%(x,text))
  exit(1)
 """
 # iterate over Devanagari text strings
 for m in re.finditer(r'{@(.*?)@}',x):
  b = parse_sanskrit_string(m.group(1)) # list of 'distinct' words
  #if L == '6844':print('find_sanskrit_words chk: %s  -> %s'%(m.group(1),b))
  a = a + b
 return a

special_L = {
 # manual adjustments to upasargas for a given entry
 #'6563':['pari','pra','sam'],  #  kzi
 
}
def find_upasargas(recs,knownupad):
 nrec = 0
 nupa = 0
 for rec in recs:
  entry = rec.entry
  upasargas = []
  L = entry.metad['L']
  k1 = entry.metad['k1'] 
  rawbolds = []
  for iline,line in enumerate(entry.datalines):
   status = '+' # prob. ok.
   if iline == 0:
    line = re.sub(r'^.*¦','',line)
   elif line.startswith('<div n="P'): # n="P" or "P1"
    line = re.sub(r'<div.*?>','',line)
    line = line.strip()
    if line.startswith('-'):
     # example aYj: <div n="P1">-nákti 7) 
     status = '-'
   else:
    # skip line
    continue
   linebolds = re.findall(r'{@[^@]+@}',line)  # all bold text this line
   if (status == '+') and (len(linebolds) == 0):
    status = '-'
   line1 = line[0:20] # truncate line. upasargas should occur near beginning
   y = [b[2:-2] for b in linebolds]  # remove {@ and @}
   rawbolds = rawbolds + y
  upasargas0 = [knownupad[x] for x in rawbolds if x in knownupad]
  upasargas = []
  for u in upasargas0:
   if u not in upasargas:
    upasargas.append(u)
  #upasargas = list(set(upasargas))  # remove duplicates
  if L in special_L:
   temp = upasargas
   upasargas = special_L[L]
   print('find_upasargas adjustment for L=%s, k1=%s'%(L,k1))
   print('  computed=',temp)
   print('  adjusted=',upasargas)
  #upasargas = [x for x in sanskrit_words if x in knownupad]
  if False:
   print(L,k1,' , '.join(upasargas))
   continue
  rec.upasargas = upasargas
  if len(upasargas) > 0:
   nrec = nrec + 1
   nupa = nupa + len(upasargas)

 print(nupa,"upasargas found in",nrec,"entries")


sandhimap = {
 ('i','a'):'ya',
 ('i','A'):'yA',
 ('i','i'):'I',
 ('i','I'):'I',
 ('i','u'):'yu',
 ('i','U'):'yU',
 ('i','f'):'yf',
 ('i','F'):'yF',
 ('i','e'):'ye',
 ('i','E'):'yE',
 ('i','o'):'yo',
 ('i','O'):'yO',

 ('u','a'):'va',
 ('u','A'):'vA',
 ('u','i'):'vi',
 ('u','I'):'vI',
 ('u','u'):'U',
 ('u','U'):'U',
 ('u','f'):'vf',
 ('u','F'):'vF',
 ('u','e'):'ve',
 ('u','E'):'vE',
 ('u','o'):'vo',
 ('u','O'):'vO',

 ('a','a'):'A',
 ('a','A'):'A',
 ('A','a'):'A',
 ('A','A'):'A',
 
 ('a','i'):'e',
 ('A','i'):'e',
 ('a','I'):'e',
 ('A','I'):'e',
 
 ('a','u'):'o',
 ('A','u'):'o',
 ('a','U'):'o',
 ('A','U'):'o',
 
 ('a','f'):'Ar',
 ('A','f'):'Ar',
 ('a','e'):'e',
 ('d','s'):'ts',
 ('a','C'):'acC', # pra+Cad = pracCad
 ('A','C'):'AcC', # A + Cid = AcCid
 ('i','C'):'icC',
 ('d','q'):'qq',  # ud + qI
 ('d','k'):'tk',
 ('d','K'):'tK',
 ('d','c'):'tc',
 ('d','C'):'tC',
 ('d','w'):'tw',
 ('d','W'):'tW',
 ('d','t'):'tt',
 ('d','T'):'tT',
 ('d','p'):'tp',
 ('d','P'):'tP',
 ('d','s'):'ts',
 ('d','n'):'nn',

 ('i','st'):'izw',
 ('s','h'):'rh', # nis + han -> nirhan
 ('m','s'):'Ms', # sam + saYj -> saMsaYj
 ('m','S'):'MS',
 ('m','k'):'Mk',
 ('m','K'):'MK',
 ('m','c'):'Mc',
 ('m','C'):'MC',
 ('m','j'):'Mj',
 ('m','J'):'MJ',

 ('m','w'):'Mw',
 ('m','W'):'MW',
 ('m','t'):'Mt',
 ('m','T'):'MT',
 ('m','p'):'Mp',
 ('m','P'):'MP',

 ('m','v'):'Mv',
 ('m','l'):'Ml',
 ('m','r'):'Mr',
 ('m','y'):'My',
 ('m','n'):'Mn',
 
 ('s','k'):'zk', # nis + kf -> nizkf
 ('s','g'):'rg',
 ('s','G'):'rG',
 ('s','c'):'Sc',
 ('s','j'):'rj',
 ('s','q'):'rq',
 ('s','d'):'rd',
 ('s','D'):'rD',
 ('s','b'):'rb',
 ('s','B'):'rB',
 ('s','m'):'rm',
 ('s','n'):'rn',
 ('s','y'):'ry',
 ('s','r'):'rr',
 ('s','l'):'rl',
 ('s','v'):'rv',

 ('r','c'):'Sc',
 ('r','C'):'SC',
 ('d','l'):'ll',
 ('d','h'):'dD',
 ('d','S'):'cC',
 ('d','m'):'nm',

}
def join_prefix_verb(pfx,root):
 if pfx.endswith('ud') and (root == 'sTA'):
  return pfx[0:-2] + 'ut' + 'TA'  # ud + sTA = utTA
 if (pfx == 'saMpra') and (root in ['nad','nam','naS']):
  pfx = 'sampra'
  root = 'R' + root[1:]
  return pfx + root
 if (pfx == 'pra') and (root == 'nakz'):
  return 'pranakz' # odd, since mw has aBipraRakz
 pfx1,pfx2 = (pfx[0:-1],pfx[-1])
 root1,root2 = (root[0],root[1:])
 if (pfx2,root1) in sandhimap:
  return pfx1 + sandhimap[(pfx2,root1)] + root2
 if len(root) > 1:
  root1,root2 = (root[0:2],root[2:])
  if (pfx2,root1) in sandhimap:
   return pfx1 + sandhimap[(pfx2,root1)] + root2
 if root == 'i':
  if pfx == 'dus':
   return 'duri'
  if pfx == 'nis':
   return 'niri'
 if 'saMpra' in pfx:
  pfx = pfx.replace('saMpra','sampra')
  return pfx + root
 if  pfx.endswith(('pari','pra')) and root.startswith('n'):
  return pfx + 'R' + root[1:]  # pra + nad -> praRad
 if pfx.endswith('nis') and root.startswith(('a','I','u','U')):
  pfx = pfx.replace('nis','nir')
  return pfx + root
 ans = pfx + root
 d = {'duscar':'duScar'}
  
 if ans in d:
  ans = d[ans]
 return ans

def init_knownupas(filein):
 d = {}
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  for line in f:
   if line.startswith(';'):
    continue
   line = line.rstrip('\r\n')
   count,raw,upa = line.split('\t')
   d[raw] = upa 
 return d

def prelim(fileout,recs):
 nrec = 0
 nupa = 0
 raw_bolds = {} 
 f = codecs.open(fileout,"w","utf-8")
 for rec in recs:
  entry = rec.entry
  upasargas = []
  L = entry.metad['L']
  k1 = entry.metad['k1'] 
  bolds = [] # all text marked as bold 
  outarr = [entry.metaline]
  for iline,line in enumerate(entry.datalines):
   status = '+' # prob. ok.
   if iline == 0:
    line = re.sub(r'^.*¦','',line)
   elif line.startswith('<div n="P'): # n="P" or "P1"
    line = re.sub(r'<div.*?>','',line)
    line = line.strip()
    if line.startswith('-'):
     # example aYj: <div n="P1">-nákti 7) 
     status = '-'
   else:
    # skip line
    continue
   linebolds = re.findall(r'{@[^@]+@}',line)  # all bold text this line
   if (status == '+') and (len(linebolds) == 0):
    status = '-'
   line1 = line[0:20] # truncate line. upasargas should occur near beginning
   y = [b[2:-2] for b in linebolds]  # remove {@ and @}

   y1 = ', '.join(y)
   out = '%s %s   --> %s' %(status,line1,y1)
   outarr.append(out)
   # update raw_bolds
   for b in y:
    c = b
    if c not in raw_bolds:
     raw_bolds[c] = 0
    raw_bolds[c] = raw_bolds[c] + 1
  outarr.append('')
  for out in outarr:
   f.write(out+'\n')
 print('preverb0. Debug info written to',fileout)
 print(len(raw_bolds),"different bold text found")
 boldkeys = sorted(raw_bolds.keys())
 for b in boldkeys:
  c = re.sub(r'[,:]','',b)
  c = re.sub(r'^Mit ','',c)
  c = re.sub(r'í','i',c) # remove accents
  c = re.sub(r'ú','u',c) # remove accents
  c = re.sub(r'á','a',c) # remove accents
  c = re.sub(r'ā́','ā',c) # remove accent
  f.write('%03d\t%s\t%s\n'%(raw_bolds[b],b,c)) # two copies 
 f.close()

 #print(nupa,"upasargas found in",nrec,"entries")

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # gra_verb_filter.txt
 filein2 = sys.argv[3]  # gra_upasarga_map.txt
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 dhatus = init_ccsverbs(filein1)
 #knownupad = init_knownupas()
 find_entries(dhatus,entries)  # assign entry to each md verb record
 if False: 
  filedbg = "preverb0_dbg.txt"
  prelim(filedbg,dhatus)
 else:
  knownupad = init_knownupas(filein2)
  find_upasargas(dhatus,knownupad)  # get list of upasargas
  write(fileout,dhatus)
