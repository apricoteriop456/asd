# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:11:57 2019

@author: Administrator
"""
import pandas as pd
import numpy as np
from datetime import datetime
crime=pd.read_csv('https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/04_Apply/US_Crime_Rates/US_Crime_Rates_1960_2014.csv')
crime.head()
crime.shape
crime.Year=pd.to_datetime(crime.Year,format='%Y')
crime.Year.dtype
crime.set_index('Year',inplace=True)
crime.drop(columns=['Total'],inplace=True)
crime.info()
#每10年分组，并计算相关数据
crimes=crime.resample('10AS').sum()

#D表示天，Q表示季度，A表示年，T表示分钟，S表示秒，M表示月,可以对时间序列数据进行重采样，并进行相应计算
population=crime['Population'].resample('10AS').max()
crimes['Population']=population
crimes
crimes.idxmax(0)#返回每一列最大值对应的INDEX，也就是找各种犯罪率最高值对应的年份为最危险的10年
