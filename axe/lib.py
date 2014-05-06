from __future__ import division
import sys,re,random,math
sys.dont_write_bytecode = True

from demos    import *
from settings import *

rand = random.random
any  = random.choice
def seed(n = The.math.seed): random.seed(n)

### printing

def gs1(lst): return map(lambda x: round(x,1),lst)
def gs2(lst): return map(lambda x: round(x,2),lst)
def gs3(lst): return map(lambda x: round(x,3),lst)

def says(*lst):
  say(', '.join(map(str, lst)))
def say(x): 
  sys.stdout.write(str(x))
  sys.stdout.flush()

def rprintln(x): 
  return rprint(x,'\n')
def rprint(x, end=None, dpth=0):
  if end : space='  '
  else   : dpth,end,space = 1,'',' '
  tabs = lambda n : space * n
  q = lambda z : '\"%s\"'%z if isa(z,str) else str(z)
  def what2show(keys):
    return [k for k in sorted(keys) if not "_" in k]
  if isa(x,str) or nump(x):
    say(tabs(dpth) + q(x) + end)
  elif isa(x,dict):
    for key in what2show(x.keys()):
      value = x[key]
      say(tabs(dpth) + (':%s' % key))
      if isa(value,str) or nump(value):
        say(( ' %s' % q(value))+ end)
      else: 
        say(end)
        rprint(value, end, dpth + 1)
  elif listp(x):
    for something in x:
      rprint(something, end, dpth+1)
  else:
    left,right,name = '(',')',x.__class__.__name__
    if isa(x,Slots):
      left,right,name='{','}',''
    say(tabs(dpth) + name + left + end)
    rprint(x.__dict__, end, dpth + 1)
    say(tabs(dpth) + right + end)

def align(lsts,sep=' '):
  "Print, filled to max width of each column."
  width = {}
  for lst in lsts: # pass1- find column max widths
    for n,x in enumerate(lst):
      width[n] = max(widths.get(n,0),len('%s' % x))
  for lst in lsts: # pass2- print to max width
    for n,x in enumerate(lst):
      say(('%s' % x).rjust(width[n],' ')+sep)
    print ""
  print ""

### typings

isa  = isinstance
               
def nump(x)  : return isa(x,(int,long,float,complex))          
def listp(x) : return isa(x,(list,tuple))

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def atoms(str,sep=',', bad=The.string.white):
  str = re.sub(bad,"",str)
  if str:
    return map(atom,str.split(sep))

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'


def log2(x)  : return math.log(x,2)

def ditto(lst,old,mark="."):
  "Show 'mark' if an item of  lst is same as old."
  out = []
  for i,now in enumerate(lst):
    before = old.get(i,None) # get old it if exists
    out   += [mark if  before == now else now]
    old[i] = now # next time, 'now' is the 'old' value
  return out # the lst with ditto marks inserted


if __name__ == '__main__': eval(cmd())
