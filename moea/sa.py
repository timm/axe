from __future__ import division
import sys,random,life
sys.dont_write_bytecode = True

def copyleft(): print """
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


def brinked():
  print The.brink

###################################################
#  utils

def rseed(n = The.math.seed): random.seed(n)
def div(x,y) : return x/(y+The.math.tiny)

###################################################
# Meta knowledge 'bout the objects

  
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
