from __future__ import division
from lib    import *
from demos  import *
from counts import *
import sys
sys.dont_write_bytecode = True

def rows(file, 
          sep= The.reader.sep,
          bad= The.reader.bad):
  """Read comma-eperated rows that might be split 
  over many lines.  Finds strings that can compile 
  to nums.  Kills comments and white space."""
  n,kept = 0,""
  for line in open(file):
    now   = re.sub(bad,"",line)
    kept += now
    if kept:
      if not now[-1] == sep:
        yield n, map(atom,kept.split(sep))
        n += 1
        kept = "" 

def row(file,skip= The.reader.skip):
  "Leaps over any columns marked 'skip'."
  todo = None
  for n,line in rows(file):
    todo = todo or [col for col,name in enumerate(line) 
                    if not skip in name]
    yield n, [ line[col] for col in todo ]

## Read Headers and Rows
def table(source, rows = True, contents = row):
  t = table0(source)
  for n,cells in contents(source):  
    if n == 0 : head(cells,t) 
    else      : body(cells,t,rows) 
  #print ">>>>", t.headers
  return t

## Create Table 
def table0(source):
  return Thing(
    source = source,
    depen=[], indep=[], nums =[], syms=[], 
    more =[], less =[], klass=[], headers=[], 
    _rows=[], at   ={}, patterns= The.reader.patterns)

def head(cells,t,numc=The.reader.numc):
  for col,cell in enumerate(cells):
    this   = Num if numc in cell else Sym
    this.rank = 0
    header = this()
    header.col, header.name = col,cell
    t.at[cell] = header
    for pattern,val in t.patterns.items():
      if re.search(pattern,cell):
        where  = val(t)
        where += [header]
  return t

def body(cells,t,rows=True):
  for header in t.headers:
    header + cells[header.col]
  if rows: 
    t._rows += [Row(cells)]

class Row(Thing):
  def __init__(i,cells):
    i.newId()
    i.cells = cells
    i.pos = []
    i.x0,i.y0= 0,0

def clone(t,rows=[],discrete=False) :
  def ok(x):
    return x.replace("$",'') if discrete else x
  t= head([ok(h.name) for h in t.headers],
              table0('copy of '+t.source))
  for cells in rows:  body(cells,t,True)
  return t

@demo
def tabled(f='data/weather.csv'):
  t=table(f)
  for x in  t.indep: rprintln(x)
  #rprintln(t)

@demo
def tableCopied(f='data/weather.csv'):
  t0=table(f)
  t1=copyTable(t0)
  rprintln([t0.nums,t1.nums]); 

if __name__ == '__main__': eval(cmd())
