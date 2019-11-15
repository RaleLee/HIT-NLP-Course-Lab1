# coding=utf-8
from utils import readFile, writeDic
import re

def buildDic(lines):
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
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

# another build dict method. Number, Name, Punctuation, Time is not included in this dic
def buildSpDic(lines):
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
            if fullword[1] == "nr" or fullword[1] == "ns":
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

# another build dict method. Number, Name, Punctuation, Time is not included in this dic
def buildNumDic(lines):
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
            if fullword[1] == "nr" or fullword[1] == "ns":
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
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

def buildEnDic(lines):
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
            if fullword[1] == "nr" or fullword[1] == "ns":
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            # punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def buildPtDic(lines):
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
            if fullword[1] == "nr" or fullword[1] == "ns":
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
            #punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation = 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def buildNrDic(lines):
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
            if fullword[1] == "ns":
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def buildNsDic(lines):
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
            if fullword[1] == "nr":
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def buildNsNrDic(lines):
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
            punctuation = '\s+\.\!\/_,$%^*(+\"\')——()?【】“”！，。？、~@#￥%……&*（）°±‘’℃Ⅱ①②③④⑤⑥⑦⑵▲△○●《》『』Ⅲ‰％×〈〉∶—+·．０１２３４５６７８９＊＋－／：；＝＞［］'
            punctuation += 'ＡＢＣＤＥＦＫＩＮＬＧＳＨＪＲＴＸＭＹＰＯＶａｂｅｍｎｈｏ'
            word0 = re.sub(r'[{}]+'.format(punctuation), "", word0)
            if len(word0) == 0 or len(word0) != ori:
                continue
            if "千" == word0[-1] or "百" == word0[-1] or "亿" == word0[-1] or "万" == word0[-1] or "年" == word0[-1]:
                continue
            if "一九九" in word0 or "分之" in word0 or "一万" in word0 or "一二" == word0[0:2]:
                continue
            if len(word0) > 1 and ("十" == word0[1] or "千" == word0[1] or "百" == word0[1]):
                continue 
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

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
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

segpath = "train/trainset.txt"
dicpath = "train/trainDic.txt"
sp_dicpath = "train/sptrainDic.txt"
num_dicpath = "train/numtrainDic.txt"
nr_dicpath = "train/nrtrianDic.txt"
en_dicpath = "train/entrainDic.txt"
ns_dicpath = "train/nstrainDic.txt"
pt_dicpath = "train/pttrainDic.txt"
nsnr_dicpath = "train/nsnrtrainDic.txt"
nsrum_dicpath = "train/nsrumtrainDic.txt"

def main():
    lines = readFile(segpath)
    dic = buildDic(lines)
    dicsp = buildSpDic(lines)
    dicnum = buildNumDic(lines)
    dicen = buildEnDic(lines)
    dicpt = buildPtDic(lines)
    dicnr = buildNrDic(lines)
    dicns = buildNsDic(lines)
    dicnsnr = buildNsNrDic(lines)
    dicnsrum = buildNsrumDic(lines)
    
    writeDic(dicpath, dic)
    writeDic(sp_dicpath, dicsp)
    writeDic(num_dicpath, dicnum)
    writeDic(en_dicpath, dicen)
    writeDic(pt_dicpath, dicpt)
    writeDic(nr_dicpath, dicnr)
    writeDic(ns_dicpath, dicns)
    writeDic(nsnr_dicpath, dicnsnr)
    writeDic(nsrum_dicpath, dicnsrum)


if __name__ == "__main__":
    main()
