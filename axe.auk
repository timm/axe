#!/usr/bin/env ./auk
#- vim: ft=awk ts=2 sw=2 et :

@include "auking"

---------------------------------------------------------------------
# Polymorphic functions

function add(i,x,    f) { f= i.is"Add"; return @f(i,x) } 

---------------------------------------------------------------------
# Columns

function Col(i,pos,txt) {
  ## Generic columns
  Obj(i)
  i.pos = pos
  i.txt = txt
  i.w   = (txt ~ /</) ? -1 : 1  }

function Skip(i,pos,txt) { 
  ## Columns that we will store, but not otherwise process.
  Col(i,pos,txt); i.is = "Skip" }

function _Add(i,x) { return x } 

function Sym(i, pos,txt) { 
  ## Columns  of symbols
  Col(i,pos,txt); i.is = "Sym"  }

function _Add(i,x)  { return x } 

function Num(i,pos,txt) { 
  ## Columns of Numbers
  Col(i,pos,txt)
  i.is = "Num"
  i.lo =  1E32
  i.hi = -1E320 }

function _Add(i,x)    {
  if (x != "?") {
    if (x > i.hi) i.hi = x
    if (x < i.lo) i.lo = x }
  return x }

---------------------------------------------------------------------
# Row

function Row(i, a,cols,j) {
  Obj(i)
  has(i,"cells")
  has(i,"bins")
  for(j in a)  
    i.cells[j] = i.bins[j] = add(cols[j], a[j]) }

---------------------------------------------------------------------
# Rows

function Rows(i) {
  ## Rows have `rows` holding `Row`s (and that data is summarized in `cols`).
  Obj(i)
  i.is = "Rows"
  has(i,"rows")
  has(i,"cols") }

function _What(x)  { 
  # Decide column type
  return (x ~ /\?/) ? "Skip" : (x ~ /[<>:]/ ? "Num" : "Sym") } 

function _Add(i,a) { 
  ## First addition adds to the header, rest to data.
  length(i.cols) ? _Data(i,a) : _Head(i,a) }

function _Head(i,a,   j) { for(j in a) hAS(i.cols,j, _What(a[j]),j,a[j]) }

function _Data(i,a,  r,j) { 
  ## Make a new row at a random index (make subsequent random sampling easier)
  r = sprintf("%9.0f",1E9*rand())
  hAS(i.rows, r, "Row", a, i.cols) }
