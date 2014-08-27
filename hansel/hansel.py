from __future__ import division
import sys, random
sys.dont_write_bytecode = True

rand= random.random

def g3(lst): return gn(lst,3)
def g0(lst): return gn(lst,0)

def gn(lst,n):
  fmt = '%.' + str(n) + 'f'
  return ', '.join([(fmt % x) for x in sorted(lst)])

class Thing(object):
  def __init__(i,**fields): i.override(fields)
  def also(i,**d)         : return i.override(d)
  def override(i,d): i.__dict__.update(d); return i

The = Thing(cache= Thing(keep=128))

class Sample(Thing):
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[]):
    i._cache,i.n,i._also = [],0,None
    i.lo, i.hi = 10**32, -10**32
    for n in inits: i.__iadd__(n)
  def __iadd__(i,x):
    i.n += 1
    i.lo = min(x,i.lo)
    i.hi = max(x,i.hi)
    changed = False
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
    i.indep = [] if indep==None else indep
    i.dep   = [] if dep  ==None else dep
  def __repr__(i):
    return ':indep %s :dep %s' % (
           g3(i.indep),g3(i.dep))

class Model:
  def __init__(i):
    i.of = i.spec()
    i.log= It(indep=[Sample() for _ in i.of.indep],
               dep =[Sample() for _ in i.of.dep])
  def guess(i):
    return It([r() for r in i.of.indep])
  def score(i,one):
    one.dep = [f(one) for f in i.of.dep]
  def seen(i,one):
    for val,log in zip(one, i.log):
      if val != None:
        log += val

#It = indep,dep pair

#one = actual values
#of = meta knowledge of members of one
#log = a record of things seen in one

class ZDT1(Model):
  def spec(i):
    return It(indep= [In(0,1,x) for x in range(30)],
              dep  = [i.f1,i.f2])
  def f1(i,one):
    return one.indep[0]
  def f2(i,one):
    return 1 + 9*sum(one.indep[1:]) / 29

z= ZDT1()
one= z.guess()
z.score(one)
print one
