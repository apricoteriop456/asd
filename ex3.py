#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:23:54 2019
含有空间数据分析
查看每一列含有多少空值
data.isnull().sum()
查看每一列有多少空列表
for i in ['city','province','district','township']:#查看含有空列表的列
        print(str(i),':',(data['city'].apply(lambda x:len(x)==0)).sum())
找出含有空值的行
data[data.loncationdetail.isnull()]

@author: apple
"""
import os
os.getcwd()
#data.to_csv('/Users/apple/geodata.csv')
import pandas as pd
import numpy as np
import geopandas 
from shapely.geometry import LineString,Point
import re
import matplotlib.pyplot as plt
import matplotlib.pylab as plb
from  matplotlib import cm
import seaborn as sns
plt.rc('font', family='SimHei', size=18)# 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
sns.set()
#%matplotlib inline

import hashlib
from wordcloud import WordCloud
from matplotlib.patches import Polygon
#from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
import warnings
warnings.filterwarnings('ignore')


data=pd.read_excel('/Users/apple/Downloads/python2948/B_store.xls')
#type(data.isnull().sum(axis=1))#是序列
#data.isnull().sum(axis=1).value_counts()#查看是否有缺失值
data.isnull().sum()
data.duplicated().sum()#没有重复值

data=data.astype(str)
#data.address.values[0]
import requests
import json#json是独立于编程语言的文本格式，可以储存和表示数据，书写形式类似于字典

def get_locationdata(address):#定义获取具体位置的函数
    requests.adapters.DEFAULT_RETRIES =5
    requests.session().keep_alive = False
    url='http://restapi.amap.com/v3/geocode/geo?key=1fbbc548b828f33ccc64f4613ae52497&s=rsv3&city=35&address={}'.format(address)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if 'location' in response.text:
        for i in json.loads(response.text)['geocodes']:#json.loads()表示对数据进行解码；json.dumps()表示将数据编码为json形式
            return i.get('location')
    else:
        pass

data['loncationdetail']=data.address.apply(get_locationdata)
data[data.loncationdetail.isnull()]#显示缺失数据,返回存在空值的行
data.drop(1018,inplace=True)#删除1018行，并在愿数据中修改
data.address[95]='徐州市'+data.address[95]
data.address[332]='昆明市'+data.address[332]
data.address[648]='常州市'+data.address[648]
data.address[740]='昆明市'+data.address[740]
data.address[1033]='镇江市'+data.address[1033]
data.address[1095]='嘉兴市'+data.address[1095]
null=data[data.loncationdetail.isnull()].index
data['loncationdetail'][null]=data['address'][null].apply(get_locationdata)
data[data.loncationdetail.isnull()]#不再有缺失值

#从位置信息中得到纬度和经度
type(data.loncationdetail.values[0])
data['lon']=data.loncationdetail.str.split(',').apply(lambda x:x[0]).astype(float)
data['lat']=data.loncationdetail.str.split(',').apply(lambda x:x[1]).astype(float)

#根据经纬度获得具体位置信息
import re
#location=data.loncationdetail[1]
def get_data(location):
    url='https://restapi.amap.com/v3/geocode/regeo?key=1fbbc548b828f33ccc64f4613ae52497&s=rsv3&city=35&location={}'.format(location)
    requests.adapters.DEFAULT_RETRIES =5
    requests.session().keep_alive = False
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    address_dict={}
    if 'regeocode' in response.text:
        #address_detail0=re.search('"addressComponent":(.*?)',response.text).group(1)
        address_detail=re.search('"addressComponent":(.*),(.*),(.*),(.*)',response.text).group(1)
        address_dict['city']=json.loads(address_detail)['city']
        address_dict["province"]=json.loads(address_detail)["province"]
        address_dict["district"]=json.loads(address_detail)["district"]
        address_dict["township"]=json.loads(address_detail)["township"]
    else:
        pass
    return address_dict 

data['city']=data.loncationdetail.apply(get_data).apply(lambda x:x['city'])
data['province']=data.loncationdetail.apply(get_data).apply(lambda x:x['province'])
data['district']=data.loncationdetail.apply(get_data).apply(lambda x:x['district'])
data['township']=data.loncationdetail.apply(get_data).apply(lambda x:x['township'])
pd.write_csv()
data.head()
#显示含有空值的列,每一列有多少个缺失值
#data[['city','province','district','township']].isnull().sum()他的结果显示没有空值
#应该是查询含有空列表的数目,data['city']获得序列，data[['city']]获得数据框
#在数据框上使用apply返回每一列或每一行的最后汇总值，在序列上使用apply返回每一个数的执行结果
#(data[['city']].apply(len)==0).sum();Out[256]: 0
#(data['city'].apply(len)==0).sum();Out[257]: 294

np.isnan(data['city']).sum()#返回的是有几个数，不是每个数的长度
for i in ['city','province','district','township']:#查看含有空列表的列
        print(str(i),':',(data[i].apply(lambda x:len(x)==0)).sum())
        
#查看含有city列为空列表的行索引,并且说明缺失是因为直辖市的原因        
pd.Series((data[data.province.str.contains('市')].index)==data[data['city'].apply(lambda x:len(x)==0)].index).value_counts()
#补全city为空列表的值
data.city[data[data.province.str.contains('市')].index]=data.province[data[data.province.str.contains('市')].index]
data['city'].apply(lambda x:len(x)==0).sum()#city已经没有空列表

#查看district存在空列表的行索引
data[data['district'].apply(lambda x:len(x)==0)].index



xy = [Point(xy) for xy in zip(data.lon,data.lat)]#zip用于将可迭代的对象将为参数，将对象中对应的元素打包为一个个元祖
geo_data=geopandas.GeoDataFrame(data,geometry=xy)#geopandas结合了pandas和shapely的功能，扩展了pandas在空间数据操作方面的能力，使python可以实现空间数据分析
geo_data.head()

#导入中国地图
gdf = geopandas.read_file(r"/Users/apple/Downloads/python2948/china_basic_map/bou2_4p.shp",encoding='gbk')
#gdf比dataframe多了一个geometry变量
gdf.head()

gdf.plot(figsize=(15,15), alpha=0.5, edgecolor='black',color='gray')
plt.gca().xaxis.set_major_locator(plt.NullLocator()) #去掉x轴刻度
plt.gca().yaxis.set_major_locator(plt.NullLocator()) #去掉y轴刻度

geo_data.plot(ax=gdf.plot(figsize=(15,15),legend=True,edgecolor='white',color='gray'),color='yellow',markersize=8)
plt.rc('font', family='SimHei', size=20)# 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
plt.title('B快餐公司微信手机点餐门店城市分布图',size=20)
plt.gca().xaxis.set_major_locator(plt.NullLocator()) #去掉x轴刻度
plt.gca().yaxis.set_major_locator(plt.NullLocator()) #去掉y轴刻度

geo_data['shop_counts']=geo_data.groupby('province')['geometry'].transform(lambda x: x.count())
#transform函数与apply函数类似，但只能用于每一列的计算，输出结果与df的结构相同，所以这里要用transform,而不是apply

geo_data.plot(ax=gdf.plot(figsize=(15,15),legend=True,edgecolor='white',color='gray'),column='shop_counts', cmap='rainbow',scheme='quantiles',legend=True,figsize=(8,10)
             ,marker='o', markersize=100) #按个数多少叠加底色
plt.gca().xaxis.set_major_locator(plt.NullLocator()) #去掉x轴刻度
plt.gca().yaxis.set_major_locator(plt.NullLocator()) #去年y轴刻度

#各省市门店数
province_pc=geo_data.groupby('province',as_index=False)['shop_counts'].count().sort_values('shop_counts',ascending=False)
province_pc.head(10)
#as_index=False表示不使用分组labels作为最终输出序列的index
import squarify
labels = province_pc.apply(lambda x: str(x[0]) + "\n (" + str(x[1]) + ")", axis=1)
sizes = province_pc['shop_counts'].values.tolist()
colors = [plt.cm.Set1(i/float(len(labels))) for i in range(len(labels))]
plt.figure(figsize=(10,12),dpi= 80)
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=.8)
plt.rc('font',size=10)
plt.title('各省市门店数树形图')
plt.axis('off')#去除上边框和右边框刻度
plt.tick_params(top='off',right='off')##去除上边框和右边框刻度