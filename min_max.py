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
    FILENAME = 'darp02.txt'
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

    route = [[47, 95, 28, 11, 59, 32, 2, 80, 24, 18, 14, 76, 50, 12, 36, 66, 15, 33, 60, 72, 62, 81, 84, 8, 13, 63, 43, 61, 31, 35, 79, 91, 23, 83, 71, 56], [25, 73, 37, 9, 42, 22, 85, 29, 70, 41, 90, 77, 4, 52, 89, 57], [], [10, 6, 7, 5, 20, 38, 68, 27, 55, 19, 86, 58, 54, 75, 53, 3, 51, 48, 67, 96], [1, 30, 40, 49, 34, 82, 45, 26, 21, 46, 88, 78, 94, 44, 74, 93, 92, 39, 16, 64, 17, 69, 87, 65]]
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

    route = [[32, 18, 2, 80, 10, 48, 6, 50, 14, 96, 66, 22, 42, 29, 54, 11, 90, 77, 58, 70, 59, 62, 16, 64, 17, 65], [20, 68, 39, 5, 7, 55, 19, 37, 67, 53, 85, 87], [15, 23, 35, 4, 63, 43, 52, 28, 91, 30, 83, 71, 36, 12, 3, 76, 51, 24, 78, 60, 72, 84], [25, 73, 27, 8, 13, 61, 56, 75], [47, 1, 46, 40, 49, 34, 82, 31, 45, 79, 26, 21, 95, 33, 88, 94, 9, 69, 44, 92, 38, 93, 74, 86, 81, 41, 89, 57]]
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