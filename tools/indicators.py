# coding: utf-8
#从中证500指数的csv文件中读取数据制成另一张excel

import csv
import numpy as np
import os

import talib

originalDataPath = 'data/originalData/'
indicatorPath = 'data/indicator/'


# 读取csv文件
def getIndicators(filename,*indicator):

    csvfile = file(originalDataPath + filename +'.csv', 'rb')
    reader = csv.reader(csvfile)

    all_close = []  # 得到所有的收盘价和日期
    all_days = []
    for line in reader:
        all_close.append(line[1])
        all_days.append(line[0])

    float_allclose = [float(x) for x in all_close]

    # 获取第4天到最后一天的日期和对应的3日均值，合并他们，为写入csv文件做准备
    days = [3, 5, 10, 15, 30, 90, 200, 400]

    for day in days:
        list_alldays = all_days

        for item in indicator:
            if item == 'MA':
                list_ma = talib.MA(np.array(float_allclose), timeperiod=day)
                merge = []
                for i in range(len(list_alldays)):
                    tmp = (list_alldays[i], list_ma[i])
                    merge.append(tmp)
            if item == 'RSI':
                list_rsi = talib.RSI(np.array(float_allclose), timeperiod=day)
                merge = []
                for i in range(len(list_alldays)):
                    tmp = (list_alldays[i], list_rsi[i])
                    merge.append(tmp)

            # 写入*.csv文件
            if not os.path.exists(indicatorPath + filename + '/' + item):
                os.mkdir(indicatorPath + filename + '/' + item)
            with open(indicatorPath + filename + '/' + item + '/' + str(day) + item + '.csv', 'w') as f:
                f_csv = csv.writer(f)
                f_csv.writerows(merge)

def getAllMacdHist(filename,list_para):

    csvfile = file(originalDataPath + filename + '.csv', 'rb')
    reader = csv.reader(csvfile)

    all_close = []  # 得到所有的收盘价和日期
    all_days = []
    for line in reader:
        all_close.append(line[1])
        all_days.append(line[0])

    float_allclose = [float(x) for x in all_close]

    for para in list_para:
       list_MACD,list_signal,hist = talib.MACD(
           np.array(float_allclose),
           fastperiod=para[0],
           slowperiod=para[1],
           signalperiod=para[2]
       )

       list_hist = hist.tolist()

       # 写入*.csv文件
       if not os.path.exists(indicatorPath + filename + '/' + 'MACD'):
           os.mkdir(indicatorPath + filename + '/' + 'MACD')
       with open(indicatorPath + filename + '/' + 'MACD/'+str(para[0])+'-'+str(para[1])+'-'+str(para[2]), 'w') as f:
           f_csv = csv.writer(f)
           f_csv.writerow(list_hist)



