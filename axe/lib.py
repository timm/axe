from __future__ import division
import sys,re,random
sys.dont_write_bytecode = True

seed = random.seed
any  = random.choice

def says(*lst):
  say(', '.join(map(str, lst)))

def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def atoms(str,sep=',', bad=r'(["\' \t\r\n]|#.*)'):
  str = re.sub(bad,"",str)
  if str:
    return map(atom,str.split(sep))

isa = isinstance
def nump(x)  : return isa(x,(int,long,float,complex))          
def listp(x) : return isa(x,(list,tuple))

class Bag():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i.id = Bag.id = Bag.id + 1
  def also(i,**d)  : i.override(d) 
  def override(i,d): i.__dict__.update(d)
  def __repr__(i)  : return rprint(i)
  def __hash__(i)  : return i.id
  def __eq__(i,j)  : return i.id == j.id
  def __neq__(i,j) : return i.id != j.id

def rprintln(x) : return rprint(x,'\n')

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
    if isa(x,Bag):
      left,right,name='{','}',''
    say(tabs(dpth) + name + left + end)
    rprint(x.__dict__, end, dpth + 1)
    say(tabs(dpth) + right + end)

def align(lsts,sep=' '):
  "Print, filled to max width of each column."
  widths = {}
  for lst in lsts: # pass1- find column max widths
    for n,x in enumerate(lst):
      w = len('%s' % x)
      widths[n] = max(widths.get(n,0),w)
  for lst in lsts: # pass2- print to max width
    for n,x in enumerate(lst):
      say(('%s' % x).rjust(widths[n],' ')+sep)
    print ""
  print ""

def ditto(lst,old,mark="."):
  "Show 'mark' if an item of  lst is same as old."
  out = []
  for i,now in enumerate(lst):
    before = old.get(i,None) # get old it if exists
    out   += [mark if  before == now else now]
    old[i] = now # next time, 'now' is the 'old' value
  return out # the lst with ditto marks inserted
