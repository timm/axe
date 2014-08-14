"""
lib.py: misc python tricks
Copyright (c) 2014 tim.menzies@gmail.com

/\_ \    __ /\ \       
\//\ \  /\_\\ \ \____  
  \ \ \ \/\ \\ \ '__`\ 
   \_\ \_\ \ \\ \ \L\ \
   /\____\\ \_\\ \_,__/
   \/____/ \/_/ \/___/ 
                       
Permission is hereby granted, free of charge, to any
person obtaining a copy of this software and
associated documentation files (the "Software"), to
deal in the Software without restriction, including
without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to
whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission
notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.""" 

from __future__ import division
import sys,re,random,math
sys.dont_write_bytecode = True
from life import *
from options import *

### unit tests #####################################
def test(f=None,cache=[]):
  "Unit test decorator."
  if f: # called as decorator @test above a function
    cache += [f]
    return f
  else: # called as just test(), so run tests
    ok = no = 0
    for t in cache: 
      print '#',t.func_name ,t.__doc__ or ''
      prefix, n, found = None, 0, t() or []
      while found:
        this, that = found.pop(0), found.pop(0)
        if this == that:
          ok, n, prefix = ok+1, n+1,'CORRECT:'
        else: 
          no, n, prefix = no+1, n+1,'WRONG  :'
        print prefix,t.func_name,'test',n
    if ok+no:
      print '\n# Final score: %s/%s = %s%% CORRECT' \
          % (ok,(ok+no),int(100*ok/(ok+no)))

### Handy one-liners ###############################
def first(x): return x[0]
def second(x): return x[1]
def third(x): return x[2]
def fourth(x): return x[3]
def fifth(x): return x[4]
def last(x): return x[-1]

rand = random.random
any  = random.choice
  
### Handy random stuff #############################
def shuffle(lst) : 
  random.shuffle(lst)
  return lst
def rseed(n=The.math.seed):
  random.seed(n)

### Printing #######################################
def g1(x)    : return round(x,1)
def g2(x)    : return round(x,2)
def g3(x)    : return round(x,3)
def gs1(lst) : return map(g1,lst)
def gs2(lst) : return map(g2,lst)
def gs3(lst) : return map(g3,lst)

def nl(): print ""

# write out tricks
def saysln(*lst): 
  says(*lst); nl()
def says(*lst)  : 
  say(', '.join(map(str, lst)))
def say(x): 
  sys.stdout.write(str(x)); sys.stdout.flush()

### Coercion  #####################################
def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError: return x

### Command line processing ########################
def cmd(com="life(seed=1)"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)  
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

if __name__ == '__main__': eval(cmd())
