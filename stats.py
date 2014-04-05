import zipfile,re,os,fnmatch

def values(str,  sep=",",
           bad= r'(["\' \t\r\n]|#.*)'):
  def value(x):
    try : return int(x)
    except ValueError:
      try : return float(x)
      except ValueError : return x
  return map(value,re.sub(bad,"",str).split(sep))

def interpolate(x, points):
  lo, hi = points[0], points[-1]
  x1,y1  = lo[0], lo[1]
  for x2,y2 in points[1:]:
    if x1 <= x <= x2:
      deltay = y2 - y1
      deltax = (x- x1)*1.0/(x2- x1)
      return y1 + deltay * deltax
    x1,y1 = x2,y2
  return hi[1]

def zippedFiles(zipped):
  "Find files in a zip."
  with zipfile.ZipFile(zipped,'r') as archive:
    for file in archive.namelist():
      yield file,archive.open(file,'r')

def files(pattern):
  "Find files in a directory tree."
  for path, subdirs, files in os.walk('.'):
    for name in files:
      if fnmatch.fnmatch(name, pattern):
        yield path + '/' + name,\
              open(os.path.join(path, name))

def namedCells(source, filter=files):
  "Return cells, with header info from line1."
  for file,lines in filter(source):
    names = None
    for line in lines:
      cells = values(line)
      if not names: 
        names = cells
      else: 
        yield file,zip(names,cells) 
   
def wantgot(source,compare=lambda x,y:x - y, 
            filter=files):
  "Return cells, compared to values in first col."
  for file,found in namedCells(source,filter):
    want = found[0][1]
    for what,got in found[1:]:
      yield file, what, compare(want,got)

def ar(want,got)    : return want - got
def mar(want,got)   : return abs(ar(want,got))
def relerr(want,got): return (want-got)*1.0/want
def mre(want,got)   : return abs(relerr(want,got))

class Nums():
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
  def __add__(i,j): return Nums(i.all + j.all)
  def t(i,j):
    signal = abs(i.mu - j.mu)*1.0
    noise  = (i.s**2/i.n + j.s**2/j.n)**0.5
    return signal / noise
  def ttest(i,j,conf=95):
    return critical(i.n + j.n - 2,conf) < i.t(j)

def critical(n, conf=95):
  return interpolate(n,
                     {95:((  1, 12.70 ), ( 3, 3.182),
                          (  5,  2.571), (10, 2.228),
                          ( 20,  2.086), (80, 1.99 ),
                          (320,  1.97 )),
                      99:((  1, 63.657), ( 3, 5.841),
                          (  5,  4.032), (10, 3.169),
                          ( 20,  2.845), (80, 2.64 ),
                          (320,  2.58 ))}[conf])

def _t():
  one = [105,112,96,124,103,92,97,108,105,110]
  two = [98,108,114,106,117,118,126,116,122,108]
  for want,fudge in [(False,1.0), (False,1.1), 
                     (True,1.2),  (True,9.0)]:
    t1  = Nums(two)
    t2  = Nums(map(lambda x:x*fudge, one))
    got = t1.ttest(t2)
    print fudge,":testPassed",want == got,\
          "since :want",want,":got",got

_t()

def _demo(zipped='data/loo.zip'):
  wme = {}
  for file,rx,seen in wantgot(zipped,mre,zippedFiles):
    key = rx
    if not key in wme: 
      wme[key] = Nums()
    wme[key] % seen
  for k1,v1 in wme.items():
    for k2,v2 in wme.items():
      if k1 > k2:
        print k1,k2,v1.ttest(v2)

#_demo()
