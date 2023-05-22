#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  9 16:04:09 2022

@author: likelymax
"""

from IPython.display import Image
import sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob, os
import joblib
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
from sklearn.model_selection import StratifiedKFold
import xgboost as xgb
from scipy import ndimage, misc
from obspy import read
from sklearn.datasets import make_classification
import json

#%% read training data

path = '/Users/likelymax/Dropbox/new_project/ML/RF_moho/receiver_functions/'
files = glob.glob(path+"*.SAC")
numFile = len(files)
X = np.zeros((numFile, 311))
y1 = np.zeros(numFile) #mhdp
y2 = np.zeros(numFile) #lcvp
y3 = np.zeros(numFile) #umvp
y4 = np.zeros(numFile) #lcvs
y5 = np.zeros(numFile) #umvs
name = []

for i, filename in enumerate(files):
    print(i)
    data = np.loadtxt(filename)
    tname = filename.split("/")
    sp_name = filename.split("_")
    mhdp = float(sp_name[-6])
    lcvp = float(sp_name[-5])
    umvp = float(sp_name[-4])
    lcvs = float(sp_name[-3])
    umvs = float(sp_name[-2])
    result = ndimage.median_filter(data[:,1], size=10)
    X[i, :] = result
    name.append(tname[-1])
    y1[i] = mhdp
    y2[i] = lcvp
    y3[i] = umvp
    y4[i] = lcvs
    y5[i] = umvs
    
indices = np.argsort(y1)
X = X[indices, :]
y1 = y1[indices]
y2 = y2[indices]
y3 = y3[indices]
y4 = y4[indices]
y5 = y5[indices]

#%% xgboost training


inv = 0.8
max_sam = int(len(y1) * inv)
print("max samples for every 100 tree: %.3f" % (max_sam))
minsplit = 3
maxdpth = 18
est = 11
ranstate = 1
np.random.shuffle(indices)
train_index = 0
test_index = 0

for i in range(1):
    MyXGB = xgb.XGBRegressor(booster = 'gbtree', tree_method = 'exact', n_estimators = est, max_depth = maxdpth, random_state = 0, eta = 0.3, eval_metric = mean_absolute_error)
    XGBMSEList = []
    XGBPercentLossList = []
    tr1 = inv
    tr2 = inv + inv/5
    
    indices = np.arange(0, len(X))
    np.random.default_rng(i)
    np.random.shuffle(indices)
    
    train_index = indices[int(len(indices)*(tr1 - inv)) :int(len(indices)*tr1)]
    test_index = indices[int(len(indices)*tr1):int(len(indices)*tr2)]
    
    # moho depth
    
    X_train, y_train = X[train_index, :], y1[train_index]
    X_test,  y_test  = X[test_index,  :], y1[test_index]

    MyXGB.fit(X_train, y_train, eval_set=[(X_train, y_train)])
    
    # test on the same testing set
    XGBEst     = MyXGB.predict(X_test)
    
    # calculate the accuracy of two models

    XGBMSE = mean_squared_error(XGBEst, y_test)
    XGBPercentLoss = mean_absolute_error(XGBEst, y_test)
    XGBMSEList.append(XGBMSE)
    XGBPercentLossList.append(XGBPercentLoss)
        
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, XGBMSE, XGBPercentLoss))
    
    # save the model 
    filename = 'XGB_' + str(i) + '_mhdp.sav'
    joblib.dump(MyXGB, filename)
    
    # lower crustal vp velocity
    
    X_train, y_train = X[train_index, :], y2[train_index]
    X_test,  y_test  = X[test_index,  :], y2[test_index]
    
    # train on the same training set
    MyXGB.fit(X_train, y_train, eval_set=[(X_train, y_train)])
    
    # test on the same testing set
    XGBEst = MyXGB.predict(X_test)
    
    # calculate the accuracy of two models
    XGBMSE = mean_squared_error(XGBEst, y_test)
    XGBPercentLoss = mean_absolute_error(XGBEst, y_test)
    
    XGBMSEList.append(XGBMSE)
    XGBPercentLossList.append(XGBPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, XGBMSE, XGBPercentLoss))
    
    # save the model 
    filename = 'XGB_' + str(i) + '_lcvp.sav'
    
    joblib.dump(MyXGB, filename)
    
    # upper mantle vp velocity
    
    X_train, y_train = X[train_index, :], y3[train_index]
    X_test,  y_test  = X[test_index,  :], y3[test_index]
    
    # train on the same training set
    MyXGB.fit(X_train, y_train, eval_set=[(X_train, y_train)])
    
    # test on the same testing set
    XGBEst = MyXGB.predict(X_test)
    
    # calculate the accuracy of two models
    XGBMSE = mean_squared_error(XGBEst, y_test)
    XGBPercentLoss = mean_absolute_error(XGBEst, y_test)
    
    XGBMSEList.append(XGBMSE)
    XGBPercentLossList.append(XGBPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, XGBMSE, XGBPercentLoss))
    
    # save the model 
    filename = 'XGB_' + str(i) + '_lcvs.sav'
    
    joblib.dump(MyXGB, filename)
    
    # lower crustal vs velocity
    
    X_train, y_train = X[train_index, :], y4[train_index]
    X_test,  y_test  = X[test_index,  :], y4[test_index]
    
    # train on the same training set
    MyXGB.fit(X_train, y_train, eval_set=[(X_train, y_train)])
    
    # test on the same testing set
    XGBEst     = MyXGB.predict(X_test)
    
    # calculate the accuracy of two models
    XGBMSE = mean_squared_error(XGBEst, y_test)
    XGBPercentLoss = mean_absolute_error(XGBEst, y_test)
    
    XGBMSEList.append(XGBMSE)
    XGBPercentLossList.append(XGBPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, XGBMSE, XGBPercentLoss))
    
    # save the model 
    filename = 'XGB_' + str(i) + '_lcvs.sav'
    
    joblib.dump(MyXGB, filename)
    
    # uppermantle p velocity
    
    X_train, y_train = X[train_index, :], y5[train_index]
    X_test,  y_test  = X[test_index,  :], y5[test_index]
    
    # train on the same training set
    MyXGB.fit(X_train, y_train, eval_set=[(X_train, y_train)])
    
    # test on the same testing set
    XGBEst = MyXGB.predict(X_test)
    
    # calculate the accuracy of two models
    XGBMSE = mean_squared_error(XGBEst, y_test)
    XGBPercentLoss = mean_absolute_error(XGBEst, y_test)
    
    XGBMSEList.append(XGBMSE)
    XGBPercentLossList.append(XGBPercentLoss)
    
    print("Round %d, ForestMSE:%.3f, ForestPercentLoss:%.3f" % (i, XGBMSE, XGBPercentLoss))
    
    # save the model 
    filename = 'XGB_' + str(i) + '_umvs.sav'
    
    joblib.dump(MyXGB, filename)


