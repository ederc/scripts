#!/bin/bash
set -xv
echo $1
echo $2
for i in *.tst;
do
  echo $i
  sed -i -e "s/$1/$2/g" $i
done
