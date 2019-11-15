# coding=utf-8
from utils import readFile, writeList
from math import log
from time import time
import datetime
import HMM

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
            prefix_dict[word] += freq
        
        sum += freq

        # for word in dict, get the prefix of it
        for ch in range(len(word)):
            prefix = word[:ch + 1]
            if prefix not in prefix_dict:
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
    route[sen_len] = (0, 0)
    log_sum = log(sum)
    for idx in range(sen_len - 1, -1, -1):
        # max_tu = (-100000000,0)
        # for x in DAG[idx]:
        #     if(sen[idx : x + 1] in dic):
        #         freq = dic[sen[idx : x + 1]] or 1
        #         log_freq = log(freq)
        #         try:
        #             com = log_freq - log_sum + route[x+1][0]
        #         except TypeError:
        #             print(type(log_freq))
        #             print(type(log_sum))
        #             print(route[x+1][0])

        #         if (com, x) > max_tu:
        #             max_tu = (com, x) 
        # route[idx] = max_tu
        route[idx] = max((log(dic.get(sen[idx: x+1]) or 1) - log_sum + route[x + 1][0], x) for x in DAG[idx])
    return route


# get seg for a single sentence with DAG and HMM
def seg_sen(sen, DAG, dic, sum):
    route = {}
    route = cal_route(sen, DAG, route, dic, sum)
    # print(datetime.datetime.now())
    x = 0
    buf = ""
    length = len(sen)
    while x < length:
        y = route[x][1] + 1
        l_word = sen[x : y]
        if y - x == 1:
            buf += l_word
        else:
            if buf:
                if len(buf) == 1:
                    yield buf
                    buf = ""
                else:
                    if buf not in dic:
                        recognized = model.seg(buf)
                        for t in recognized:
                            yield t
                    else:
                        for elem in buf:
                            yield elem
                    buf = ""
            yield l_word
        x = y
    
    if buf:
        if len(buf) == 1:
            yield buf
        elif buf not in dic:
            recognized = model.seg(buf)
            for t in recognized:
                yield t
        else:
            for elem in buf:
                yield elem
    

# for line to do seg
def LM_one_gram_OOV_seg(textpath, dic, sum):
    textlines = readFile(textpath)
    textSize = len(textlines)
    seg = []
    # count = 0
    startTime = time()
    print(datetime.datetime.now())
    for i in range(textSize):
        sen = textlines[i].strip()
        if len(sen) == 0:
            seg.append("")
            continue
        linebegin = sen[:19]
        sen = sen[19:]
        DAG = build_DAG(sen, dic)
        sen_seg = linebegin  + "/ " + "/ ".join(seg_sen(sen, DAG, dic, sum)) + "/ "
        seg.append(sen_seg)
        # print(datetime.datetime.now())
    endTime = time()
    print((endTime - startTime))
    return seg


dicpath = "outputs/LMdic.txt"
textpath = "dataset/199801_sent.txt"
save_model_path = "outputs/save.pkl"
segpath = "outputs/seg_withLM1OOV.txt"
model = HMM.HMM()
def main():
    dic, sum = build_prefix_dict(dicpath)
    model.load(save_model_path)

    seg = LM_one_gram_OOV_seg(textpath, dic, sum)

    writeList(segpath, seg)
    return

if __name__ == "__main__":
    main()