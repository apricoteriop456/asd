# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:34:27 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
euro12=pd.read_csv(r'C:\Users\Administrator\Desktop\pandas_exercises-master\02_Filtering_&_Sorting\Euro12\Euro_2012_stats_TEAM.csv')
euro12.columns
euro12.Goals
euro12.Team.value_counts().count()
len(euro12.columns)
discipline=euro12[['Team','Yellow Cards','Red Cards']]
discipline.sort_values(by=['Red Cards','Yellow Cards'],ascending=False)
discipline['Yellow Cards'].mean()
euro12.info()
euro12[euro12.Goals>6]
euro12[euro12.Team.str[0:1]=='G']
#euro12[euro12.Team.str.startswith('G')]
euro12.iloc[:,0:7]
euro12.iloc[:,:-3]
f=euro12[(euro12.Team=='England') | (euro12.Team=='Italy') | (euro12.Team=='Russia')]
f.loc[:,['Team','Shooting Accuracy']]
euro12.loc[euro12.Team.isin(['England', 'Italy', 'Russia']), ['Team','Shooting Accuracy']]
