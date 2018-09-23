#!/usr/bin/env python
# encoding: utf-8

'''
    online

Usage:
    online.py <perf_file> <feature_file> <step> <predicted_values>

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
from joblib import Parallel, delayed
from sklearn.model_selection import GridSearchCV
from sklearn import decomposition
from sklearn.tree import DecisionTreeRegressor
import random


print("Importing Data.")
X = pd.read_csv(args["<feature_file>"],sep=",",header=None)
Y = pd.read_csv(args["<perf_file>"],sep=",",header=None)
#file = "o/zymakefile_online_classify/o.KTH-SP2.table.prf"
#Y = pd.read_csv(file, sep=',',header=None)
#file = "o/zymakefile_online_classify/o.KTH-SP2.table.features"
#X = pd.read_csv(file, sep=',',header=None)

X = X.drop(X.columns[[17]], axis=1)

y_raw = Y.copy()


# shifting of values
Y=Y.apply(lambda x: x-x.mean() , axis=1) #lambda - one-line function 
#!!!!!!!!!!: in python axis = 0 is for columns, axis = 1 is for rows

print("Data Ready.")



print("Preparation Started")
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
    'max_depth':[5,6,7,8,9,10],
    'random_state':[0,6,10],
    'criterion':["mae"]
    #',warm_start':[True]
    #,'max_features':["sqrt"]
}
rf = DecisionTreeRegressor() #RandomForestRegressor()

print("Preparation Finished")





#gsv=GridSearchCV(rf,hyper_params,scoring=loss)
#gsv.fit(X, Y)
#Yp=gsv.best_estimator_.predict(X)

#i = np.arange(Yp.shape[0])
#j = pd.DataFrame(Yp).idxmin(axis=1)
#j = np.asarray(j)
y = np.asarray(y_raw)
#Predicted = y[i,j]

m=min(y.sum(0))
BestFixed = y[:,random.choice([i for i in range(len(y[0,:])) if sum(y[:,i]) == m])]
BestContexual = y_raw.apply(min,axis=1)
#print(sum(BestFixed),sum(Predicted), sum(BestContexual))





PredictedValues = []
N = len(Y.ix[:,0])
step = int(args["<step>"])


#Transformation of X
X_new = []
for i in range(step,N):
    newline = []
    for j in range(step+1):
        newline += list(X.ix[(j+i-step),:])
    X_new.append(newline)
x_new = np.asarray(X_new)
X_new = pd.DataFrame(X_new)



#Transformation of Y
Y_new = []
for i in range(step,N):
    newline = []
    for j in range(step):
        newline += list(Y.ix[(j+i-step),:])
    Y_new.append(newline)
y_new = np.asarray(Y_new)
Y_new = pd.DataFrame(Y_new)




Train = pd.concat([X_new, Y_new], axis=1)
Response = Y.ix[step:,:]
Response = Response.reset_index(drop=True)


pca = decomposition.PCA(n_components=7)
pca.fit(Train)
Train = pd.DataFrame(pca.transform(Train))



#PredictedValues = pd.DataFrame(PredictedValues)

#PredictedValues.to_csv(args["<predicted_values>"],sep=',',index=False)


def train_model(train, response, t):
    CurrentTrain = train.ix[0:t,:]
    CurrentResponse = response.ix[0:t,:]
    #gsv=GridSearchCV(rf,hyper_params,scoring=loss)
    gsv = RandomForestRegressor(bootstrap=True, criterion='mae', max_depth=10,
           max_features='auto', max_leaf_nodes=None,
           min_impurity_split=1e-07, min_samples_leaf=1,
           min_samples_split=2, min_weight_fraction_leaf=0.0,
           n_estimators=10, n_jobs=-1, oob_score=False, random_state=0,
           verbose=0, warm_start=True)
    #gsv = DecisionTreeRegressor( criterion='mae', max_depth=10,
    #        max_features='auto', max_leaf_nodes=None,
    #        min_impurity_split=1e-07, min_samples_leaf=1,
    #        min_samples_split=2, min_weight_fraction_leaf=0.0,
    #        random_state=0)
    gsv.fit(CurrentTrain, CurrentResponse)
    print("going to execute", t)
    return gsv.predict(Train.ix[t+1,:].values.reshape(1, -1)).reshape(-1).tolist()
    #gsv.best_estimator_.
    
result = []
for t in range(2,len(Train)-1):
	result.append(train_model(Train, Response, t))
#result = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(2, (len(Train)-1) ) )

#result2 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(40, 80 ) )

#result3 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(80, 120 ) )

#result4 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(120, 160 ) )

#result5 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(160, 200 ) )

#result6 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(200, 240 ) )

#result7 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(240, 280 ) )

#result8 = Parallel(n_jobs=4)(delayed(train_model)(Train, Response, t) for t in range(280, (len(Train)-1) ) )

#result = result1 + result2 + result3 + result4 + result5 + result6 + result7 + result8
#PredictedValues = [] 
#for r in result:
#	r = r[1:(-1)]
#	a = list(map(int, list(r.split(', '))))
#	PredictedValues.append()

result = pd.DataFrame(result)

result.to_csv(args["<predicted_values>"],sep=',',index=False,header=False)


#ouf = open(args["<predicted_values>"], 'w')
#ouf.write(result)

