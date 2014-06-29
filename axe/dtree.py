from __future__ import division
from lib    import *
from demos  import *
from fi     import *
import sys
sys.dont_write_bytecode = True

def bestFeature(rows,t):
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
  all = sorted(ranked(f) for f in t.indep)
  return all[0]
         
def tdiv1(t,rows,lvl=-1,asIs=10**32,up=None,
                  f=None,val=None,opt=None):
  here = Thing(t=t,kids=[],f=f,val=val,up=up,lvl=lvl,rows=rows,e=0)
  if f and opt.debug:
    print ('|.. ' * lvl) + f.name ,"=",val,len(rows)
  here.mode=classStats(here).mode()
  if lvl > 10 : return here
  toBe, splitter, syms,splits = bestFeature(rows,t)
  if not toBe < asIs: return here
  here.e = e= sum(syms[key].ent() for key in splits.keys())
  
  if 1:
    for key in sorted(splits.keys()):
      someRows = splits[key] 
      #if f:
       # print('??? '* (lvl+1) + str(key) +"="+str(val)+ '; ' + 
      if len(someRows) > opt.min and len(someRows) < len(rows)  and syms[key].ent():
        here.kids += [tdiv1(t,someRows,lvl+1,asIs=toBe,
                            up=here,f=splitter,val=key,opt=opt)]
  return here

def tdiv(t,rows,opt=The.tree):
  return tdiv1(t,rows,opt=opt)


def classStats(n):
  klass=lambda x: x.cells[n.t.klass[0].col]
  return Sym(klass(x) for x in n.rows)
  
def showTdiv(n,lvl=-1):
  if n.f:
    say(('|..' * lvl)+str(n.f.name)+"=" +str(n.val) +  "/"+str(n.mode))
  if n.kids: 
    nl();
    for k in n.kids: 
      showTdiv(k,lvl+1)
  else:
    s=classStats(n)
    print " : "+ s.mode() + ' '+str(int(100*s.counts[s.mode()]/len(n.rows)))+'% * '+str(len(n.rows))

@demo
def tdived(file='data/diabetes.csv'):
  t = discreteTable(file)
  #exit()
  showTdiv(tdiv(t,t._rows))



if __name__ == '__main__': eval(cmd())

