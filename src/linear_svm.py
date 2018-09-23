import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
import pandas as pd
from sklearn.metrics import make_scorer
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV


def costum_looss_function_SVM(ground_truth, predictions):

    def extract_value(y_partial,y_complete):
        temp=[]
        print("aaaaa")
        for a in y_partial:
            #print(y_complete.loc[y_partial.index[i]][a])
            temp.append(y_complete.loc[y_partial.index[i]][a])
        return np.array(temp)


    y_train= pd.read_csv("y_train.csv",sep=",")
    t1=extract_value(ground_truth,y_train)
    t2=extract_value(predictions,y_train)

    return (t2-t1).mean()


Xy= pd.read_csv("large.ssv",sep=" ")
X = Xy.ix[:,10:len(Xy.columns)-8]
y = Xy.ix[:,0:9]

Xy= pd.read_csv("large.ssv",sep=" ")
y=y.apply(lambda x: x , axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=10000,random_state=4)
y_test.to_csv("y_test.csv")
y_train.to_csv("y_train.csv")



y_min=y_train.idxmin(axis=1)
loss_svc=make_scorer(costum_looss_function_SVM, greater_is_better=False)

hyper_params={
    'penalty':["l2","l1"],
#    'loss':["squared_hinge"],
    'tol':[1e-5,1e-3,1e-7]
}
svc=LinearSVC(dual=False)
gsv=GridSearchCV(svc,hyper_params)
gsv.fit(X_train,y_train.idxmin(axis=1))
print("best parms:",gsv.best_params_)
print("best score:",gsv.best_score_)
print(gsv.grid_scores_)
