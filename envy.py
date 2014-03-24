import re

class Items():
  "Place to read/write/show named fields."
  def items(i) : return i.__dict__ 
  def override(i,d): i.items().update(d); return i
  def also(i, **d) : i.override(d)
  def __repr__(i) : 
      return '{'+ ' '.join([':%s %s' % (k,v) 
                   for k,v in
                   sorted(i.items().items())
                    if not "_" in k])  + '}'

class Slots(Items):
  "Items with a unique Id"
  id = -1
  def __init__(i,**d) : 
    i.id = Slots.id = Slots.id + 1
    i.override(d)
  def __eq__(i,j)  : return i.id == j.id   
  def __ne__(i,j)  : return i.id != j.id   


The=Slots(reader = Slots(bad     = r'(["\' \t\r\n]|#.*)',
                         filter  = lambda x: atom(x),
                         keeping = '$=.<>!',
                         char    = Slots(sep=",",
                                         skip = '?')),
           nums = Slots(cache=128,
                        bins=5,
                        tiny=0.1, # dull= 60%-50% 
                        enough=10) 
)

def atom(x):
  try: return float(x)
  except: return x

def identity(X): return x

def item(x) : 
  if isa(x,(tuple,list)):
    for y in x:
      for z in item(y): yield z
  else: yield x

def rows(file, 
          sep   = The.reader.char.sep,
          bad   = The.reader.bad,
          filter= The.reader.filter):
  """Read comma-eperated rows that might be split 
  over many lines.  Finds strings that can compile 
  to nums.  Kills comments and white space."""
  n,kept = 0,""
  for line in open(file):
    now   = re.sub(bad,"",line)
    kept += now
    if kept:
      if not now[-1] == sep:
        yield n, map(filter,kept.split(sep))
        n += 1
        kept = "" 

def row(file,skip=The.reader.char.skip):
  "Leaps over any columns marked 'skip'."
  todo = None
  for n,line in rows(file):
    todo = todo or [col for col,name in enumerate(line) 
                    if not skip in name]
    yield n, [ line[col] for col in todo ]

def table(source, rows = True, contents = row):
  t= table0(source)
  for n,cells in contents(source):  
    if n == 0: head(cells,t) 
    else     : body(cells,t,rows) 
  return t

def table0(source, keepers= The.reader.keeping):
  t = Slots(source=source, headers={}, _rows=[],at={})
  for keeper in keepers: 
    t.headers[keeper] = []
  return t

def head(cells,t, keepers= The.reader.keeping):
  num = keepers[0]
  for col,cell in enumerate(cells):
    what   = Num if num in cell else Sym
    header = what()
    header.col, header.name = col,cell
    t.at[cell] = header
    for keeper in keepers:
      if keeper in cell:
        t.headers[keeper] += [header]

def body(cells,t,rows):
  for header in  t.at.values():
    header + cells[header.col]
  if rows: 
    t._rows += [cells]

class Sym(Items):
  "An Accumulator for syms"
  def __init__(i): 
    i.n=i.most=0; i.mode= None; i.counts={}
  def __add__(i,x):
    i.n += 1    
    new  = i.counts.get(x,0) + 1
    if new > i.most:
      i.most, i.mode = new, x
    i.counts[x] = new

class Num(Items):
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
  def median(i) : i.ok(); return i._median 
  def breaks(i) : i.ok(); return i._breaks
  def ok(i):
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

def _disc1():
  t= table("nasa93less.csv")
  for name,col in t.at.items():
    print "\n",name
    if isinstance(col,Sym):
      for key,count in col.counts.items():
        print "\t",key,count
    else:
      for key,x in enumerate(col.some.breaks()): 
        print "\t",key,x

_disc1()
