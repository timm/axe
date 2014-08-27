from __future__ import division
import sys, random
sys.dont_write_bytecode = True

### Place to store things and stuff ################
class Thing(object):
  def __init__(i,**d): i.__dict__.update(d)

### Place to store options #########################

The = Thing(cache= Thing(keep=128))

### Misc utils #####################################
rand= random.random

# seperate d sub-lists from print sublists
def hasd(d):
  name = d.__class__.__name__
  d=  d  if isinstance(d,dict) else d.__dict__
  for k in sorted(d.keys):
    val = k[d]
    if isinstance(val,(dict,Thing)):
      s += showd(d,lvl+1)
    else:
      s += '\n#   ' * lvl + (':%s %v' % (k,d[k]))
  return s

def g3(lst): return gn(lst,3)
def g0(lst): return gn(lst,0)

def gn(lst,n):
  fmt = '%.' + str(n) + 'f'
  return ', '.join([(fmt % x) for x in sorted(lst)])

### Classes ########################################

class Sample(Thing):
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],nump=True):
    i._cache,i.n,i._also = [],0,None
    i.nump = nump
    if i.nump:
      i.lo, i.hi = 10**32, -10**32
    for n in inits: i.__iadd__(n)
  def __iadd__(i,x):
    changed = False
    i.n += 1
    if i.nump:
      i.lo = min(x,i.lo)
      i.hi = max(x,i.hi)
    if len(i._cache) < The.cache.keep:
      changed = True
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._cache[int(rand()*The.cache.keep)] = x
    if changed: 
      i._also = None
    return i
  def median(i) : return i.also().median
  def iqr(i)    : return i.also().iqr
  def also(i):
    if not i._also:
      n = len(i._cache)
      lst = i._cache = sorted(i._cache)
      p = q = n//2
      if (n % 2) == 0 : q = p + 1
      i._also = Thing(
        median = (lst[p] + lst[q])*0.5,
        iqr    = lst[int(n*.75)] - lst[int(n*.5)])
    return i._also

###############################

class In:
  def __init__(i,lo=0,hi=1,txt=""):
    i.txt,i.lo,i.hi = txt,lo,hi
  def __call__(i): 
    return i.lo+(i.hi - i.lo)*rand()

class It:
  def __init__(i, indep=None, dep=None):
    i.indep, i.dep = indep,dep
  def __repr__(i):
    return ':indep %s :dep %s' % (
           g3(i.indep),g3(i.dep))

class Model:
  def __init__(i):
    i.of = i.spec()
    i.log= It(indep=[Sample() for _ in i.of.indep],
               dep =[Sample() for _ in i.of.dep])
  def indepIT(i):
    "Make new it."
    return It([f() for f in i.of.indep])
  def depIT(i,it):
    "Complete it's dep variables."
    it.dep = [f(it) for f in i.of.dep]
  def logIT(i,it):
    "Remember what we have see in it."
    for val,log in zip(it, i.log):
      if val != None:
        log += val
  def aroundIT(i,it,p=0.5):
    "Find some place around it."
    def n(val,f): 
      return f() if rand() < p else x
    old = it.indep
    new = [n(val,f) for val,f in zip(old,i.of.indep)]
    return It(indep=new, dep=old.dep)

#It = a class describing indep,dep pair

#it = actual values
#of = meta knowledge of members of it
#log = a record of things seen in it

class ZDT1(Model):
  def spec(i):
    return It(indep= [In(0,1,x) for x in range(30)],
              dep  = [i.f1,i.f2])
  def f1(i,it):
    return it.indep[0]
  def f2(i,it):
    return 1 + 9*sum(it.indep[1:]) / 29

z= ZDT1()
for _ in xrange(10000):
  it= z.indepIT()
  z.depIT(it)
  #print it
