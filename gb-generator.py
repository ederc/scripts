#!/usr/bin/python

import sys
import fnmatch
import os
import shutil
import argparse
import time

# generates a 10 digit hash value from the current date and time
# to append to the already existing ".singularrc" filename in order
# to restore it later on
def hash():
  return '{0:010x}'.format(int(time.time() * 256))[:10]

# gets number of lines in a given text file
def linesInFile(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
  
currentdir = os.getcwd()

parser = argparse.ArgumentParser(description='Generates a "*.txt" file that\
    can be loaded to Singular to generate a new benchmark for mathicgb.\n\
    NOTE: For this ".singularrc" is overriden. The script tries to copy\
    a currently available ".singularrc" beforehand and restore it afterwards,\
    so please make sure the rights for your ".singularrc" are correct or you\
    have already copied it by your own.')
parser.add_argument('-o', '--output', required=True,
    help='Output file name')
parser.add_argument('-c', '--char', required=True,
    help='Characteristic of the underlying field; must be > 0')
parser.add_argument('-n', '--nvariables', type=int, required=True, 
    help='Number of variables to be used; must be > 0 and < 53')
parser.add_argument('-p', '--npolys', default='5', required=False, 
    help='Number of polynomials in the system; default is 5, if benchmark is\
    given then this number is overwritten')
parser.add_argument('-ord', '--ordering', default='dp', required=False,
    help='Define the ordering in which you need the example to be generated.\n\
    Default is "dp".')
parser.add_argument('-b', '--bench', default='', required=False,
    help='Define to use one of Singular\'s predefined benchmarks like\
    cyclic or katsura')
parser.add_argument('-i', '--interred', action="store_true", default=False,
    help='set this flag if the ideal has to be interreduced')
parser.add_argument('-hg', '--homog', action="store_true", default=False,
    help='Set this flag if the ideal should be homogenized.\
    Note that this flag increases the number of variables by 1.')

args = parser.parse_args()

# generate hash value if needed
hash_value = hash()

# old_singularrc?
old_singularrc = 0

# generate list of variables (alphabetical letters, small first, then capital)
variables = []

# get 1 more variable if homogenization is wanted
if args.homog:
  args.nvariables += 1

print args.nvariables
if args.nvariables < 27:
  variables.extend(map(chr, range(97, 97+args.nvariables)))
else:
  variables.extend(map(chr, range(97, 123)))
  variables.extend(map(chr, range(65, 65-26+args.nvariables)))

# set number of variables down again if homogenization wanted in order to
# generate the correct benchmarks with -b option
if args.homog:
  args.nvariables -= 1

print variables

if os.path.exists('.singularrc'):
  old_singularrc = 1
  shutil.copyfile('.singularrc', '.singularrc-'+hash_value)

# write new ".singularrc" file
f = open('.singularrc', 'w')
f.write('\
option("noredefine");\n\
option("redSB");\n\
LIB"poly.lib";\nLIB"random.lib";\n\
ring RR = '+args.char+', (')

var_string =''
for l in variables:
  var_string += l+', '

var_string = var_string[:len(var_string)-2]
f.write(var_string+'), '+args.ordering+';\n')

# if bench is given
if args.bench:
  f.write('ideal II = '+args.bench+'('+str(args.nvariables)+');\n')
if args.homog:
  f.write('II = homog(II,var('+str(args.nvariables+1)+'));\n')

#else we generate a random sparse ideal
else:
  f.write('ideal II = sparseid('+args.npolys+', 2, 5, 90);\n')

# if trimming is wished
if args.interred:
  f.write('II = interred(II);')

f.write('II;\n')
f.write('$')
f.close()

# call Singular and generate output string
os.system('Singular -q > '+args.output+'.tmp.ideal')
ideal_string = ''
f = open(args.output+'.tmp.ideal', 'r')
lines = f.readlines()
for l in lines:
  pos = l.find('=')
  ideal_string += l[pos+1:]

f.close()

# start generating output file
os.system('touch '+args.output+'.ideal')
f = open(args.output+'.ideal', 'w')
f.write(args.char+' '+str(args.nvariables))
i = 0
while i < int(args.nvariables):
  f.write(' 1')
  i += 1
f.write('\n')
f.write(str(linesInFile(args.output+'.tmp.ideal'))+'\n')

# now add the ideal_string to this file
f.write(ideal_string)
f.close()

# get rid of generated ".singuarrc" file
os.remove('.singularrc')

# get rid of temporary file
os.remove(args.output+'.tmp.ideal')

# restore old ".singularrc" if it existed
if old_singularrc == 1:
  shutil.copyfile('.singularrc-'+hash_value, '.singularrc')
  os.remove('.singularrc-'+hash_value)
