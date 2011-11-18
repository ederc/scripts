#!/usr/bin/python

#############################################
# this script uses two Singular programs
# the respective std implementation against
# each other.
#############################################

import re
import glob
import os

# set paths for comparison
pathsig   = "/home/ederc/uni/repos/devel/Singular"
pathstd   = "/home/ederc/uni/repos/singular/Singular"
pathcurr  = os.getcwd()
# compute data
os.system(pathsig+'/Singular -q > testsig.txt')
os.system(pathstd+'/Singular -q > teststd.txt')

# write all data to be compared into 
# compare.txt
# NOTE: do not forget to add ";" at the end of each
#       line in order to achieve correct Singular
#       code
compare = open('compare.txt','w')

# initialize first ideal
testsig = open('testsig.txt','r')
lines = testsig.readlines()

# first of all:
# define ring stuff out of first 3 lines
compare.write('ring r = ('+\
      lines[0].replace('\n','')+'),('+\
      lines[1].replace('\n','')+'),('+\
      lines[2].replace('\n','')+');\n')
compare.write('ideal g;\n')
for i in range(3,len(lines)-2):
  lines[i] = lines[i].replace('\n',';\n')
  compare.write(lines[i])
timersig = lines[len(lines)-2].replace('\n','')
sizesig = lines[len(lines)-1].replace('\n','')
testsig.close()

  
# initialize second ideal
compare.write('ideal G;\n')
teststd = open('teststd.txt','r')
lines = teststd.readlines()
for i in range(3,len(lines)-2):
  lines[i] = lines[i].replace('\n',';\n')
  lines[i] = lines[i].replace(lines[i][0],'G')
  compare.write(lines[i])
timerstd = lines[len(lines)-2].replace('\n','')
sizestd = lines[len(lines)-1].replace('\n','')
teststd.close()

maxtime = max(int(len(timerstd)),int(len(timersig)))
maxsize = max(int(len(sizestd)),int(len(sizesig)))
strstd = 'Time %*s  --  Size %*s  ( STD )' % (maxtime,timerstd,maxsize,sizestd)
strsig = 'Time %*s  --  Size %*s  ( SIGNATURE-BASED )' % (maxtime,timersig,maxsize,sizesig)
print strstd
print strsig
# reduce the standard basis against each other
# store the result in a list l
# if there exists at least one nonzero entry in l
# then print 1,
# else print 0
compare.write('attrib(g,"isSB",1);')
compare.write('attrib(G,"isSB",1);')
compare.write('list l = reduce(g,G);\nint tt=0;\n')
# NOTE: In Singular size(ideal i) gives you the number of
#       nonzero generators in i. 
# => checking if size(l[1])>0 is enough for us
compare.write('if(size(l[1])!=0){tt=1;}\n')
compare.write('printf("reduce STD with SIG: %s",tt);')
compare.write('l = reduce(G,g);\n')
compare.write('if(size(l[1])!=0){tt=1;}\n')
compare.write('printf("reduce SIG with STD: %s",tt);')
compare.write('$')
compare.close()
os.system(pathstd+'/Singular -q --no-rc < '+pathcurr+'/compare.txt')
