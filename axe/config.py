from lib import *
import sys
sys.dont_write_bytecode = True

def settings():
  return Bag(
    a=1,
    b=2,
    c=Bag(d=[1,2,3,4],
          g=dict(aa=23,bb=23),
          e='f'))
