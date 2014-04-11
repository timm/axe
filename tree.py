import re,math

def golf(): return """
   outlook, temp,humidity,wind,play
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

class Col:
  def __init__(i,name):
    i.name=name
    i.nump=True
    i._all=[]
  def __add__(i,x):
    i.nump = i.nump and isinstance(x,(float,int))
    i._all += [x]
  def __repr__(i):
    return 'Col'+showd(i)

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

def table(rows,t = None):
  for row in rows:
    if not t:
      t = [Col(name) for name in row]
    else:
      for i,cell in enumerate(row):
        t[i] + cell
  return t

def nchops(t):
  cols = t[:-1]
  klass   = t[1]
  return [nchop(col,klass) for col in cols ]

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

def ecut(above,min=2):
  right    = Counts([x for (_,x) in above]))
  least, n = right.ent(), len(right)*1.0
  cut,left = None,Counts() 
  for j,(num,k) in enumerate(above):
    right[k] -= 1
    left[k]  += 1
    n1,n2 = len(left), len(right)
    if n1 > min and n2 > min:
      tmp = n1/n*left.ent() + n2/n*right.ent()
      if tmp < least :
        cut,least = j,tmp
  return cut

print table(rows(golf))

