import sys
from bag import *
from lib import *
sys.dont_write_bytecode = True

class Sym(Bag):
  def __init__(i,inits=[]): 
    i.n,i.most,i.mode,i._e = 0,0,0,None
    i.counts = {}
    for symbol in inits: i + symbol
  def __add__(i,symbol): 
    i.inc(symbol,  1)
  def __sub__(i,symbol): 
    i.most = i.mode = None 
    i.inc(symbol, -1)
  def inc(i,x,n=1):
    i._e = None
    i.n += n
    new  = i.counts.get(x,0) + n
    if new > i.most:
      i.most, i.mode = new, x
    i.counts[x] = new
  def k(i): 
    return len(i.cache.keys())
  def ent(i): 
    if i._e == None: 
      i._e = i.most = i.mode = 0
      for symbol in i.counts:
        if i.counts[symbol] > i.most:
          i.most,i.mode = i.counts[symbol],symbol
        p = i.counts[symbol]*1.0/i.n
        if p: i._e -= p*log2(p)*1.0
    return i._e

class Num(Bag):
  "An Accumulator for numbers"
  def __init__(i,init=[],
               cache=The.nums.cache,
               bins = The.nums.bins,
               tiny = The.nums.tiny): 
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
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)

class Sample(Items):
  "Keep a random sample of stuff seen so far."
  def __init__(i,cache = 128, bins = 7, tiny=0.1):
    i._cache, i.size, i.n = [], cache, 0.0
    i.bins, i.tiny = bins, tiny
    i.stale()
  def stale(i)  : i._median,i._breaks = None,None
  def median(i) : i.fresh(); return i._median 
  def breaks(i) : i.fresh(); return i._breaks
  def fresh(i):
    if not i._median: 
      lst  = i._cache
      n    = len(lst)
      lst  = sorted(lst)
      p= q = int(n*0.5)
      r    = int(n*(0.5 + i.tiny))
      dull = lst[r] - lst[p]
      if n % 2: q = p + 1
      i._median = (lst[p] + lst[q])*0.5
      i._breaks = chops(lst, bins=i.bins,
                        sorted=True, dull=dull)
  def __add__(i,x):
    i.n += 1
    if len(i._cache) < i.size : # if cache not full
      i.stale()
      i._cache += [x]           # then add
    else: # otherwise, maybe replace an old item
      if random.random() <= i.size/i.n:
        i.stale()
        i._cache[int(random.random()*i.size)] = x

def chops(lst,
          sorted= False,
          dull  = 0,
          bins  = 7,
          enough= The.nums.enough):
  def chop(bins, before, i):
    rest = len(lst) - i
    if rest < enough:
      return []
    inc = rest*1.0/bins
    j   = int(i + inc)
    while j < len(lst) and lst[j] <= before+dull:
      j += 1
    if j >= len(lst):
      return []
    now = lst[j]
    return [now] + chop(bins - 1, now,j)
  if not sorted:
    lst   = sorted(lst)
  now   = lst[0]
  return [now] + chop(bins, now,0)
