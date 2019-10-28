#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 14:51:26 2019
1.usecols=basic_colnames,nrows=500000，学会这两个的用法
2.["user_roomservice_4_%sratio_3month" % i for i in [0,2,3,4,5]]
相似的结构用正则表达式
3.np.argmax返回最大值对应的index
4.all["service_equal_%s"%i] = list(map(lambda x, y: 1 if x == y else 0, all["roomservice_%s"%i], all["user_roomservice_%s_max"%i]))
两个注意点，第一all["service_equal_%s"%i]表明可以在名称中使用循环，比如循环生成表格名称有相同结构时可以使用；第二list(map(function,parameters))中的map和list配合使用
5.dataset=dataset.dropna(how='all',axis=1)可以找到某个属性全部缺失的特征
6.dataset.isnull().any()找到存在缺失值的属性
7.dataset.ix[:,[0,1,3,4,5]]=dataset.ix[:,[0,1,3,4,5]].applymap(lambda x :re.search('\d+',x).group())
re.search().group()中research和group联合使用可以返回查询结果，上述例子删掉特征中的文字部分,如‘ORDER_12194265’，然后返回‘12194265’
8.all.duplicated()返回数据集的每一行是否是重复的，即检测是否存在重复记录，返回一个长度和数据集一样的序列
9.feature_df.drop_duplicates(["orderid","basicroomid"],keep="last")表示删除["orderid","basicroomid"]当中出现的重复记录，只保留最后一次出现的那条记录

@author: apple
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
#一、现对数据集做简单分析
variable=pd.read_excel(r'/Users/apple/Downloads/ctrip/数据字典样例说明.xlsx')
basic_colnames = ['orderid','uid','orderdate','hotelid','basicroomid','roomid', 'orderlabel', 'star', 'rank', 'returnvalue', 'price_deduct', 'basic_minarea', 'basic_maxarea']
competition_train=pd.read_csv(r'/Users/apple/Downloads/ctrip/competition_train.txt',sep='\t',header=0, usecols=basic_colnames,nrows=500000)
competition_train.info()
competition_train.orderid.value_counts()
#订单号为ORDER_12207960最多为164，一共有304个订单号
competition_train.uid.value_counts()
#用户名为USER_130264最多为164，一共有300个用户名
competition_train.hotelid.value_counts()
#295家酒店,酒店id为HOTEL_133467的最多，记录有211次
competition_train['basicroomid'].value_counts()
#BASIC_477780的记录最多有40，共有1726条记录
competition_train['orderlabel'].value_counts()
#未预定记录有9698条，预定成功有302条
competition_train['star'].value_counts()
#酒店的级别只有4种，5、7、9、11，并且纪录数依次上升
competition_train['orderdate'].value_counts()
#**************************************************
#找出同一个用户在几家酒店有过预定记录

competition_train.isnull().sum()
#basic_minarea和basic_maxarea有缺失值
competition_train.basic_minarea.describe()
index_min=competition_train.basic_minarea[competition_train.basic_minarea==-1].index#109条记录的basic_minarea为-1
index_max=competition_train.basic_maxarea[competition_train.basic_maxarea==-1].index
(index_max==index_min).sum()#说明异常数据存在于相同的记录中，接下来将其删除
data=competition_train.drop(index_max)
data1=data[data['orderlabel']==1]

#查看订购房型的价格分布，想要知道不同价格的订单数
plt.figure(figsize=(15, 5))
plt.subplot(1,3,1)
data1['price_deduct'].plot(kind='hist',bins=20,label='直方图')
plt.subplot(1,3,2)
data1['price_deduct'].plot(kind='kde',label='核密度图')
plt.subplot(1,3,3)
data1[data1.price_deduct<6000].price_deduct.plot(kind='hist',bins=100,label='直方图')
#订单最多的集中在1000附近


#预定酒店的星级分布，star应该是分类型变量
data1.star=data1.star.astype('str')
data1.dtypes

plt.figure(figsize=[10,5])
plt.axes(aspect='equal')
data1.star.value_counts().plot(kind='pie',autopct='%.2f%%',labels=data1.star.value_counts().index)
#分析酒店星级与价格之间的关系
data_hist=data1.groupby('star')[['price_deduct','returnvalue']].mean()
data_hist.reset_index(inplace=True)
plt.subplot(1,2,1)
data_hist.plot(kind='bar',x='star',y=['price_deduct'],color=['steelblue'],rot=0)
for x,y in enumerate(data_hist.price_deduct):
    plt.text(x, y+0.001, '%.1f'% y, ha='center', va='bottom', fontsize=10)
plt.subplot(1,2,2)
data_hist.plot(kind='bar',x='star',y=['price_deduct','returnvalue'],color=['steelblue','indianred'],rot=0)

#二、数据清洗
import re
dataset=pd.read_csv(r'/Users/apple/Downloads/ctrip/competition_train.txt',sep='\t',header=0,nrows=500000)
dataset.describe()
dataset.dtypes
dataset.isnull().all().value_counts()
#可以找到某个属性全部缺失的特征
dataset=dataset.dropna(how='all',axis=1)
dataset.isnull().any()
#找到存在缺失值的属性
dataset=dataset.fillna(-1)
dataset['user_roomservice_8_345ratio']=dataset['user_roomservice_5_345ratio']
del dataset['user_roomservice_5_345ratio']

#re.search('\d+',dataset['orderid'][0]).group()
dataset.ix[:,[0,1,3,4,5]]=dataset.ix[:,[0,1,3,4,5]].applymap(lambda x :re.search('\d+',x).group())
dataset.ix[0:6,0:5]
dt1=pd.to_datetime(dataset['orderdate'])
dataset['orderdate']=dt1.dt.dayofyear
dataset=dataset.apply(pd.to_numeric)
dataset.info()

