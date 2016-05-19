# coding: utf-8
# 生成最终的excel
import csv
import os

import pandas as pd

import xlwt
import math

def makeExcel(filename):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('InputSheet')  # 命名sheet的名字

    # 生成表格的表头列
    ws.write(0, 0, 'time')
    list = [3, 5, 10, 15, 30, 90, 200, 400]

    k = 1
    for i in range(len(list)):
        for j in range(i + 1, len(list)):
            ws.write(0, k, str(list[i]) + 'rsi-' + str(list[j]) + 'rsi')
            k += 1
    ws.write(0, 29, 'results')
    # 将所有的ma对齐放入ma_all2中
    ma_all = []

    for i in list:
        csvfile = file('data/stockRSI/'+filename+'/'+str(i) + 'rsi.csv', 'rb')
        reader = csv.reader(csvfile)
        tmp = []
        for line in reader:
            tmp.append(line)
        ma_all.append(tmp)

    ma_all2 = []
    for ma in ma_all:
        ma = ma[400:]
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
    csvfile2 = file('data/originalData/'+filename+'.csv', 'rb')
    reader2 = csv.reader(csvfile2)
    prices = []  # 拿到所有的价格
    for line in reader2:
        prices.append(line[1])

    results = []  # 写入结果，涨1，跌0
    # 400-1
    for i in range(399, len(prices) - 1):
        # if float(prices[i+1])>float(prices[i]):
        #     results.append(1)
        # else:
        #     results.append(0)
        p = (float(prices[i + 1]) - float(prices[i])) / float(prices[i])
        result = 1 / (1 + math.exp(-p * 100))
        results.append(result)

    for i in range(len(results)):
        ws.write(i + 1, 29, results[i])

    if not os.path.exists('data/neuralInput/' + filename):
        os.mkdir('data/neuralInput/' + filename)
    wb.save('data/neuralInput/'+filename+'/'+'inputRSI.xls')