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
import pandas as pd
import subprocess
import os
import time
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

with open(args["<norm_file>"]) as f:
  norm = [[float(e) for e in l.split(",")] for l in f]

with open(args["<vec_in>"]) as f:
  x = [[float(e) for e in l.split(",")] for l in f][0]

  #adding a mask for the three parameters we want to work on

with open(args["<more_arg>"]) as f:
  more_arg = [l.strip() for l in f]

def v2s(v):
  return(','.join([str(e) for e in v]))

def makev(x,norm,a,b):

  return("%s:%s:%s" %(v2s(x[a:b]),v2s(norm[0][a:b]),v2s(norm[1][a:b])))

def getperf(f,x):
  name="".join([str(i) for i in x])

  if name in policy_translation_dict:
      name=policy_translation_dict[name]
  else:
      name="learned"
  s=["ocs"
    ,"mixed"
    ,f
    ,"--alpha=%s" %makev(x,norm,0,len(x))
    ,"--threshold=200000"
    # ,"--alphathreshold=%s" %makev(x,norm,3,len(x))
    ,'--backfill=spf'
    ,'--stat=cumwait'
    ,"--ft_out=logs/"+name
    ]#+more_arg
  #print(s)
  #print(makev(x,norm,0,len(x)))
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
  return(sum(objs))


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



print("performance of pure policies on testing set:")
print("***************************")
for i in range(len(x)):
    policy_vector_short=v_one(i,1)
    policy_vector_long=v_one(i,-1)

    policy_name=policy_translation_dict[''.join(str(nb) for nb in policy_vector_short)]
    print("Testing,",policy_name,",",objf(policy_vector_short),sep="")
    policy_name=policy_translation_dict[''.join(str(nb) for nb in policy_vector_long)]
    print("Testing,",policy_name,",",objf(policy_vector_long),sep="")
    #va.append(objf(v_one(i,1)))

x_learned_combination=x
object_cum=objf(x_learned_combination,learned=True)
x_learned_combination_result=np.append(x_learned_combination,object_cum)
print("Testing,xnes",",",str(objf(x_learned_combination)),sep="")

# all_6=[0.39907593458657592, 0.083622307628245712, -0.041834035269045847, -0.23596929430357885, -0.039615326319370731, 0.19988312788222323]
# best_3=[0.12157746943579764, 0, 0, -0.77791115188174653, 0, 0.091226592066140685]
# best_3_of_1000=[0.16006270824621785, 0, -0.090181898686537434, 0, 0, 0.81206360146501111]
# first_3=[0.73885503700848676, 0.20039415601293994, -0.060750799943598603, 0, 0, 0]
# last_3=[0, 0, 0, -0.46089994306617332, -0.069728882531712819, 0.46937117856007143]
# print("Testing,all_6,",str(objf(all_6)),sep="")
# print("Testing,best_3,",str(objf(best_3)),sep="")
# print("Testing,best_3_of_1000,",str(objf(best_3_of_1000)),sep="")
# print("Testing,first_3,",str(objf(first_3)),sep="")
# print("Testing,last_3,",str(objf(last_3)),sep="")

# dict_learned={}
# dict_learned["all_6"]=[0.39907593458657592, 0.083622307628245712, -0.041834035269045847, -0.23596929430357885, -0.039615326319370731, 0.19988312788222323]
# dict_learned["best_3"]=[0.12157746943579764, 0, 0, -0.77791115188174653, 0, 0.091226592066140685]
# dict_learned["best_3_of_1000"]=[0.16006270824621785, 0, -0.090181898686537434, 0, 0, 0.81206360146501111]
# dict_learned["first_3"]=[0.73885503700848676, 0.20039415601293994, -0.060750799943598603, 0, 0, 0]
# dict_learned["first_3"]=[0.73885503700848676, 0.20039415601293994, -0.060750799943598603, 0, 0, 0]
# for comb in dict_learned:
#     print("Testing,",comb,",",objf(dict_learned[comb]),sep="")




print("***************************")

print("max :: ",str(max(values)))
print("min :: ",min(values))
print("performance of learned policy on testing set:")


print("learned combination :: ",str(object_cum))
print(x_learned_combination)


f=open("comp.txt","a")
f.write(str(x_learned_combination_result)+"\n")
f.close()

import itertools
import pandas as pd

lst = list(itertools.product([0, 1], repeat=6))
full_list=[]
for l in lst:
    x=array(x_learned_combination)*array(l)
    xl=list(x)
    xl.append(objf(xl,learned=True))
    full_list.append(xl)

d=pd.DataFrame(full_list,columns=[1,2,3,4,5,6,'cumwait'])
d.to_csv("logs/comparaison.csv")



print("extracting stat: maxwait time::")
for policy in policy_translation_dict:
    X = pd.read_csv("logs/"+policy_translation_dict[policy])
    X = X.ix[:,2:len(X.columns)]
    print('max,',policy_translation_dict[policy],",",X.abs().max()["w"],sep='')

X = pd.read_csv("logs/learned")
X = X.ix[:,2:len(X.columns)]
print("max,xnes,",X.abs().max()['w'],sep='')
    





print("extracting stat: cumwait time::")
for policy in policy_translation_dict:
    X = pd.read_csv("logs/"+policy_translation_dict[policy])
    X = X.ix[:,2:len(X.columns)]
    print("mean,",policy_translation_dict[policy],",",X["w"].abs().mean(),sep='')

X = pd.read_csv("logs/learned")
X = X.ix[:,2:len(X.columns)]
print("mean,learned,",X["w"].abs().mean(),sep='')





#print(','.join([str(e) for e in X.mean()]))
#print(','.join([str(e) for e in X.var()]))

# print(" max:")
# val={}
# i=0
# l=["q",'p','w','exp','r','a']
# for e in X.abs().max():
#     val[l[i]]=e
#     i+=1

 #print(val)
