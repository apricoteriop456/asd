# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 16:11:29 2019

@author: Administrator
"""

import pandas as pd
drinks=pd.read_csv('https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv',sep=',')
drinks.info()
g=drinks.groupby(['continent'])
g.beer_servings.mean().sort_values(ascending=False)
g.wine_servings.sum().describe()
g.mean()
g.median()
g.spirit_servings.aggregate(['mean','min','max'])
