
V="5.1.0"

getgawk() {
  wget -O gawk.tar.gz https://ftp.gnu.org/gnu/gawk/gawk-${V}.tar.gz
  tar xzf gawk.tar.gz
  cd gawk-${V}
  ./configure; sudo make; sudo make install
  cd ..
  rm -rf gawk.tar.gz gawk-${V}
}

chmod +x *.auk auk
which gawk > /dev/null || getgawk
