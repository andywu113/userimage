from sqlalchemy import create_engine
import time
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def convert_time(t):
    t = time.localtime(t)
    dt = time.strftime('%Y-%m-%d %H:%M:%S', t)
    return dt

def company_number(num,conn):
    sql = '''select * from `%s`'''%num
    df = pd.read_sql(sql, con=conn)
    df.time_stamp=df.time_stamp.values.astype('int64')/1000
    df.time_stamp=df.time_stamp.astype(int)
    df.index=df.time_stamp.apply(convert_time)
    df=df.drop(['time_stamp'],axis=1)
    return df

def getData(i):
    duiying=pd.read_csv(r'E:\mysite\celery_tasks\userimage\libs\export.csv',encoding='utf-8')
    duiying=duiying.drop_duplicates()
    engine = create_engine("mysql+pymysql://root:Ene!@#2019@192.168.1.157/fangrong_history?charset=utf8")
    conn = engine.connect()
    sql = '''show tables'''
    gongsi=pd.read_sql(sql, con=conn)
    num=gongsi.Tables_in_fangrong_history[i]
    temp=duiying[duiying['name']==int(num)]['mdmid'].values
    data=company_number(num,conn)
    mid=list(set(data.mdmid))
    data1={}
    for x in temp:
        temp1=data[data.mdmid==x]['Meter.Ptotal'].drop_duplicates()
        temp1=pd.to_numeric(temp1, errors='coerce')
        temp1.index=pd.to_datetime(temp1.index)
        temp1.sort_index(inplace=True)
        if len(temp1)!=0:
            data1[x]=temp1
    return pd.DataFrame(data1)

def totaldata(i):
    data0 = getData(i)
    data0 = data0.fillna(method="ffill").fillna(method="bfill")
    data = data0.sum(axis=1)
    return data

def dataClean(seriesData):
    seriesData = seriesData.resample("15min").asfreq()
    seriesData = seriesData.fillna(method="ffill").fillna(method="bfill")
    mean = np.mean(seriesData)
    std = np.std(seriesData)
    for i in range(len(seriesData)):
        if (seriesData[i] <= mean-3*std) or (seriesData[i] >= mean+3*std):
            try:
                seriesData[i] = np.sum(seriesData[i-3:i]+seriesData[i+1:i+4])/6
            except:
                seriesData[i] = mean
            continue
    return seriesData

def company_and_dateBegin2dateEnd(data,begin,end):
    data=data[begin*96:end*96]
    data=np.array(data)
    data=np.reshape(data,(end-begin,96))
    return data

def trueData(i,begin,end):
    data1 = totaldata(i)
    data2 = dataClean(data1)
    data = company_and_dateBegin2dateEnd(data2,begin,end)
    return data

