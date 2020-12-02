#!/usr/bin/env bash

# configuration
Auk=$HOME/opt/auk

# stop configuration
mkdir -p $Auk
Src=$(cd $( dirname "${BASH_SOURCE[0]}" ) && pwd )

alias ls="ls -G"
alias gp="git add *; git commit -am saving; git push; git status"

transpile() { gawk '
  BEGIN             { RS=""; FS="\n"
                      Gold["dot"] = sprintf("%c",42) 
                    } 
  /@include/        { print $0 "\n"; next}
  $NF !~ /}[ \t]*$/ { for(i=1;i<=NF;i++) print "#" $i 
                      print ""; next }
  /^func(tion)?[ \t]+[A-Z][^\(]*\(/ {
      split($1,a,/[ \t\(]/)
      PREFIX = a[2]
  }
  { gsub(/ _/," " PREFIX,$0)
    for(i=1;i<=NF;i++)
      print gensub(/\.([^0-9\\*\\$\\+])([a-zA-Z0-9_]*)/, 
                   "[\"\\1\\2\"]","g", $i);
   print "" } '
}

for f in *.auk; do
  g=$Auk/${f%.*}.awk
  if [ "$f" -nt "$g" ]; then cat $f | transpile > $g; fi
done
  
if [ -n "$1" ]; then
  g=$Auk/${1%.*}.awk
  shift
  Auk="$Auk:$AWKPATH::./" 
  if [ -t 0 ]
  then         AWKPATH=$Auk gawk -f $g $*
  else cat - | AWKPATH=$Auk gawk -f $g $*
  fi
fi
