#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <n> <more_arg> <norm_file> <vec_out> <swf_file>... [-h]

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
import subprocess
import os
import time
import pandas as pd

#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

with open(args["<norm_file>"]) as f:
 norm = [[float(e) for e in l.split(",")] for l in f]

with open(args["<more_arg>"]) as f:
 more_arg = [l.strip() for l in f]

def v2s(v):
  return(','.join([str(e) for e in v]))

def makev(x,norm,a,b):
  #print("!!!! what is this!!")
  #print(v2s(x[a:b]),".......")
  #print(v2s(norm[0][a:b]),".......")
  #print(v2s(norm[1][a:b]),".......")
  return("%s:%s:%s" %(v2s(x[a:b]),v2s(norm[0][a:b]),v2s(norm[1][a:b])))

def getperf(f,x):
  s=["ocs"
    ,"mixed"
    ,f
    ,"--alpha=%s" %makev(x,norm,0,len(x))
    ,"--threshold=200000"
    # ,"--alphathreshold=%s" %makev(x,norm,3,len(x))
    ]+more_arg
  return(" ".join(s))

# ,"--alphapoly=%s" %(makev(x,norm[0],norm[1])
import csv

import numpy as np
def objf(x):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]

  sum_objs=sum(objs)



  scaling_term=a=10**(len(str(int(sum_objs)))-1)# scaling term to give penalty the same size of the objective
  penalty=np.sum(np.abs(x)) + 1/np.sum(np.abs(x))# the penalty term to stop the values from converging to 0


  iteration=list(x[:])
  iteration.append(sum_objs)

  with open("logs/alphas.csv", "a") as myfile:
      myfile.write(str(iteration)[1:-1]+'\n')


  #maxi=max(objs)
  #objs=np.array(objs)* np.array(objs)/maxi
  #print("obejective::",sum_objs)
  #print("penalty::", penalty*scaling_term)

  # global minimun_value
  # if (sum_objs==minimun_value):
  #   sum_objs=sum_objs*1.2
  #   print("same old!!!")
  # elif (sum_objs<minimun_value):
  #   minimun_value=sum_objs
  #   print("aha, a pertubence in the force")
  return(sum_objs + penalty*scaling_term)
def objf_pure(x):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]
  sum_objs=sum(objs)
  return(sum_objs)
print("blablabla")
for f in args["<swf_file>"]:
  print(f)

print("performance of optimized policy on training set:")
#x0 = array([0.0 for e in norm[0]])
x0=array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
import pybrain.optimization as opt
lopt = [
        ("xnes",opt.XNES(objf, x0)),
    # ("r1",opt.Rank1NES(objf, x0)),
        # ("snes",opt.SNES(objf, x0)),
        # ("fem",opt.FEM(objf, x0)),
    # ("ves",opt.VanillaGradientEvolutionStrategies(objf, x0)),
        # ("memetic",opt.MemeticSearch(objf, x0)),
        # ("inmemetic",opt.InnerMemeticSearch(objf, x0)),
        # ("imemetic",opt.InverseMemeticSearch(objf, x0)),
        # ("inimemetic",opt.InnerInverseMemeticSearch(objf, x0)),
    # ("pso",opt.ParticleSwarmOptimizer(objf, x0)),
    # ("ga",opt.GA(objf, x0)),
        # ("spsa",opt.SimpleSPSA(objf, x0)),
        # ("pgpe",opt.PGPE(objf, x0)),
        # ("es",opt.ES(objf, x0))
    ]
for desc,l in lopt:
  l.minimize = True
  l.mustMinimize = True
  l.verbose = True
  storeAllEvaluations=True
  storeAllEvaluated=True
  #l.maxEvaluations = int(args["<n>"])
  l.maxLearningSteps=int(args["<n>"])
  l.batchSize=25
  r=l.learn()
  allEvaluations=l._allEvaluations
  allEvaluated=l._allEvaluated
  d=pd.DataFrame(allEvaluations,columns=['cumbsld'])
  d.to_csv("logs/allEvaluations.csv")

  d=pd.DataFrame(allEvaluated,columns=["q","p","w","exp","r","a"])
  d.to_csv("logs/allEvaluated.csv")


  #print('\n    all  Evaluations\n', allEvaluations)
  #print('\n    all  allEvaluated\n', allEvaluated)



with open(args["<vec_out>"], 'w') as f:
  f.write(",".join([str(e) for e in r[0]]))

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
print('\n')


print("performance of pure policies on training set:")
def v_one(i,m):
  x = [0 for e in norm[0]]
  x[i]=m
  return(x)


va=[]
print("***************************")
for i in range(len(x0)):
    policy_vector_short=v_one(i,1)
    policy_vector_long=v_one(i,-1)

    policy_name=policy_translation_dict[''.join(str(nb) for nb in policy_vector_short)]
    print("Training,",policy_name,",",objf_pure(policy_vector_short),sep="")
    policy_name=policy_translation_dict[''.join(str(nb) for nb in policy_vector_long)]
    print("Training,",policy_name,",",objf_pure(policy_vector_long),sep="")
    #va.append(objf(v_one(i,1)))
print("Training,",desc,",",str(objf_pure(r[0])),sep="")
print("***************************")

values=[objf_pure(v_one(i,1)) for i in range(len(x0))]+[objf_pure(v_one(i,-1)) for i in range(len(x0))]

print("max:")
print(max(values))
print("min:")
print(min(values))
