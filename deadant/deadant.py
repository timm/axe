from __future__ import print_function, division
import sys,math
sys.dont_write_bytecode = True

class o:
  def __init__(i,**d): i.has().update(d)
  def has(i)         : return i.__dict__

The=o(cache=o(dist=True))

def div(x,y): return x/(y+0.00001)
def lt(x,y) : return x<y
def gt(x,y) : return x>y

class Model: 
  id = 1
  def blank(i):
    id = Model.id = Model.id+1
    return o(id = id,
             x  = [None]*len(i.decisions()),
             y  = [None]*len(i.objectives()))
  memos = {}
  def dist(i,j,k):
    if not The.cache.dist: 
      return i.dist0(i,j,k)
    if j.id > k.id: 
      return i.dist(k,j):
    key = j.id,k.id
    if key in Model.memos: 
      return Model.memos[key]
    d= Model.memos[key] = dist0(i,j,k)
    return d
  def dist0(i,j,k):
    deltas,ws = 0,0
    for c in range(len(j.x)):
      n1 = i.norm(c, j.x[d])
      n2 = i.norm(c, k.y[d])
      deltas += (n1-n2)**2
      ws     += i.w(c)
    return deltas**0.5 / ws**0.5
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
  def decisions(i) : return [0,1,2,3,4]
  def objectives(i): return [0,1,2,3]
  def lo(i,c)      : return 0.0
  def hi(i,c)      : return 1.0
  def w( i,c)      : return 1 # min,max is -1,1
  def score(i,it):
    x, y = it.x, i.it.y
    y[0] = x[0] *  x[1]
    y[1] = x[2] ** x[3]
    y[2] = 2*x[3]*x[4] / (x[3] + x[4])
    y[3] = x[2]/(1 + math.e**(-1*x[2]))

def deadant(m,n=20):
  m = m()
  pop = [m.blank() for _ in range(n)]
  
