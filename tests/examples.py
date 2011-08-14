#!/usr/bin/python

#############################################
# this script gets all computed examples,
# starts SINGULAR and generates the ideals,
# then prints the ideals to a tex file
# => it generates an APPENDIX FOR MY THESIS!
#############################################

# for sorting in the the natural way, i.e. "k11" is greater than "k2"
# this is needed for sorting the examples computed, e.g. 
# "Katsura 10" should be listed after "Katsura 9", but before "Katsura 11"

############################################################
# TOODOO: Need also the variables resp. the ring data
#         to define the ideals correclty!    
############################################################


import re
def natural_key(string_):
  """See http://www.codinghorror.com/blog/archives/001018.html"""
  return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',string_)]

import glob
import os

# get number of examples computed
pathtst = '*.tst'
tst = glob.glob(pathtst)

data = {}
ex = {}
linelength = 50

for t in tst:
  f = open(t,'r')
  lines = f.readlines()
  for idx,l in enumerate(lines):
    if 'Example:' in l:
      e1 = lines[idx].replace('Example: ','')
      e1 = e1.replace('sprintf("','')
      e1 = e1.replace('");','')
      e1 = e1.replace('\012','')
      e2 = lines[idx+1].replace('\012','')
      #e = e.replace('(','\(')
      #e = e.replace(')','\)')
      ex[e1] = e2
      break
  f.close()
print ex

tex = 'appendixIdeals.tex'
tex = open(tex,'w')

# write prelude for example appendix in
# phd thesis

tex.write('\chapter{Examples}\n\n')
tex.write('In the following we give a complete list of \
all examples used in this thesis. The examples are sorted \
by their names in increasing order. The code is given in \
the \\singular language and is the exact data used for \
the computations done. \n\nNote that ``\\verb?-h?\'\' at \
the ending of an example\'s name indicates that the \
corresponding ideal is homogeneous.\n\n')
for k in sorted(ex.iterkeys(),key=natural_key):
  data[k] = list()
  d = "LIB\\\"f5ex2.lib\\\";" + ex[k] + "i;$"
  ####################################################
  # still needs:
  # 1. numvars(basering)
  # 2. varstr(basering)
  # This data needs to be added in thesis, too!
  ####################################################

  # we preload data to 'exPhd.txt'

  os.system('echo "'+ d + '" | ./../Singular --no-rc -q > exPhd.txt')
  exphd = open('exPhd.txt','r')
  lines = exphd.readlines()
  
  # write example name
  
  tex.write('\\newpage\n\n\\large\n\n')
  tex.write('\\begin{center}\n'+ k + '\n\end{center}\n')
  tex.write('\\begin{center}\n')
  tex.write('\\small$\n\\begin{array}{lcl}\n') 
  #tex.write('\\begin{align*}')
  # write example code
  i = 1
  for l in lines:
    sl = l.split('=')
    s = sl[1].replace('\012','')
    if i<len(lines):
      tex.write('{\\tt ' + sl[0] + '} & {\\tt =} & ')
      w = len(s)
      if w<=linelength:
        s = s.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ s + '}\\\ \n')
      else:
        idx1 = s.find("+",linelength-10)
        idx2 = s.find("-",linelength-10)
        idx = min(idx1,idx2)
        if idx < 0:
          idx = max(idx1,idx2)
        sp = s[:idx]
        s = s[(idx):]
        # need to find the index of the next + or -
        # to cut at this point! TOODOO
        sp = sp.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ sp + '}\\\ \n')
        tex.write(' & &{} ')
        w = len(s)
        while w>linelength:
          idx1 = s.find("+",linelength-10)
          idx2 = s.find("-",linelength-10)
          idx = min(idx1,idx2)
          if idx < 0:
            idx = max(idx1,idx2)
          sp = s[:idx]
          s = s[(idx):]
          sp = sp.replace('^','\\mbox{\\textasciicircum}')
          tex.write('{\\tt '+ sp + '}\\\ \n')
          tex.write(' & &{} ')
          w = len(s)
        s = s.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ s + '}\\\ \n')
    else:
      tex.write('{\\tt ' + sl[0] + '} & {\\tt =} & ')
      w = len(s)
      if w<=linelength:
        s = s.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ s + '} \n')
      else:
        idx1 = s.find("+",linelength-10)
        idx2 = s.find("-",linelength-10)
        idx = min(idx1,idx2)
        if idx < 0:
          idx = max(idx1,idx2)
        sp = s[:idx]
        s = s[(idx):]
        # need to find the index of the next + or -
        # to cut at this point! TOODOO
        sp = sp.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ sp + '}\\\ \n')
        tex.write(' & &{} ')
        w = len(s)
        while w>linelength:
          idx1 = s.find("+",linelength-10)
          idx2 = s.find("-",linelength-10)
          idx = min(idx1,idx2)
          if idx < 0:
            idx = max(idx1,idx2)
          sp = s[:idx]
          s = s[(idx):]
          sp = sp.replace('^','\\mbox{\\textasciicircum}')
          tex.write('{\\tt '+ sp + '}\\\ \n')
          tex.write(' & &{} ')
          w = len(s)
        s = s.replace('^','\\mbox{\\textasciicircum}')
        tex.write('{\\tt '+ s + '} \n')
    i = i+1

  #tex.write('\\end{align*}')
  tex.write('\\end{array}\n$\n') 
  tex.write('\\end{center}\n\n')
tex.write('\\normalsize')
