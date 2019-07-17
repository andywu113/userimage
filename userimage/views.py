from django.shortcuts import render
# Create your views here.
import django
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from sklearn.cluster import KMeans
from celery_tasks.userimage.tasks import cluster
from .libs.getCompaniesData import getOriginalCompaniesData,getScalerCompaniesData
import warnings
warnings.filterwarnings("ignore")

@csrf_exempt
def principleCurve(request):
    """
    :param request:
    :return: best k,chscore and principle curve,it is a dic
    """
    try:
        i = int(request.GET.get("i",0))
    except:
        return JsonResponse({'code':0,'msg':'参数i错误'})
    try:
        begin = int(request.GET.get("begin",0))
    except:
        return JsonResponse({'code':0,'msg':'参数begin错误'})
    try:
        end = int(request.GET.get("end",100))
    except:
        return JsonResponse({'code':0,'msg':'参数end错误'})
    solve = cluster.delay(i,begin,end)
    result = solve.get()
    if solve.ready():
        return JsonResponse({'code':'1','msg':'SUCCESS','result':result})


@csrf_exempt
def companiesCluster(request):
    """
    :param request:
    :return:cluster result,a dic
    """
    try:
        k = int(request.GET.get("k",15))
    except:
        return JsonResponse({'code':0,'msg':'参数k错误'})
    dataForCluster = getScalerCompaniesData()
    dataOrigin = getOriginalCompaniesData()
    estimator = KMeans(n_clusters=k, random_state=9)
    estimator.fit(dataForCluster)
    label = estimator.labels_
    index = list(dataForCluster.index)
    # CHscore = metrics.calinski_harabaz_score(dataForCluster, label)
    result = {}
    for j in range(k):
        data_fig = [dataOrigin.iloc[i, :] for i in range(len(label)) if label[i] == j]
        comList = []
        for i in range(len(label)):
            if label[i] == j:
                comList.append(index[i])
        result[j] = comList
    return JsonResponse({'code':'1','msg':'SUCCESS','result':result})
    #return JsonResponse(json.dumps(dic),safe=False)


# celery -A celery_tasks worker -l info -P eventlet
