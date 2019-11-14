import re
from utils import readFile, writeList
#前面长串数字，，方括号[]

givenList = []
FMMList = []

def match_date(line):
    line = re.match("(\d{8}-\d{2}-\d{3}-\d{3})", line)
    if(line == None):
        return False
    return True

def calculate():
    TP = 0 #正确的被判断正确
    P = 0 #自己分词总数
    T = 0 #seg标准分词总数

    lengthGivenList = len(givenList)##  i  大
    lengthFMMList = len(FMMList)##  j 小
    i = 0
    j = 0
    while(j < lengthFMMList and i<lengthGivenList):

        givenWordList = givenList[i]  # m 小
        FMMWordList = FMMList[j]  # n  大

        P = P+len(FMMWordList)
        T = T+len(givenWordList)

        m = 0
        n = 0
        while n < len(FMMWordList) and m<len(givenWordList):
            FMMWord = FMMWordList[n]
            givenWord = givenWordList[m]
            if(FMMWord == givenWord):
                m = m+1
                n = n+1
                TP = TP+1
                continue
            #不相等，则在分词集中不断取词，直到与given相等
            k = 0
            l = 0
            while FMMWord != givenWord:
                if(len(FMMWord) <= len(givenWord)):
                    k = k+1
                    FMMWord = FMMWord + FMMWordList[n+k]

                else:
                    l = l+1
                    givenWord = givenWord+givenWordList[m+l]

            n = n + k + 1
            m = m + l + 1
            #TP = TP+1

        i = i+1
        j = j+1

        # 解决空行问题。。
        while j < lengthFMMList and FMMList[j] == []:
            j = j + 1
        while i < lengthGivenList and givenList[i] == []:
            i = i + 1

    result = []
    result.append(TP)
    result.append(P)
    result.append(T)
    return result

if __name__ == "__main__":
#每一行句子里面为词的list

    
    with open('dataset/199801_seg.txt', 'r') as rGiven:
        for sentence in rGiven.readlines():
            givenWordList = []
            line = sentence.split()
            for part in line:
                word = part.split('/')[0]  # 获得词
                word = re.sub('\[', '', word)  # 去除词中[
                # if (match_date(word)):  # 去除日期
                #     continue
                givenWordList.append(word)
            givenList.append(givenWordList)
        rGiven.close()

    #FMM
    FMMList = []
    with open('outputs/seg_FMM_test.txt', 'r') as fr:
        for sentence in fr.readlines():
            FMMWordList = []
            line = sentence.split()
            for part in line:
                word = part.split('/')[0]  # 获得词
                # if (match_date(word)):  # 去除日期
                #     continue
                FMMWordList.append(word)
            FMMList.append(FMMWordList)
        fr.close()
    result1 = calculate()
    print(result1)
    precision1 = result1[0] / result1[1]
    recall1 = result1[0] / result1[2]
    F1 = (2*precision1*recall1)/(precision1+recall1)

    #BMM
    # FMMList = []
    # with open('./seg_BMM.txt', 'r') as br:
    #     for sentence in br.readlines():
    #         FMMWordList = []
    #         line = sentence.split()
    #         for part in line:
    #             word = part.split('/')[0]  # 获得词
    #             FMMWordList.append(word)
    #         FMMList.append(FMMWordList)
    #     br.close()
    # result2 = calculate()
    # print(result2)
    # precision2 = result2[0] / result2[1]
    # recall2 = result2[0] /  result2[2]
    # F2 = (2 * precision2 * recall2) / (precision2 + recall2)

    # #unigram
    # FMMList = []
    # with open('./seg_LM.txt', 'r') as br:
    #     for sentence in br.readlines():
    #         FMMWordList = []
    #         line = sentence.split()
    #         for part in line:
    #             word = part.split('/')[0]  # 获得词
    #             FMMWordList.append(word)
    #         FMMList.append(FMMWordList)
    #     br.close()
    # result3 = calculate()
    # print("unigram: ")
    # print(result3)
    # precision3 = result3[0] / result3[1]
    # recall3 = result3[0] /  result3[2]
    # F3 = (2 * precision3 * recall3) / (precision3 + recall3)
    # print("precision:\t"+str(precision3))
    # print("recall:\t"+str(recall3))
    # print("F:\t"+str(F3))
    # print()

    # #bigram
    # FMMList = []
    # with open('./seg_LM_bigram.txt', 'r') as br:
    #     for sentence in br.readlines():
    #         FMMWordList = []
    #         line = sentence.split()
    #         for part in line:
    #             word = part.split('/')[0]  # 获得词
    #             FMMWordList.append(word)
    #         FMMList.append(FMMWordList)
    #     br.close()
    # result4 = calculate()
    # print("bigram: ")
    # print(result4)
    # precision4 = result4[0] / result4[1]
    # recall4 = result4[0] /  result4[2]
    # F4 = (2 * precision4 * recall4) / (precision4 + recall4)
    # print("precision:\t"+str(precision4))
    # print("recall:\t"+str(recall4))
    # print("F:\t"+str(F4))

    with open('outputs/score_FMM_test3.txt', 'w') as w:
        w.write("FMM:\n")
        w.write("准确率（precision）:\t"+ str(precision1)+"\n")
        w.write("召回率（recall）:\t" + str(recall1) + "\n")
        w.write("F值:\t"+str(F1)+"\n\n")

        # w.write("BMM:\n")
        # w.write("准确率（precision）:\t" + str(precision2) + "\n")
        # w.write("召回率（recall）:\t" + str(recall2) + "\n")
        # w.write("F值:\t" + str(F2) + "\n")

        w.close()
