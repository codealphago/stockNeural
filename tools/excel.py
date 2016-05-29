# coding: utf-8
# 生成最终的excel
import csv
import os

import pandas as pd

import xlwt
import math

indicatorPath = 'data/indicator/'
originalDataPath = 'data/originalData/'


def makeExcel(filename,type,indicator):
    neuralInputPath = 'data/neuralInput/' + filename + '/' + type + '/'
    diff = 0
    if indicator == 'MA':
        diff = -1

    wb = xlwt.Workbook()
    ws = wb.add_sheet('InputSheet')  # 命名sheet的名字

    # 生成表格的表头列
    ws.write(0, 0, 'time')
    list = [3, 5, 10, 15, 30, 90, 200, 400]

    k = 1
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            ws.write(0, k, str(list[i]) + indicator +'-' + str(list[j]) + indicator)
            k += 1
    ws.write(0, 29, 'results')
    # 将所有的ma对齐放入ma_all2中
    ma_all = []

    for i in list:
        csvfile = file(indicatorPath+filename+'/'+ indicator+ '/' +str(i) + indicator+'.csv', 'rb')
        reader = csv.reader(csvfile)
        tmp = []
        for line in reader:
            tmp.append(line)
        ma_all.append(tmp)

    ma_all2 = []
    for ma in ma_all:
        ma = ma[400+diff:]
        ma_all2.append(ma)

    # 写入输入的数据
    k = 1
    for i in range(len(ma_all2)):
        for j in range(i + 1, len(ma_all2)):
            #       实现向量相减  ma_all2[i]-ma_all2[j]
            for w in range(len(ma_all2[i])):
                ws.write(w + 1, k, float(ma_all2[i][w][1]) - float(ma_all2[j][w][1]))
            k += 1
    # 写入日期
    for i in range(len(ma_all2[0])):
        ws.write(i + 1, 0, ma_all2[0][i][0])

    # 写入结果
    csvfile2 = file(originalDataPath+filename+'.csv', 'rb')
    reader2 = csv.reader(csvfile2)
    prices = []  # 拿到所有的价格
    for line in reader2:
        prices.append(line[1])

    results = []  # 写入结果，涨1，跌0
    # 400-1
    for i in range(399+diff, len(prices) - 1):
        if type == 'binary':
            if float(prices[i+1])>float(prices[i]):
                results.append(1)
            else:
                results.append(0)
        elif type == 'real':
            p = (float(prices[i + 1]) - float(prices[i])) / float(prices[i])
            result = 1 / (1 + math.exp(-p * 100))
            results.append(result)

    for i in range(len(results)):
        ws.write(i + 1, 29, results[i])

    if not os.path.exists(neuralInputPath):
        os.mkdir(neuralInputPath)
    wb.save(neuralInputPath + 'input'+indicator+'.xls')

def makeMACDExcel(filename,type):
    neuralInputPath = 'data/neuralInput/' + filename + '/' + type + '/'
    wb = xlwt.Workbook()
    ws = wb.add_sheet('InputSheet')  # 命名sheet的名字
    # 写入表头行
    ws.write(0, 0, 'time')
    list_para = [
        '5-10-30',
        '5-34-21',
        '5-35-5',
        '5-55-10',
        '6-10-5',
        '6-30-3',
        '6-30-6',
        '6-30-9',
        '7-19-9',
        '8-13-9',
        '12-26-9'
    ]

    i=1
    for para in list_para:
        ws.write(0,i,para)
        i+=1

    ws.write(0,i,'result')
    # 写入日期数据
    csvfile = file(originalDataPath +filename+'.csv', 'rb')
    reader = csv.reader(csvfile)

    list_close = []
    for item in reader:
        list_close.append(item)

    j=1
    for item in list_close[55+10-2:]:
        time = item[0]
        ws.write(j,0,time)
        j+=1

    # 写入macdhist数据
    j=1
    for para in list_para:
        csvfile = file(indicatorPath+filename+'/'+'MACD/'+para,'rb')
        reader = csv.reader(csvfile)

        list_temp = []
        for item in reader:
            list_temp = item

        i= 1
        for item in list_temp[55+10-2:]:
            ws.write(i,j,item)
            i+=1
        j+=1

    # 写入结果
    results = []
    for i in range(len(list_close[55+10-2:])):
        price = list_close[i+(55+10-2)-1][1]
        price_next = list_close[i+(55+10-2)][1]
        if float(price_next) > float(price):
            results.append(1)
        else:
            results.append(0)

    i=1
    for result in results:
        ws.write(i,j,result)
        i+=1


    wb.save(neuralInputPath + 'input' + 'MACD' + '.xls')