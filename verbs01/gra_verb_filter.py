#-*- coding:utf-8 -*-
"""gra_verb_filter.py
 
 
"""
from __future__ import print_function
import sys, re,codecs
from parseheadline import parseheadline
#import transcoder
#transcoder.transcoder_set_dir('transcoder')

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
  self.markcode = None
  self.markline = None

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

exclusion_patterns = [
 # 10787 entries
 #Analysis of first lines (contain '¦')
 "¦ [mfna][.][, ]",  # 2792 remain
 "¦ adv[.][, ]",  # 2783 remain
 "¦, [mfna][.][, ]",  # 2296 remain
 "-.*?¦",  # 2013 remain   (hyphenated words
 "[aá][,.})@]+¦",  # 1482 remain
 "tás[,.@})]+¦",  # 1469 remain
 "vát[,.@})]+¦",  # 1433 remain
 "ṣas[,.@})]+¦",  # 1431 remain
 "śás[,.@})]+¦",  # 1420 remain
 "¦ *[0-9]+[)] [mfna][.][, ]",  # 1412 remain
 "Ablativ",  # 1407 remain
 "ā́t[,.@})]+¦",  # 1398 remain
 "tas[,.@})]+¦",  # 1388 remain
 "á.[,.@})]+¦",  # 1307 remain  penultimate accented 'a'.
 "āt[,.@})]+¦",  # 1298 remain  
 "@[})]+¦[, ]*{@[^@]+@} *[mfna][.]",  # 1212 remain more substantives
 "[áa]thā.*¦",  # 1199 remain
 "é.*¦",  # 1189 remain
 "[áíú].*¦",  # 1051 remain accented vowel in headword
 "fem[.]",  # 1036 remain
 "ā́.*¦.*Instr.",  # 1029 remain
 "a[^@]+ā́[,.@})]+¦",  # 1001 remain
 "īm[,.@})]+¦", # 995 
 "vat[,.@})]+¦",
 ]

def unused_mark_entries_verb(entries,exclusions,inclusions):
 """ gra verbs:  by exclusion
  This gives same filter as mark_entries_verb
  but does not use exclusions/inclusions
 """
 # these exclusion patterns determined manually (with Emacs)
 # If the first line of an entry matches one of these patterns
 # then the entry is believed to be a non-verb.
 # Each entry.markcode is initially None (from init_entries)
 # Assign 'None' to a new attribute 'exclude' of each entry
 remain_count = [0 for regex in exclusion_patterns]
 for entry in entries:
  entry.exclude = None
 for iregex,regex in enumerate(exclusion_patterns):
  for entry in entries:
   if entry.exclude != None:
    # already excluded
    continue
   if re.search(regex,entry.datalines[0]):
    entry.exclude = iregex # 
   else:
    remain_count[iregex] = remain_count[iregex] + 1
  print('remain_count after %s = %s' %(iregex,remain_count[iregex]))
 # Now set markcode to 'V' for each entry not excluded
 for entry in entries:
  if entry.exclude == None:
   entry.markcode = 'V'

 return
 for entry in entries:
  # first exclude known non-verbs
  if entry.metaline in exclusions:
   exclusions[entry.metaline] = True  # so we know exclusion has been used
   continue 
  if entry.metaline in inclusions:
   entry.markcode = 'X'
   continue
  k1 = entry.metad['k1']
  L  = entry.metad['L']
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline
  datalines = entry.datalines
  # Assume a root unless excluded
  isverb = True
  for iregex,regex in enumerate(exclusion_patterns):
   # if True: print(iregex,regex)
   if re.search(regex,datalines[0]):
    isverb=False
    break
  if not isverb:
   continue
  entry.markcode = 'V'
  continue
 for x in exclusions:
  if not exclusions[x]:
   print('Unused exclusion:',x)

def mark_entries_verb(entries,exclusions,inclusions):
 """ gra verbs:  by exclusion
  
 """
 # these exclusion patterns determined manually (with Emacs)
 # If the first line of an entry matches one of these patterns
 # then the entry is believed to be a non-verb.
 for entry in entries:
  # first exclude known non-verbs
  if entry.metaline in exclusions:
   exclusions[entry.metaline] = True  # so we know exclusion has been used
   continue 
  if entry.metaline in inclusions:
   entry.markcode = 'X'
   continue
  k1 = entry.metad['k1']
  L  = entry.metad['L']
  code = None
  linenum1 = entry.linenum1  # integer line number of metaline
  datalines = entry.datalines
  # Assume a root unless excluded
  isverb = True
  for iregex,regex in enumerate(exclusion_patterns):
   # if True: print(iregex,regex)
   if re.search(regex,datalines[0]):
    isverb=False
    break
  if not isverb:
   continue
  entry.markcode = 'V'
  continue
 for x in exclusions:
  if not exclusions[x]:
   print('Unused exclusion:',x)

def adjust_k2(x):
 x = re.sub(r' +','',x) # remove spaces
 x = re.sub(r',','_',x) # replace comma with underscore
 return x

def write_verbs(fileout,entries):
 n = 0
 coded = {}
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   if code not in coded:
    coded[code] = 0
   coded[code] = coded[code] + 1
   n = n + 1
   outarr = []
   k1 = entry.metad['k1']  
   L =  entry.metad['L']
   k2 = entry.metad['k2']
   k2a = adjust_k2(k2)  
   outarr.append(';; Case %04d: L=%s, k1=%s, k2=%s, code=%s' %(n,L,k1,k2a,code))
   for out in outarr:
    f.write(out+'\n')

 code_keys = sorted(coded.keys())
 for code in code_keys:
  print('%04d %s' %(coded[code],code))
 print('%04d' %n,"verbs written to",fileout)

def write_line1(fileout,entries):
 with codecs.open(fileout,"w","utf-8") as f:
  for ientry,entry in enumerate(entries):
   code = entry.markcode
   if not code:
    continue
   out = entry.datalines[0]
   f.write(out+'\n')
 print('line1 records written to',fileout)

def init_exclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

def init_inclusions(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [x.rstrip() for x in f if not x.startswith(';')]
 d = {}
 for rec in recs:
  d[rec] = False
 print(len(recs),"records read from",filein)
 return d

if __name__=="__main__": 
 filein = sys.argv[1] #  xxx.txt (path to digitization of xxx
 filein1 = sys.argv[2] # xxx_verb_exclude.txt
 filein2 = sys.argv[3] # xxx_verb_include.txt
 fileout = sys.argv[4] # 
 entries = init_entries(filein)
 #exclusions = {}
 #inclusions = {}
 exclusions = init_exclusions(filein1)
 inclusions = init_inclusions(filein2)
 mark_entries_verb(entries,exclusions,inclusions)
 write_verbs(fileout,entries)
 write_line1('templog_'+fileout,entries)
