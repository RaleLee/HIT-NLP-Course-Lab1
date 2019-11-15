# coding=utf-8
from utils import readFile, writeSeg
import time

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
    dic =  set(dic)
    # count time
    startTime = time.time()
    # Do FMM
    textSize = len(textlines)
    seg = []
    # count = 0
    for i in range(textSize):
        text = textlines[i].strip()
        wordList = []
        if not len(text) == 0:
            linebegin = text[:19]
            text = text[19:]
            wordList.append(linebegin)

        while len(text) > 0:
            # True_statements if expression else False_statements
            lenTryWord = maxWordLen if len(text) > maxWordLen else len(text) 
            tryWord = text[:lenTryWord]
            while tryWord not in dic:
                if len(tryWord) == 1:
                    break
                tryWord = tryWord[:len(tryWord) - 1]
            # match successfully

            wordList.append(tryWord)
            # start match the remain part
            text = text[len(tryWord):]
        seg.append(wordList)
        # count += 1
        # print(count)
    endTime = time.time()
    print((endTime - startTime))
    return seg 



dicpath = "train/trainDic.txt"
sp_dicpath = "train/sptrainDic.txt"
num_dicpath = "train/numtrainDic.txt"
nr_dicpath = "train/nrtrianDic.txt"
en_dicpath = "train/entrainDic.txt"
ns_dicpath = "train/nstrainDic.txt"
pt_dicpath = "train/pttrainDic.txt"
nsnr_dicpath = "train/nsnrtrainDic.txt"
nsrum_dicpath = "train/nsrumtrainDic.txt"
textpath = "train/testsent.txt"
segpath = "train/seg_all.txt"
sp_segpath = "train/seg_sp.txt"
num_segpath = "train/seg_num.txt"
nr_segpath = "train/seg_nr.txt"
en_segpath = "train/seg_en.txt"
ns_segpath = "train/seg_ns.txt"
pt_segpath = "train/seg_pt.txt"
nsnr_segpath = "train/seg_nsnr.txt"
nsrum_segpath = "train/seg_nsrum.txt"
# test_path = "dataset/199801_sent.txt"
# test_dic = "outputs/dic.txt"
# test_segpath = "outputs/seg_FMM.txt"

def main():
    seg_all = FMM(dicpath, textpath)
    seg_sp = FMM(sp_dicpath, textpath)
    seg_num = FMM(num_dicpath, textpath)
    seg_nr = FMM(nr_dicpath, textpath)
    seg_ns = FMM(ns_dicpath, textpath)
    seg_en = FMM(en_dicpath, textpath)
    seg_pt = FMM(pt_dicpath, textpath)
    seg_nsnr = FMM(nsnr_dicpath, textpath)
    seg_nsrum = FMM(nsrum_dicpath, textpath)
    
    writeSeg(segpath, seg_all)
    writeSeg(sp_segpath, seg_sp)
    writeSeg(num_segpath, seg_num)
    writeSeg(nr_segpath, seg_nr)
    writeSeg(ns_segpath, seg_ns)
    writeSeg(en_segpath, seg_en)
    writeSeg(pt_segpath, seg_pt)
    writeSeg(nsnr_segpath, seg_nsnr)
    writeSeg(nsrum_segpath, seg_nsrum)

    # seg = FMM(test_dic, test_path)
    # writeSeg(test_segpath, seg)
    return

if __name__ == "__main__":
    main()