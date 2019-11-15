# coding=utf-8
from utils import readFile, writeList, writeSeg
from time import time
from math import log


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
            if(prefix) not in prefix_dict:
                prefix_dict[prefix] = 0
    return prefix_dict, sum

# build prefix dict with the new dict
def build_bi_prefix_dict(dicpath):
    prefix_dict = {}    # dic with word pair frequence

    lines = readFile(dicpath)
    for line in lines:
        if len(line) == 0:
            continue
        tmp = line.strip().split(" ")
        word1, word2, freq = tmp[0], tmp[1], int(tmp[2])
        if word1 not in prefix_dict:
            tmp_dic = {}
            tmp_dic[word2] = freq
            prefix_dict[word1] = tmp_dic
        else:
            prefix_dict[word1][word2] = freq
    
    return prefix_dict

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

def cal_score(word1, word2, dict, bidict):
    pword1 = 0
    if word1 in dict:
        pword1 = dict[word1]
    if pword1 == 0:
        pword1 = 0.5  # Laplace smoothing 
    pword2 = 0
    if word2 in bidict:
        if word1 in bidict[word2]:
            pword2 = bidict[word2][word1]
    if pword2 == 0:
        pword2 = 0.000001 # smoothing
    plog = log(pword2) - log(pword1)
    return plog

# calculate the route
def cal_route_two(sen, DAG, route, dic, bi_dic):
    seg = []
    pos = 5    # BOS
    length = len(sen) - 5    # EOS
    left_g = {}
    right_g = {}
    first_g = {}
    for x in DAG[5]:
        first_g[(5, x+1)] = cal_score("<BOS>", sen[5:x+1], dic, bi_dic)
    left_g["<BOS>"] = first_g

    while pos < length:
        idx = DAG[pos]
        for x in idx:
            left_w = sen[pos : x + 1]
            cur_pos = x + 1
            cur_idx = DAG[x + 1]
            tmp = {}
            for cx in cur_idx:
                right_w = sen[cur_pos : cx + 1]
                if right_w == "<":
                    right_w = "<EOS>"
                    tmp[right_w] = cal_score(left_w, right_w, dic, bi_dic)
                else:
                    tmp[(cur_pos, cx + 1)] = cal_score(left_w, right_w, dic, bi_dic)
            left_g[(pos, x + 1)] = tmp
        pos += 1
    
    keys = list(left_g.keys())
    # right_graph
    for key in keys:
        nodes = left_g[key].keys()
        for node in nodes:
            if node in right_g:
                right_g[node] = right_g[node]
            else:
                right_g[node] = []
            right_g[node].append(key)

    # dp
    
    keys.append("<EOS>")
    for key in keys:
        if key == "<BOS>":
            route[key] = (0.0, "<BOS>")
        else:
            if key in right_g:
                nodes = right_g[key]
            else:
                route[key] = (-65507, "<BOS>")
                continue
            route[key] = max((left_g[node][key] + route[node][0], node) for node in nodes)

    # flash back
    pos = "<EOS>"
    while True:
        pos = route[pos][1]
        if pos == "<BOS>":
            break
        seg.insert(0, sen[pos[0] : pos[1]])            
    # print(seg)
    return seg



def LM_two_gram_seg(textpath, dic, bi_dic):
    textlines = readFile(textpath)
    textSize = len(textlines)

    seg = []
    # count = 0
    startTime = time()
    for i in range(textSize):
        sen = textlines[i].strip()
        if len(sen) == 0:
            sen_seg = []
            seg.append(sen_seg)
            continue
        linebegin = sen[:19]
        sen = sen[19:]
        sen = "<BOS>" + sen + "<EOS>"
        route = {}
        DAG = build_DAG(sen, dic)
        sen_seg = cal_route_two(sen, DAG, route, dic, bi_dic)
        sen_seg.insert(0, linebegin)
        seg.append(sen_seg)
    endTime = time()
    print((endTime - startTime))
    return seg

dicpath = "outputs/LMdic.txt"
bi_dicpath = "outputs/bidic.txt"
textpath = "dataset/199801_sent.txt"
segpath = "outputs/seg_withLM2.txt"

def main():
    dic, _ = build_prefix_dict(dicpath)
    bi_dic = build_bi_prefix_dict(bi_dicpath)
    seg = LM_two_gram_seg(textpath, dic, bi_dic)
    writeSeg(segpath, seg)
    return

if __name__ == "__main__":
    main()