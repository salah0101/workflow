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
    # ,"--alphathreshold=%s" %makev(x,norm,3,len(x))
    ]+more_arg
  return(" ".join(s))

# ,"--alphapoly=%s" %(makev(x,norm[0],norm[1])
import csv
def objf(x):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]

  iteration=list(x[:])
  #iteration=[_ for _ in x]
  iteration.append(sum(objs))
  #print("iteration:",iteration)
  with open("logs/alphas.csv", "a") as myfile:
      myfile.write(str(iteration)[1:-1]+'\n')

  #print("objectives: ",str(sum(objs)))
  return(sum(objs))

print("performance of optimized policy on training set:")
x0 = array([0.0 for e in norm[0]])
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
  l.maxLearningSteps=20
  l.batchSize=25
  r=l.learn()
  allEvaluations=l._allEvaluations
  allEvaluated=l._allEvaluated
  d=pd.DataFrame(allEvaluations,columns=['cumwait'])
  d.to_csv("logs/allEvaluations.csv")

  d=pd.DataFrame(allEvaluated,columns=["q","p","w","exp","r","a"])
  d.to_csv("logs/allEvaluated.csv")


  #print('\n    all  Evaluations\n', allEvaluations)
  #print('\n    all  allEvaluated\n', allEvaluated)

  print(desc)
  print(objf(r[0]))

with open(args["<vec_out>"], 'w') as f:
  f.write(",".join([str(e) for e in r[0]]))

print("performance of pure policies on training set:")
def v_one(i,m):
  x = [0 for e in norm[0]]
  x[i]=m
  print(x)
  return(x)


va=[]
print("***************************")
for i in range(len(x0)):
    print(objf(v_one(i,1)))
    print(objf(v_one(i,-1)))
    #va.append(objf(v_one(i,1)))

print("***************************")

values=[objf(v_one(i,1)) for i in range(len(x0))]+[objf(v_one(i,-1)) for i in range(len(x0))]

print("max:")
print(max(values))
print("min:")
print(min(values))
