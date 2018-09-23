#!/usr/bin/env python3

from vowpalwabbit.pyvw import vw
from sklearn import datasets
import pandas as pd

def argmin(iterable):
  return min(enumerate(iterable), key=lambda x: x[1])[0]

step=2

Yin = pd.read_csv( "o/zymakefile_online_classify/o.SDSC-BLU.table.prf", sep=',', header = None)
Xin = pd.read_csv( "o/zymakefile_online_classify/o.SDSC-BLU.table.features", sep=',', header = None)

d = len(Yin.columns) #policies
n = len(Xin.columns) #features
m = len(Xin)         #instances ('examples')
assert(m == len(Yin))

print("There are %d features, d %d policies and the sample size is %d." %(n,d,m))


# making formula wrapper for vw
def tovwstr_x(pos,name,X): # pos - position
  return(' '.join( ["x_"+str(name)+"_"+str(feature_id)+":"+str(X.ix[pos,feature_id]) for feature_id in range(n)]))

def tovwstr_y(pos,name,Y): # pos - position
  return(' '.join( ["y_"+str(name)+"_"+str(policy_id)+":"+str(Y.ix[pos,policy_id]) for policy_id in range(d)]))


def output (performances, number_of_policies):
  print("Fixed costs:")
  print(performances[0:number_of_policies])
  print("Regression Losses:")
  print(performances[number_of_policies:(2*number_of_policies)])
  print("Worst contextual cost:")
  print(performances[2*number_of_policies])
  print("Worst fixed cost:")
  print(performances[2*number_of_policies+1])
  print("Best fixed cost:")
  print(performances[2*number_of_policies+2])
  print("Learned strategy ('argmin(yhat)') costs:")
  print(performances[2*number_of_policies+3])
  print("Best contextual cost:")
  print(performances[2*number_of_policies+4])


def our_learning(X, Y, train_perf = False, is_l2 = False, coef_regular = 1000):
	
  #d = len(Y.columns) #policies
  #n = len(X.columns) #features
  m = len(X)
  print("Initializing the %d models." %d)
  if (is_l2):
    models = [vw(l2=coef_regular) for i in range(d)]
  else:
    models = [vw(l1=coef_regular) for i in range(d)]
	
  iterative_l2_regression_performance = [0]*d
  iterative_cum_wait_learning = 0
  iterative_cum_wait_fixed = [0]*d
  iterative_cum_wait_best_ctx = 0
  iterative_cum_wait_worst_ctx = 0

  for i in range(step,m):


    vwstrings = [tovwstr_x(pos=(i-i_i),name=i_i,X=X) for i_i in range(step)] + [tovwstr_y(pos=(i-1-i_i),name=i_i,Y=Y) for i_i in range(step-1)]
    x_vw = ' '.join(vwstrings)

    # x_vw = ' '.join([tovwstr_x(i,name=1)])

    #vwstrings_2 = [tovwstr_x(i-i_i-1,name=i_i) for i_i in range(step)] + [tovwstr_y(i-1-i_i,name=i_i) for i_i in range(step-1)]
    # x_vw = ' '.join(vwstrings_2)

    # for separated regression
    for j in range(d): 
      ec_vw = str(Y.ix[i,j])+' |n ' + x_vw
      models[j].learn(ec_vw)

    #actual cost:
    yhat=[models[j].predict('|n '+x_vw) for j in range(d)]
    # print("Predicted Targets: "+str(["%0.3f" %v for v in yhat]))
    # print("Real Targets:      "+str(["%0.3f" %(Y.ix[i,j]) for j in range(d)]))
    iterative_cum_wait_learning += Y.ix[i,argmin(yhat)]

    #regression losses:
    iterative_l2_regression_performance = [ iterative_l2_regression_performance[j] + (yhat[j]-Y.ix[i,j])**2 for j in range(d)]

    #fixed choice costs:
    iterative_cum_wait_fixed = [iterative_cum_wait_fixed[j]+Y.ix[i,j] for j in range(d)]
	  
    #best contexual:
    iterative_cum_wait_best_ctx += min(Y.ix[i,:])
	  
    #worst contexual:
    iterative_cum_wait_worst_ctx += max(Y.ix[i,:])

    m_d = m-step

    #for model in models:
      #model.finish()
        
    if (train_perf):
      output([e/m_d for e in iterative_cum_wait_fixed]+ [e/m_d for e in iterative_l2_regression_performance] + [iterative_cum_wait_worst_ctx/m_d] + [max([e/m_d for e in    iterative_cum_wait_fixed])] + [min([e/m_d for e in iterative_cum_wait_fixed])] + [iterative_cum_wait_learning/m_d] + [iterative_cum_wait_best_ctx/m_d],d)
    return models



