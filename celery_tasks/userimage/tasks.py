from __future__ import absolute_import, unicode_literals
from .libs.data_transform import trueData
from .libs.function import AutoEncoder
from celery_tasks.celery import app
import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
import json

@app.task(bind=True)
def cluster(self,i,begin,end):
    """
    :param i:表示第i家公司
    :param begin:开始的天数
    :param end:结束的天数
    :return:返回一个字典，包含最优簇数、轮廓系数和主负荷曲线数据
    """
    data = AutoEncoder(i,begin,end)
    dataOrigin = trueData(i, begin, end)
    score = []
    dic = {}
    for i in range(2,int((end-begin)/10)):
        estimatorK = KMeans(n_clusters=i,random_state=9)
        y_pred = estimatorK.fit_predict(data)
        score.append(metrics.calinski_harabaz_score(data,y_pred))
    best_n = score.index(np.max(score)) + 2
    estimator = KMeans(n_clusters=best_n,random_state=9)
    estimator.fit(data)
    label = estimator.labels_
    CHscore = metrics.calinski_harabaz_score(data,label)
    length=[]
    for j in range(best_n):
        data_fig=[dataOrigin[i] for i in range(len(label)) if label[i]==j]
        #dayList=[i for i in range(len(label)) if label[i]==j]
        length.append(len(data_fig))
    data_fig_max=length.index(np.max(length))
    data_max=[dataOrigin[i] for i in range(len(label)) if label[i]==data_fig_max]
    data_mean=np.array(data_max).mean(axis=0)
    data_mean = list(data_mean)
    print("成功一次")
    dic["best_k"] = best_n
    dic["CHscore"] = CHscore
    dic["principleCurve"] = data_mean
    return json.dumps(dic)

# @app.task(bind=True)
# def clusterBetweenCompany(self,k):
#     dataForCluster = getScalerCompaniesData()
#     dataOrigin = getOriginalCompaniesData()
#     estimator = KMeans(n_clusters=k, random_state=9)
#     estimator.fit(dataForCluster)
#     label = estimator.labels_
#     index = list(dataForCluster.index)
#     #CHscore = metrics.calinski_harabaz_score(dataForCluster, label)
#     dic = {}
#     for j in range(k):
#         data_fig = [dataOrigin.iloc[i,:] for i in range(len(label)) if label[i] == j]
#         comList = []
#         for i in range(len(label)):
#             if label[i] == j:
#                 comList.append(index[i])
#         dic[j] = comList
#     return json.dumps(dic)