import sys

class Bag():
  id = -1
  def __init__(i,**fields) : 
    i.override(fields)
    i.id = Bag.id = Bag.id + 1
  def also(i,**d)  : i.override(d) 
  def override(i,d): i.__dict__.update(d)
  def __repr__(i)  : return rprint(i)
  def __hash__(i)  : return i.id
  def __eq__(i,j)  : return i.id == j.id
  def __neq__(i,j) : return i.id != j.id

