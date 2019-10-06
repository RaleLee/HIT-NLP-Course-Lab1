# coding=utf-8
from utils import readFile, writeSeg
import DoubleArrayTrie
import time

def FMM(dicpath, textpath):
    # read text from file
    textlines = readFile(textpath)

    # read dic from file
    oriDic = readFile(dicpath)
    # new a dic for running code and the origin dic won't be destroy
    dic = DoubleArrayTrie.DoubleArrayTrie()
    # count the maxlen of a word
    maxWordLen = 0
    dicSize = len(oriDic)
    for i in range(dicSize):
        tmp = oriDic[i].split(" ") # the dic format: word POS times
        word = []
        for ch in tmp[0]:
            word.append(ch)
        dic.add(word) # only needs word
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
            tryWord = text[:lenTryWord]
            word = []
            for ch in tryWord:
                word.append(ch)
            while word not in dic:
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[:len(tryWord) - 1]
                word = word[:len(word) - 1]
            # match successfully
            wordList.append(tryWord)
            # start match the remain part
            text = text[len(tryWord):]
        seg.append(wordList)
        # count += 1
        # print(count)
    endTime = time.time()
    print((endTime - startTime) * 1000)
    return seg 



dicpath = "dic.txt"
textpath = "199801_sent.txt"
segpath = "seg_FMM_withDAT.txt"
def main():
    seg = FMM(dicpath, textpath)
    writeSeg(segpath, seg)
    return

if __name__ == "__main__":
    main()