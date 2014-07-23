from __future__ import division
from lib    import *
from demos  import *
from fi     import *
from Abcd   import *

import sys
sys.dont_write_bytecode = True

def rankedFeatures(rows,t,features=None):
  features = features if features else t.indep
  klass = t.klass[0].col
  def ranked(f):
    syms, at, n  = {}, {}, len(rows)
    for x in f.counts.keys(): 
      syms[x] = Sym()
    for row in rows: 
      key = row.cells[f.col]
      val = row.cells[klass]
      syms[key] + val
      at[key] = at.get(key,[]) + [row]
    e = 0
    for val in syms.values(): 
      if val.n:
        e += val.n/n * val.ent()
    return e,f,syms,at
  return sorted(ranked(f) for f in features)

def infogain(t,opt=The.tree):
  def norm(x): return (x - lo)/(hi - lo+0.0001)
  lst = rankedFeatures(t._rows,t)
  n = int(len(lst)*opt.infoPrune)
  return [f for e,f,syms,at in lst[:n]]

def tdiv1(t,rows,lvl=-1,asIs=10**32,up=None,features=None,
                  f=None,val=None,opt=None):
  here = Thing(t=t,kids=[],f=f,val=val,up=up,lvl=lvl,rows=rows,modes={})
  if f and opt.debug: 
    print ('|.. ' * lvl) + f.name ,"=",val,len(rows)
  here.mode = classStats(here).mode()
  if lvl > 10 : return here
  if len(rows) < opt.min : return here
  if asIs==0: return here
  toBe, splitter, syms,splits = rankedFeatures(rows,t,features)[0]  
  if opt.variancePrune:
    if not toBe < asIs: return here
  for key in sorted(splits.keys()):
    someRows = splits[key] 
    if opt.min <= len(someRows) < len(rows) :
      here.kids += [tdiv1(t,someRows,lvl=lvl+1,asIs=toBe,features=features,
                          up=here,f=splitter,val=key,opt=opt)]
  return here

def tdiv(t,rows,opt=The.tree):
  features= infogain(t,opt)
  n=tdiv1(t,rows,opt=opt,features=features)
  if opt.prune:
    modes(n)
    prune(n)
  return n

def modes(n):
  if not n.modes:
    n.modes = {n.mode: True}
    for kid in n.kids: 
      for mode in modes(kid):
        n.modes[mode]=True
  return n.modes

def nmodes(n): return len(n.modes.keys())

def prune(n):
  if nmodes(n)==1: n.kids=[]
  for kid in n.kids:
      prune(kid)

def classStats(n):
  klass=lambda x: x.cells[n.t.klass[0].col]
  return Sym(klass(x) for x in n.rows)
  
def showTdiv(n,lvl=-1):  
  if n.f:
    say(('|..' * lvl)+str(n.f.name)+"=" +str(n.val) +  "\t:"+str(n.mode)+" #"+str(nmodes(n)))
  if n.kids: 
    nl();
    for k in n.kids: 
      showTdiv(k,lvl+1)
  else:
    s=classStats(n)
    print ' '+str(int(100*s.counts[s.mode()]/len(n.rows)))+'% * '+str(len(n.rows))

def nodes(tree):
  if tree:
    yield tree
    for kid in tree.kids:
      for sub in nodes(kid):
        yield sub

def leaves(tree):
  for node in nodes(tree):
    print "K>", str(tree.kids)
    if not tree.kids:
      yield node

#if tree:   
 #   if tree.kids:
  #    for kid in tree.kids:
   #     for leaf in leaves(kid):
    #      yield leaf
    #else:
     # yield tree

def xval(tbl,m=5,n=5,opt=The.tree):
  cells = map(lambda row: opt.cells(row), tbl._rows)
  for i in range(m):
    say("*")
    cells = shuffle(cells)
    div = len(cells)//n
    for j in range(n):
      say("+")
      lo = j*div
      hi = lo + div
      train = clone(tbl,cells[:lo]+cells[hi:])
      test  = map(Row,cells[lo:hi])
      yield test,train
  
def classify1(cells,tree,opt=The.tree):
  def equals(val,span):
    if val == opt.missing : return True
    elif val == span      : return True
    else:
      lo,hi = span
      return lo <= val < hi
  found = False
  for kid in tree.kids:
    col = kid.f.col
    val = cells[col]
    if equals(val,kid.val):
      for sub in classify1(cells,kid,opt):
        found = True
        yield sub
  if not found:
    yield tree


def classify(test,tree,opt=The.tree):
  all= [(len(x.rows),x.mode) 
        for x in classify1(opt.cells(test),tree,opt)]
  return second(last(sorted(all)))

def rows1(row,tbl,cells=lambda r: r.cells):
  print ""
  for h,cell in zip(tbl.headers,cells(row)):
    print h.col, ") ", h.name,cell

@demo
def tdived(file='data/diabetes.csv'):
  t = discreteTable(file)  
  #exit()
  tree= tdiv(t,t._rows)
  showTdiv(tree)
 
 
@demo
def cross(file='data/housingD.csv'):
  def klass(test):
    return test.cells[train.klass[0].col]
  tbl = discreteTable(file)
  n=0
  abcd=Abcd()
  for tests, train in xval(tbl):
     tree=tdiv(train,train._rows)
     print ":nodes" , len([n for n in nodes(tree)]), \
           ":leaves", len([n for n in leaves(tree)])
     showTdiv(tree)
     print [l for l in nodes(tree)] 
     exit()
     for test in tests:
       want = klass(test)
       got= classify(test,tree)
       abcd(want,got)
  nl()
  abcd.header()
  abcd.report()
  
if __name__ == '__main__': eval(cmd())

