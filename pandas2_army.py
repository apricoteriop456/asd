# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:45:05 2019

@author: Administrator
"""

import pandas as pd
raw_data={'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
            'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'],
            'deaths': [523, 52, 25, 616, 43, 234, 523, 62, 62, 73, 37, 35],
            'battles': [5, 42, 2, 2, 4, 7, 8, 3, 4, 7, 8, 9],
            'size': [1045, 957, 1099, 1400, 1592, 1006, 987, 849, 973, 1005, 1099, 1523],
            'veterans': [1, 5, 62, 26, 73, 37, 949, 48, 48, 435, 63, 345],
            'readiness': [1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 2, 3],
            'armored': [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            'deserters': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
            'origin': ['Arizona', 'California', 'Texas', 'Florida', 'Maine', 'Iowa', 'Alaska', 'Washington', 'Oregon', 'Wyoming', 'Louisana', 'Georgia']}
army=pd.DataFrame(raw_data)
army.info()
army.set_index('origin',inplace=True)#Set the 'origin' colum as the index of the dataframe
army.veterans
army.loc[:,['veterans','deaths']]
army[['veterans','deaths']]
army.loc[army.index.isin(['Maine','Alaska']),[ 'deaths', 'size', 'deserters']]
army.loc[["Maine", "Alaska"], ["deaths", "size", "deserters"]]
army.iloc[2:7,2:6]
army.iloc[4:,:]
army.iloc[:4,:]
army.iloc[:,2:7]
army[army.deaths>50]
army[army.regiment!='Dragoons']
army.loc[["Texas", "Arizona"],:]
army.ix[['Arizona'],2]
army.ix[2,['deaths']]
