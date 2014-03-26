#!/bin/bash
# -*- bash -*- 
#######################################################
# begin config section

Default=index
Src=${Src='https://raw.githubusercontent.com/timm/axe/master'}
Cat=${Cat=" wget -q -O - $Src"}
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

# end config section
#########################################################
# from here down, you should not need to change anything
[ -n "$1" ] && QUERY_STRING=$1

Q=${QUERY_STRING:=$Default}
Q=$(echo $Q | sed 's/[^\/\.0-9a-zA-Z]//g')

[ "$2" = "render" ]  && Cat="cat ."

makedown(){   
   cat<<EOF > $Tmp/markup.py
import markdown,sys
str = '\n'.join(map(lambda x: x.rstrip('\n'),
                     sys.stdin.readlines()))
print markdown.Markdown(extensions=['footnotes',
           'def_list','tables','toc']).convert(str)
EOF
}

mkdir -p $Tmp
[ ! -f $Tmp/markup.py ] &&  makedown

if   [ "$Q" = "RESET" ]
then   
    makedown
    $Cat/index.cgi > index.cgi 
    chmod 755 index.cgi
    echo "<pre>"; echo ""; date
    cksum  *
    echo "`cat * | cksum` TOTAL"
    echo '<a href="index.cgi">Continue.</a>'
    exit 1
fi


py2md() {  cat - |
  gawk '       
  /^#</,/^#>/               { next }
  InQ &&  gsub(/^""".*/,"") { InQ = 0; print "<pre>" ; next}
  InQ                       { print $0; next}
  !InQ && gsub(/^""".*/,"") {InQ=1; print "</pre>"; next}
  !InQ                      { print pretty($0) }
  END                       { if (InQ) print "</pre>" }

   BEGIN {
     Color4="brown"
     Color2="teal"  
     Color1="DarkBlue"
     Color3="f79a32"
     Words = "def "      \
             " for in int if or len  True False str lambda and not "\
             " class else while print import " \
             " sprintf rand :  switch"          \
             " BEGIN END next continue  "        \
             " return length "
     split(Words,Tmp," ")
     for(Word in Tmp) {
        Pat = Pat Sep "\\y" Tmp[Word] "\\y"
        Sep = "|"
     }
     Pat = "(" Pat ")"
    }
    function pretty(str) {
       line++
       pre=""
       if (str !~ /^[ \t]*$/)
         pre= sprintf("<font color=#BBB>%5d:</font>   ",line)
       gsub(/[\+=\*-/<>^]/,
            "<font color=black>&</font>",str)
       gsub(/<[\/]?code>/,"",str)
       gsub(Pat,      "<font color="Color1">&</font>",str) 
       gsub(/"[^"]*"/,"<font color="Color2">&</font>",str)
       gsub(/#.*/,   "<font color="Color3">&</font>",str)
       str = gensub(/(\y[_a-zA-Z0-9]+\y)\(/,
           "<font color="Color4">\\1</font>(","g",str)
       return pre str
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
    exit 1
fi
if true
then
    header $Q
    #$Cat/header.html
    echo "</head><body>"
    if [[ "$Q" =~ .*py$ ]]
    then $Cat/$Q  | py2md
    else $Cat/$Q.md
    fi | python $Tmp/markup.py
    #echo $Cat/footer.html
fi