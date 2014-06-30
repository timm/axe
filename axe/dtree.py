from __future__ import division
from lib    import *
from demos  import *
from fi     import *
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
  n   = int(len(lst)*opt.infoPrune)
  return [f for _,f,x,y in lst[:n]]

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
  if not toBe < asIs: return here
  for key in sorted(splits.keys()):
    someRows = splits[key] 
    if len(someRows) < len(rows) :
      here.kids += [tdiv1(t,someRows,lvl=lvl+1,asIs=toBe,features=features,
                          up=here,f=splitter,val=key,opt=opt)]
  return here

def tdiv(t,rows,opt=The.tree):
  features= infogain(t,opt)
  print(len(features))
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
    say(('|..' * lvl)+str(n.f.name)+"=" +str(n.val) +  "\t"+str(n.mode)+" #"+str(nmodes(n)))
  if n.kids: 
    nl();
    for k in n.kids: 
      showTdiv(k,lvl+1)
  else:
    s=classStats(n)
    print ' '+str(int(100*s.counts[s.mode()]/len(n.rows)))+'% * '+str(len(n.rows))

@demo
def tdived(file='data/diabetes.csv'):
  t = discreteTable(file)  
  #exit()
  showTdiv(tdiv(t,t._rows))
  infogain(t)



if __name__ == '__main__': eval(cmd())

