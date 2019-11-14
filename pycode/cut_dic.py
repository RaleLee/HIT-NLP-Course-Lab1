# coding=utf-8
from utils import readFile, writeTrainList

traindicpath = "train/trainset.txt"
testsentpath = "train/testsent.txt"
testsegpath = "train/testset.txt"
segpath = "dataset/199801_seg&pos.txt"
sentpath = "dataset/199801_sent.txt"

def main():
    trainSet = []
    testSet = []
    testSent = []
    lines = readFile(segpath)
    sentlines = readFile(sentpath)
    length = len(lines)
    length_sent = len(sentlines)
    assert length == length_sent , "Not Equal!!"
    for i in range(length):
        if i % 10 == 7 or i % 10 == 8 or i % 10 == 9:
            testSet.append(lines[i])
            testSent.append(sentlines[i])
        else:
            trainSet.append(lines[i])
    writeTrainList(testsentpath, testSent)
    writeTrainList(testsegpath, testSet)
    writeTrainList(traindicpath, trainSet)

if __name__ == "__main__":
    main()