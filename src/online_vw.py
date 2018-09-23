#!/usr/bin/env python3

from vowpalwabbit.pyvw import vw
from sklearn import datasets
import pandas as pd

def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

step=1

Y = pd.read_csv( "o/zymakefile_online_classify/o.KTH-SP2.table.prf", sep=',', header=None)
X = pd.read_csv( "o/zymakefile_online_classify/o.KTH-SP2.table.features", sep=',', header=None)

d = len(Y.columns) #policies
n = len(X.columns) #features
m = len(X)         #instances ('examples')
assert(m == len(Y))

print("There are %d features, d %d policies and the sample size is %d." %(n,d,m))

print("Initializing the %d models." %d)
models_reg = [vw(l1=0.001) for i in range(d)]

iterative_l2_regression_performance = [0]*d
iterative_cum_wait_learning = 0
iterative_cum_wait_fixed = [0]*d
for i in range(10,m):

  # for simple online classification
  def tovwstr_x(i_i,name):
    return(' '.join( ["x_"+str(name)+"_"+str(feature_id)+":"+str(X.ix[i_i,feature_id]) for feature_id in range(n)]))

  def tovwstr_y(i_i,name):
    return(' '.join( ["y_"+str(name)+"_"+str(policy_id)+":"+str(Y.ix[i_i,policy_id]) for policy_id in range(d)]))

  vwstrings = [tovwstr_x(i-i_i,name=i_i) for i_i in range(step)] + [tovwstr_y(i-1-i_i,name=i_i) for i_i in range(step-1)]
  print(vwstrings)
  x_vw = ' '.join(vwstrings)

  print(x_vw)

  # for separated regression
  for j in range(d): 
    ec_vw = str(Y.ix[i,j])+' |n ' + x_vw
    models[j].learn(ec_vw)

  #actual cost:
  yhat=[models[j].predict('|n '+x_vw) for j in range(d)]
  print("Predicted Targets: "+str(["%0.3f" %v for v in yhat]))
  print("Real Targets:      "+str(["%0.3f" %(Y.ix[i,j]) for j in range(d)]))
  iterative_cum_wait_learning = iterative_cum_wait_learning + Y.ix[i,argmin(yhat)]

  #regression losses:
  iterative_l2_regression_performance = [ iterative_l2_regression_performance[j] + (yhat[j]-Y.ix[i,j])**2 for j in range(d)]

  #fixed choice costs:
  iterative_cum_wait_fixed = [iterative_cum_wait_fixed[j]+Y.ix[i,j] for j in range(d)]

for model in models:
  model.finish()
print("Fixed costs:")
print([e/m for e in iterative_cum_wait_fixed])
print("Regression Losses:")
print([e/m for e in iterative_l2_regression_performance])
print("Learned strategy ('argmin(yhat)') costs:")
print(iterative_cum_wait_learning/m)
print("Best fixed cost:")
print(min([e/m for e in iterative_cum_wait_fixed]))
