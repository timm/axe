"""
#<
ediv: entropy-based division of numerics
Copyright (c) 2014, Tim Menzies, tim.menzies@gmail.com
All rights reserved.  
  
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

import sys,math
sys.dont_write_bytecode = True
log=math.log

class Counts():
  "Place to add/delete counts of symbols."
  def __init__(i,inits=[]):
    i.n = 0
    i.cache = {}
    for symbol in inits:  i + symbol
  def __add__(i,symbol) :
    i.n += 1
    i.cache[symbol] = i.cache.get(symbol,0) + 1
  def __sub__(i,symbol) : 
    i.n -= 1
    i.cache[symbol] = i.cache.get(symbol,0) - 1
  def ent(i):
    e = 0
    for symbol in i.cache:
      p  = i.cache[symbol]*1.0/i.n
      if p:
        e -= p*log(p)*1.0/log(2)
    return e

def ediv(pairs,gets,cuts):
  "Divide pairs of (numbers,symbols) using entropy."
  cut,e = ecut(pairs,gets)
  if cut:
    ediv(pairs[:cut], gets, cuts)
    ediv(pairs[cut:], gets, cuts)
  else:
    cuts += [(e,pairs)]
  return cuts
 
def ecut(pairs,(num,sym),min=3):
  "Find best place to divide pairs of (num,sym)."
  cut,least= None,None
  left     = Counts()
  right    = Counts(sym(x) for x in pairs)
  n        = len(pairs) * 1.0
  least    = right.ent()
  for j,x  in enumerate(pairs):
    n1,n2 = left.n, right.n
    if n1 > min and n2 > min:
      tmp = n1/n*left.ent() + n2/n*right.ent()
      if tmp < least :
        cut,least = j,tmp
    right - sym(x)
    left  + sym(x)    
  return cut,least

def _ediv():
  "Demo code to test the above."
  def first(x) : return x[0]
  def second(x) : return x[1]
  def go(lst):
    print ""; print lst
    for d in  ediv(sorted(lst,key=first),(first,second),[]):
      print d[1][0][0]
  X,Y="X","Y"
  go([(1,X),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,Y),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,X),(2,X),(3,X),(4,X),(11,X),(12,X),(13,X),(14,X)])
  go([(64,X),(65,Y),(68,X),(69,Y),(70,X),(71,Y),
      (72,X),(72,Y),(75,X),(75,X),
      (80,Y),(81,Y),(83,Y),(85,Y)])

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
11

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'X'), (12, 'X'), (13, 'X'), (14, 'X')]
1


[(64, 'X'), (65, 'Y'), (68, 'X'), (69, 'Y'), (70, 'X'), (71, 'Y'), 
 (72, 'X'), (72, 'Y'), (75, 'X'), (75, 'X'), 
 (80, 'Y'), (81, 'Y'), (83, 'Y'), (85, 'Y')]
64
72
80
"""

