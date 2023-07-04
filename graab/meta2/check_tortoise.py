# coding=utf-8
""" check_tortoise.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def find_instances(lines):
 d = {} # key is line number. value is list of regex matches
 metaline = None
 regexraw = r'〔.*?〕'
 regex = re.compile(regexraw)
 n = 0
 for iline,line in enumerate(lines):
  if line.startswith('<L>'):
   metaline = line
   #continue
  a = re.findall(regex,line)
  if a != []:
   lnum = iline + 1
   d[lnum] = (metaline,a)
   n = n + len(a)
 print(n,'instances found')
 return d


def write_instances(fileout,d):
 keys = d.keys() # lnum
 keys = sorted(keys)
 # generate change transactions
 outarr = []
 for lnum in keys:
  val = d[lnum]
  (metaline,instances) = val
  s = ' : ' . join(instances)
  outarr.append('%s\t%s' %(lnum,s))
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')
 print(len(outarr),"records written to",fileout)

if __name__=="__main__":
 filein = sys.argv[1]  # temp_graab_x
 fileout = sys.argv[2] # 
 lines = read_lines(filein)
 instancesd = find_instances(lines)
 write_instances(fileout,instancesd)
 


