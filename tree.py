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
  name=''
  if not isinstance(d,dict):
    name = d.__class__.__name__
    d    = d.__dict__
  return name + '{'+ ' '.join([':%s %s' % (k,v)
            for k,v in sorted(d.items())
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

class Bag():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i.id = Bag.id = Bag.id + 1
  def also(i,**d)   : i.override(d) 
  def override(i,d) : i.__dict__.update(d)
  def __repr__(i)   : return showd(i)

class Col(object):
  def __init__(i,name,pos):
    i.name, i.pos = name,pos
    i._where = DefaultDict(default=lambda:[])
  def seen(i,x,at):
    i._where[x] += [at]
    return x
  def __repr__(i) : return showd(i)

class Num(Col): pass
 
class Sym(Col):
  def __init__(i,name,pos):
    super(Sym,i).__init__(name,pos)
    i.counts = Counts()
  def seen(i,x,at) : 
    i.counts[x] += 1; 
    return super(Sym,i).seen(x,at) 

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

def newTable(cells):
  def what(txt,j): 
    klass = Num if '$' in txt else Sym
    return klass(txt,j)
  def nump(x):
    return isinstance(x,(float,int))
  t = Bag(rows = [],
          cols = [what(txt,pos) for pos,txt
                  in enumerate(cells)])
  t.dep   = t.cols[-1]
  t.indep = t.cols[:-1]
  t.nums  = [c for c in t.indep if nump(c)]
  t.syms  = [c for c in t.cols  if not nump(c)]
  return t

def newRow(t,cells):
  row = Bag(of = t)
  row.cells = [col.seen(cells[col.pos],row) 
               for col in t.cols] 
  t.rows += [row]
  return t

def table(lst,t = None):
  for cells in lst:
    if t : newRow(t,cells)
    else : t = newTable(cells)
  return t

# def nchops(t):
#   for num in t.nums:
#     t.chops=[]
#     ediv(
# (col,klass) for col in cols ]

# def chop(col,klass):
#   if col.nump: 
#    col.cuts = ediv(sorted(zip(col._all,klass._all)),[])
#   return col

# def ediv(pairs,cuts):
#   cut = ecut(pairs)
#   if cut:
#     cuts += [cut]
#     ediv(pairs[:cut],cuts)
#     ediv(pairs[cut:],cuts
#   return cuts

# def leftRight(all):
#   right = Counts(x for (_,x) in all)
#   left  = Counts()
#   for j,(num,klass) in enumerate(all):
#     right[klass] -= 1
#     left[klass]  += 1
#     yield j,left,right

# def ecut(all,min=2):
#   least, n = all.ent(), len(all)*1.0
#   cut,lefts,rights  = None,None,None
#   for j,left,right in leftRight(all):
#     n1,n2 = len(left), len(right)
#     if n1 > min and n2 > min:
#       tmp = n1/n*left.ent() + n2/n*right.ent()
#       if tmp < least :
#         cut,least,lefts,rights = j,tmp,left,right
#   return cut,left,right

for row in table(rows(golf)).rows:
  print "\n",row

