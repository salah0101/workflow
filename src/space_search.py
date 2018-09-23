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
from random import randint,choice
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
    ,f #f is the name of file we are working on
    ,"--alpha=%s" %makev(x,norm,0,len(x))
    ,"--threshold=200000"
    # ,"--alphathreshold=%s" %makev(x,norm,3,len(x))
    ,'--backfill=spf'
    ,'--stat=cumwait'
    ]#+more_arg
  #print(s)
  return(" ".join(s))

def objf(x):
  processes = [subprocess.Popen(getperf(f,x),stdout=subprocess.PIPE,shell=True) for f in args["<swf_file>"]]
  for p in processes:
    if p.poll() is None:
       p.wait()
  objs = [float(x.stdout.read()) for x in processes]
  return(list(objs))

if __name__=="__main__":
    # prepare the linst of value that will be tested:
    space=[]
    for i in range(10):
        q=randint(0,100)
        p=randint(0,100-q)
        w=(100-q-p)
        l=[q/100*choice([-1,1]),p/100*choice([-1,1]),w/100*choice([-1,1])]
        if (l not in  space):
            space.append(l)

    #then we execute the testing process

    space_res=[]
    ch="q,p,w,"+",".join(["week"+str(i) for i in range(1,31)])+",cumwait"
    print(ch)
    #print("q,p,w,cumwait")
    for comb in space:

        res=objf(comb+[0,0,0])
        comb+=res 
        comb.append(sum(res))
        space_res.append(comb)
        print(",".join(str(e) for e in comb))
        #print(comb)
