#-*- coding:utf-8 -*-
"""diff2.py
"""
from __future__ import print_function
import sys, re,codecs

def remove_corr_markup(line,c):
 regex = r'<%s .*?>(.*?)</%s>' %(c,c)
 line = re.sub(regex,r'\1',line)
 return line

def adjustlines1(lines1):
 # changes to temp_gra_6
 ans = []
 dab = {}
 for line in lines1:
  x = line
  x = re.sub(r' +$','',x) # remove space at end of line
  # remove <lbinfo.*/>
  x = re.sub(r' <lbinfo.*?/>','',x)
  # abbreviations
  update_dab(line,dab)
  x = re.sub(r'<ab>([^<]*?)</ab>',r'\1',x)
  # <c n>X</c> -> X. Similarly for <a n> and <d n>
  for c in ('c','d','a'):
   x = remove_corr_markup(x,c)
  # .%} -> %}.
  x = x.replace('.%}','%}.')
  # diff2:  replace all 〰 by …
  x = x.replace('〰','…')
  # done
  ans.append(x)
 return ans,dab

def update_dab(line,dab):
 # modifies dab
 abs = re.findall(r'<ab>([^<]*?)</ab>',line)
 for ab in abs:
  if ab not in dab:
   dab[ab] = 0
  dab[ab] = dab[ab] + 1

def update_dls(line,dls):
 # modifies dls
 lss = re.findall(r'<ls>([^<]*?)</ls>',line)
 for ls in lss:
  if ls not in dls:
   dls[ls] = 0
  dls[ls] = dls[ls] + 1
 
def adjustlines2(lines2):
 ans = [] 
 dab = {}
 dls = {}
 for line in lines2:
  x = line
  x = re.sub(r' +$','',x) # remove space at end of line
  update_dab(line,dab)
  # <ab>X</ab> -> X
  x = re.sub(r'<ab>([^<]*?)</ab>',r'\1',x)
  update_dls(line,dls)
  x = re.sub(r'<ls>([^<]*?)</ls>',r'\1',x)
  # diff2:  replace all 〰 by …
  x = x.replace('〰','…')
  ans.append(x)
 return ans,dab,dls

def write_diff(fileout,lines1a,lines2a):
 outrecs = []
 for i,x1 in enumerate(lines1a):
  x2 = lines2a[i]
  if x1 == x2:
   continue
  outarr = []
  lnum = i+1
  outarr = []
  outarr.append('%s old %s' %(lnum,x1))
  outarr.append('%s new %s' %(lnum,x2))
  outarr.append('')
  outrecs.append(outarr)
 
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out + '\n')
 print(len(outrecs),"remaining differences written to",fileout)

def write_abbrevs(fileout,dab1,dab2):
 # sort dab alphabetically by lower case
 keys = sorted(dab.keys(),key = lambda x: x.lower())
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for key in keys:
   n = dab[key]
   out = '%04d : %s' %(n,key)
   f.write(out + '\n')
 print(len(keys),"abbreviations written to",fileout)
 
def unused_write_abbrevs(fileout,dab1,dab2):
 # sort dab alphabetically by lower case
 keys = sorted(dab.keys(),key = lambda x: x.lower())
 with codecs.open(fileout,encoding='utf-8',mode='w') as f:
  for key in keys:
   n = dab[key]
   out = '%04d : %s' %(n,key)
   f.write(out + '\n')
 print(len(keys),"abbreviations written to",fileout)
 
if __name__=="__main__": 
 filein1 = sys.argv[1] #  temp_gra_6
 filein2 = sys.argv[2] #  temp_gra_.CSL._.AB.txt
 fileout1 = sys.argv[3] # diffs
 fileout2 = sys.argv[4] # list of <ab>X</ab> markup

 with codecs.open(filein1,encoding='utf-8',mode='r') as f:
  lines1 = [line.rstrip('\r\n') for line in f]
 print(len(lines1),"read from",filein1)

 with codecs.open(filein2,encoding='utf-8',mode='r') as f:
  lines2 = [line.rstrip('\r\n') for line in f]
 print(len(lines2),"read from",filein2)
 
 lines2a,abbrev2d,ls2d = adjustlines2(lines2)
 lines1a,abbrev1d = adjustlines1(lines1)
 write_diff(fileout1,lines1a,lines2a)
 # write_abbrevs(fileout2,abbrev1d,abbrev2d)
 
