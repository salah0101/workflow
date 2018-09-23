#!/usr/bin/env python
# encoding: utf-8
'''
    predict 

Usage:
    mlc_apply.py <perf_file> <feature_file> <model_file>

Options:
    -o <option>    some option
    -h --help      show this help message and exit.
'''
from docopt import docopt
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

#!/usr/bin/env python
# encoding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
import pandas as pd
from sklearn.externals import joblib

print("Importing Data.")
X = pd.read_csv(args["<feature_file>"],sep=",")
y = pd.read_csv(args["<perf_file>"],sep=",")
p = joblib.load(args['<model_file>']) 
yp=p.predict(X)

min_ids=pd.DataFrame(yp).idxmin(axis=1)

def custom_loss(ground_truth, predictions):
    my=ground_truth
    min_ids=pd.DataFrame(predictions).idxmin(axis=1)
    lmy=my.reset_index()
    lmy.columns=range(0,len(lmy.columns))
    lmy=lmy.drop(lmy.columns[[0]],axis=1)
    lmy.columns=range(0,len(lmy.columns))
    return(lmy.lookup(range(len(lmy.index)),min_ids.values)).mean()

print("Worst contextual performance   %s or %0.3f%% of FCFS" % (y.max(axis=1).mean(),100*(y.max(axis=1).mean()-y.ix[:,0].mean())/y.ix[:,0].mean()))
print("Worst fixed performance        %s or %0.3f%% of FCFS" % (y.mean().max(),100*(y.mean().max()-y.ix[:,0].mean())/y.ix[:,0].mean()))
print("Best fixed performance         %s or %0.3f%% of FCFS" % (y.mean().min(),100*(y.mean().min()-y.ix[:,0].mean())/y.ix[:,0].mean()))
print("Learned performance rf         %s or %0.3f%% of FCFS" % (custom_loss(y,yp),100*(custom_loss(y,yp)-y.ix[:,0].mean())/y.ix[:,0].mean()))
print("Best contextual performance    %s or %0.3f%% of FCFS" % (y.min(axis=1).mean(),100*(y.min(axis=1).mean()-y.ix[:,0].mean())/y.ix[:,0].mean()))
