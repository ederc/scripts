#!/bin/bash

#####################################################
# This is a script to automize the testings of 
# diverse signature-based standard basis algorithms.
# It does not only save the results in a human
# readable file, but also creates a file for the 
# latex import.
#####################################################

echo -e "------------------------------\n \
EXPERIMENTAL RESULTS FOR ${1} \n\
------------------------------" > tests/${1}.res;
for i in tests/*.tst;
do
  echo -e "\n" >> tests/${1}.res;
  ./Singular -q --no-rc < ${i} >> tests/${1}.res;
# get gb size out of file
  siz=`sed -n '$p' tests/${1}.res`;
  sed -i '$d' tests/${1}.res;
# get input ideal size out of file
  isiz=`sed -n '$p' tests/${1}.res`;
  sed -i '$d' tests/${1}.res;
# get number of variables in poly ring
  vars=`sed -n '$p' tests/${1}.res`;
  sed -i '$d' tests/${1}.res;
# get memory consumption out of file
# computed in bytes
  mem=`sed -n '$p' tests/${1}.res`;
  sed -i '$d' tests/${1}.res;
# get timings out of file
# computed in milliseconds
  tim=`sed -n '$p' tests/${1}.res`;
  sed -i '$d' tests/${1}.res;
  echo -n "Size: " >> tests/${1}.res;
  echo "$siz" >> tests/${1}.res;
  echo -n "Memory consumption: " >> tests/${1}.res;
# compute memory consumption in mega bytes and 
# write it back to the expresults file
  # mem=`echo "scale=3; $mem / 1048576" | bc`;
  echo "$mem Bytes" >> tests/${1}.res;
  echo -n "Timings: " >> tests/${1}.res;
# compute timings in seconds and 
# write it back to the expresults file
  #tim=`echo "scale=3; $tim / 1000" | bc`;
  echo "$tim millisec" >> tests/${1}.res;
  echo "$i done."
done
