from lib import *
from os  import *
import sys
sys.dont_write_bytecode = True

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def demo(f=None,demos=[]): 
  def demoDoc(d):
    return '# '+d.__doc__+"\n" if d.__doc__ else ""  
  if f == '-h':
    for d in demos: 
      print 'python axe.py',d.func_name,demoDoc(d)
  if f: demos.append(f); return f
  s='|'+'='*40 +'\n'
  for d in demos: 
    print '\n==|',d.func_name,s,demoDoc(d),d()

