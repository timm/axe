import sys,random
sys.dont_write_bytecode = True
rand=random.random

class Counts(): # Add/delete counts of numbers.
  def __init__(i,inits=[]):
    i.n = i.mu = i.m2 = 0.0
    for number in inits: i + number 
  def __add__(i,x):
    i.n  += 1
    delta = x - i.mu
    i.mu += delta/(1.0*i.n)
    i.m2 += delta*(x - i.mu)
  def __sub__(i,x):
    if i.n > 1:
      i.n  -= 1
      delta = x - i.mu
      i.mu -= delta/(1.0*i.n)
      i.m2 -= delta*(x - i.mu)    
  def sd(i): return i.m2*1.0/(i.n -1)

f   = [rand()**2 for _ in range(10)]
rhs = Counts(f)
lhs = Counts()
print f

for i,f1 in enumerate(f):
  lhs + f1
  if lhs.n > 2: 
    print i, lhs.mu,lhs.sd()

for j,f1 in enumerate(reversed(f)):
  rhs - f1
  if rhs.n > 2: 
    print j, rhs.mu, rhs.sd()


