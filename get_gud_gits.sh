#!/bin/sh
#bash get_gud_gits.sh <list>.txt
readarray array <<< $( cat "$@" )

mkdir -p ~/gits && cd ~/gits

for element in ${array[@]}
do
  echo "clonning $element"
  git clone $element
done