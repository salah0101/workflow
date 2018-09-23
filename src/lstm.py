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
from sklearn import decomposition
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import random

print("Importing Data.")
file = "o/zymakefile_online_classify/o.KTH-SP2.table.prf"
Y = pd.read_csv(file, sep=',',header=None)
file = "o/zymakefile_online_classify/o.KTH-SP2.table.features"
X = pd.read_csv(file, sep=',',header=None)
X = X.drop(X.columns[[17]], axis=1)
y_raw = Y.copy()
Y=Y.apply(lambda x: x-x.mean() , axis=1) 
print("Data Ready.")

N = len(Y.ix[:,0])
step = 1
P = len(Y.ix[0,:])
Response = np.asarray(Y.ix[step:,:])

#Transformation of X
X_new = []
for i in range(step,N):
    newline = []
    for j in range(step+1):
        newline += list(X.ix[(j+i-step),:])
    X_new.append(newline)
X_new = pd.DataFrame(X_new)

#scale = StandardScaler(with_mean=0, with_std=1)
scale = MinMaxScaler(feature_range=(-1, 1))
scale.fit(X_new)
X_new =  scale.transform(X_new)
x_new = np.asarray(X_new)
#scaler.inverse_transform(X_new)

def fit_lstm(x, y, batch_size, nb_epoch, neurons):
    x = x.reshape(x.shape[0], 1, x.shape[1])
    p = len(y[0,:])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, x.shape[1], x.shape[2]), stateful=True))
    model.add(Dense(p))
    model.compile(loss='mean_absolute_error', optimizer='adam')
    for i in range(nb_epoch):
        model.fit(x, y, nb_epoch=1, batch_size=batch_size, verbose=0, shuffle=False)#epochs
        model.reset_states()
    return model


lstm_model = fit_lstm(x_new, Response, 1, 3000, 4)

preval=lstm_model.predict(x_new.reshape(x_new.shape[0], 1, x_new.shape[1]), batch_size=1)
i = np.arange(preval.shape[0])
j = pd.DataFrame(preval).idxmin(axis=1)
j = np.asarray(j)
y = np.asarray(y_raw)
Predicted = y[i,j]
m=min(y.sum(0))
BestFixed = y[:,random.choice([i for i in range(len(y[0,:])) if sum(y[:,i]) == m])]
BestContexual = y_raw.apply(min,axis=1)
BestContexual=BestContexual[1:,]
BestFixed=BestFixed[1:,]
print(sum(BestFixed),sum(Predicted), sum(BestContexual))

