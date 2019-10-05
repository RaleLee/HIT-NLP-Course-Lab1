# coding=utf-8
from utils import readFile, writeDic

def FMM(dicpath, textpath):
    # read text from file
    textlines = readFile(textpath)

    # read dic from file
    oriDic = readFile(dicpath)
    # new a dic for running code and the origin dic won't be destroy
    dic = []
    # count the maxlen of a word
    maxWordLen = 0
    dicSize = len(oriDic)
    for i in range(dicSize):
        tmp = oriDic[i].split(" ") # the dic format: word POS times
        dic.append(tmp[0]) # only needs word
        if(len(tmp[0]) > maxWordLen):
            maxWordLen = len(tmp[0])
    # Do FMM
    textSize = len(textlines)
    for i in range(textSize):
        text = textlines[i]
        wordList = []
        # True_statements if expression else False_statements
        len = maxWordLen if len(text) > maxWordLen else len(text) 
        tryWord = text[:len]
        while tryWord not in dic:
            

    return 



dicpath = "dic.txt"
textpath = "199801_sent.txt"
def main():
    FMM(dicpath, textpath)
    return

if __name__ == "__main__":
    main()