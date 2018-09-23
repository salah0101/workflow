#!/usr/bin/env python3
# encoding: utf-8

'''
    normalize

Usage:
    normalize.py <file> [-h]

Options:
    <file>     an input file
    -h --help      show this help message and exit.
'''
from docopt import docopt
import pandas as pd
args = docopt(__doc__, version='1.0.0rc2')

X = pd.read_csv(args["<file>"],sep=",",dtype=float,header=0)
X = X.ix[:,2:len(X.columns)]

#print(','.join([str(e) for e in X.mean()]))
#print(','.join([str(e) for e in X.var()]))

print(','.join([str(e) for e in X.abs().min()]))
print(','.join([str(e) for e in X.abs().max()-X.abs().min()]))
#print(','.join(['0.5' for e in X.abs().min()]))
#print(','.join(['0.5' for e in X.abs().max()-X.abs().min()]))
