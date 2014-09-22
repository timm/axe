from __future__ import print_function, division
import sys,math,random
sys.dont_write_bytecode = True

any = random.choice

def one(lst): return lst[ int(any(len(lst))) ]
def any(n)  : return random.uniform(0,n)

def wiggle(lst):
  j = int(any(len(lst)))
  lst[0], lst[j] = lst[j],lst[0]
  return lst[0]

class o:
  def __init__(i,**d): i.has().update(d)
  def has(i)         : return i.__dict__

The=o(cache = o(dist=True),
      sym  = o(miss="?"))

def div(x,y): return x/(y+0.00001)
def lt(x,y) : return x<y
def gt(x,y) : return x>y

def  memo2(f):
  def wrapper(obj,j,k):  
    jid,kid = id(j),id(k)
    x = (jid,kid) if jid<kid else (kid,jid)
    if x in cache:
      return cache[x]
    else:
      tmp = cache[x] = f(obj,j,k)
      return tmp
  return wrapper

def distN(i,j,norm):
  if i==The.char.missing:
    j = norm(j)
    i = j if j > 0.5 else 1 - j 
  if j==The.char.missing:
    i = norm(i)
    j = i if i > 0.5 else 1 - i
  return abs(i - j)

def distS(i,j,ignore):
  if i==The.sym.miss or j=The.sym.miss:
    return 1
  else:
    return 0 if i==j else 1

class N: pass
class S: pass

class Model: 
  def __init__(i):
    i.decisions = []
    i.nums      = []
    i.syms      = []
    i.decLog    = []
    i.objLog    = []
    i.objectives= []
    i.less      = []
    i.more      = []
    i.lo        = lambda c: 0
    i.hi        = lambda c: 1
    i.w         = lambda c: 1
    i.eval      = lambda it: True
    i.spec()
  def i.spec(): pass
  def blank(i):
    return o(dead= False,
             x   = [None]*len(i.decisions()),
             y   = [None]*len(i.objectives())) 
  @memo2
  def dist(i,j,k):
    def inc(f,c,helper=None)
      v1, v2 = i[c], j[c]
      if not v1==v2==The.sym.miss:
        d        = f(v1,v2, helper)
        deltas  += d**2
        weights += i.w(c)
    deltas,weights = 0,0
    for c in i.nums:
      inc(distN, c, lambda: x:i.norm(c,x))
    for c in i.syms:
      inc(distS, c)
    return deltas**0.5 / weights**0.5
  def norm(i,c,x):
    return div(x - i.lo(c), i.hi(c) - i.lo(c))
  def furthest(i,j,all, init=0, better=gt):
    out,d= j,init
    for k in all:
      if not j.id == k.id:
        tmp = i.dist(j,k)
        if better(tmp,d): out,d = j,tmp
    return out
  def closest(i,j,all):
    return i.furthest(j,all, init=10**32, better=lt)
  def neighbors(i,j,all):
    return sorted([(i.dist(j,k),k) 
                   for k in all if not k.id == j.id])

class Schaffer(Model):
  def spec(i):
    i.decisions = [0,1,2,3,4]
    i.decLog    = [N,N,N,N,N]
    i.nums      = [0,1,2,3,4]
    i.syms      = []
    i.objectives= [0,1,2,3]
    i.objLog    = [N,N,N,N]
    i.less      = [0,  2  ]
    i.more      = [  1,  3]
    i.lo        = lambda z: 0
    i.hi        = lambda z: 1
    i.w         = lambda z: 1
    i.score     = lambda z: i.scores(z)
  def scores(i,it):
    x, y = it.x, i.it.y
    y[0] = x[0] *  x[1]
    y[1] = x[2] ** x[3]
    y[2] = 2*x[3]*x[4] / (x[3] + x[4])
    y[3] = x[2]/(1 + math.e**(-1*x[2]))

def deadant(m,n=20):
  m = m()
  pop = [m.blank() for _ in range(n)]
  k = 1000
  while k > 0:
    k += 1
    head = wiggle(pop)
    tail = pop[1:]
    one,two = m.neighbors(head,tail)[:2]
    if close(one):
      if one.dead:
        head.dead = True

"""
  try:
      cache = obj.__cache
    except AttributeError:
      cache = obj.__cache = {}
"""
