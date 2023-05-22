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

#%% input testing data

path = '/Users/likelymax/Dropbox/new_project/ML/RF_moho/test_data/'
files = glob.glob(path+"*_tmp")
numFile = len(files)
xslope = np.zeros((numFile, 311))
yslope = np.zeros(numFile)
stlo = np.zeros(numFile)
stla = np.zeros(numFile)
name = []

k = 0

tmppath = '/Users/likelymax/Dropbox/US/ML_operator/'


for filename in Lines:
    filename=filename.split("\n")[0]
    for i, F in enumerate(files):
        NF = F.split("/")[-1]
        if filename == NF:
            print(filename)
            data = np.loadtxt(F)
            sp_name = filename.split("_")
            mhdp = float(sp_name[-4])
            lat = float(sp_name[-6])
            lon = float(sp_name[-8])
            xslope[k, :] = data[:, 1]
            yslope[k] = mhdp
            stlo[k] = lon
            stla[k] = lat
            name.append(filename)
            k = k + 1
            
#%% ground truth

path = '/Users/likelymax/Dropbox/new_project/Whole_US/ML/reference_crustal_thickness/'

fi = 'average_new_moho_depth.dat'
f1 = open(path + fi, 'r')
Lines = f1.readlines()
ygt = [] # value

xgt = [] # lon
zgt = [] # lat
for line in Lines:
    tmp = line.split(" ")
    print(tmp)
    ygt.append(float(tmp[2]))
    xgt.append(float(tmp[0]))
    zgt.append(float(tmp[1]))

xgt = np.array(xgt)
ygt = np.array(ygt)
zgt = np.array(zgt)
xgt, ygt, zgt = xgt.flatten(), ygt.flatten(), zgt.flatten()

#%% crustal thickness estimation from XGBoost

#% the example is upper mantle vs

typef = 'umvs'
slopeMSEList = []
slopePercentLossList = []
mse = 0
loss = 0

op = '/Users/likelymax/Dropbox/new_project/ML/RF_moho/new_try_synthetics/xgboost/operators/'
path = '/Users/likelymax/Dropbox/new_project/ML/RF_moho/new_try_synthetics/xgboost/'

test = glob.glob(op+"XGB_real_rf_umvs.sav")

for k, filename in enumerate(test):
    tmp = filename.split("_")
    tmp2 = tmp[-1].split(".")
    etas = tmp[-2]
    
    typef = tmp2[0]
    MyXGB = joblib.load(filename)
    slopeEst     = MyXGB.predict(xslope)
    if typef == 'mhdp':
        with open(path + "est_result_XGB_" + typef + '_mhdp.dat', "a") as file:    
            tmpx = np.zeros(len(yslope))
            tmpy = np.zeros(len(yslope))
            j = 0
            for i in range(len(yslope)):
                X_test = xslope[i:i+1, :]
                sample_id = 0
                tmpx[j] = slopeEst[i]
                tmpy[j] = yslope[i]
                j = j + 1
                temp = np.round(np.array([stlo[i], stla[i], slopeEst[i]]), decimals = 5)
                temp = " ".join(list(map(lambda x : str(x), temp)))
                file.write(temp + "\n")                        
    else:
        with open(path + "est_result_XGB_" + typef + '_' + typef + '.dat', "a") as file:
            tmpx = np.zeros(len(yslope))
            tmpy = np.zeros(len(yslope))
            j = 0
            for i in range(len(yslope)):
                X_test = xslope[i:i+1, :]
                sample_id = 0
                slopeEst[i] = slopeEst[i]
                tmpx[j] = slopeEst[i]
                tmpy[j] = yslope[i]               
                temp = np.round(np.array([stlo[i], stla[i], slopeEst[i]]), decimals = 5)
                temp = " ".join(list(map(lambda x : str(x), temp)))
                file.write(temp + "\n")

    slopeMSE = mean_squared_error(tmpx, tmpy)
    slopePercentLoss = mean_absolute_error(tmpx, tmpy)
    
    slopeMSEList.append(slopeMSE)
    slopePercentLossList.append(slopePercentLoss)
    
    mse = mse + slopeMSE 
    loss = loss + slopePercentLoss
    
    #% transfer to probability
    
    binnum = 10
    
    dp_p = np.histogram(slopeEst, bins = binnum)
    prob_dpth = dp_p[0]/np.sum(dp_p[0])
    
    ave_p = np.histogram(ygt, bins = binnum)
    prob_ave = ave_p[0]/np.sum(ave_p[0])
    
    
    #% JSD calculation
    
    value = distance.jensenshannon(prob_dpth, prob_ave)
    print("JSD is %f" % (value))

    
