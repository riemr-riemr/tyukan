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
    FILENAME = 'darp20.txt'
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

    route = [[118, 123, 112, 97, 267, 66, 43, 262, 91, 241, 53, 256, 107, 58, 210, 82, 187, 197, 50, 235, 54, 108, 251, 32, 226, 202, 198, 5, 194, 252, 3, 176, 149, 18, 47, 80, 95, 96, 239, 162, 224, 191, 147, 240], [62, 206, 64, 30, 24, 104, 130, 15, 174, 208, 248, 72, 128, 127, 159, 271, 216, 168, 92, 274, 122, 51, 236, 57, 272, 33, 195, 266, 48, 177, 192, 22, 166, 201], [126, 87, 139, 42, 46, 283, 133, 186, 231, 136, 270, 31, 37, 117, 190, 261, 277, 129, 17, 77, 280, 138, 175, 83, 161, 181, 221, 61, 227, 273, 12, 88, 71, 215, 282, 156, 232, 205], [49, 28, 134, 35, 179, 93, 193, 278, 19, 60, 4, 163, 172, 73, 90, 237, 148, 68, 204, 217, 67, 234, 55, 26, 211, 212, 170, 199], [86, 141, 106, 285, 59, 131, 275, 203, 230, 78, 41, 111, 250, 255, 105, 222, 185, 115, 259, 249], [114, 25, 258, 6, 169, 121, 150, 89, 7, 16, 151, 34, 20, 142, 178, 286, 164, 265, 160, 233, 100, 244], [119, 124, 143, 144, 84, 75, 263, 288, 268, 219, 228, 287], [69, 94, 29, 21, 79, 213, 140, 223, 85, 165, 173, 238, 70, 229, 135, 113, 103, 279, 284, 247, 214, 257], [109, 253, 137, 45, 44, 38, 2, 1, 145, 13, 146, 65, 189, 281, 209, 116, 182, 188, 260, 157], [23, 36, 11, 39, 155, 110, 120, 183, 125, 167, 269, 264, 180, 52, 254, 196, 81, 74, 102, 132, 99, 63, 243, 27, 218, 8, 225, 276, 98, 40, 246, 14, 184, 9, 171, 207, 10, 153, 76, 152, 158, 242, 56, 101, 200, 245, 220, 154]]
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

    route = [[1, 6, 110, 41, 111, 74, 255, 150, 15, 39, 254, 23, 145, 185, 159, 218, 120, 183, 125, 167, 140, 269, 284, 264], [51, 40, 62, 206, 184, 77, 70, 195, 113, 104, 96, 240, 72, 248, 87, 109, 221, 61, 214, 114, 257, 127, 271, 231, 216, 253, 131, 205, 275, 88, 71, 215, 258, 232], [94, 19, 238, 103, 123, 14, 83, 43, 267, 163, 247, 227, 137, 45, 12, 158, 68, 56, 200, 156, 212, 187, 135, 189, 281, 279], [86, 93, 143, 4, 117, 261, 287, 8, 25, 152, 230, 169, 121, 237, 148, 132, 99, 63, 78, 243, 27, 222, 46, 49, 276, 265, 9, 48, 171, 207, 193, 190, 192, 153], [52, 47, 80, 95, 55, 26, 239, 224, 196, 191, 91, 170, 199, 141, 20, 97, 119, 98, 263, 138, 235, 164, 142, 241, 285, 282, 89, 105, 59, 286, 242, 203, 115, 259, 249, 233], [34, 66, 76, 128, 101, 245, 220, 57, 272, 210, 33, 178, 29, 21, 2, 79, 201, 85, 223, 165, 173, 177, 229, 146], [35, 129, 100, 179, 84, 75, 118, 244, 13, 262, 42, 133, 186, 273, 136, 3, 228, 219, 124, 92, 277, 17, 157, 10, 280, 24, 236, 154, 36, 147, 69, 161, 268, 126, 213, 168, 270, 180], [28, 134, 38, 44, 90, 73, 172, 18, 188, 60, 182, 278, 144, 30, 234, 217, 204, 11, 162, 174, 7, 155, 151, 288], [112, 64, 67, 53, 256, 58, 82, 107, 197, 130, 211, 139, 208, 16, 202, 283, 226, 251, 274, 122, 65, 116, 209, 266, 260, 160], [106, 250, 81, 102, 5, 31, 225, 32, 108, 246, 50, 175, 54, 22, 166, 149, 37, 176, 252, 198, 194, 181]]
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