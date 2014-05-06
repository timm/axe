import sys
sys.dont_write_bytecode = True 
from demos import *

class Slots():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i._id = Slots.id = Slots.id + 1
  def also(i,**d)  : i.override(d) 
  def override(i,d): i.__dict__.update(d)
  def __hash__(i)  : return i._id
  def __eq__(i,j)  : return i._id == j._id
  def __neq__(i,j) : return i._id != j._id

The = Slots()
def settings(f=None):
  if f : The.__dict__[f.func_name[:-4]] = f() 
  else : rprintln(The)
  return f

@settings
def stringings(): return Slots(
  white= r'(["\' \t\r\n]|#.*)')

@settings
def mathings(): return Slots(
  seed  = 1,
  inf   =    10**32,
  ninf  = -1*10**32,
  teeny =    10**-32,
  brink = Slots(
    hedges= [ .39, 1.0 ][0], 
    cohen = [ .3 ,  .5 ][0],
    conf  = [ .95,  .99][0]))

@settings
def sampleings(): return Slots(
  keep = 256,
  bins = 5,
  tiny = 0.1,
  enough=10)

@demo
def thesed():
  return 2
