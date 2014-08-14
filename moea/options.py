"""
options.py: option management (setting and sharing
and printing options) 
Copyright (c) 2014 tim.menzies@gmail.com

             /\ \__  __                             
  ___    _____ \ \ ,_\/\_\     ___     ___      ____  
 / __`\ /\ '__`\\ \ \/\/\ \   / __`\ /' _ `\   /',__\ 
/\ \L\ \\ \ \L\ \\ \ \_\ \ \ /\ \L\ \/\ \/\ \ /\__, `\
\ \____/ \ \ ,__/ \ \__\\ \_\\ \____/\ \_\ \_\\/\____/
 \/___/   \ \ \/   \/__/ \/_/ \/___/  \/_/\/_/ \/___/ 
           \ \_\                                      
            \/_/ 

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
import sys
sys.dont_write_bytecode = True

class Thing(object):
  def __init__(i,**dict): i.update(dict)
  def also(i,**dict)    : i.update(dict); return i
  def update(i,dict)    : i.__dict__.update(dict)
  def __repr__(i)  : return dump(i.__dict__,'',0)

def dump(d,s='',lvl=0):
  later = []
  s += '# '+'   ' * lvl
  for k,v in sorted(d.items()):
    if isinstance(v,Thing): 
      later += [(k,v.__dict__)]
    elif isinstance(v,dict):
      later += [(k,v)]
    else:
      s += ':%s %s ' % (k,
                        v.__name__ if callable(v) else v)
  s += '\n'
  for k,v in later:
    s += '# '+('   ' *  lvl) + ':%s' % k + '\n'
    s= dump(v,s,lvl+1)
  return s

The = Thing()
def settings(f=None):
  if f : The.__dict__[f.func_name[:-4]] = f() 
  else : print The
  return f

@settings
def mathings(): return Thing(
  inf = float("inf"),
  ninf = float("-inf"),
  seed = 1,
  tiny = 10**-32,
  centralLimitThreshold=20)

@settings
def brinkings(): return Thing(
  tconf=0.95,
  hot = 102)

@settings
def symings(): return Thing(
  missing="?",
  numc     ='$',
  patterns = {
    '\$'     : lambda z: z.nums,
    '\.'     : lambda z: z.syms,
    '>'      : lambda z: z.more,
    '<'      : lambda z: z.less,
    '[=<>]'  : lambda z: z.depen,
    '^[^=<>]': lambda z: z.indep,
    '.'      : lambda z: z.headers})

if __name__ == "__main__": print The
