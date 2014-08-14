"""
about.py: meta-knowledge of variables
Copyright (c) 2014 tim.menzies@gmail.com
 ______      __                          __      
/\  _  \    /\ \                        /\ \__   
\ \ \L\ \   \ \ \____    ___    __  __  \ \ ,_\  
 \ \  __ \   \ \ '__`\  / __`\ /\ \/\ \  \ \ \/  
  \ \ \/\ \   \ \ \L\ \/\ \L\ \\ \ \_\ \  \ \ \_ 
   \ \_\ \_\   \ \_,__/\ \____/ \ \____/   \ \__\
    \/_/\/_/    \/___/  \/___/   \/___/     \/__/
 
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and
associated documentation files (the "Software"), to
deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission
notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE."""                                                 
  
from __future__ import division
import sys,re,random,math
sys.dont_write_bytecode = True
from options import *
from lib import *
                                  
"""
Bout
|-- About
|-- |-- Schaffer
|-- About1
|-- |-- Id
|-- |-- Fixed
|-- |-- Sym
|-- |-- Num
"""             

class Bout(object): 
  def ok(i,x)   : pass
  def guess(i,old,control=None): pass
  def __repr__(i): return prettyd(i)
  
class About(Bout):
  def __init__(i,cols=[]):
    i.depen, i.indep,  i.nums, i.syms= [],[],[],[] 
    i.more,  i.less, i.about, i.where = [],[],[],{}
    i.cols(cols)
  def cols(i,lst,numc=The.sym.numc):
    for col,header in enumerate(lst): 
      header.col = col
      i.where[header.name] = col
      for pattern,val in The.sym.patterns.items():
        if re.search(pattern,header.name):
          val(i).append(header)
  def ok(i,lst):
    for about,x in zip(i.about(),lst):
      if not about.ok(x):
        return False
    return True
  def guess(i,olds=None,control=None):
    lst = olds or [None] * len(i.about)
    for header,old in zip(i.indep,lst):
      lst[header.col] = header.guess(old)
    return lst
  def score(i,lst): pass
  def set(i,name,lst, val):
    print name
    lst[i.where[name].col] = val
    return val
  def get(i,lst,name):
    print name
    return lst[i.where[name].col]

class Schaffer(About):
  def __init__(i):
    super(Schaffer,i).__init__()
    i.cols([ Num(name='$x', 
                 bounds = (-10000,10000))
            ,Num(name='<f1')
            ,Num(name='<f2')
             ])
  def score(i,lst):
    x = i.get(lst, "$x")
    i.set("<f1", lst, x**2       )
    i.set("<f2", lst, (x - 2)**2 )
    
def _schaffered1():
  s= Schaffer()
  print "\n:about", s.about
  print "\n:indep", s.indep
  print "\n:depen", s.depen
  
def _schaffered2():
  rseed()
  about= Schaffer()
  for _ in range(10):
    one = about.guess()
    about.score(one)
    print one
    
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
  """Num has 'bounds' of legal (min,max) values as well
   as well as observed 'lo','hi' nums seen so far."""
  def __init__(i,inits=[],name='',
               bounds=(The.math.ninf, The.math.inf)):
    i.zero()
    i.name = name
    i.bounds = bounds
    for x in inits: i.inc(x)
  def ok(i,n):
    "Legal if in bounds (or unknown)"
    if n == The.sym.missing:
      return True
    if n == i.bounds: return True
    return i.bounds[0] <= n < i.bounds[1]
  def guess(i,old):
    "Use old values to guess new value."
    if i.n > The.math.centralLimitThreshold:
      return random.gauss(i.mu,i.sd())
    else:
      lo,hi = i.bounds[0], i.bounds[1]
      return lo + rand()*(hi - lo)
  def zero(i):
    "Reset all knowledge back to Eden."
    i.lo,i.hi = The.math.inf,The.math.ninf
    i.n = i.mu = i.m2 = 0
  def __lt__(i,j): 
    "Sorting function."
    return i.mu < j.mu
  def __iadd__(i,x): i.inc(x); return i
  def __isub__(i,x): i.sub(x); return i
  def inc(i,x):
    "Remember 'x'."
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  def sub(i,x):
    "Forget 'x'."
    if i.n < 2:  return i.zero()
    i.n  -= 1
    delta = x - i.mu
    i.mu -= delta/(1.0*i.n)
    i.m2 -= delta*(x - i.mu) 
  def sd(i) :
    "Diversity around the mean"
    if i.n < 2: return 0 
    return (max(0,i.m2)/(i.n - 1))**0.5
  def norm(i,x):
    "Map 'x' to 0..1 for lo..hi"
    return (x - i.lo)/ (i.hi - i.lo + 0.00001)
  def t(i,j):
    "Difference in means, adjusted for sd."
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
    "Test for statistically significant difference"
    v     = i.n + j.n - 2
    pairs = threshold[conf]
    delta = intrapolate(v,pairs)
    return delta >= i.t(j)


if __name__ == "__main__": eval(cmd())
