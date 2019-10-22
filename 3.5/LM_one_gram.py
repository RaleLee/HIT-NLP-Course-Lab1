# coding=utf-8
from utils import readFile, writeSeg
from math import log
from time import time
import datetime

# build prefix dict
def build_prefix_dict(dicpath):
    prefix_dict = {}    # dic with frequence
    sum = 0    # total words num, including same words
    
    lines = readFile(dicpath)
    for line in lines:
        if len(line) == 0:
            continue
        tmp = line.strip().split(" ")   # the dic format: word POS times
        word, freq = tmp[0], int(tmp[2])
        if word not in prefix_dict:
            prefix_dict[word] = freq
        else:
            prefix_dict += freq
        
        sum += freq

        # for word in dict, get the prefix of it
        for ch in range(len(word)):
            prefix = word[:ch + 1]
            if(prefix) not in prefix_dict:
                prefix_dict[prefix] = 0
    return prefix_dict, sum

# build DAG
def build_DAG(sen, dic):
    DAG = {}
    sen_len = len(sen)
    for i in range(sen_len):
        tmp = []
        cur = i
        prefix = sen[i]
        while cur < sen_len and prefix in dic:
            if(dic[prefix] > 0):
                tmp.append(cur)
            cur += 1
            prefix = sen[i: cur + 1]
        if not tmp:
            tmp.append(i)
        DAG[i] = tmp

    return DAG 

# calculate the route
def cal_route(sen, DAG, route, dic, sum):
    sen_len = len(sen)
    route[sen_len] = (-0, 0)
    log_sum = log(sum)
    for idx in range(sen_len - 1, -1, -1):
        max_tu = (-100000000,0)
        for x in DAG[idx]:
            if(sen[idx : x + 1] in dic):
                freq = dic[sen[idx : x + 1]] or 1
                log_freq = log(freq)
                try:
                    com = log_freq - log_sum + route[x+1][0]
                except TypeError:
                    print(type(log_freq))
                    print(type(log_sum))
                    print(route[x+1][0])

                if (com, x) > max_tu:
                    max_tu = (com, x) 
        route[idx] = max_tu
        # route[idx] = max((log(dic[sen[idx : x + 1]] or 1) - log_sum + route[x+1][0], x) for x in DAG[idx])
    return route

# for line to do seg
def LM_one_gram_seg(textpath, dic, sum):
    textlines = readFile(textpath)
    textSize = len(textlines)
    seg = []
    # count = 0
    startTime = time()
    for i in range(textSize):
        sen = textlines[i].strip()
        route = {}
        DAG = build_DAG(sen, dic)
        # print(DAG)
        route =  cal_route(sen, DAG, route, dic, sum)
        sen_len = len(sen)
        sen_seg = []
        j = 0
        # print(datetime.datetime.now())
        # print(route)
        while j < sen_len:
            cur = route[j][1]
            sen_seg.append(sen[j:cur+1])
            j = cur + 1
            # print(sen_len)
            # print(sen[j:cur+1] + "fuck")
            # print(datetime.datetime.now())
            # print(j)
        seg.append(sen_seg)
        print(datetime.datetime.now())
    endTime = time()
    print((endTime - startTime) * 1000)
    return seg


dicpath = "outputs/dic.txt"
textpath = "dataset/199801_sent.txt"
segpath = "outputs/seg_withLM1.txt"
def main():
    dic, sum = build_prefix_dict(dicpath)
    seg = LM_one_gram_seg(textpath, dic, sum)
    writeSeg(segpath, seg)
    return

if __name__ == "__main__":
    main()