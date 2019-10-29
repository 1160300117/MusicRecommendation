import numpy as np

class wash:
    def __init__(self):
        self.alias_dict = dict()

    # 处理映射集
    def read_alias(self):
        with open("data/artist_alias.txt", 'r') as f:
            for line in f.readlines():
                tmp = line.split("\t")
                self.alias_dict[tmp[0]] = tmp[1]

    # 将 artist 规范化
    def replace_artist(self):
        with open("data/user_artist_data.txt", 'r') as f:
            for line in f.readlines():
                tmp = line.split(" ")
                write_line = ""
                if(tmp[1] in self.alias_dict.keys()):
                    write_line = tmp[0] + ' ' + self.alias_dict[tmp[1]] + ' ' + tmp[2]
                else: write_line = line
                with open("output/replaced_user_artist_data.txt", "a") as mon:
                    mon.write(write_line)
    
    # 按 user 合并相同 artist 的次数（针对该数据集似乎并不需要）
    def score_merge(self):
        with open("data/replaced_user_artist_data.txt", "r") as f:
            user_id = ""
            one_user = []
            for line in f.readlines():
                line_arr = line.replace("\n", '').split(" ")
                if(len(line_arr) == 3):
                    line_arr[2] = int(line_arr[2])
                    if(line_arr[0] != user_id):
                        self.merge(one_user)
                        user_id = line_arr[0]
                        one_user = []
                    one_user.append(line_arr)

    # 合并单个 user 的 artist
    def merge(self, mat):
        artist_line_dict = dict()
        res = []
        i = 0
        for line in mat:
            if line[1] not in artist_line_dict.keys():
                artist_line_dict[line[1]] = i
                res.append(line)
                i += 1
            else:
                res[artist_line_dict[line[1]]][2] += line[2]
        for line in res:
            write_line = line[0] + " " + line[1] + " " + str(line[2]) + "\n"
            with open("output/merged_user_artist_data.txt", "a") as mon:
                mon.write(write_line)
    
    # 输出对应稀疏矩阵
    def output(self):
        # with open("output/train.txt", "r") as f:
        with open("output/merged_user_artist_data.txt", "r") as f:
            userid2int = dict()
            artist2int = dict()
            iu = 0
            ia = 0
            # 将user和artist的id转换为序号
            for line in f.readlines():
                line_arr = line.replace("\n", "").split(" ")
                newline = ""
                if(line_arr[0] not in userid2int.keys()):
                    userid2int[line_arr[0]] = iu
                    newline = str(iu) + " "
                    iu += 1
                else:
                     newline = str(userid2int[line_arr[0]]) + " "

                if(line_arr[1] not in artist2int.keys()):
                    artist2int[line_arr[1]] = ia
                    newline = newline + str(ia) + " "
                    ia += 1
                else:
                    newline = newline + str(artist2int[line_arr[1]]) + " "

                newline = newline + line_arr[2] + "\n"
                with open("output/final_data.txt", 'a') as mon:
                    mon.write(newline)

    def score(self):
        with open("output/final_data.txt", 'r') as f:
            for line in f.readlines():
                line_arr = line.replace("\n", "").split(" ")
                newline = line_arr[0] + ' ' + line_arr[1] + ' ' + item_score(line_arr[2]) + '\n'
                with open("output/final_scored_data.txt", 'a') as mon:
                    mon.write(newline)

# 评分
def item_score(str):
    cnt = int(str)
    res = '0'
    if(cnt > 5 and cnt <= 15):
        res = '1'
    elif(cnt > 15 and cnt <= 40):
        res = '2'
    elif(cnt > 40 and cnt <= 60):
        res = '3'
    elif(cnt > 50 and cnt <= 100):
        res = '4'
    elif(cnt > 100):
        res = '5'
    return res