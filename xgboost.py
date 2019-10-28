#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 17:35:38 2019

@author: apple
"""
import pandas as pd
creditcard=pd.read_csv(r'/Users/apple/Downloads/creditcard.csv')
counts=creditcard.Class.value_counts()
from imblearn.over_sampling import SMOTE
creditcard.drop(['Time'],axis=1)
#conda install imblearn
import sys
print(sys.path)
import os
os.getcwd()
