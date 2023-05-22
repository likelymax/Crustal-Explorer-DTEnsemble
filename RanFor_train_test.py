#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 09:03:45 2021

@author: likelymax
"""

from IPython.display import Image
import sklearn
import pandas as pd
import numpy as np
import glob, os
import joblib
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

#%% path and files of the input training data (SynRFs)
path = '/Volumes/Yitan-4Tb/ML/RF_moho/new_try_synthetics/synthetic_based_on_ccp_randomforest/varies_lower_crust_p/flat/RF_qualified_ratio_0.15'
files = glob.glob(path+"*_xy")
numFile = len(files)
X = np.zeros((numFile, 500))
y = np.zeros(numFile)
  
#%% read the files
for i, filename in enumerate(files):
    data = np.loadtxt(filename)
    sp_name = filename.split("_")
    mhdp = float(sp_name[-2]) #% I put the labeled moho depth in the name of the corresponding SynRFs
    result = ndimage.median_filter(data[:,1], size=10)
    X[i, :] = result
    y[i] = mhdp
    
#%% sort the indices
indices = np.argsort(y)
X = X[indices, :]
y = y[indices]

#%% RanFor algorithm training processes

max_sam = int(len(y) * 0.8)
print("max samples for every 100 tree: %.3f" % (max_sam))

MyRandomForest = RandomForestRegressor(random_state  = 0, max_samples = max_sam, oob_score = 'True', n_estimators = 71, max_features = 'log2', min_samples_split = 4)
ForestMSEList = []
ForestPercentLossList = []


for i in range(10):
    indices = np.arange(0, len(X))
    np.random.shuffle(indices)
    train_index = indices[:int(len(indices)*0.8)]
    test_index = indices[int(len(indices)*0.8):]
    
    X_train, y_train = X[train_index, :], y[train_index]
    X_test,  y_test  = X[test_index,  :], y[test_index]
    
    # train on the same training set
    MyRandomForest.fit(X_train, y_train)
    
    # test on the same testing set
    ForestEst     = MyRandomForest.predict(X_test)
    
    # calculate the accuracy of two models
    ForestMSE = mean_squared_error(ForestEst, y_test)
    ForestPercentLoss = mean_absolute_error(ForestEst, y_test)
    
    ForestMSEList.append(ForestMSE)
    ForestPercentLossList.append(ForestPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, ForestMSE, ForestPercentLoss))
    
    # save the model 
    filename = 'random_forest_' + str(i) + '.sav'
    
    joblib.dump(MyRandomForest, filename)
      
#%% offset data test

path = '/Users/likelymax/Dropbox/new_project/ML/RF_moho/Synthetics/offset/xyfiles_15km_60km/'
files = glob.glob(path+"*_xy")
numFile = len(files)
xoffset = np.zeros((numFile, 500))
yoffset = np.zeros(numFile)
stlo = np.zeros(numFile)
stla = np.zeros(numFile)
      
#%% read data

for i, filename in enumerate(files):
    print(filename)
    data = np.loadtxt(filename)
    sp_name = filename.split("_")

    mhdp = float(sp_name[-2])
    lat = float(sp_name[-4])
    lon = float(sp_name[-6])
    print(mhdp)
    xoffset[i, :] = data[:, 1]
    yoffset[i] = mhdp
    stlo[i] = lon
    stla[i] = lat
    
#%% offset test

offsetMSEList = []
offsetPercentLossList = []
path='/Users/likelymax/Dropbox/new_project/ML/RF_moho/Synthetics/ForestEst/larger_p_model/'

for i in range(8):
    
    # test on the same testing set
    MyRandomForest = joblib.load(path + 'random_forest_' + str(i) + '.sav')
    offsetEst     = MyRandomForest.predict(xoffset)
    with open("est_result.txt", "a") as file:
        for i in range(len(yoffset)):
            temp = np.round(np.array([stlo[i], stla[i], offsetEst[i]]), decimals = 3)
            temp = " ".join(list(map(lambda x : str(x), temp)))
            file.write(temp + "\n")
    
    # calculate the accuracy of two models
    offsetMSE = mean_squared_error(offsetEst, yoffset)
    offsetPercentLoss = mean_absolute_error(offsetEst, yoffset)
    
    offsetMSEList.append(offsetMSE)
    offsetPercentLossList.append(offsetPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, offsetMSE, offsetPercentLoss))