def cross_validated_results(X, Y): #10-fold
	
  #number of rows in each chunk
  part_size = len(X)/10

  #Splitting to chunks	
  Xparts = [X.ix[(part_size*i):(part_size*(i+1)-1),:] for i in range(10) ]
  Yparts = [Y.ix[(part_size*i):(part_size*(i+1)-1),:] for i in range(10) ]
	
  fixed_costs  = [0]*d
  l2_regression_performance = [0]*d
  wait_learning = 0
  wait_best_ctx = 0
  wait_worst_ctx = 0
  best_fixed = 0
  worst_fixed = 0

  for k in range(10):
		
    trainX = pd.concat([x for j,x in enumerate(Xparts) if j!=k])
    testX = Xparts[k]
    trainY = pd.concat([x for j,x in enumerate(Yparts) if j!=k])
    testY = Yparts[k]
    trainX = trainX.reset_index(drop=True)
    testX = testX.reset_index(drop=True)
    trainY = trainY.reset_index(drop=True)
    testY = testY.reset_index(drop=True)
		
    iterative_cum_wait_fixed = [0]*d
    models = our_learning(trainX, trainY)
    for i in range(step,len(testX)):		
						
      vwstrings = [tovwstr_x(pos=(i-i_i), name=i_i, X=testX) for i_i in range(step)] + [tovwstr_y(pos=(i-1-i_i), name=i_i, Y=testY) for i_i in range(step-1)]
      x_vw = ' '.join(vwstrings)			

      #actual cost:
      yhat=[models[j].predict('|n '+x_vw) for j in range(d)]
      wait_learning += testY.ix[i,argmin(yhat)]

      #regression losses:
      l2_regression_performance = [ l2_regression_performance[j] + (yhat[j]-testY.ix[i,j])**2 for j in range(d)]

      #fixed choice costs:
      iterative_cum_wait_fixed = [iterative_cum_wait_fixed[j]+testY.ix[i,j] for j in range(d)]

      #best contexual:
      wait_best_ctx += min(testY.ix[i,:])

      #worst contexual:
      wait_worst_ctx += max(testY.ix[i,:])
    #end loop for i
		
    #fixed costs:
    fixed_costs = [fixed_costs[j] + iterative_cum_wait_fixed[j] for j in range(d)]
 
    #best fixed:
    best_fixed += min(iterative_cum_wait_fixed)

    #worst fixed:
    worst_fixed += max(iterative_cum_wait_fixed)
	
  #end of loop for k-folds
  wait_learning /= (10*(part_size-step))
  fixed_costs = [ fixed_costs[j]/(10*(part_size-step)) for j in range(d)]
  l2_regression_performance = [ l2_regression_performance[j]/(10*(part_size-step)) for j in range(d)]
  wait_best_ctx /= (10*(part_size-step))
  wait_worst_ctx /= (10*(part_size-step))
  best_fixed /= (10*(part_size-step))
  worst_fixed /= (10*(part_size-step))
  return fixed_costs + l2_regression_performance + [wait_worst_ctx] + [worst_fixed] + [best_fixed] + [wait_learning] + [wait_best_ctx]
#end of function cross_validated_results

cv = cross_validated_results(Xin, Yin)
output(cv,d)
		
