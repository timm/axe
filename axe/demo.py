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
  elif f: 
    demos.append(f); 
  else:
    s='|'+'='*40 +'\n'
    for d in demos: 
      print '\n==|',d.func_name,s,demoDoc(d),d()
  return f

def test(f=None,tests=[]): 
  if f: tests.append(f); return f
  ok=no=0
  for t in tests: 
    print "#",t.func_name + ': ',t.__doc__
    for n,(want,got) in  enumerate(t()):
      if want == got:
        ok += 1; print "CORRECT:",t.func_name,'question', n+1
      else:
        no += 1; print "WRONG  :",t.func_name,'question',n+1
  if tests:
    print '\n# Final score = %s/%s = %s%% CORRECT' \
            % (ok,(ok+no),round(100*ok/(ok+no)))

