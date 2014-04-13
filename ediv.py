"""
#<
ediv: entropy-based division of numerics .
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved.  

This code implements the Fayyad and Irani MDL
discretizer of numerics as described in Supervised
and Unsupervised Discretization of Continuous
Features, James Dougherty, Ron Kohavi, Mehran
Sahami, ICML'95
  
Redistribution and use in source and binary forms,
with or without modification, are permitted provided
that the following conditions are met:

1. Redistributions of source code must retain the
above copyright notice, this list of conditions and
the following disclaimer.

2. Redistributions in binary form must reproduce the
above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the
names of its contributors may be used to endorse or
promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS
AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

###################################################
"""

import sys,random
sys.dont_write_bytecode = True

def ediv(lst,num=lambda x:x[0], sym=lambda x:x[1]):
  "Divide lst of (numbers,symbols) using entropy."
  import math
  def log2(x) : return math.log(x,2)
  #----------------------------------------------
  class Counts(): # Add/delete counts of symbols.
    def __init__(i,inits=[]):
      i.n, i._e = 0, None
      i.cache = {}
      for symbol in inits: i + symbol
    def __add__(i,symbol): i.inc(symbol,  1)
    def __sub__(i,symbol): i.inc(symbol, -1)
    def inc(i,symbol,n=1): 
      i._e = None
      i.n += n
      i.cache[symbol] = i.cache.get(symbol,0) + n
    def k(i)  : return len(i.cache.keys())
    def ke(i) : return i.k()*i.ent()
    def ent(i): 
      if i._e == None: 
        i._e = 0
        for symbol in i.cache:
          p  = i.cache[symbol]*1.0/i.n
          if p: i._e -= p*log2(p)*1.0
      return i._e
  #----------------------------------------------
  def recurse(lst):
    cut,e = ecut(lst,sym)
    if cut: 
      recurse(lst[:cut])
      recurse(lst[cut:])
    else:   
      cuts.append((e,lst))
    return cuts
  #----------------------------------------------
  def ecut(lst,sym): # Find best division of lst.
    lhs,rhs   = Counts(), Counts(sym(x) for x in lst)
    k, e, ke  = rhs.k(), rhs.ent(), rhs.ke()
    cut,min,n = None, e, len(lst)*1.0
    for j,x  in enumerate(lst):
      maybe = lhs.n/n*lhs.ent() + rhs.n/n*rhs.ent()
      if maybe < min :  
        gain  = e - maybe
        delta = log2(3**k-2)- (ke- rhs.ke()-lhs.ke())
        if gain >= (log2(n-1) + delta)/n: 
          cut,min = j,maybe
      rhs - sym(x)
      lhs + sym(x)    
    return cut,min
  #---| main |----
  cuts = []
  if lst: 
    return recurse(sorted(lst,key=num))

def _ediv():
  "Demo code to test the above."
  import random
  bell= random.gauss
  random.seed(1)
  def go(lst):
    print ""; print lst[:10]
    for d in  ediv(lst):
      print d[1][0][0]
  X,Y="X","Y"
  go([(1,X),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,Y),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,X),(2,X),(3,X),(4,X),(11,X),(12,X),(13,X),(14,X)])
  go([(64,X),(65,Y),(68,X),(69,Y),(70,X),(71,Y),
      (72,X),(72,Y),(75,X),(75,X),
      (80,Y),(81,Y),(83,Y),(85,Y)])
  l=[]
  for _ in range(1000): 
    l += [(bell(20,1),  X),(bell(10,1),Y),
          (bell(30,1),'Z'),(bell(40,1),'W')] 
  go(l)
  go([(1,X)])
  
_ediv()

"""
Output:

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')]
1
11

[(1, 'Y'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')]
1

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'X'), (12, 'X'), (13, 'X'), (14, 'X')]
1

[(64, 'X'), (65, 'Y'), (68, 'X'), (69, 'Y'), 
 (70, 'X'), (71, 'Y'), (72, 'X'), (72, 'Y'), 
 (75, 'X'), (75, 'X')]
64

[(21.288184753155463, 'X'), (11.44944560869977, 'Y'), 
 (30.066335808938263, 'Z'), (39.23545634902837, 'W'), 
 (18.90782678489586, 'X'), (10.031334516831716, 'Y'),
  (28.977896829989128, 'Z'), (38.56317055489747, 'W'), 
 (20.199311976483752, 'X'), (10.133374604658606, 'Y')]
6.90037812106
16.907507693
26.850034984
36.8600218357

[(1, 'X')]
1
"""
