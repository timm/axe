from __future__ import division
import sys
sys.dont_write_bytecode = True
import random
import life

def help(): print """
de.py: differential evolution 
Copyright (c) 2014 Tim Menzies

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from library import *

@settings
def mathings(): return Thing(
  inf = float("inf"),
  ninf = float("-inf"),
  seed = 1,
  tiny = 1/float("inf"),
  centralLimitThreshold=20)

@settings
def brinkings(): return Thing(
  tconf=0.95,
  hot = 102,
  _secret=30)

@settings
def symings(): return Thing(
  missing="?",
  numc     ='$',
  patterns = {
    '\$'     : lambda z: z.nums,
    '\.'     : lambda z: z.syms,
    '>'      : lambda z: z.more,
    '<'      : lambda z: z.less,
    '[=<>]'  : lambda z: z.depen,
    '^[^=<>]': lambda z: z.indep,
    '.'      : lambda z: z.headers})


def brinked():
  print The.brink

###################################################
#  utils

def rseed(n = The.math.seed): random.seed(n)
def div(x,y) : return x/(y+The.math.tiny)

###################################################
# Meta knowledge 'bout the objects

class Bout(object): 
  def ok(i,x)   : pass
  def guess(i,old): pass
  def __repr__(i): return prettyd(i)
  
class About(Bout):
  def __init__(i,cols=[]):
    i.depen, i.indep,  i.nums, i.syms= [],[],[],[] 
    i.more,  i.less, i.headers, i.where = [],[],[],{}
    i.cols(cols)
  def cols(i,lst):
    for n,one in enumerate(lst): i.has(n,one)
  def has(i,col,header,numc=The.sym.numc):
    if isinstance(col,str):
      this = Num if numc in header else Sym
      header = this(name=col)
    header.col = col
    i.where[col.name] = header
    for pattern,val in The.sym.patterns.items():
      if re.search(pattern,col.name):
        where  = val(i)
        where += [header]
  def ok(i,lst):
    for about,x in zip(i.about(),lst):
      if not about.ok(x):
        return False
    return True
  def guess(i,olds=None):
    lst = olds or [None] * len(i.headers)
    for header,old in zip(i.indep,lst):
      lst[header.pos] = header.guess(old)
    return lst
  def score(i): guess
  def set(i,name,lst, val):
    lst[i.where[name].col] = val
    return val
  def get(i,lst,name):
    return lst[i.where[name].col]

class Schaffer(About):
  def __init__(i):
    super(Schaffer,i).__init__()
    lohi = (-10000,10000)
    i.cols([ Num(name='$x', bounds = lohi)
            ,Num(name='<f1')
            ,Num(name='<f2')
           ])
  def score(i,lst):
    x = i.get(lst, "$x")
    i.set("<f1", lst, x**2       )
    i.set("<f2", lst, (x - 2)**2 )
    
    
    
      
             

###################################################
class About1(Bout):
  def about(i): i

class Id(About1):
  id=0
  def guess(i,old):
    x = Id.id = Id.id+1 
    return x

class Fixed(About1):
  def __init__(i):
    i.cache=None
  def guess(i,old):
    return i.cache

class Sym(About1) : pass

class Num(About1):
  "Num has 'bounds' of legal (min,max) values as well
   as well as "
  def __init__(i,inits=[],name='',
               bounds=(The.math.ninf, The.math.inf)):
    i.zero()
    i.name = name
    i.bounds = bounds
    for x in inits: i.inc(x)
  def ok(i,n):
    if n == The.sym.missing:
      return True
    if n == i.bound: return True
    return i.bound[0] <= n < i.bound[1]
  def guess(i,old):
    if i.n > The.math.centralLimitThreshold:
      return random.gauss(i.mu,i.sd())
    else:
      lo,hi = i.bound[0], i.bound[1]
      return lo + rand()*(hi - lo)
  def zero(i):
    i.lo,i.hi = The.math.inf,The.math.ninf
    i.n = i.mu = i.m2 = 0
  def __lt__(i,j): 
    return i.mu < j.mu
  def sd(i) :
     if i.n < 2: return 0 
     return (max(0,i.m2)/(i.n - 1))**0.5
  def __iadd__(i,x): i.inc(x); return i
  def __isub__(i,x): i.sub(x); return i
  def inc(i,x):
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    if i.n < 2:  return i.zero()
    i.n  -= 1
    delta = x - i.mu
    i.mu -= delta/(1.0*i.n)
    i.m2 -= delta*(x - i.mu) 
  def norm(i,x):
    return (x - i.lo)/ (i.hi - i.lo + 0.00001)
  def t(i,j):
    signal = abs(i.mu - j.mu)
    noise  = (i.sd()**2/i.n + j.sd()**2/j.n)**0.5
    return signal / noise
  def same(i,j,
           conf=The.brink.tconf,
           threshold={.95:((  1, 12.70 ),( 3, 3.182),
                           (  5,  2.571),(10, 2.228),
                           ( 20,  2.086),(80, 1.99 ),
                           (320,  1.97 )),
                      .99:((  1, 63.657),( 3, 5.841),
                           (  5,  4.032),(10, 3.169),
                           ( 20,  2.845),(80, 2.64 ),
                           (320,  2.58 ))}):
    v     = i.n + j.n - 2
    pairs = threshold[conf]
    delta = intrapolate(v,pairs)
    return delta >= i.t(j)
  
def intrapolate(x, points):
  """find adjacent points containing 'x',
   return 'y', extrapolating over neighbor 'x's"""
  lo, hi = points[0], points[-1]
  x1, y1 = lo[0], lo[1]
  if x < x1: return y1
  for x2,y2 in points[1:]:
    if x1 <= x < x2:
      deltay = y2 - y1
      deltax = (x- x1)/(x2- x1)
      return y1 + deltay * deltax
    x1,y1 = x2,y2
  return hi[1]

@test
def numed():
  "check the Num class"
  rseed(1)
  def push(x,n=0.2):
    return x*(1 + n*rand())
  n1=Num(x    for x in range(30))
  n2=Num(30+x for x in range(30))
  lst1 = [x   for x in range(30)]
  n3, n4 = Num(lst1), Num()
  for x in lst1:  n4 += x
  for x in lst1: n4 -= x
  n5 = Num(0.0001+x for x in range(30))
  return [14.5, n1.mu
         ,8.80, g2(n1.sd())
         ,30,   n2.lo
         ,59,   n2.hi
         ,0,    n4.sd()
         ,0,    n4.n
         ,True, n5.same(n1)
         ,False,n5.same(n2)
         ]

test(); exit()

def interpolated(n=1.5): 
  print interpolate(n, [(1,10),(2, 20),(3, 30)])

################################################################### Models

def what(): print "de@tim.2014"

#Schaffer()

if __name__ == "__main__": eval(cmd("life.life()"))
