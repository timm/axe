"""
sdiv: standard-division of numerics .
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved. 
      _____                                _______
    ,/_    ``-._                          /       \ 
   ,|:          `'-..__               ___|         |_
  ,|:_                 ``'''-----''''`_::~-.......-'~\ 
 ,|:_                                 _:    . ' .    :
 |:_                                  _:  .   '   .  |
 |:_                                  _:  '   .   '  |
 |:_                                  _:    ' . '    :
 |:_                    __,,...---...,,:_,.-'''''-.,_/
 |:_              _,.-``                 |         |
 |:_           ,-`                       |         |
 |:_         ,`                          |         |
 `|:_      ,'                            |         |
  |:_     /                              |         |
  `|:_   /                               |         |
   `|:_ :                                |         |
     \: |                                |         |
      \:|                                |         | cjr
       ~                                             

""" 

import sys,random
sys.dont_write_bytecode = True

def sdiv(lst, tiny=2,,cohen=0.3,
         num1=lambda x:x[0], num2=lambda x:x[1]):
  "Divide lst of (num1,num2) using variance of num2."
  #----------------------------------------------
  class Counts(): # Add/delete counts of numbers.
    def __init__(i,inits=[]):
      i.n = i.mu = i.m2 = 0.0
      for number in inits: i + number 
    def __add__(i,x):
      i.n  += 1
      delta = x - i.mu
      i.mu += delta/(1.0*i.n)
      i.m2 += delta*(x - i.mu)
    def __sub__(i,x):
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/n
      i.m2 -= delta*(x - i.mu)    
    def sd(i): return i.m2*1.0/(i.n -1)
  #----------------------------------------------
  def divide(this): # Find best divide of 'this' lst.
    lhs,rhs = Counts(),Counts(num2(x) for x in this)
    n0,sd0  = 1.0*rhs.n, rhs.sd()
    cut, least  = None, sd0
    for j,x  in enumerate(this): 
      if lhs.n > tiny and rhs.n > tiny: 
        maybe= lhs.n/n0*lhs.sd()+ rhs.n/n0*rhs.sd()
        if maybe < least :  
          if abs(lhs.mu - rhs.mu) >= cohen*sd0:
            cut,least = j,maybe
      rhs - num2(x)
      lhs + num2(x)    
    return cut,least
  #----------------------------------------------
  def recurse(this, cuts):
    cut,e = divide(this)
    if cut: 
      recurse(this[:cut], cuts)
      recurse(this[cut:], cuts)
    else:   
      cuts += [(e,this)]
    return cuts
  #---| main |-----------------------------------
  if lst: 
    return recurse(sorted(lst,key=num1),[])

def _sdiv():
  "Demo code to test the above."
  import random
  bell= random.gauss
  random.seed(1)
  def go(lst):
    print ""; print sorted(lst)[:10],"..."
    for d in  ediv(lst):
      print d[1][0][0]
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
  
if __name__ == '__main__': _ediv()

"""
Output:

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')] ...
1
11

[(1, 'Y'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')] ...
1

[(1, 'Y'), (1, 'Y'), (2, 'X'), (2, 'X'), 
 (3, 'X'), (3, 'X'), (4, 'X'), (4, 'X'), (11, 'Y'), (11, 'Y')] ...
1
11

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'X'), (12, 'X'), (13, 'X'), (14, 'X')] ...
1

[(64, 'X'), (64, 'X'), (65, 'Y'), (65, 'Y'), 
 (68, 'X'), (68, 'X'), (69, 'Y'), (69, 'Y'), (70, 'X'), (70, 'X')] ...
64
80

[(6.900378121061215, 'Y'), (7.038785729480842, 'Y'), 
 (7.31690058848835, 'Y'), (7.359039915634471, 'Y'), 
 (7.364480069138072, 'Y'), (7.553496312538384, 'Y'), 
 (7.581606303196569, 'Y'), (7.651878578401048, 'Y'), 
 (7.655341871448137, 'Y'), (7.677081766167625, 'Y')] ...
6.90037812106
16.907507693
26.850034984
36.8600218357

[(1, 'X')] ...
1



"""
