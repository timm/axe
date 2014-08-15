"""
sa101.py: simulated annealling
Copyright (c) 2014 tim.menzies@gmail.com

/\  _`\ /\  _  \              /' \  /'__`\  /' \    
\ \,\L\_\ \ \L\ \      __    /\_, \/\ \/\ \/\_, \   
 \/_\__ \\ \  __ \    /\_\   \/_/\ \ \ \ \ \/_/\ \  
   /\ \L\ \ \ \/\ \   \/_/_     \ \ \ \ \_\ \ \ \ \ 
   \ `\____\ \_\ \_\    /\_\     \ \_\ \____/  \ \_\
    \/_____/\/_/\/_/    \/_/      \/_/\/___/    \/_/                                                    
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
from lib import *

class Watch(object):
  def __iter__(i): return i
  def __init__(i,m):
    i.m = m
    i.step, i.jump = 0, 0
    i.logs = []
  def newLogs(i,at):
    tmp = i.m.clone()
    for one in tmp: one.at = at
    return tmp
  def seen(i,one):
    i.tick()
    i.logs[0].seen(one)
  def tick(i):
    i.step += 1
    if i.step > i.jump:
      if len(i.logs)> 1:
        one,two= i.logs[0], i.logs[1]
        if one.same(two):
          raise StopIteration()
      i.logs  = [i.newLogs(i.jump)] + i.logs
      i.jump += The.sa.era
    return i.step
  def next(i):
    if i.step <= The.sa.kmax:
      return i.tick()
    else:
      raise StopIteration()

w = Watch(10)
for x in w: 
  print x
  w.tick()
  w.tick()
  w.tick()

exit()

# def watch(report=f):
#   k = knext = 0
#   while k < (kmax):
#     k += 1
#     if k >= knext:
#       knext +=  The.sa.era 
#     log = Num()
#     logs = [log]+ logs
#     yield k,log,logs
#     if len(log) > 1:
#       if log[0].same(log[1]):
#         break
#   report(logs)
 
# def sa(model=Schaffer, p=The.sa.p, kmax=The.sa.kmax,
#        epsilon=The.sa.epsilon, seed=The.
#        runs=The.sa.runs,
#        stagger=The.sa.stagger): 
#   "Simulated annealing."
#   def baseline(): 
#     for _ in range(100): m.guess() 
#   def maybe(old,new,t): 
#     return math.e**((old - new)*1.0/max(1,t)) < rand()
#   def neighbor(lst):
#     for h in m.t.nums:
#       if rand() < p:
#         lst[h.pos] = any(h.lo,h.hi)
#     if m.valid(lst):
#       return m.seen(lst)
#     else:
#       return lst
#   def logs(lst=[]):
#     return  [Num()] + lst
  
#   #--------------------
  
#   rseed(seed)
#   for k,log, in xrange(kmax):
#     log = 
#     say('.')
#     m   = model()
#     baseline()
#     sb  = s = m.any()
#     eb  = e = fromhell(s, m.t)
#     for k,inner in do(range(kmax),
#                       epsilon,"best",era,also=outer):
#       sn = neighbor(s[:])
#       en = fromhell(sn,m.t)
#       if en > eb: 
#         sb,eb = sn,en
#       if en > e:
#         s,e = sn,en
#       elif maybe(e, en, k*1.0/kmax**stagger) :
#         s,e = sn,en
#       inner.seen(k, best=eb, every=e)
#   done(outer, 0,1,
#        key   = lambda z: '%2d'   % z,
#        value = lambda z: '%4.2f' % z)
