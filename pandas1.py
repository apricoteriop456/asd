# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 13:46:16 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/chipotle.tsv'  
chipo = pd.read_csv(url, sep = '\t')
chipo.head(10)
chipo.shape
chipo.info()
c=chipo.groupby(['item_name'])
c=c.sum()
c=c.sort_values(['quantity'],ascending=False)
c.head(1)
chipo['item_name'].nunique()
chipo.item_name.value_counts().count()
#chipo['item_name'].unique()可以列出唯一值具体有哪些
chipo['choice_description'][4]
d=chipo.groupby(['choice_description']).sum()
d=d.sort_values(['quantity'],ascending=False)
total_items_orders=chipo.quantity.sum()
#把价格转化为浮点型数据
chipo.item_price=chipo.item_price.str[1:].astype('float')
type(chipo.item_price.values[0])
chipo.item_price.dtype
chipo.dtypes
chipo['revenue']=chipo.item_price*chipo.quantity
chipo.revenue.sum()
chipo['order_id'].nunique()
e=chipo.groupby(['order_id']).sum()
e['revenue'].mean()

chipo.dtypes
dayu10=chipo[chipo.item_price>10]
dayu10['item_name'].value_counts()
len(chipo[chipo['item_name']=='Veggie Salad Bowl'])
len(chipo[(chipo.item_name=='Canned Soda') & (chipo.quantity>1)])

import matplotlib.pyplot as plt
from collections import Counter

x=chipo.item_name
letter_counts=Counter(x)
#以上函数相当于的结果储存在字典中
letter_counts.sort()
type(letter_counts)
letter_counts.keys()x.value_counts()
#df=pd.DataFrame(letter_counts,index=letter_counts.keys())是错的
df.info()
df.head()
df = pd.DataFrame.from_dict(letter_counts, orient='index')
df=df.sort_values(0)[45:50]
df.plot(kind='bar')

df2=pd.DataFrame(x.value_counts())
df2[0:5].plot(kind='bar')

plt.xlabel('Items')
plt.ylabel('Price')
plt.title('Most ordered Chipotle\'s Items')

#商品价格和订购数量的散点图,通过列表生成式可以生成一个序列
chipo.item_price=[float(value[1:-1]) for value in chipo.item_price]
type(chipo.item_price)
orders = chipo.groupby('order_id').sum()
plt.scatter(x = orders.item_price, y = orders.quantity, s = 30, c = 'green')

# Set the title and labels
plt.xlabel('Order Price')
plt.ylabel('Items ordered')
plt.title('Number of items ordered per order price')
plt.ylim(0,40)
?plt.ylim
