from __future__ import division
import sys
from lib import *
sys.dont_write_bytecode = True

class Sym(Slots):
  def __init__(i,inits=[]): 
    i.n,i.counts,i._also = 0,{},None
    for symbol in inits: i + symbol
  def __add__(i,symbol): i.inc(symbol,  1)
  def __sub__(i,symbol): i.inc(symbol, -1)
  def inc(i,x,n=1):
    i._also = None
    i.n += n
    i.counts[x] = i.counts.get(x,0) + n
  def k(i): 
    return len(i.counts.keys())
  def most(i): return i.also().most
  def mode(i): return i.also().mode
  def ent(i) : return i.also().e
  def also(i):
    if not i._also:
      e,most,mode = 0,0,None
      for symbol in i.counts:
        if i.counts[symbol] > most:
          most,mode = i.counts[symbol],symbol
        p = i.counts[symbol]/i.n
        if p: 
          e -= p*log2(p)
        i._also = Slots(most=most,mode=mode,e=e)
    return i._also

@test
def symed():
  "Counting symbols"
  s=Sym(list('first kick I took was when I hit'))
  return {' '  : s.mode(),
          7    : s.most(),
          3.628: round(s.ent(),3)}

class Sample(Slots):
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],opts=The.sample):
    i._cache,i.n,i.opts,i._also = [],0,opts,None
    for number in inits: i + number
  def __add__(i,x):
    i.n += 1
    if len(i._cache) < i.opts.keep: # if not full
      i._also = None
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if random.random() <= i.opts.keep/i.n:
        i._also=None
        i._cache[int(random.random()*i.ops.keep)] = x
  def median(i) : i.also().median
  def breaks(i) : i.also().breaks
  def also(i):
    if not i._also:
      lst  = i._cache
      n    = len(lst)
      lst  = sorted(lst)
      p= q = int(n*0.5)
      r    = int(n*(0.5 + i.opts.tiny))
      dull = lst[r] - lst[p]
      if n % 2: q = p + 1
      i._also = Slots(
        median = (lst[p] + lst[q])*0.5,
        breaks = chops(lst, opts=i.opts,
                        sorted=True, dull=dull))
    return i._also
 
@test
def sampled():
  seed()
  s=Sample(rand()**2 for _ in range(20))
  print s.breaks()
  return {1:1}
  
def chops(lst,sorted=False,dull=0,opts=The.sample):
  def chop(bins, before, i):
    rest = len(lst) - i
    if rest < opts.enough:
      return []
    j   = int(i + rest/bins)
    while j < len(lst) and lst[j] <= before+dull:
      j += 1
    if j >= len(lst):
      return []
    now = lst[j]
    return [now] + chop(bins - 1, now,j)
  lst = lst if sorted else sorted(lst)
  now = lst[0]
  return [now] + chop(i.opts.bins, now,0)

class Num(Slots):
  "An Accumulator for numbers"
  def __init__(i,init=[],
                tiny=0.1,
                 opts=The.sample):
    i.n = i.m2 = i.mu = 0.0
    i.hi, i.lo = -1*10**32, 10**32
    i.some = Sample(cache=cache,bins=bins,tiny=tiny)
    for x in init: i + x
  def s(i) : return (i.m2/(i.n - 1))**0.5
  def __lt__(i,j): return i.mu < j.mu
  def __add__(i,x):
    i.some + x
    if x > i.hi: i.hi = x
    if x < i.lo: i.lo = x
    i.n   += 1    
    delta  = x - i.mu
    i.mu  += delta/i.n
    i.m2  += delta*(x - i.mu)

if __name__ == '__main__': eval(cmd())
