import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from sklearn.model_selection import GridSearchCV

def summary(mx,my):
      def get_perfs_predictor(predictor):
        min_ids=pd.DataFrame(predictor.predict(mx)).idxmin(axis=1)
        lmy=my.reset_index()
        lmy.columns=range(0,len(lmy.columns))
        lmy=lmy.drop(lmy.columns[[0]],axis=1)
        lmy.columns=range(0,len(lmy.columns))
        return(lmy.lookup(range(len(lmy.index)),min_ids.values))


      print("Worst contextual performance           %s" %my.max(axis=1).mean())
      print("Worst fixed performance                %s" %my.mean().max())
      print("Best fixed performance                 %s" %my.mean().min())
      print("Learned performance for random forest  %s" %(get_perfs_predictor(regr_rf).mean()))
      # print("Learned performance for multirf        %s" %(get_perfs_predictor(regr_multirf).mean()))
      print("Best contextual performance            %s" %my.min(axis=1).mean())


Xy= pd.read_csv("large.ssv",sep=" ")

X = Xy.ix[:,10:len(Xy.columns)-8]
y = Xy.ix[:,0:9]
y=y.apply(lambda x: x , axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=10000,random_state=4)


loss=make_scorer(costum_loss_function_RF, greater_is_better=False)
hyper_params={
    'max_depth':[10,20,30,40,50,60,70,80,90,100],
    'random_state':[1,2,3,4,5,6,7,8,9,10],
    'criterion':["mse"]
}
rf = RandomForestRegressor()
gsv=GridSearchCV(rf,hyper_params,scoring=loss)
gsv.fit(X_train,y_train)
