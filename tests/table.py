#!/usr/bin/python

# for sorting in the the natural way, i.e. "k11" is greater than "k2"
# this is needed for sorting the examples computed, e.g. 
# "Katsura 10" should be listed after "Katsura 9", but before "Katsura 11"
import re
def natural_key(string_):
  """See http://www.codinghorror.com/blog/archives/001018.html"""
  return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',string_)]

import glob
from random import choice
import operator

# get number of examples computed
pathtst = '*.tst'
tst = glob.glob(pathtst)
numExamples = len(tst)

# get all result files
# their number is equal to the number
# of algorithms compared
pathres = '*.res'
res = glob.glob(pathres)

data = {}
examples = list()
# create 2-dimensional arrays for 
# each algorithm:
# size: numExamples x 5
# 5 <=> (zeroReds,singleReds,totalReds,timings,memory)
# in the end we have a 3-dimensional array:
# data --> results --> example --> algorithm
# note that this a bit strange order is useful, since we
# want to create latex tables out of it!

# initialize examples entry in dictionary at the beginning
# stores all examples in a list => need to search them only once!

init = choice(res)
init = open(init,'r')
lines = init.readlines()
for l in lines:
  if l.find('Example:') != -1:
    ex = l.replace('Example: ','')
    ex = ex.replace('\012','') # deletes newline
    ex = '{\\tt ' + ex + '}'
    examples.append(ex)
init.close()

dic = {'zero':'Zero','singleRed':'Reductions','totalRed':'steps',\
'time':'Timings','memory':'Memory consumption', 'size':'Size'}
for k in dic: 
  data[k] = {}
  
  for ex in examples:
    data[k][ex] = {}

  # now we start the loop over all results
  for f in res:
    tmp = f.split('.')
    if tmp[0] == 'sigstd':
      tmp[0] = 1
    elif tmp[0] == 'sigstdr':
      tmp[0] = 2
    elif tmp[0] == 'ap':
      tmp[0] = 3
    elif tmp[0] == 'mm':
      tmp[0] = 4
    elif tmp[0] == 'ggv':
      tmp[0] = 5

    f = open(f,'r')
    lines = f.readlines()
    for l in lines:
      if l.find('Example:') != -1:
        ex = l.replace('Example: ','')
        ex = ex.replace('\012','') # deletes newline
        ex = '{\\tt ' + ex + '}'
      if l.find(dic[k]) != -1:
        val = ''.join(i for i in l if i.isdigit())
        if k == 'time' and val != '':
          val = long(val)/1000.0
          data[k][ex][tmp[0]]=val
        elif k == 'memory' and val != '':
          val = (int(val)/1048576.0)
          data[k][ex][tmp[0]]=val
        elif k == 'singleRed' and val != '':
          val = int(val)
          data[k][ex][tmp[0]]=val
        elif k == 'totalRed' and val != '':
          val = int(val)
          data[k][ex][tmp[0]]=val
        elif k == 'zero' and val != '':
          val = int(val)
          data[k][ex][tmp[0]]=val
        elif k == 'size' and val != '':
          val = int(val)
          data[k][ex][tmp[0]]=val
    f.close()

print '---------------'
print data
print '---------------'
# sort data lists by respective keys to print their values in the 
# correct colors
for iter in ['time','memory']:
  for ex in examples: 
    col = 1
    tempDat = data[iter][ex]
    tempDatTmp = ''
    
    for key,val in sorted(tempDat.iteritems(), key=operator.itemgetter(1)):
    #for key,val in sorted(tempDat.iteritems(), key=lambda\
    #(k,v):(v,k)):
      #print tempDat[key] + '---' + tempDatTmp
      if tempDat[key] == tempDatTmp:
        tempDat[key]= '{\color{' + str(colTmp) + '}' + format(val,',.3f') + '}'
        col += 1
      else:
        tempDatTmp = tempDat[key]
        tempDat[key]= '{\color{' + str(col) + '}' + format(val,',.3f') + '}'
        colTmp = col
        col += 1

for iter in ['singleRed','totalRed','zero','size']:
  for ex in examples: 
    col = 1
    tempDat = data[iter][ex]
    tempDatTmp = ''
    
    for key,val in sorted(tempDat.iteritems(), key=operator.itemgetter(1)):
    #for key,val in sorted(tempDat.iteritems(), key=lambda\
    #(k,v):(v,k)):
      #print tempDat[key] + '---' + tempDatTmp
      if tempDat[key] == tempDatTmp:
        tempDat[key]= '{\color{' + str(colTmp) + '}' + format(val,',') + '}'
        col += 1
      else:
        tempDatTmp = tempDat[key]
        tempDat[key]= '{\color{' + str(col) + '}' + format(val,',') + '}'
        colTmp = col
        col += 1