#三、构造特征
#每个basicroomid价格的中位数
def df_median(df):
    add=pd.DataFrame(df.groupby(['orderid','basicroomid']).price_deduct.median()).reset_index()
    add.columns=['orderid','basicroomid','basicroomid_price_deduct——median']
    df=df.merge(add,on=['orderid','basicroomid'],how='left')
    return df
data3=dataset.copy()
#data3=df_median(data3)
#df_median(dataset)[df_median(dataset).orderid==12251191][['orderid','basicroomid','basicroomid_price_deduct']]
#每个basicroomid价格的最小值
def df_min(df):
    add=pd.DataFrame(df.groupby(['orderid','basicroomid']).price_deduct.min()).reset_index()
    add.columns=['orderid','basicroomid','basicroomid_price_deduct_min']
    df=df.merge(add,on=['orderid','basicroomid'],how='left')
    return df
#data3=df_min(data3)
#每个订单价格的最小值
def df_min_orderid(df):
    add=pd.DataFrame(df.groupby(['orderid']).price_deduct.min()).reset_index()
    add.columns=['orderid','orderid_price_deduct_min']
    df=df.merge(add,on=['orderid'],how='left')
    return df
#data3=df_min_orderid(data3)
#排序特征
#data3.ix[:,-1]
def df_rank_mean(df):
    add=pd.DataFrame(df.groupby('basicroomid').orderid_price_deduct_min.mean()).reset_index()
    add.columns=['basicroomid','orderid_price_deduct_min_mean']
    df=df.merge(add,on=['basicroomid'],how='left')
    return df
#data3 = df_rank_mean(data3)
    
all = data3.copy()

all["user_roomservice_2_0ratio"]=1-all["user_roomservice_2_1ratio"]
all["user_roomservice_3_0ratio"]=1-all["user_roomservice_3_123ratio"]
all["user_roomservice_5_0ratio"]=1-all["user_roomservice_5_1ratio"]
all["user_roomservice_7_1ratio"]=1-all["user_roomservice_7_0ratio"]
all["user_roomservice_8_2ratio"]=1-all["user_roomservice_8_345ratio"]-all["user_roomservice_8_1ratio"]
all["user_roomservice_4_1ratio_3month"] = 1 - all[["user_roomservice_4_%sratio_3month" % i for i in [0,2,3,4,5]]].sum(axis=1)
all["user_roomservice_4_1ratio_1month"] = 1 - all[["user_roomservice_4_%sratio_1month" % i for i in [0,2,3,4,5]]].sum(axis=1)
all["user_roomservice_4_1ratio_1week"] = 1 - all[["user_roomservice_4_%sratio_1week" % i for i in [0,2,3,4,5]]].sum(axis=1)

#这样处理不妥
all["user_roomservice_2_max"] = np.argmax(all[["user_roomservice_2_%sratio" % i for i in range(2)]].values,axis=1)
all["user_roomservice_3_max"] = np.argmax(all[["user_roomservice_3_%sratio" % i for i in [0,123]]].values, axis=1)
all["user_roomservice_4_max"] = np.argmax(all[["user_roomservice_4_%sratio" % i for i in range(6)]].values, axis=1)
all["user_roomservice_5_max"] = np.argmax(all[["user_roomservice_5_%sratio" % i for i in range(2)]].values, axis=1)
all["user_roomservice_6_max"] = np.argmax(all[["user_roomservice_6_%sratio" % i for i in range(3)]].values, axis=1)
all["user_roomservice_7_max"] = np.argmax(all[["user_roomservice_7_%sratio" % i for i in range(2)]].values, axis=1)
all["user_roomservice_8_max"] = np.argmax(all[["user_roomservice_8_%sratio" % i for i in [1,2,345]]].values, axis=1)

all["user_roomservice_4_max_1week"]=np.argmax(all[["user_roomservice_4_%sratio_1week"%i for i in range(6)]].values,axis=1)
all["user_roomservice_4_max_1month"]=np.argmax(all[["user_roomservice_4_%sratio_1month"%i for i in range(6)]].values,axis=1)
all["user_roomservice_4_max_3month"]=np.argmax(all[["user_roomservice_4_%sratio_3month"%i for i in range(6)]].values,axis=1)

all["roomservice_8"]=all["roomservice_8"].apply(lambda x:2 if x>2 else x-1)
all["roomservice_3"]=all["roomservice_3"].apply(lambda x:1 if x>0 else 0)

for i in range(2,9):
    all["service_equal_%s"%i] = list(map(lambda x, y: 1 if x == y else 0, all["roomservice_%s"%i], all["user_roomservice_%s_max"%i]))
del all["user_roomservice_2_0ratio"]
del all["user_roomservice_3_0ratio"]
del all["user_roomservice_5_0ratio"]
del all["user_roomservice_7_1ratio"]

#添加转化率特征
#提取basicroomid的转化率
feature_df=all[["orderid","basicroomid","orderlabel"]].copy()
feature_df.sort_values("orderlabel")
feature_df=feature_df.drop_duplicates(["orderid","basicroomid"],keep="last")
basicroom_mean=pd.DataFrame(feature_df.groupby("basicroomid").orderlabel.mean()).reset_index()
basicroom_mean.columns=["basicroomid","basicroomid_mean"]

basicroom_sum=pd.DataFrame(feature_df.groupby("basicroomid").orderlabel.sum()).reset_index()
basicroom_sum.columns=["basicroomid","basicroomid_sum"]

all["price_tail1"]=all["price_deduct"]%10