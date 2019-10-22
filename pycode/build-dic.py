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

def main(segpath, dicpath):
    lines = readFile(segpath)
    dic = buildDic(lines)
    writeDic(dicpath, dic)


segpath = "dataset/199801_seg.txt"
dicpath = "outputs/dic.txt"

if __name__ == "__main__":
    main(segpath, dicpath)
