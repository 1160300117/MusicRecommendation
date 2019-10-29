# 矩阵分解
import numpy as np
import math
import threading
import scipy.sparse as ss


class UV:
    def __init__(self, fileaddr, d):
        self.mat = [] # 将txt中的数据转存至稀疏矩阵
        with open(fileaddr, 'r') as f:
            for line in f.readlines():
                line_arr = line.replace("\n", "").split(" ")
                self.mat.append(line_arr)
        # 手动设置artist，user，潜在因子数量
        self.musicians = 488184
        self.users = 89450
        self.d = d
        # 初始化U、V矩阵
        self.U = np.ones((self.users, self.d))
        self.V = np.ones((self.d, self.musicians))
        # 记录每行/列中不为空的元素位置
        self.posU = []
        self.posV = []
        # 计算posU和posV
        self.step = 0.05 # 迭代步长
        for ii in range(self.users):
            self.posU.append([])
        for ii in range(self.musicians):
            self.posV.append([])
        # 创建字典，(user, artist)为key，播放次数为value
        self.dictMat = dict()
        for row in self.mat:
            self.posU[int(row[0])].append(int(row[1]))
            self.posV[int(row[1])].append(int(row[0]))
            self.dictMat[(int(row[0]), int(row[1]))] = int(row[2])

    # 求均方根误差
    def getRMSE(self):
        RMSE = 0
        i = 0
        for lists in self.posU:
            for x in lists:
                RMSE += pow((self.dictMat.get((i, x)) - self.getM(i, x)), 2)
            i += 1
        return math.sqrt(RMSE)

    # 输入位置坐标row, col
    # 返回U、V乘积矩阵在[row][col]位置上的值
    def getM(self, row, col):
        res = 0
        for i in range(self.d):
            res += self.U[row][i] * self.V[i][col]
        return res

    # 迭代一代
    def loop(self):
        for i in range(self.d):
            # 先U的第i列
            for j in range(self.users):
                # U[j][i]
                self.increaseU(j, i)
            # 再V的第i行
            for j in range(self.musicians):
                # V[i][j]
                self.increaseV(i, j)

    # userid:r, d:s
    # 计算U[r][s]
    def increaseU(self, r, s):
        sum1 = 0
        sum2 = 0
        for j in self.posU[r]:
            # 上面括号内求和
            sum3 = 0
            for k in range(self.d):
                if k != s:
                    sum3 += self.U[r][k] * self.V[k][j]
            # 上面求和
            sum1 += self.V[s][j] * (self.dictMat.get((r, j)) - sum3)
            # 下面求和
            sum2 += pow(self.V[s][j], 2)
        if sum2 == 0:
            self.U[r][s] = 0
        else:
            if (sum1 / sum2 > self.U[r][s]):
                self.U[r][s] = sum1 / sum2
            else:
                self.U[r][s] = sum1 / sum2


    # artistid:s, d:r
    # 计算V[r][s]
    def increaseV(self, r, s):
        sum1 = 0
        sum2 = 0
        for i in self.posV[s]:
            sum3 = 0
            for k in range(self.d):
                if k != r:
                    sum3 += self.U[i][k] * self.V[k][s]

            sum1 += self.U[i][r] * (self.dictMat.get((i, s)) - sum3)

            sum2 += pow(self.U[i][r], 2)
        if sum2 == 0:
            self.V[r][s] = 0
        else:
            if (sum1 / sum2 > self.V[r][s]):
                self.V[r][s] = sum1 / sum2
            else:
                self.V[r][s] = sum1 / sum2

    def output(self):
        # 输出U矩阵
        for row in self.U:
            line = str(row[0])
            for i in range(self.d - 1):
                line = line + ' ' + str(row[i + 1])
            line = line + "\n"
            with open("output/UmatS.txt", 'a') as mon:
                mon.write(line)
        # 输出V矩阵
        for row in self.V:
            line = str(row[0])
            for i in range(self.musicians - 1):
                line = line + ' ' + str(row[i + 1])
            line = line + "\n"
            with open("output/VmatS.txt", 'a') as mon:
                mon.write(line)
