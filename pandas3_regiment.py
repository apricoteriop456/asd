# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:24:46 2019

@author: Administrator
"""

import pandas as pd
raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'], 
        'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'], 
        'name': ['Miller', 'Jacobson', 'Ali', 'Milner', 'Cooze', 'Jacon', 'Ryaner', 'Sone', 'Sloan', 'Piger', 'Riani', 'Ali'], 
        'preTestScore': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],regiment=pd.DataFrame(raw_data)
regiment.columns
regiment[regiment.regiment=='Nighthawks',preTestScore].mean()
regiment.loc[regiment.regiment=='Nighthawks',preTestScore].mean()
regiment.loc[regiment.regiment=='Nighthawks',regiment.preTestScore].mean()
regiment.loc[regiment.regiment=='Nighthawks',regiment.preTestScore]
regiment.regiment=='Nighthawks'
regiment.loc[regiment.regiment=='Nighthawks','regiment.preTestScore'].mean()
regiment.loc[regiment.regiment=='Nighthawks',['regiment.preTestScore']].mean()
regiment.loc[regiment.regiment=='Nighthawks',['preTestScore']].mean()
regiment.loc[regiment.regiment=='Nighthawks',['preTestScore']]
regiment.loc[regiment.regiment=='Nighthawks','preTestScore'].mean()
regiment.company.describe()
regiment.grouped('company').describe()
regiment.groupby('company').describe()
regiment.groupby('company')['preTestScore'].mean()
regiment.groupby(['regiment','company'])['preTestScore'].mean()
regiment.groupby(['regiment','company'])['preTestScore'].mean().index
regiment.groupby(['regiment', 'company']).preTestScore.mean().unstack()
regiment.groupby(['regiment', 'company']).mean()
regiment.groupby(['regiment', 'company']).value_counts()
regiment.groupby(['regiment', 'company']).nunique()
regiment.groupby(['regiment', 'company']).size()
regiment.mean()
regiment.mean
regiment
for group,name in regiment.groupby('regiment'):
    print(name)
    print(group)
