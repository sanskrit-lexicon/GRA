#-*- coding:utf-8 -*-
"""cae_verb_filter_map.py
"""
from __future__ import print_function
import sys, re,codecs

class Caeverb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  m = re.search(r'L=([^,]*), k1=([^,]*), k2=([^,]*), code=(.*)$',line)
  self.L,self.k1,self.k2,self.code = m.group(1),m.group(2),m.group(3),m.group(4)
  self.pw=None
  self.mw = None
 
def init_caeverb(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Caeverb(x) for x in f if x.startswith(';; Case')]
 print(len(recs),"records read from",filein)
 return recs

class Pwmw(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.pw,self.mw = line.split(':')
 
def init_pw_mw(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [Pwmw(x) for x in f if not x.startswith(';')]
 print(len(recs),"records read from",filein)
 return recs

class MWVerb(object):
 def __init__(self,line):
  line = line.rstrip()
  self.line = line
  self.k1,self.L,self.cat,self.cps,self.parse = line.split(':')
  self.used = False

def init_mwverbs(filein):
 with codecs.open(filein,"r","utf-8") as f:
  recs = [MWVerb(x) for x in f]
 print(len(recs),"mwverbs read from",filein)
 #recs = [r for r in recs if r.cat == 'verb']
 #recs = [r for r in recs if r.cat in ['root','genuineroot']]
 #recs = [r for r in recs if r.cat == 'verb']
 print(len(recs),"verbs returned from mwverbs")
 d = {}
 for rec in recs:
  k1 = rec.k1
  if k1 in d:
   print('init_mwverbs: Unexpected duplicate',k1)
  d[k1] = rec
 return recs,d

map2mw_special = {
 #'aNkUy':'aNkUy',  # MW aNkUyat
 #'anniy':'anniy',  # MW anniyat
 'ar':'f',  # 
 'arC':'fC',  # 
 'arD':'fD',  # 
 #'arS':'arS',  # not a verb in MW. Although under 'arSa', MW mentions root fS
 'arz':'fz',  # 
 #'avAyat':'avAyat',  # participle of 'i' ?
 #'avizy':'avizy',  # MW has avizyat
 'ij':'yaj',  # 
 'iD':'inD',  #
 'uj':'vaj',  # 
 #'UNK':'UNK',  # 
 'kar':'kf',  # 
 'karS':'kfS',  # 
 'karz':'kfz',  # 
 'kalp':'kxp',  # 
 #'kavIy':'kavIy',  # MW kavIy
 'kir':'kF',  # 
 'kuB':'kumB',  # 
 #'kulAyay':'kulAyay',  # MW kulAyayat
 'kfpaR':'kfpaRya',  # 
 #'kru':'kru',  # 
 #'kzemay':'kzemay',  # 
 'kzA':'kzE',
 'gar':'gF',  # 
 'gir':'gF',  # 
 'gUrDay':'gUrD',  # cl. 10
 'gfB':'graB',  # 
 'graB':'grah',
 'glA':'glE',  #
 'Gar':'Gf',
 #'caraRIy':'caraRIy',  # MW caraRIyamAna
 'jaNgahe':'jaMh',  # intensive 3s of jaMh
 #'jaJJ':'jaJJ',  # 
 'jar':'jF',  #
 'jah':'hA',  # a stem of 2nd hA in jahita
 #'jmAy':'jmAy',  # MW jmAyat
 'tar':'tF',  # 
 'taruzy':'taruz',  # MW taruzyat
 'tarh':'tfh',  # 
 'tir':'tF',  # 
 'tUrv':'turv',  # 
 'trA':'trE',  #
 #'tvAy':'tvAy',  # MW tvAyat  tvAy now in gra_verb_exclude.txt
 'dan':'dan',  #  MW has 'dan' - but not currently recognized as verb
 'dar':'dF',  # 
 'darB':'dfB',  # 
 'dir':'dF',  # 
 'devya':'devya',  # 
 #'dvay':'dvay',  # MW dvayat, a-dvayat
 'dvar':'dvf',  # 
 'Dur':'DUrv',  # 
 'DyA':'DyE',  #
 'Dvas':'DvaMs',  # 
 'nIq':'nIqaya',  # 
 'no':'no',  # 
 'paTI':'paTI',  # 
 'par':'pF',  # 
 #'par':'pf',  # L=5261
 'pAtu':'pA',  # inf. of 'protect'
 #'pfkz':'pfkz',  # 
 'pfC':'praC',  # 
 'pi':'pyE',
 'pyA':'pyE',  #
 #'prakz':'prakz',  # GRA = pfkz
 #'prahantf':'prahantf',  # 
 'pruzAy':'pruz',  # 
 'barh':'bfh',
 'BIs':'BI',  # Causal
 'Bfjj':'Brajj',  #
 'mantray':'mantr',  #
 'mar':'mf',  # 
 'miG':'mih',  # 
 'mur':'mF',
 #'mUr':'mUr',  # 
 'mfgay':'mfg',  # cl. 10
 'mlA':'mlE',  #
 #'yah':'yah',  # 
 #'raGuy':'raGuy',  # 
 #'rayIy':'rayIy',  # 
 #'raS':'raS',  # 
 'ri':'rI',
 'rucay':'ruc',  # denom. von ruc
 'vakz':'ukz',
 'vasAy':'vas',  # cl 10. ?
 'vivAs':'van',  # desiderative
 'vIray':'vIr',  # causal
 #'vfzaRy':'vfzaRy',  #
 'vyA':'vye',  #
 'Sat':'Sad',  #
 'Sar':'SF',  # 
 'SarD':'SfD',  #
 'SA':'Si',  #
 'Sir':'SF',  # 
 'Smasi':'vaS',  # inflected
 'SyA':'SyE',  #
 'SritI':'SritI',  # 
 #'SruDIy':'SruDIy',  # 
 'SvA':'Svi',  # a collateral form of SU (gra); MW SU a weak form of Svo
 #'sanizy':'sanizy',  # 
 #'sI':'sI',  # mw: or a lost root meaning) ‘to draw a straight line’ 
 'saj':'saYj',
 'sA':'so',  # ?
 'sIkz':'sah',  # desiderative
 'sud':'svad',  # 
 'skad':'skand',  # 
 'skaBAy':'skaB',  # or skamB. Causal.
 'skf':'kf',  # form after some prefixes
 'sKid':'Kid',  # form after some prefixes
 'staBAy':'stamB',  # Causal
 'star':'stF',  # 
 'stA':'stE',  # 
 'sTU':'sTU',  # 
 'spaS':'paS',
 #'spij':'spij',  # 
 'spUrD':'sparD',  # 
 'smar':'smf',  # 
 'syad':'syand',
 'sraj':'sfj',  # 
 'sras':'sraMs',
 'srA':'srE',  # ?
 #'sruh':'sruh',  # 
 'svar':'svf',
 'har':'Gf',  # 
 'hAs':'hA',  # ?
 'hU':'hve',  # 

 'arTay':'arT',  # cl. 10
 'staB':'stamB', # mw has prefixes under stamB
}
map2mw_special_L = {
  '5261':'pf',
  '8679':'Sri',
  '3428':'jf', #2 jar
}

def map2mw(d,k1,L):
 if L in map2mw_special_L:
  return map2mw_special_L[L]
 if k1 in map2mw_special:
  return map2mw_special[k1]
 if k1 in d:
  return k1

 if k1.endswith('y'):
  k = k1 + 'a'
  if k in d:
   return k
 
 return '?'


def caemap(recs,mwd):
 for rec in recs:
  rec.mw = map2mw(mwd,rec.k1,rec.L)

def write(fileout,recs):
 n = 0
 nomw = 0
 with codecs.open(fileout,"w","utf-8") as f:
  for rec in recs:
   n = n + 1
   line = rec.line
   # add mw
   out = '%s, mw=%s' %(line,rec.mw)
   if rec.mw == '?':
    nomw = nomw + 1
   f.write(out + '\n')
 print(n,"records written to",fileout)
 print(nomw,"records not yet mapped to mw")


if __name__=="__main__": 
 filein = sys.argv[1] #  cae_verb_filter.txt
 filein1 = sys.argv[2] # mwverbs1
 fileout = sys.argv[3]

 recs = init_caeverb(filein)
 mwverbrecs,mwverbsd= init_mwverbs(filein1)
 caemap(recs,mwverbsd)
 write(fileout,recs)
