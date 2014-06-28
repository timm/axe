from __future__ import division
from lib    import *
from demos  import *
from counts import *
from table  import *
import sys
sys.dont_write_bytecode = True

def discreteTable(f="data/diabetes.csv",contents=row):
  rows, t = [],  table0(f)
  for n,cells in contents(f):  
    if n==0 : head(cells,t) 
    else    : rows += [cells]
  for num in t.nums: 
    for cut in ediv(rows,1 if num.name=="$insu" else 0,
                  num=lambda x:x[num.col],
                  sym=lambda x:x[t.klass[0].col]):
      for row in cut._has:
        row[num.col] = cut.at
  return clone(t, discrete=True, rows=rows)

def ediv(lst, watch, lvl=0,tiny=The.tree.min,
         num=lambda x:x[0], sym=lambda x:x[1]):
  "Divide lst of (numbers,symbols) using entropy."
  #----------------------------------------------
  print watch
  def divide(this,lvl): # Find best divide of 'this' lst.
    print watch
    def ke(z): return z.k()*z.ent()
    lhs,rhs   = Sym(),Sym(sym(x) for x in this)
    if watch: print '|.. ' * lvl
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
  #--------------------------------------------
  def recurse(this, cuts,lvl):
    cut,e = divide(this,lvl)
    if watch == "1": print(num(x) for x in this)
    if cut: 
      print this[:cut]
      recurse(this[:cut], cuts, lvl+1); 
      recurse(this[cut:], cuts, lvl+1)
    else:   
      cuts += [Thing(at=num(this[0]),e=e,_has=this)]
    return cuts
  #---| main |-----------------------------------
  return recurse(sorted(lst,key=num),[],0)
   
@demo
def _fi1(f="data/diabetes.csv",contents=row):
  def discretize(rows,col,klass):
    return ediv(rows, 
                num = lambda row: row[col.col],
                sym = lambda row: row[klass.col])
  rows = []
  t0   = table0(f)
  for n,cells in contents(f):  
    if n == 0 : head(cells,t0) 
    else      : rows += [cells]
  for num in t0.nums: 
    #print num.name
    for split in discretize(rows,num,t0.klass[0]):
      print num.col, split.at, len(split._has)
      for row in split._has:
        row[num.col] = split.at
  print ""
  exit()
  for row in t0._rows:
    print row.cells
  t1 = clone(t0,
             discrete=True,
             rows=rows)
  print 1
  rprint(t1.headers)
  print 2
@demo
  
@demo
def _ediv():
  "Demo code to test the above."
  import random
  bell= random.gauss
  random.seed(1)
  def go(lst):
    print ""; print sorted(lst)[:10],"..."
    for d in  ediv(lst):
      rprint(d); nl()
  X,Y="X","Y"
  l=[(1,X),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)]
  go(l)
  l[0] = (1,Y)
  go(l)
  go(l*2)
  go([(1,X),(2,X),(3,X),(4,X),(11,X),(12,X),(13,X),(14,X)])
  go([(64,X),(65,Y),(68,X),(69,Y),(70,X),(71,Y),
      (72,X),(72,Y),(75,X),(75,X),
      (80,Y),(81,Y),(83,Y),(85,Y)]*2)
  l=[]
  for _ in range(1000): 
    l += [(bell(20,1),  X),(bell(10,1),Y),
          (bell(30,1),'Z'),(bell(40,1),'W')] 
  go(l)
  go([(1,X)])


  
if __name__ == '__main__': eval(cmd())