# at this point all the data is generated and added to "data"
# next we need to extract latex code out of it

for k in data:
  print data
    # we want to have the data being aligned at the
    # decimal dot
    # => this only happens for
    #    MEMORY & TIMINGS!
    # => we need to make three parts of our number:
    #    a) the part bigger 1
    #    b) the dot
    #    c) the part smaller 1
    # since we are coloring the numbers, we need to 
    # color each part (also the dot!)!
  if k in ['memory','time']:
    tex = k + '.tex'
    tex = open(tex,'w')
    tex.write('\\begin{table}\n\\begin{centering}\n\
  \t\\begin{tabular}{|c|D{.}{.}{-1}|D{.}{.}{-1}|D{.}{.}{-1}|D{.}{.}{-1}|D{.}{.}{-1}|}\n\t\t\hline\n\
  \t\tTest case & \\multicolumn{1}{c|}{$\sigstd$} & \\multicolumn{1}{c|}{$\sigstdr$} \
  & \\multicolumn{1}{c|}{$\\ap$} & \\multicolumn{1}{c|}{$\mm$} \
  & \\multicolumn{1}{c|}{$\ggv$}\\\ \n\t\t\\hline\n\t\t\\hline\n')
    
  # we insert the data and sort it by the names of the examples
  # using the above defined natural sort key such that, for 
  # example, "Katsura 9" is smaller than "Katsura 10"
    for l in sorted(data[k].iterkeys(),key=natural_key):
      tex.write('\t\t' + l)
      for m in data[k][l]:
        # get substring containing coloring information
        col1 = data[k][l][m][:10]
        col2 = '}'
        tmp = data[k][l][m].split('.')
        val1 = tmp[0] + col2
        
        # we cannot colorize the dot as otherwise dcolumn gets bollocks!
        #val2 = col1 + '.' + col2
        val2 = '.'
        val3 = col1 + tmp[1]
        tex.write(' & ' + val1 + val2 + val3)

      tex.write('\\\ \n\t\t\\hline\n')
    tex.write('\t\\end{tabular}\n\t\\par\n\\end{centering}\n\n\\caption{')
  else:
    tex = k + '.tex'
    tex = open(tex,'w')
    tex.write('\\begin{table}\n\\begin{centering}\n\
  \t\\begin{tabular}{|c|c|c|c|c|c|}\n\t\t\hline\n\
  \t\tTest case & $\sigstd$ & $\sigstdr$ \
  & $\\ap$ & $\mm$ & $\ggv$ \\\ \
  \n\t\t\\hline\n\t\t\\hline\n')
    
  # we insert the data and sort it by the names of the examples
  # using the above defined natural sort key such that, for 
  # example, "Katsura 9" is smaller than "Katsura 10"
    for l in sorted(data[k].iterkeys(),key=natural_key):
      tex.write('\t\t' + l)
      for m in data[k][l]:

        tex.write(' & ' + str(data[k][l][m]))
      tex.write('\\\ \n\t\t\\hline\n')
    tex.write('\t\\end{tabular}\n\t\\par\n\\end{centering}\n\n\\caption{')
# fills the caption of the tables depending on the corresponding
# data presented
  if k == 'singleRed':
    tex.write('Number of critical pairs not detected by the respective \
criteria used.')
  elif k == 'totalRed':
    tex.write('Number of all reduction steps throughout the computations \
of the algorithms.')
  elif k == 'zero':
    tex.write('Number of zero reductions computed by the algorithms.')
  elif k == 'time':
    tex.write('Time needed to compute a standard basis of the respective test \
case, given in seconds.')
  elif k == 'memory':
    tex.write('Memory used to compute a standard basis of the respective test \
case, given in Megabyte.')
  elif k == 'size':
    tex.write('Size of the resulting standard basis.')
  tex.write('}\n\
\\label{tab:ch5:' + k + '}')
  tex.write('\n\\end{table}')
  tex.close()

# as a last step we merge all resulting latex tables in
# one tex file

tex = 'complete.tex'
tex = open(tex,'w')
pathtex = '*.tex'
texs = glob.glob(pathtex)
for t in texs:

# if complete.tex already exists it should not be
# looped over!
  if t in ['singleRed.tex','totalRed.tex','size.tex','zero.tex','time.tex','memory.tex']:
    t = open(t,'r')
    lines = t.readlines()
    for l in lines:
      tex.write(l)
    tex.write('\n\n\n')
tex.close()  
