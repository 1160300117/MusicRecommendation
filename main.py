import heapq as hq
import random
import numpy as np
import UV
import data_washing

# 数据预处理
wa = data_washing.wash() # 初始化
wa.read_alias() # 处理映射集
print("映射集处理结束")
wa.replace_artist() # 规范化 artist
print("规范化结束")
wa.output() # 输出稀疏矩阵
print("稀疏矩阵输出结束")
wa.score() # 评分
print("评分结束")

# 把处理好的数据划分为 train 和 verify
with open("output/final_scored_data.txt", 'r') as f:
    choose_rate = 0.2 # 80%数据用于测试， 20%数据用于验证
    i = 0
    for line in f.readlines():
        i += 1
        if(random.random() > choose_rate):
            with open("output/train.txt", 'a') as train:
                train.write(line)
        else:
            with open("output/train.txt", 'a') as verify:
                verify.write(line)
        print("done line " + i)

# 建立 UV 模型
uv = UV.UV("output/train.txt", 5)
rmse = uv.getRMSE()
for i in range(50):
    uv.loop()
    rmse = uv.getRMSE()
    if rmse < 1000:
        break
    print(rmse)
uv.output()

# 读取 U、V 矩阵
with open("output/UmatS.txt", 'r') as f:
    Umat = []
    for line in f.readlines():
        line_arr = line.replace("\n", "").split(" ")
        new_arr = []
        for item in line_arr:
            new_arr.append(float(item))
        Umat.append(new_arr)
with open("output/VmatS.txt", 'r') as f:
    Vmat = []
    for line in f.readlines():
        line_arr = line.replace("\n", "").split(" ")
        new_arr = []
        for item in line_arr:
            new_arr.append(float(item))
        Vmat.append(new_arr)

# 验证
with open("output/verify.txt", 'a') as verify:
    good = 0 # 得分一致
    ok = 0 # 相差1分以内
    bad = 0 # 得分不一致
    for line in verify.readlines():
        line_arr = line.replace("\n", "").split(" ")
        i = int(line_arr[0])
        j = int(line_arr[1])
        new = 0
        for k in range(5):
            new += Umat[i][k] * Vmat[k][j]
        score = int(new)
        if score == int(line_arr[2]):
            good = good + 1
        elif score >= int(line_arr[2]) - 1 and score <= int(line_arr[2]) + 1:
            ok = ok + 1
        else:
            bad = bad + 1
print("good = " + good + ", ok = " + ok + ", bad = " + bad)