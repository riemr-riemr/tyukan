import numpy as np
import random
import sys
import math
import time
import copy
import csv
import matplotlib.pyplot as plt

def hyojun(route): #標準偏差の計算, disに各車両の移動距離格納
    dis = []
    for i in range(len(route)):
        a = 0
        if len(route[i]) != 0:
            for j in range(len(route[i]) - 1):
                a += c[route[i][j]][route[i][j + 1]]
            a += c[0][route[i][0]]
            a += c[0][route[i][j + 1]]
        dis.append(a)
    return np.std(dis)*2

def distance(x1, x2, y1, y2):
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d

def Setting(FILENAME):
    mat = []             # 距離計算用のdepo+出発地+目的地
    with open('/home/rei/ドキュメント/benchmark/' + FILENAME, 'r', encoding='utf-8') as fin:
        for line in fin.readlines():
            row = []
            toks = line.split()
            for tok in toks:
                try:
                    num = float(tok)
                except ValueError:
                    continue
                row.append(num)
            mat.append(row)

    # インスタンスの複数の行（問題設定）を取り出す
    Setting_Info = mat.pop(0)  # 0:車両数、4:キャパシティ、8:一台あたりの最大移動時間(min)、9:一人あたりの最大移動時間(min)

    # デポの座標を取り出す
    depo_zahyo = np.zeros(2)  # デポ座標配列
    x = mat.pop(-1)
    depo_zahyo[0] = x[1]
    depo_zahyo[1] = x[2]


    # 各距離の計算
    c = np.zeros((len(mat), len(mat)), dtype=float, order='C')
    for i in range(len(mat)):
        for j in range(len(mat)):
            c[i][j] = distance(mat[i][1], mat[j][1], mat[i][2], mat[j][2])

    request_number = len(mat) - 1

    #乗り降りの0-1情報を格納
    noriori = np.zeros(len(mat), dtype=int, order='C')
    for i in range(len(mat)):
        noriori[i] = mat[i][4]

    return Setting_Info, request_number, depo_zahyo, c, noriori

def Route_cost(route):
    Route_sum = 0
    Route_sum_k = np.zeros(len(route), dtype=float, order='C')
    for i in range(len(route)):
        if len(route[i]) == 0:
            Route_sum_k[i] = 0
        else:
            for j in range(len(route[i]) - 1):
                Route_sum_k[i] = Route_sum_k[i] + c[route[i][j]][route[i][j + 1]]
            Route_sum_k[i] = Route_sum_k[i] + c[0][route[i][0]]
            Route_sum_k[i] = Route_sum_k[i] + c[0][route[i][j + 1]]
        Route_sum = Route_sum + Route_sum_k[i]

    return Route_sum


def route_k_cost_sum(route_k):
    route_k_sum = 0
    if not len(route_k) == 0:
        for i in range(len(route_k) - 1):
            route_k_sum = route_k_sum + c[route_k[i]][route_k[i + 1]]
        route_k_sum = route_k_sum + c[0][route_k[0]]
        route_k_sum = route_k_sum + c[0][route_k[i + 1]]

    return route_k_sum

if __name__ == '__main__':
    FILENAME = 'darp01.txt'
    print(FILENAME)
    Setting_Info = Setting(FILENAME)[0]

    n = int(Setting(FILENAME)[1])  # depoを除いたノード数
    m = int(Setting_Info[0])  # 車両数
    d = 5  # 乗り降りの時間
    Q_max = Setting_Info[4]  # 車両の最大容量 global変数 capacity関数で使用
    T_max = Setting_Info[8]  # 一台当たりの最大移動時間
    L_max = Setting_Info[9]  # 一人あたりの最大移動時間


    noriori = np.zeros(n + 1, dtype=int, order='C')
    noriori = Setting(FILENAME)[4]  # global変数  capacity関数で使用

    depo_zahyo = Setting(FILENAME)[2]  # デポの座標

    c = np.zeros((n + 1, n + 1), dtype=float, order='C')
    c = Setting(FILENAME)[3]  # 各ノード間のコスト

    route = [[9, 2, 1, 20, 33, 19, 4, 14, 28, 16, 26, 25, 40, 38, 43, 44], [5, 29, 8, 13, 17, 18, 7, 41, 31, 32, 42, 11, 10, 34, 35, 37], [23, 15, 47, 21, 12, 24, 39, 48, 6, 3, 27, 22, 45, 46, 30, 36]]
    min = 10000
    max = 0
    print('swap&hyojun無し')
    for i in range(len(route)):  #初期解
        print(route_k_cost_sum(route[i]))
        if max <= route_k_cost_sum(route[i]):
            max = route_k_cost_sum(route[i])
        if min >= route_k_cost_sum(route[i]):
            min = route_k_cost_sum(route[i])
    print('max',max)


    print("~~~~~~~~~~~~")

    route = [[9, 2, 1, 20, 33, 19, 4, 14, 28, 16, 26, 25, 40, 38, 43, 44], [5, 29, 8, 13, 17, 18, 7, 41, 31, 32, 42, 11, 10, 34, 35, 37], [23, 15, 47, 21, 12, 24, 39, 48, 6, 3, 27, 22, 45, 46, 30, 36]]
    min = 10000
    max = 0
    print('swap&hyojun有り')
    for i in range(len(route)):  #解
        print(route_k_cost_sum(route[i]))
        if max <= route_k_cost_sum(route[i]):
            max = route_k_cost_sum(route[i])
        if min >= route_k_cost_sum(route[i]):
            min = route_k_cost_sum(route[i])
    print('max',max)