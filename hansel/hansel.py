from __future__ import division
import sys, random,math
sys.dont_write_bytecode = True

### Place to store things and stuff ################
class Thing:
  def __init__(i,**d): i.__dict__.update(d)

### Place to store options #########################

The = Thing(cache= Thing(keep    = 128,
                         pending = 4),
            sa   = Thing(cooling = 0.6,
                         kmax    = 1000,
                         epsilon = 1.01,
                         verbose = True,
                         era     = 50,
                         baseline = 100))

### Misc utils #####################################
rand= random.random
any=  random.choice
def log2(x): return math.log(x)/math.log(2)
def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()

def showd(d,lvl=0): 
  d = d if isinstance(d,dict) else d.__dict__
  after, line,gap = [], '', '\t' * lvl
  for k in sorted(d.keys()):
    if k[0] == "_": continue
    val = d[k]
    if isinstance(val,(dict,Thing)):
       after += [k]
    else:
      if callable(val):
        val = val.__name__
      line += (':%s %s ' % (k,val))
  print gap + line
  for k in after: 
      print gap + (':%s' % k)
      showd(d[k],lvl+1)

def g3(lst): return gn(lst,3)
def g2(lst): return gn(lst,2)
def g0(lst): return gn(lst,0)

def gn(lst,n):
  fmt = '%.' + str(n) + 'f'
  return ', '.join([(fmt % x) for x in sorted(lst)])

### Classes ########################################

class Log(Thing):
  "Keep a random sample of stuff seen so far."
  def __init__(i,inits=[],label=''):
    i.label = label
    i._cache,i.n,i._report = [],0,None
    i.setup()
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    if x == None: return x
    i.n += 1
    changed = False
    if len(i._cache) < The.cache.keep:
      changed = True
      i._cache += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.keep/i.n:
        changed = True
        i._cache[int(rand()*The.cache.keep)] = x
    if changed:      
      i._report = None # wipe out 'what follows'
      i.change(x)
    return i
  def any(i):  
    return  any(i._cache)
  def has(i):
    i._report = i._report or i.report()
    return i._report
  def setup(i): pass

class Num(Log):
  def setup(i):
    i.lo, i.hi = 10**32, -10**32
  def change(i,x):
    i.lo = min(i.lo, x)
    i.hi = max(i.hi, x)
  def report(i):
    lst = i._cache = sorted(i._cache)
    n   = len(lst)     
    return Thing(
      median= i.median(),
      iqr   = lst[int(n*.75)] - lst[int(n*.5)],
      lo    = i.lo, 
      hi    = i.hi)
  def ish(i,f=0.1): 
    return i.any() + f*(i.any() - i.any())
  def median(i):
    n = len(i._cache)
    p = n // 2
    if (n % 2):  return i._cache[p]
    q = p + 1
    q = max(0,(min(q,n)))
    return (i._cache[p] + i._cache[q])/2

class Sym(Log):
  def setup(i):
    i.counts,i.mode,i.most={},None,0
  def change(i,x):
    c= i.counts[x]= i.counts.get(x,0) + 1
    if c > i.most:
      i.mode,i.most = x,c
  def report(i):
     return Thing(dist= i.dist(), 
                  ent = i.entropy(),
                  mode= i.mode)
  def dist(i):
    n = sum(i.counts.values())
    return sorted([(d[k]/n, k) for 
                   k in i.counts.keys()], 
                  reverse=True)
  def ish(i):
    r,tmp = rand(),0
    for w,x in i.has().dist:
      tmp  += w
      if tmp >= r: 
        return x
    return x
  def entropy(i,e=0):
    for k in i.counts:
      p = i.counts[k]/len(i._cache)
      e -= p*log2(p) if p else 0
    return e    

### Classes ########################################

class In:
  def __init__(i,lo=0,hi=1,txt=""):
    i.txt,i.lo,i.hi = txt,lo,hi
  def __call__(i): 
    return i.lo + (i.hi - i.lo)*rand()
  def log(i): 
    return Num()

class XY:
  def __init__(i, x=None, y=None):
    i.x, i.y = x,y
  def __repr__(i):
    return ', '.join(map(str,[':x',i.x,':y',i.y]))

class Model:
  def __init__(i):
    i.of = i.spec()
    i.log= XY(x= [z.log() for z in i.of.x],
              y= [Num()   for _ in i.of.y])
  def indepIT(i):
    "Make new it."
    return XY(x=[z() for z in i.of.x])
  def depIT(i,it):
    "Complete it's dep variables."
    it.y = [f(it) for f in i.of.y]
  def logIT(i,it):
    "Remember what we have see in it."
    for val,log in zip(it, i.log):
      log += val
  def aroundIT(i,it,p=0.5):
    "Find some place around it."
    def n(val,f): 
      return f() if rand() < p else val
    old = it.x
    new = [n(x,f) for x,f in zip(old,i.of.x)]
    return XY(x=new)

#XY = a pair of related indep,dep lists

#it = actual values
#of = meta knowledge of members of it
#log = a record of things seen in it

#seperate (1) guesses indep variables (2) using them to
#calc dep values (3) logging what was picked

class ZDT1(Model):
  def spec(i):
    return XY(x= [In(0,1,z) for z in range(30)],
              y= [i.f1,i.f2])
  def f1(i,it):
    return it.x[0]
  def f2(i,it):
    return 1 + 9*sum(it.x[1:]) / 29

class Schaffer(Model):
  def spec(i):
    return XY(x= [In(-10,10,0)],
              y= [i.f1,i.f2])
  def f1(i,it):
    x=it.x[0]; return x**2
  def f2(i,it):
    x=it.x[0]; return (x-2)**2

def burp(x):  
  The.sa.verbose and say(x)

def sa(m):
  return sa1(m, The.sa.epsilon,
                The.sa.kmax,
                The.sa.cooling,
                The.sa.era,
                The.sa.baseline)

def sa1(m, epsilon,kmax,cooling,era,baseline):
  def energy(it): 
    m.depIT(it)
    return sum(it.y)
  def norm(e,lo,hi):
    return 1 - (e - lo) / (hi - lo)
  def candidate():
    it = m.indepIT()
    m.depIT(it)
    return it
  def maybe(old,new,temp): 
    return math.e**(-1*(old - new)/temp) < rand()
  def baseline():
    es = []
    for _ in xrange(The.sa.baseline):
      it = m.indepIT()
      es += [energy(it)]
    es = sorted(es)
    return es[0],es[-1]
  lo,hi = baseline()
  sb = s = m.indepIT()
  eb = e = norm(energy(s),lo,hi)
  print eb
  for k in xrange(kmax):
    k += 1
    sn = m.aroundIT(s)
    en = norm(energy(sn),lo,hi)
    if en > (eb * epsilon):
      sb,sb = sn,en; burp("!")
    if en > (e *  epsilon):
      s,e = sn,en; burp("+")
    elif maybe(e,en, k/kmax):
      s,e = sn,en; burp("?")
    if not k % era: 
      burp("\n" + str(eb) + " ")
    burp(".")
  print eb    

print sa(Schaffer())
