# coding=utf-8
""" reform.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Rvlink(object):
 def __init__(self,line):
  parts = line.split('\t')
  self.count = parts[0]
  self.old = parts[1]
  self.new = None
  self.tag = '?'
  
def init_rvlinks(filein):
 lines = read_lines(filein)
 recs = [Rvlink(line) for line in lines]
 print('%s non-standard rvlinks read from %s' % (len(recs),filein))
 return recs


def write_rvlinks(fileout,rvlinks):
 outarr = []
 for rvlink in rvlinks:
  if rvlink.new == None:
   out = '%s,%s\t%s' % (rvlink.count,rvlink.tag,rvlink.old)
  else:
   out = '%s,%s\t%s\t%s' % (rvlink.count,rvlink.tag,rvlink.old,rvlink.new)
  outarr.append(out)

 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(rvlinks),"lines written to",fileout)

def option_A(recs):
 # modify some recs
 # {A B} where
 # A = N,N.
 # B = N
 tag = 'A'
 n = 0 # number of recs changed
 for rec in recs:
  if rec.new != None:
   # already solved
   continue
  old = rec.old
  new = re.sub(r'^{([0-9]+),([0-9]+)\. ([0-9]+)}$',
             r'{\1,\2}. _{\1,\3}', old)
  if new == old:
   # this option does not apply
   continue
  # this option applies
  rec.new = new
  # Add the 'tag' to count
  rec.tag = tag
  n = n + 1
 print('option_%s %s changes' %(tag,n))

def option_B(recs):
 # modify some recs
 # {X Y ... Z} where
 # {A B ... Y Z} where
 # X = N,N.
 # B = N.
 # ....
 # Y = N.
 # Z = N
 tag = 'B'
 n = 0 # number of recs changed
 for irec,rec in enumerate(recs):
  if rec.new != None:
   # already solved
   continue
  old = rec.old  # {X}
  m = re.search(r'^{(.*)}$',old)
  data = m.group(1)  # X Y ...
  parts = data.split(' ')
  first = parts[0]
  m = re.search(r'^([0-9]+),([0-9]+)\.$',first)
  if m == None:
   continue
  base = m.group(1)
  second = m.group(2)
  ansarr = []
  ansarr.append('{%s,%s}.' % (base,second))
  problem = False
  nparts = len(parts)
  ilast = nparts - 1
  for ipart,part in enumerate(parts):
   if ipart == 0:
    continue
   if ipart == ilast: 
    m = re.search(r'^([0-9]+)$',part)
    if m == None:
     problem = True
     break
    second = m.group(1)
    ansarr.append('_{%s,%s}' % (base,second))
   else:
    # not the last part. period ends
    m = re.search(r'^([0-9]+)\.$',part)
    if m == None:
     problem = True
     break
    second = m.group(1)
    ansarr.append('_{%s,%s}.' % (base,second))
  #
  if problem:
   continue
  # this option applies
  new = ' '.join(ansarr)
  rec.new = new
  # Add the 'tag'
  rec.tag = tag
  n = n + 1
 print('option_%s %s changes' %(tag,n))

def C_helper_2(y):
 if y.endswith('.'):
  period = '.'
  z = y[0:-1]
 else:
  period = '' # no ending period
  z = y
 if re.search(r'^[0-9]+$',z):
  seconds = [z]
 else:
  m = re.search(r'^([0-9]+)—([0-9]+)$',z)
  if m == None:
   return None
  seconds = (m.group(1),m.group(2))
 ans = seconds,period
 return ans

def C_helper_1(x):
 # x = N0,s or N0,s. and 
 # s = N1 OR s = N1—N2
 # returns N0,N1,period  OR
 # N0,N1,N2,period  (where period = '.' or '')
 # if x is of different form, returns None
 parts = x.split(',')
 ansdefault = None
 if len(parts) != 2:
  return ansdefault
 base = parts[0]
 y = parts[1]
 temp = C_helper_2(y)
 if temp == None:
  return ansdefault
 seconds,period = temp
 ans = (base,seconds,period)
 return ans

def option_C(recs):
 # modify some recs
 # {A B ... Y Z} where
 # X = N,x.
 # B = x.
 # ....
 # Y = x.
 # Z = x
 # where either x = N  OR x = N1—N2
 tag = 'C'
 n = 0 # number of recs changed
 for irec,rec in enumerate(recs):
  if rec.new != None:
   # already solved
   continue
  dbg = False # 
  old = rec.old  # {X}
  if dbg: print('dbg begins for %s' % old)
  m = re.search(r'^{(.*)}$',old)
  data = m.group(1)  # X Y ...
  parts = data.split(' ')
  first = parts[0]
  temp = C_helper_1(first)
  if temp == None:
   # not applicable
   if dbg: print(' dbg 1',first)
   continue
  base,seconds,period = temp
  if (len(parts) == 1) and (period == '.'):
   # require no period
   if dbg: print(' dbg 2')
   continue   
  ansarr = []
  if len(seconds) == 1:
   ansarr.append('{%s,%s}%s' % (base,seconds[0],period))
  else:
   ansarr.append('{%s,%s}—_{%s,%s}%s' %(base,seconds[0],base,seconds[1],period))
  problem = False
  nparts = len(parts)
  ilast = nparts - 1
  for ipart,part in enumerate(parts):
   if ipart == 0:
    continue
   temp = C_helper_2(part)
   if temp == None:
    problem = True
    if dbg: print(' dbg 3, part=',part)
    break
   seconds,period = temp
   if (ipart == ilast) and (period == '.'):
    problem = True
    if dbg: print(' dbg 4, part=',part)
    break
   if (ipart < ilast) and (period == ''):
    problem = True
    if dbg: print(' dbg 5, part=',part)
    break
   if len(seconds) == 1:
    ansarr.append('_{%s,%s}%s' % (base,seconds[0],period))
   else:
    ansarr.append('_{%s,%s}—_{%s,%s}%s' %(base,seconds[0],base,seconds[1],period))
  if problem:
   continue
  # this option applies
  new = ' '.join(ansarr)
  rec.new = new
  # Add the 'tag'
  rec.tag = tag
  n = n + 1
 print('option_%s %s changes' %(tag,n))

def option_D(recs):
 # {N,N*} -> _{N,N}*
 tag = 'D'
 n = 0 # number of recs changed
 for rec in recs:
  if rec.new != None:
   # already solved
   continue
  old = rec.old
  new = re.sub(r'^{([0-9]+),([0-9]+)\*}$',
             r'{\1,\2}*', old)
  if new == old:
   # this option does not apply
   continue
  # this option applies
  rec.new = new
  # Add the 'tag' to count
  rec.tag = tag
  n = n + 1
 print('option_%s %s changes' %(tag,n))

def option_E(recs):
 # {N,Nx} -> _{N,N}x where x is [a-d]
 tag = 'E'
 n = 0 # number of recs changed
 for rec in recs:
  if rec.new != None:
   # already solved
   continue
  old = rec.old
  new = re.sub(r'^{([0-9]+),([0-9]+)([a-d])}$',
             r'{\1,\2}\3', old)
  if new == old:
   # this option does not apply
   continue
  # this option applies
  rec.new = new
  # Add the 'tag' to count
  rec.tag = tag
  n = n + 1
 print('option_%s %s changes' %(tag,n))


if __name__=="__main__":
 filein = sys.argv[1]  # oldrvlinks
 fileout = sys.argv[2] # newrvlinks
 recs = init_rvlinks(filein)
 option_A(recs)
 option_B(recs)
 option_C(recs)
 option_D(recs)
 option_E(recs)
 write_rvlinks(fileout,recs)

