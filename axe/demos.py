from __future__ import division
import sys
sys.dont_write_bytecode = True

def cmd(com="demo('-h')"):
  "Convert command line to a function call."
  if len(sys.argv) < 2: return com
  def strp(x): return isinstance(x,basestring)
  def wrap(x): return "'%s'"%x if strp(x) else str(x)
  words = map(wrap,map(atom,sys.argv[2:]))
  return sys.argv[1] + '(' + ','.join(words) + ')'

def demo(f=None,cache=[]): 
  def doc(d):
    return '# '+d.__doc__ if d.__doc__ else ""  
  if f == '-h':
    print '# sample demos'
    for n,d in enumerate(cache): 
      print '%3s) ' %(n+1),d.func_name,doc(d)
  elif f: 
    cache.append(f); 
  else:
    s='|'+'='*40 +'\n'
    for d in cache: 
      print '\n==|',d.func_name,s,doc(d),d()
  return f

def test(f=None,cache=[]):
  def doc(t):
    return ': '+t.__doc__ if t.__doc__ else ""  
  if f: 
    cache.append(f)
  else:
    ok=no=0
    for t in cache: 
      print "#",t.func_name ,doc(t)
      n=0
      for want,got in  t():
        n += 1
        if want == got:
          ok += 1
          print "CORRECT:",t.func_name,'question', n
        else:
          no += 1
          print "WRONG  :",t.func_name,'question',n
    if cache:
      print '\n# Final score = %s/%s = %s%% CORRECT' \
          % (ok,(ok+no),round(100*ok/(ok+no)))
  return f

@demo
def demoed(show=1):
  "Sample demo."
  print show/2
