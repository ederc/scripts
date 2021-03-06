#!/usr/bin/python

import sys
import os

benchs = 'cyclicnh(7)','cyclicn(7)','f744h()','f744()','katsuranh(11)',\
'katsuran(11)','katsuranh(12)','katsuran(12)','cyclicnh(8)','cyclicn(8)',\
'f855h()','f855()','econh(10)','econ(10)','econh(11)','econ(11)','noon8h()',\
'noon8()','noon9h()','noon9()'
tests = 'sba(i,1,0)','sba(i,1,1)','sba(i,0,0)','sba(i,0,1)'
names = 'sprintf("--- SBA(INC,F5) COMPUTING ---");\n',\
'sprintf("--- SBA(INC,ARRI) COMPUTING ---");\n','sprintf("--- SBA(NONINC,F5)\
COMPUTING ---");\n','sprintf("--- SBA(NONINC,ARRI) COMPUTING ---");\n'
# get number of examples computed

i = 0
while i < len(benchs):
  print benchs[i]+' start'
  j = 0
  while j < len(names):
    f = open('.singularrc','w')
    f.write('\
  system("--min-time", "0.001");\n\
  system("--ticks-per-sec", 1000);\n\
  option(noredefine);\n\
  LIB"f5ex2.lib";\n\n\
  string bench = '+benchs[i]+';\n\
  sprintf(bench);\n\
  int t = timer;\n'+\
  names[j]+'\
  ideal f = '+tests[j]+';\n\
  printf("SIZE OF BASIS:    %s",size(f));\n\
  printf("TIME:             %s", timer-t);\n\
  $')
    f.close()

    os.system('./Singular -q > temp.txt')
    testfile = 'tests/'+benchs[i]+'.res'
    f = open(testfile,'a')
    g = open('temp.txt','r')
    lines = g.readlines()
    for l in lines:
      f.write(l)
    f.close()
    g.close()
    j = j+1
  print benchs[i]+' done'
  print '----------------'
  i = i+1

os.system('rm -f temp.txt')
