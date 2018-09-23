#!/usr/bin/env python
# encoding: utf-8

'''
    mlc

Usage:
    mlc.py <perf_file> <feature_file> <split> <model_out>

Options:
    -o <option>    some option
    -h --help      show this help message and exit.
'''
from docopt import docopt
#retrieving arguments
args = docopt(__doc__, version='1.0.0rc2')

import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from sklearn.metrics import make_scorer
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV

print("Importing Data.")
X = pd.read_csv(args["<feature_file>"],sep=",")
y = pd.read_csv(args["<perf_file>"],sep=",")
y_raw = y.copy()
# sk.preprocessing.normalize(X, norm='l2', axis=0, copy=False, return_norm=False)
# sk.preprocessing.normalize(y, norm='l2', axis=1, copy=False, return_norm=False)
y=y.apply(lambda x: x-x.mean() , axis=1)
X_train, X_test, y_train, y_test, y_train_raw, y_test_raw = train_test_split(X, y, y_raw,
                                                                             train_size=int(args["<split>"]),
                                                                             random_state=4)

print("Data Ready.")

print("***************Multi-output regression RF approach.*****************")
def custom_loss(ground_truth, predictions):
    my=ground_truth
    min_ids=pd.DataFrame(predictions).idxmin(axis=1)
    lmy=my.reset_index()
    lmy.columns=range(0,len(lmy.columns))
    lmy=lmy.drop(lmy.columns[[0]],axis=1)
    lmy.columns=range(0,len(lmy.columns))
    return(lmy.lookup(range(len(lmy.index)),min_ids.values)).mean()


loss=make_scorer(custom_loss, greater_is_better=False)
hyper_params={
    'max_depth':[5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,40,80,160,200,400],
    'random_state':[6],
    'criterion':["mse"]
}
rf = RandomForestRegressor()

gsv=GridSearchCV(rf,hyper_params,scoring=loss)
gsv.fit(X_train, y_train)

def summary(mx,my):
  my_scaled = - my.sub(my.ix[:,0],axis=0).div(my.ix[:,0] + 1, axis=0) 
  def get_perfs_predictor(predictor,myp):
    min_ids=pd.DataFrame(predictor.predict(mx)).idxmin(axis=1)
    lmy=myp.reset_index()
    lmy.columns=range(0,len(lmy.columns))
    lmy=lmy.drop(lmy.columns[[0]],axis=1)
    lmy.columns=range(0,len(lmy.columns))
    return(lmy.lookup(range(len(lmy.index)),min_ids.values))
  # def print_perf(string,pf):
      # my_scaled = - my.sub(my[0],axis=0).div(my[0] + 1, axis=0) 
      # print(s+" %s or %s of FCFS" %(pf()))
  print("Worst contextual performance   %s or %0.3f%% of FCFS" % (my.max(axis=1).mean(),100*(my.max(axis=1).mean()-my.ix[:,0].mean())/my.ix[:,0].mean()))
  print("Worst fixed performance        %s or %0.3f%% of FCFS" % (my.mean().max(),100*(my.mean().max()-my.ix[:,0].mean())/my.ix[:,0].mean()))
  print("Best fixed performance         %s or %0.3f%% of FCFS" % (my.mean().min(),100*(my.mean().min()-my.ix[:,0].mean())/my.ix[:,0].mean()))
  print("Learned performance rf         %s or %0.3f%% of FCFS" % ((get_perfs_predictor(gsv,my).mean()),100*((get_perfs_predictor(gsv,my).mean())-my.ix[:,0].mean())/my.ix[:,0].mean()))
  print("Best contextual performance    %s or %0.3f%% of FCFS" % (my.min(axis=1).mean(),100*(my.min(axis=1).mean()-my.ix[:,0].mean())/my.ix[:,0].mean()))

print("TRAINING performance:")
summary(X_train,y_train_raw)
print("TESTING performance:")
summary(X_test,y_test_raw)
print("feature importances:")
print(gsv.best_estimator_.feature_importances_)

from sklearn.externals import joblib
gsvf=GridSearchCV(rf,hyper_params,scoring=loss)
gsvf.fit(X, y)
joblib.dump(gsvf.best_estimator_, args["<model_out>"]) 

# print("********************** SVM approach.*****************")

# def custom_loss_function_SVM(ground_truth, predictions):
    # def extract_value(y_partial,y_complete):
        # temp=[]
        # for a in y_partial:
            # temp.append(y_complete.loc[y_partial.index[i]][a])
        # return np.array(temp)
    # # y_train= pd.read_csv("y_train.csv",sep=",")
    # t1=extract_value(ground_truth,y_train)
    # t2=extract_value(predictions,y_train)
    # return (t2-t1).mean()

# y_min=y_train.idxmin(axis=1)
# loss_svc=make_scorer(custom_loss_function_SVM, greater_is_better=False)
# hyper_params={
    # 'penalty':["l2","l1"],
# #    'loss':["squared_hinge"],
    # 'tol':[1e-5,1e-3,1e-7]
# }
# svc=LinearSVC(dual=False)
# gsv=GridSearchCV(svc,hyper_params)
# gsv.fit(X_train,y_train.idxmin(axis=1))
# print("best parms:",gsv.best_params_)
# print("best score:",gsv.best_score_)
# print(gsv.grid_scores_)
