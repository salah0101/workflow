#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <more_arg> <norm_file> <vec_in> <swf_file>... [-h]

Options:
    <n>            budget
    <swf_file>     an input file
    <more_arg>     extra cli ocs arguments
    <vec_out>      output vector
    <norm_file>    normalizer file
    -h --help      show this help message and exit.
'''
from docopt import docopt
import pybrain
from subprocess import check_output
from numpy import array
import numpy as np
import subprocess
import os
import time
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

with open(args["<norm_file>"]) as f:
  norm = [[float(e) for e in l.split(",")] for l in f]

with open(args["<vec_in>"]) as f:
  x = [[float(e) for e in l.split(",")] for l in f][0]

with open(args["<more_arg>"]) as f:
  more_arg = [l.strip() for l in f]

def v2s(v):
  return(','.join([str(e) for e in v]))

def makev(x,norm,a,b):

  return("%s:%s:%s" %(v2s(x[a:b]),v2s(norm[0][a:b]),v2s(norm[1][a:b])))

def getperf(f,x):
  s=["ocs"
    ,"mixed"
    ,f
    ,"--alpha=%s" %makev(x,norm,0,len(x))
    ,"--threshold=200000"
    # ,"--alphathreshold=%s" %makev(x,norm,3,len(x))
    ,'--backfill=spf'
    ,'--stat=cumwait'
    ]#+more_arg
  #print(s)
  return(" ".join(s))

# ,"--alphapoly=%s" %(makev(x,norm[0],norm[1])

def objf(x,learned=False):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]

  if(learned):

      #print (objs)
      np.savetxt('logs/leanred_pol.csv',np.asarray(objs),delimiter=',')
    #  for obj in objs:
    #      print(obj)
  else:
      ch=""
      for i in range(len(x)):
          ch+=str(x[i])
      np.savetxt("logs/p"+ch+"_pol.csv",np.asarray(objs),delimiter=',')
      #pd_data=pd.read_csv("./leanred_pol.csv",delimiter=" ",names=["aa"])
  return objs


policy_translation_dict={'-100000': 'lqf',
 '0-10000': 'lpf',
 '00-1000': 'lcfs',
 '000-100': 'lexp',
 '0000-10': 'lrf',
 '00000-1': 'laf',
 '000001': 'saf',
 '000010': 'srf',
 '000100': 'sexp',
 '001000': 'fcfs',
 '010000': 'spf',
 '100000': 'sqf'}
print('\n\n')

def v_one(i,m):
  x = [0 for e in norm[0]]
  x[i]=m
  #print(x)
  return(x)
values=[objf(v_one(i,1)) for i in range(len(x))]+[objf(v_one(i,-1)) for i in range(len(x))]

import pandas as pd
df=pd.DataFrame()
dict_res={}
for i in range(len(x)):
    policy_vector_short=v_one(i,1)
    policy_vector_long=v_one(i,-1)

    policy_name_short=policy_translation_dict[''.join(str(nb) for nb in policy_vector_short)]
    print(policy_vector_short)
    print(objf(policy_vector_short))
    #df[policy_name_short]=objf(policy_vector_short)
    dict_res[policy_name_short]=objf(policy_vector_short)

    policy_name_long=policy_translation_dict[''.join(str(nb) for nb in policy_vector_long)]
    #print(policy_vector_long)
    #print(objf(policy_vector_long))
    #df[policy_vector_long]=objf(policy_vector_long)
    dict_res[policy_name_long]=objf(policy_vector_long)
    #va.append(objf(v_one(i,1)))
print("the final results is:::: ")
print(dict_res)
import csv
w = csv.writer(open("output_dict.csv", "w"))
for key, val in dict_res.items():
    w.writerow([key]+val)
