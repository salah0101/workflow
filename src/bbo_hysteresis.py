#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <n> <more_arg> <vec_out> <swf_file>... [-h]

Options:
    <n>            budget
    <swf_file>     an input file
    <more_arg>     extra cli ocs arguments
    <vec_out>      output vector
    -h --help      show this help message and exit.
'''
from docopt import docopt
import pybrain
from subprocess import check_output
from numpy import array
import subprocess
import os
import time

#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

with open(args["<more_arg>"]) as f:
 more_arg = [l.strip() for l in f]

def v2s(v):
  return(','.join([str(e) for e in v]))

def getperf(f,x):
  s=["ocs"
    ,"hysteresis"
    ,f
    ,"--thresholds=%s" %v2s(x)
    ]+more_arg
  return(" ".join(s))

def objf(x):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]
  return(sum(objs))

print("performance of optimized policy on training set:")
x0 = array([0.0,0.0])
import pybrain.optimization as opt
lopt = [("xnes",opt.XNES(objf, x0))]
    # ("snes",opt.SNES(objf, x0)),
    # ("fem",opt.FEM(objf, x0)),
    # ("memetic",opt.MemeticSearch(objf, x0)),
    # ("inmemetic",opt.InnerMemeticSearch(objf, x0)),
    # ("imemetic",opt.InverseMemeticSearch(objf, x0)),
    # ("inimemetic",opt.InnerInverseMemeticSearch(objf, x0)),
    # ("spsa",opt.SimpleSPSA(objf, x0)),
    # ("pgpe",opt.PGPE(objf, x0)),
    # ("es",opt.ES(objf, x0))]
for desc,l in lopt:
  l.minimize = True
  l.mustMinimize = True
  l.maxEvaluations = int(args["<n>"])
  r=l.learn()
  print(desc)
  print(objf(r[0]))

with open(args["<vec_out>"], 'w') as f:
  f.write(",".join([str(e) for e in r[0]]))

print("performance of pure policies on training set:")

values=[objf(x) for x in [(0,0.00001),(1000000,1000001)]]
print("max:")
print(max(values))
print("min:")
print(min(values))
