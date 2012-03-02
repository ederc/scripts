#!/usr/bin/python

import sys
import os

# get number of examples computed

print "here"
f = open('.singularrc','w')
f.write('\
system("--min-time", "0.001");\n\
system("--ticks-per-sec", 1000);\n\
option(noredefine);\n\
LIB"f5ex2.lib";\n\n\
string bench = '+sys.argv[1]+';\n\
sprintf(bench);\n\
int t = timer;\n\
sprintf("--- sba(inc,f5) computing ---");\n\
ideal f = sba(i);\n\
size(f);\n\
printf("Time: %s", timer-t);\n\
killall();\n\
string bench = '+sys.argv[1]+';\n\
sprintf(bench);\n\
int t = timer;\n\
sprintf("--- sba(inc,arri) computing ---");\n\
ideal f = sba(i,1,1);\n\
size(f);\n\
printf("Time: %s", timer-t);\n\
killall();\n\
string bench = '+sys.argv[1]+';\n\
sprintf(bench);\n\
int t = timer;\n\
sprintf("--- sbai(noninc,f5) computing ---");\n\
ideal f = sba(i,0,0);\n\
size(f);\n\
printf("Time: %s", timer-t);\n\
killall();\n\
string bench = '+sys.argv[1]+';\n\
sprintf(bench);\n\
int t = timer;\n\
sprintf("--- sba(noninc,arri) computing ---");\n\
ideal f = sba(i,0,1);\n\
size(f);\n\
printf("Time: %s", timer-t);\n\
$')
print "there"
f.close()
