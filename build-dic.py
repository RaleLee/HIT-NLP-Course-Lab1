# coding=utf-8
from utils import readFile, writeDic

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
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    dic = sorted(dic.items(), key=lambda e: e[0][0], reverse = False)
    return dic

def main(segpath, dicpath):
    lines = readFile(segpath)
    dic = buildDic(lines)
    writeDic(dicpath, dic)


segpath = '199801_seg.txt'
dicpath = "dic.txt"

if __name__ == "__main__":
    main(segpath, dicpath)
