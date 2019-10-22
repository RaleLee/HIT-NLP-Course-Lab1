# coding=utf-8
from utils import readFile, writeSeg, binary_search
import time

def BMM(dicpath, textpath):
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
    # count time
    startTime = time.time()
    # Do FMM
    textSize = len(textlines)
    seg = []
    # count = 0
    for i in range(textSize):
        text = textlines[i].strip()
        wordList = []
        while len(text) > 0:
            # True_statements if expression else False_statements
            lenTryWord = maxWordLen if len(text) > maxWordLen else len(text) 
            tryWord = text[len(text) - lenTryWord:]
            while not binary_search(dic, tryWord):
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[1:]
            # match successfully
            wordList.insert(0, tryWord)
            # start match the remain part
            text = text[:len(text) - len(tryWord)]
        seg.append(wordList)
    endTime = time.time()
    print((endTime - startTime) * 1000)
    return seg 



dicpath = "outputs/dic.txt"
textpath = "dataset/199801_sent.txt"
segpath = "outputs/seg_BMM.txt"
def main():
    seg = BMM(dicpath, textpath)
    writeSeg(segpath, seg)
    return

if __name__ == "__main__":
    main()