#!/usr/bin/env python3
# encoding: utf-8

'''
    bbo

Usage:
    bbo.py <more_arg> <vec_in> <swf_file>... [-h]

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

with open(args["<vec_in>"]) as f:
  x = [[float(e) for e in l.split(",")] for l in f][0]

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

print("performance of learned policy on testing set:")
print(objf(x))

print("performance of pure policies on testing set:")

values=[objf(x) for x in [(-1,0),(1000000,1000001)]]
print("max:")
print(max(values))
print("min:")
print(min(values))
