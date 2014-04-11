import re,math

def golf(): return """
   outlook, $temp,$humidity,wind,play
   overcast, 83, 86, false, yes
   overcast, 64, 65, true, yes
   overcast, 72, 90, true, yes
   overcast, 81, 75, false, yes
   rainy, 70, 96, false, yes
   rainy, 68, 80, false, yes
   rainy, 65, 70, true, no
   rainy, 75, 80, false, yes
   rainy, 71, 91, true, no
   sunny, 85, 85, false, no
   sunny, 80, 90, true, no
   sunny, 72, 95, false, no
   sunny, 69, 70, false, yes
   sunny, 75, 70, true, yes
   """

def showd(d):
  """Catch key values to string, sorted on keys.
     Ignore hard to read items (marked with '_')."""
  d = d if  isinstance(d,dict) else d.__dict__
  return '{'+ ' '.join([':%s %s' % (k,v)
                        for k,v in
                        sorted(d.items())
                        if not "_" in k]) + '}'

class DefaultDict(dict):
  def __init__(i, default=lambda:[]):
    i.default = default
  def __getitem__(i, key):
    if key in i: return i.get(key)
    return i.setdefault(key,i.default())

class Counts(DefaultDict):
  def __init__(i,inits=[]):
    i.default = lambda :0
    for x in inits: i + x
  def __add__(i,x): i[x] += 1
  def ent(i):
    e = 0
    n = 1.0*len(i)
    for x in i:
      p = i[x]/n
      e -= p*log(p)/log(2)
    return e

class Slots():
  def __init__(i,**fields) : i.also(fields)
  def also(i,d)  : i.__dict__.update(d)
  def __repr_(i) : return showd(i)

class Col(object):
  def __init__(i,name,pos):
    i.name, i.pos = name,pos
    i.where = DefaultDict(default=lambda : [])
  def seen(i,x,y,at):
    i.where[(x,at)] += [y]
    return x

class Num(Col):
  def __init__(i,name,pos):
    i._pairs = name,pos,[]
    
  def seen(i,z,row) : 
    i._pairs += [(z,row)]; 
    return z
  def __repr__(i) : return 'Num'+showd(i)

class Sym:
  def __init__(i,name,pos):
    i.name,i.pos,i.counts = name,pos,Counts()
  def seen(i,z,row) : i.counts[z] += 1; return z
  def __repr__(i) : return 'Col'+showd(i)

def rows(f,
         sep=",",
         bad=r'(["\' \t\r\n]|#.*)'): 
  def atom(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError: return x 
  for row in f().splitlines():
    row = re.sub(bad,"",row)
    if row:
      yield map(atom,row.split(sep))

def table(lst,t = None):
  def what(txt,pos): 
    return (Num if '$' in txt else Sym)(txt,pos)
  for row in lst:
    if not t:
      t = Table(rows = [],
                cols = [what(txt,pos) for pos,txt
                        in enumerate(row)])
      t.dep   = t.cols[-1]
      t.indep = t.cols[:-1]
      t.nums  = [c for c in t.indep if type(c)=='Num']
      t.syms  = [c for c in t.cols  if type(c)!='Num']
    else:
      nth = len(t.rows)
      row = [col.seen(row[col],nth) for col in t.cols] 
      t.rows += [row]
  return t

def nchops(t):
  for num in t.nums:
    t.chops=[]
    edivnchop(col,klass) for col in cols ]

def chop(col,klass):
  if col.nump: 
   col.cuts = ediv(sorted(zip(col._all,klass._all)),[])
  return col

def ediv(pairs,cuts):
  cut = ecut(pairs)
  if cut:
    cuts += [cut]
    ediv(pairs[:cut],cuts)
    ediv(pairs[cut:],cuts)
  return cuts

def leftRight(all):
  right = Counts(x for (_,x) in all)
  left  = Counts()
  for j,(num,klass) in enumerate(all):
    right[klass] -= 1
    left[klass]  += 1
    yield j,left,right

def ecut(all,min=2):
  least, n = all.ent(), len(all)*1.0
  cut,lefts,rights  = None,None,None
  for j,left,right in leftRight(all):
    n1,n2 = len(left), len(right)
    if n1 > min and n2 > min:
      tmp = n1/n*left.ent() + n2/n*right.ent()
      if tmp < least :
        cut,least,lefts,rights = j,tmp,left,right
  return cut,left,right

print table(rows(golf))

