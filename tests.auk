#!/usr/bin/env ./auk
#- vim: ft=awk ts=2 sw=2 et :

@include "auking"
@include "axe"

function eg1(f,   i) {
  Rows(i)
  print "data/" f D "csv"
  reads(i,"data/" f D "csv") }

#  oo(i) }

BEGIN { 
  eg1("weather")
  rogues() 
}
