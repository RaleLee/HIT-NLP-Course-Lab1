# coding=utf-8
from utils import readFile, writeDic
import re

def buildNsrumDic(lines):
    dic = dict()
    words = set()
    for line in lines:       
        linewords = line.split(" ")
        linewords = linewords[1:]
        for word in linewords:
            if(word == " "):
                continue
            fullword = tuple(word.strip().split("/"))
            if(len(fullword[0]) == 0 or len(fullword[1]) == 0):
                continue
            copy = fullword
            if fullword[0][0] == "[" and len(fullword[0]) > 1:
                fullword = (fullword[0][1:], copy[1])
            copy = fullword
            if "]" in fullword[1]:
                tmp_list = fullword[1].split("]")
                fullword = ( copy[0],tmp_list[0]) 
            # to cut all the numbers, punctuations, times
            word0 = fullword[0]
            ori = len(word0)
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            # punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

segpath = "dataset/199801_seg&pos.txt"
dicpath = "outputs/dic.txt"

def main():
    lines = readFile(segpath)
    dic = buildNsrumDic(lines)
    writeDic(dicpath, dic)

if __name__ == "__main__":
    main()
