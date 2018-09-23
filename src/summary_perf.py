#!/usr/bin/env python
# encoding: utf-8

'''
    summary

Usage:
    summary.py <perf_file>

Options:
    -o <option>    some option
    -h --help      show this help message and exit.
'''
from docopt import docopt
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

import numpy as np
import pandas as pd

print("Importing Data.")
y = pd.read_csv(args["<perf_file>"],sep=",")
yctx = y.ix[:,0]
yf = y.ix[:,1:]

print("Worst fixed performance %s or %0.3f%% of FCFS" % (yf.mean().max(),100*(yf.mean().max()-y.ix[:,1].mean())/y.ix[:,1].mean()))
print("Best fixed performance  %s or %0.3f%% of FCFS" % (yf.mean().min(),100*(yf.mean().min()-y.ix[:,1].mean())/y.ix[:,1].mean()))
print("Learned performance rf  %s or %0.3f%% of FCFS" % (yctx.mean(),100*((yctx.mean())-y.ix[:,1].mean())/y.ix[:,1].mean()))
