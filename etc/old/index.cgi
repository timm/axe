#!/bin/bash
# -*- bash -*- 
########################################################
# begin config section

Default=index
# the est
Src=${Src='https://rawgithub.com/timm/axe/master'}
Cat=${Cat=" wget -q -O - $Src"}

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

# end config section
#########################################################
# from here down, you should not need to change anything
[ -n "$1" ] && QUERY_STRING=$1

Q=${QUERY_STRING:=$Default}
Q=$(echo $Q | sed 's/[^\/\.0-9a-zA-Z]//g')

[ "$2" = "render" ] && Cat="cat ./"

makedown() {   cat<<EOF > $Tmp/markup.py
import markdown,sys
str = '\n'.join(map(lambda x: x.rstrip('\n'),
                     sys.stdin.readlines()))
print markdown.Markdown(extensions=['footnotes',
           'def_list','tables','toc']).convert(str)
EOF
}
makemd() { cat<<"EOF" > $Tmp/py2md.awk
/^#aka /                  { Subs[$2] = $3 }
/^#</,/^#>/               { next }
                          { for (Sub in Subs) 
                               gsub("\y" Sub "\\y",Subs[Sub]) }
InQ &&  gsub(/^""".*/,"") { InQ = 0; print "<pre>" ; next}
InQ                       { print $0; next}
!InQ && gsub(/^""".*/,"") {InQ=1; print "</pre>"; next}
!InQ                      { print pretty($0) }
END                       { if (InQ) print "</pre>" }
BEGIN {

     Color4="brown"; 
     Color2="teal"  
     Color1="DarkBlue"
     Color3="f79a32"

     Words = "def "      \
             " for in int if or elif sorted float True False str lambda and not "\
             " class else while print import " \
             " sprintf rand :  switch"          \
             " BEGIN END next continue  "        \
             " return len "
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
  gsub(/[\+=\*-/<>^{}\[\]]/,
        "<font color=gray><b>&</b></font>",str)
  gsub(/<[\/]?code>/,"",str)
  gsub(Pat,      "<font color="Color1"><b>&</b></font>",str) 
  gsub(/"[^"]*"/,"<font color="Color2">&</font>",str)
  gsub(/#.*/,   "<font color="Color3">&</font>",str)
  str = gensub(/(\y[_a-zA-Z0-9]+\y)\(/,
        "<font color="Color4">\\1</font>(","g",str)
  return pre str
}
EOF
}
mkdir -p $Tmp
[ ! -f "$Tmp/markup.py" ] && makedown
[ ! -f "$Tmp/py2md.awk" ] && makemd

if   [ "$Q" = "REFRESH" ]
then
    makedown
    makemd
    $Cat/index.cgi > index.cgi
    chmod 755 index.cgi
    chmod +x index.cgi
    echo "<p>"; date
    echo "<p>"; cksum  index.cgi
    echo "<p>"; ls -lsat
    echo '<p><a href="index.cgi">Continue.</a>'
    exit 1    
fi
  
echo "Content-type: text/html"
echo ""
header $Q
#$Cat/header.html
echo "</head><body>"
if [[ "$Q" =~ .*py$ ]]
    then $Cat/$Q  | gawk -f $Tmp/py2md.awk
    else $Cat/$Q
fi | python $Tmp/markup.py
#echo $Cat/footer.html
