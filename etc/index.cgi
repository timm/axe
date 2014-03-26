#!/bin/bash
# -*- bash -*- 
#######################################################
# begin config section

Default=index
Src=${Src='https://raw.githubusercontent.com/timm/axe/master/'}
Cat=${Cat=' wget -q -O - '}
Files='index.cgi'
Tmp=/tmp/$USER

header() { cat<<-EOF
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" 
		"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html 	xmlns="http://www.w3.org/1999/xhtml" 
		xml:lang="en" 
		lang="en">
<head>
<title> $1 </title>
<link rel="stylesheet" href="$Src/etc/img/style.css"   type="text/css"  />
<link rel="icon"       href="$Src/etc/img/favicon.png" type="image/png" /
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />

EOF
}

# end config
########################################################
# making dirs and files

mkdir -p $Tmp

cat<<EOF > $Tmp/markup.py
import markdown
import sys
str = '\n'.join(map(lambda x: x.rstrip('\n'),
                     sys.stdin.readlines()))
print markdown.Markdown(extensions=['footnotes',
           'def_list','tables','toc']).convert(str)
EOF


# end config section
#########################################################
# from here down, you should not need to change anything
[ -n "$1" ] && QUERY_STRING=$1

Q=${QUERY_STRING:=$Default}
Q=$(echo $Q | sed 's/[^\/\.0-9a-zA-Z]//g')

py2md() {  cat - |
  gawk '
  BEGIN    { skip = 1 }
  /^"""/   { skip = 0 }
  skip     { next     }
  gsub(/^""".*/,"") { In =  1 - In }
           { print In? $0 : "       " pretty($0) }

  BEGIN {
     Color1="brown"
     Color2="teal"  
     Color3="blue"
     Words = "function gsub sub gensub "      \
             " for in int if else while print printf" \
             " sprintf rand switch"                    \
             " BEGIN END next continue  "               \
             " return length "
     split(Words,Tmp," ")
     for(Word in Tmp) {
        Pat = Pat Sep "\\y" Tmp[Word] "\\y"
        Sep = "|"
      }
      Pat = "(" Pat ")"
  }
  function pretty(s) {
       gsub(/<[\/]?code>/,"",s)
       gsub(Pat,      "<b><font color="Color1">&</font></b>",s) 
       gsub(/"[^"]*"/,"<b><font color="Color2">&</font></b>",s)
       gsub(/#.*/,   "<b><font color="Color3">&</font></b>",s)
       gsub(/[{}]/,   "<b>&</b>",s)
       return s 
  }

'
}

echo "Content-type: text/html"
echo ""

if [ "$Q" = "REFRESH" ]
then
    for i in $Files; do
	wget -q -O - $Src/$i > $i
    done
    chmod 755 index.cgi
    echo "<pre>"; echo ""; date
    cksum  $Files
    echo "`cat $Files | cksum` TOTAL"
    echo '<a href="index.cgi">Continue.</a>'
else
    header $Q
    #$Cat $Src/header.html
    if [[ "$Q" =~ .*py$ ]]
    then cat $Q  | py2md
    else cat $Q.md
    fi 
    #$Cat $Src/footer.html
fi
