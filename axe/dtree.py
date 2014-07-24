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
  for f in t.headers:
    f.selected=False
  lst = rankedFeatures(t._rows,t)
  n = int(len(lst)*opt.infoPrune)
  n = max(n,1)
  for _,f,_,_ in lst[:n]:
    f.selected=True
  return [f for e,f,syms,at in lst[:n]]

def tdiv1(t,rows,lvl=-1,asIs=10**32,up=None,features=None,
                  f=None,val=None,opt=None):
  here = Thing(t=t,kids=[],f=f,val=val,up=up,lvl=lvl,rows=rows,modes={})
  if f and opt.debug: 
    print ('|.. ' * lvl) + f.name ,"=",val,len(rows)
  here.mode = classStats(here).mode()
  if lvl > 10 : return here
  if asIs==0: return here
  _, splitter, syms,splits = rankedFeatures(rows,t,features)[0]  
  for key in sorted(splits.keys()):
    someRows = splits[key] 
    toBe = syms[key].ent()
    if opt.variancePrune and lvl > 1 and toBe >= asIs:
        continue
    if opt.min <= len(someRows) < len(rows) :
      here.kids += [tdiv1(t,someRows,lvl=lvl+1,asIs=toBe,features=features,
                          up=here,f=splitter,val=key,opt=opt)]
  return here

def tdiv(t,rows,opt=The.tree):
  features= infogain(t,opt)
#  opt.min = len(rows)**0.5
  tree=tdiv1(t,rows,opt=opt,features=features)
  if opt.prune:
    modes(tree)
    prune(tree)
  return tree

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
    says(n.id,('|..' * lvl)+str(n.f.name)+"=" +str(n.val) +  "\t:"+str(n.mode)+" #"+str(nmodes(n)))
  if n.kids: 
    nl();
    for k in n.kids: 
      showTdiv(k,lvl+1)
  else:
    s=classStats(n)
    print ' '+str(int(100*s.counts[s.mode()]/len(n.rows)))+'% * '+str(len(n.rows))

def dtnodes(tree):
  if tree:
    if tree.up:
      yield tree
    for kid in tree.kids:
      for sub in dtnodes(kid):
        yield sub

def dtleaves(tree):
  for node in dtnodes(tree):
    #print "K>", tree.kids[0].__dict__.keys()
    if not node.kids:
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
  "find the most supported branch selected by test"
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
  tree,_= tdiv(t,t._rows)
  showTdiv(tree)
 
 
@demo
def cross(file='data/housingD.csv',rseed=1):
  def klass(test):
    return test.cells[train.klass[0].col]
  seed(rseed)
  tbl = discreteTable(file)
  n=0
  abcd=Abcd()
  nLeaves=Num()
  nNodes=Num()
  for tests, train in xval(tbl):
     tree = tdiv(train,train._rows)
     nLeaves + len([n for n in dtleaves(tree)])
     nNodes +  len([n for n in dtnodes(tree)])
     for test in tests:
       want = klass(test)
       got  = classify(test,tree)
       abcd(want,got)
  nl()
  abcd.header()
  abcd.report()
  print ":nodes",sorted(nNodes.some.all())
  print ":leaves",sorted(nLeaves.some.all())

@demo
def snl(file='data/housingD.csv',rseed=1,w=dict(_1=0,_0=1)):
  
  seed(rseed)
  tbl = discreteTable(file)
  abcd=Abcd()
  def klass(x): return x.cells[train.klass[0].col]
  def l2t(l)  : return l.tbl
  def xpect(tbl): return tbl.klass[0].centroid()
  def score(l): return w[xpect(l2t(l))]
  for tests, train in xval(tbl):
     tree = tdiv(train,train._rows)
     #print "1>",[h.col for h in train.headers if h.selected]
     nodes = [node for node in dtnodes(tree)]
     for node in nodes:
       node.tbl = clone(train,
                        rows=map(lambda x:x.cells,node.rows),
                        keepSelections=True)
       node.tbl.centroid= centroid(node.tbl,selections=True)
     for node1 in nodes:
       id1 = node1._id
       node1.near = []
       for node2 in nodes:
         id2 =  node2._id
         if id1 > id2:
           delta = overlap(node1.tbl.centroid,node2.tbl.centroid)
           score12    = score(node2) - score(node1)
           score21    = score(node1) - score(node2)
           node1.near += [(delta,node2,xpect(l2t(node2)),score12)]
           node2.near += [(delta,node1,xpect(l2t(node2)),score21)]
     for node in nodes:
       node.near = sorted(node.near,key= lambda x: -1*first(x)) 
       print ""
       for x in node.near: print "\t",x
     for test in tests:
       want = klass(test)
       got  = classify(test,tree)
       abcd(want,got)
  nl()
  abcd.header()
  abcd.report()
  
if __name__ == '__main__': eval(cmd())

