# coding=utf-8
""" vn_hws.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry

class unused_VNHW(object):
 def __init__(self,hw,hwtype):
  self.hw = hw
  self.hwtype = hwtype

def find_vn_hws(entries):
 recs = []
 for entry in entries:
  hw = entry.metad['k1']
  vntypes = []
  for line in entry.datalines:
   for hwtype in ["chg","del","add"]:
    if '<chg type="%s"'%hwtype in line:
     if hwtype not in vntypes:
      vntypes.append(hwtype)
    if '<info vn="%s'%hwtype in line:
     if hwtype not in vntypes:
      vntypes.append(hwtype)
  hw = entry.metad['k1']
  if vntypes != []:
   recs.append((hw,vntypes))
 return recs


def mergevn(vnrecs):
 d = {}
 hws = []
 for hw,vntypes in vnrecs:
  if hw not in d:
   d[hw] = []
   hws.append(hw)
  for vntype in vntypes:
   if vntype not in d[hw]:
    d[hw].append(vntype)
 recs = []
 # sort the hws
 slp_from = "aAiIuUfFxXeEoOMHkKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzsh"
 slp_to =   "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw"
 slp_from_to = str.maketrans(slp_from,slp_to)
 sorted_hws = sorted(hws,key = lambda x: x.translate(slp_from_to))
 for hw in sorted_hws:
  vntypes = d[hw]
  rec = (hw,vntypes)
  recs.append(rec)
 return recs

def write_vn_test(fileout,vnrecs):

 with codecs.open(fileout,"w","utf-8") as f:
  for vnrec in vnrecs:
   hw,vntypes = vnrec
   vntypes_str = ', '.join(vntypes)
   out = '%s %s' %(hw,vntypes_str)
   f.write(out+'\n')
 print(len(vnrecs),"records written to",fileout)

if __name__=="__main__":
 filein1 = sys.argv[1] # temp_gra_9.txt
 fileout = sys.argv[2] # 
 entries = digentry.init(filein1)
 vnrecs0 = find_vn_hws(entries)
 vnrecs = mergevn(vnrecs0)
 write_vn_test(fileout,vnrecs)
