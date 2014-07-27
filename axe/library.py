from __future__ import division
import sys,re,random,math
sys.dont_write_bytecode = True

class Thing(object):
  def __init__(i,**fields) : i.override(fields)
  def also(i,**d)          : return i.override(d)
  def override(i,d)        : i.__dict__.update(d); return i

  def __repr__(i): return prettyd(i,"Thing")

def prettyd(i,name=None):
  "show public keys, in sorted order"
  def public(key): 
      return not key[0] == "_"
  me    = i.__dict__
  name = name or i.__class__.__name__
  order = sorted(k for k in me.keys() 
                 if public(k))
  pairs = [':%s %s' % (k,me[k]) for k in order]
  return name+'{'+ ', '.join(pairs) +'}'

def test(f=None,cache=[]):
  if f: 
    cache += [f]
    return f
  ok = no = 0
  for t in cache: 
    print '#',t.func_name ,t.__doc__ or ''
    prefix, n, found = None, 0, t() or []
    while found:
      this, that = found.pop(0), found.pop(0)
      if this == that:
        ok, n, prefix = ok+1, n+1,'CORRECT:'
      else: 
        no, n, prefix = no+1, n+1,'WRONG  :'
      print prefix,t.func_name,'test',n
  if ok+no:
    print '\n# Final score: %s/%s = %s%% CORRECT' \
        % (ok,(ok+no),int(100*ok/(ok+no)))

###################################################
# "The" settings

The = Thing()
def settings(f=None):
  if f : The.__dict__[f.func_name[:-4]] = f() 
  else : print The
  return f

####################################################
# Other utils

rand  = random.random
any   = random.choice
def shuffle(lst) : random.shuffle(lst); return lst

def first(x): return x[0]
def second(x): return x[1]
def third(x): return x[2]
def fourth(x): return x[3]
def fifth(x): return x[4]
def last(x): return x[-1]

### printing

def g1(x)    : return round(x,1)
def g2(x)    : return round(x,2)
def g3(x)    : return round(x,3)
def gs1(lst) : return map(g1,lst)
def gs2(lst) : return map(g2,lst)
def gs3(lst) : return map(g3,lst)

def nl(): print ""
def saysln(*lst): say(', '.join(map(str, lst))); nl()
def says(*lst)  : say(', '.join(map(str, lst)))
def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def cmd(com="life(1)"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'
