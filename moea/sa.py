"""
sa.py: generics for all optimizers
Copyright (c) 2014 tim.menzies@gmail.com

/\  _`\ /\  _  \    
\ \,\L\_\ \ \L\ \   
 \/_\__ \\ \  __ \  
   /\ \L\ \ \ \/\ \ 
   \ `\____\ \_\ \_\
    \/_____/\/_/\/_/

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
import sys,math
sys.dont_write_bytecode = True
from lib import *
from models import *
from optimize import *

def sa(model=Schaffer):
  def maybe(old,new,t):
    return math.e**((old - new)*1.0/t) < rand()
  def neighbor(lst):
    for header in model.indep:
      if rand() > The.sa

if __name__ == '__main__': eval(cmd())
