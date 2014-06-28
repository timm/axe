from __future__ import division
from lib    import *
from demos  import *
from counts import *
import sys
sys.dont_write_bytecode = True

@demo
def dtreed(f='data/weather.csv'):
  t=table(f)
  

def esplit(lst, tiny=The.treeings.min,
         num=lambda x:x.cells[0], 
         sym=lambda x:x.cells[-1]):
  "Divide lst of (numbers,symbols) using entropy."
  def divide(this): # Find best divide of 'this' lst.
    def ke(z): return z.k()*z.ent()
    lhs,rhs   = Sym(),Sym(sym(x) for x in this)
    n0,k0,e0,ke0= 1.0*rhs.n,rhs.k(),rhs.ent(),ke(rhs)
    cut, least  = None, e0
    for j,x  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.ent()+ rhs.n/n0*rhs.ent()
        if maybe < least :  
          gain = e0 - maybe
          delta= log2(3**k0-2)-(ke0- ke(rhs)-ke(lhs))
          if gain >= (log2(n0-1) + delta)/n0: 
            cut,least = j,maybe
      rhs - sym(x)
      lhs + sym(x)    
    return cut,least
  return divide(sorted(lst,key=num),[])

