# Create your views here.
# import os
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings("ignore")

#对企业间进行聚类的数据进行处理
def getDataFramne(df):
    """
    :param df:输入一个数据框
    :return: 返回一个处理后的数据框
    """
    index = df.iloc[:,0]
    columns = df.columns[1:]
    values = df.values[:,1:]
    return pd.DataFrame(values,index=index,columns=columns)

def getOriginalCompaniesData():
    """
    自行导入所有公司的主负荷曲线数据
    :return:返回一个公司的主负荷曲线数据
    """
    path = r"E:\mysite\userimage\libs\companyCurve.csv"
    data = pd.read_csv(path)
    dataCompany = getDataFramne(data).dropna()
    return dataCompany

def getScalerCompaniesData():
    """
    自行导入所有公司的主负荷曲线数据
    :return:返回一个处理后的公司的主负荷曲线数据
    """
    path = r"E:\mysite\userimage\libs\companyCurve.csv"
    data = pd.read_csv(path)
    dataOringinCompany = getDataFramne(data).dropna()
    index = dataOringinCompany.index
    scaler = MinMaxScaler()
    scalerData = scaler.fit_transform(dataOringinCompany.T)
    dataMinMax = scalerData.T
    dataCompany = pd.DataFrame(dataMinMax,index=index)
    return dataCompany
