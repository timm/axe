import sys,math
sys.dont_write_bytecode = True
log=math.log

class Counts():
  "Place to add/delete counts of symbols."
  def __init__(i,inits=[]):
    i.n = 0
    i.cache = {}
    for symbol in inits:  i + symbol
  def __add__(i,symbol) :
    i.n += 1
    i.cache[symbol] = i.cache.get(symbol,0) + 1
  def __sub__(i,symbol) : 
    i.n -= 1
    i.cache[symbol] = i.cache.get(symbol,0) - 1
  def ent(i):
    e = 0
    for symbol in i.cache:
      p  = i.cache[symbol]*1.0/i.n
      if p:
        e -= p*log(p)*1.0/log(2)
    return e

def ediv(pairs,gets,cuts):
  "Divide pairs of (numbers,symbols) using entropy."
  cut,e = ecut(pairs,gets)
  if cut:
    ediv(pairs[:cut], gets, cuts)
    ediv(pairs[cut:], gets, cuts)
  else:
    cuts += [(e,pairs)]
  return cuts
 
def ecut(pairs,(num,sym),min=3):
  "Find best place to divide pairs of (num,sym)."
  cut,least= None,None
  left     = Counts()
  right    = Counts(sym(x) for x in pairs)
  n        = len(pairs) * 1.0
  least    = right.ent()
  for j,x  in enumerate(pairs):
    n1,n2 = left.n, right.n
    if n1 > min and n2 > min:
      tmp = n1/n*left.ent() + n2/n*right.ent()
      if tmp < least :
        cut,least = j,tmp
    right - sym(x)
    left  + sym(x)    
  return cut,least

def _ecut():
  "Demo code to test the above."
  def first(x) : return x[0]
  def second(x) : return x[1]
  def go(lst):
    print ""; print lst
    for d in  ediv(sorted(lst,key=first),(first,second),[]):
      print d[1][0][0]
  X,Y="X","Y"
  go([(1,X),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,Y),(2,X),(3,X),(4,X),(11,Y),(12,Y),(13,Y),(14,Y)])
  go([(1,X),(2,X),(3,X),(4,X),(11,X),(12,X),(13,X),(14,X)])
  go([(64,X),(65,Y),(68,X),(69,Y),(70,X),(71,Y),
      (72,X),(72,Y),(75,X),(75,X),
      (80,Y),(81,Y),(83,Y),(85,Y)])

_ecut()

"""
Output:

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')]
1
11

[(1, 'Y'), (2, 'X'), (3, 'X'), (4, 'X'),
 (11, 'Y'), (12, 'Y'), (13, 'Y'), (14, 'Y')]
1
11

[(1, 'X'), (2, 'X'), (3, 'X'), (4, 'X'), 
 (11, 'X'), (12, 'X'), (13, 'X'), (14, 'X')]
1


[(64, 'X'), (65, 'Y'), (68, 'X'), (69, 'Y'), (70, 'X'), (71, 'Y'), 
 (72, 'X'), (72, 'Y'), (75, 'X'), (75, 'X'), 
 (80, 'Y'), (81, 'Y'), (83, 'Y'), (85, 'Y')]
64
72
80
"""

