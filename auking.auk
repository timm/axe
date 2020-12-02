#!/usr/bin/env ./auk
#- vim: ft=awk ts=2 sw=2 et :

BEGIN { D=sprintf("%c",46) }

### Crate an empty list
function Obj(i) { i[0]; delete i[0] }

#### Initiate field `k` in array `i`. 
## If `f` is supplied, initialize that field with that function.
## If arguments `x,y,z` are supplied, use those in the initialization.
function has(i,k,f)       { has0(i,k); if(f) @f(i[k])      } 
function haS(i,k,f,x)     { has0(i,k); if(f) @f(i[k],x)    } 
function hAS(i,k,f,x,y)   { has0(i,k); if(f) @f(i[k],x,y)  } 
function HAS(i,k,f,x,y,z) { has0(i,k); if(f) @f(i[k],x,y,z)} 

function has0(i,k) { i[k]["\16"]; delete i[k]["\16"] }

### Simple print for a flat list.
function o(a,  i) { for(i in a) printf("-- %s",a[i]); print "" }

### Recursive print of an array
function oo(a,prefix,    gap,   i,t) {
  t = gap ? gap : (prefix D )
  if (!isarray(a)) {print(a); return 1}
  for(i in a)  
    if  (isarray(a[i])) {print(t i"" ); oo(a[i],"","|  " gap) } 
    else                 print(t i (a[i]==""?"": ": " a[i]))  }

### Report fugue locals
function rogues(   s,ignore) { 
  for(s in SYMTAB) 
    if (s ~ /^[_a-z]/) 
      print "#W> Rogue: "  s>"/dev/stderr" }

### Read multiple records
function reads(i,f,    a) {
  f  = f ? f : "-"
  FS = ","
  while ((getline < f) > 0) { readrow(a); add(i,a) }}

### Read one  record
function readrow(a,   j,tmp) {
  for(j=1;j<=NF;j++) {
    tmp  = $j + 0
    a[j] = $j == tmp ? tmp : $j }}
