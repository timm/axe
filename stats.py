import zipfile,re

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

def atoms(str, 
          sep=",",
          bad= r'(["\' \t\r\n]|#.*)'):
  return map(atom,re.sub(bad,"",str).split(sep))

def identity(*lst): 
  return lst[0] if len(lst)==1 else lst

def unzip(zipped):
  with zipfile.ZipFile(zipped,'r') as archive:
    for file in archive.namelist():
      yield file,archive.open(file,'r')

def namedZipCells(zipped):
  for file,lines in unzip(zipped):
    line, names = None, None
    for line in lines:
      cells = atoms(line)
      if not names: 
        names = cells
      else: 
        yield file,zip(names,cells) 
   
def wantgot(zipped,f=identity):
  for file,found in namedZipCells(zipped):
    want = found[0][1]
    for what,got in found[1:]:
      yield file,what,f(want,got)

def ar(want,got)    : return want - got
def mar(want,got)   : return abs(ar(want,got))
def relerr(want,got): return (want-got)*1.0/want
def mre(want,got)   : return abs(relerr(want,got))

class Total():
  def __init__(i,some=[]):
    i.n = i.mu = i.m2 = i.s = 0.0; i.all=[]
    for x in some: i % x
  def __mod__(i,x):
    i.all += [x]
    i.n   += 1; 
    delta  = x - i.mu
    i.mu  += delta*1.0/i.n
    i.m2  += delta*(x - i.mu)
    if i.n > 1: i.s = 1.0*(i.m2/(i.n - 1))**0.5
  def __add__(i,j): return Total(i.all + j.all)
  def t(i,j):
    signal = abs(i.mu - j.mu)*1.0
    noise  = (i.s**2/i.n + j.s**2/j.n)**0.5
    return signal / noise
  def ttest(i,j,conf=95):
    return critical(i.n + j.n - 2,conf) < i.t(j)

def critical(n, conf=95,
             ts= {95: ((  1, 12.70 ), ( 3, 3.182),
                       (  5,  2.571), (10, 2.228),
                       ( 20,  2.086), (80, 1.99 ),
                       (320,  1.97 )),
                  99: ((  1, 63.657), ( 3, 5.841),
                       (  5,  4.032), (10, 3.169),
                       ( 20,  2.845), (80, 2.64 ),
                       (320,  2.58 ))}):
  confs  = ts[conf]
  lo, hi = confs[0], confs[-1]
  n1,t1  = lo[0], lo[1]
  for n2,t2 in confs:
    if n1 <= n <= n2:
      return t1+ (t2- t1)* (n- n1)*1.0/(n2- n1)
    n1,t1 = n2,t2
  return hi[1]

def _t():
  one = [105,112,96,124,103,92,97,108,105,110]
  two = [98,108,114,106,117,118,126,116,122,108]
  for want,fudge in [(False,1.0), (False,1.1), 
                     (True,1.2),  (True,9.0)]:
    t1  = Total(two)
    t2  = Total(map(lambda x:x*fudge, one))
    got = t1.ttest(t2)
    print fudge,":testPassed",want == got,\
          "since :want",want,":got",got

def _demo(zipped='data/loo.zip'):
  wme = {}
  for file,rx,seen in wantgot(zipped,mre):
    key = rx
    if not key in wme: 
      wme[key] = Total()
    wme[key] % seen
  for k1,v1 in wme.items():
    for k2,v2 in wme.items():
      if k1 > k2:
        print k1,k2,v1.ttest(v2)

_demo()
