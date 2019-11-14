import re

def analysis(givenList, FMMList):
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

standard_path = "dataset/199801_seg&pos.txt"
seg_FMM = "outputs/seg_FMM.txt"
seg_BMM = "outputs/seg_BMM.txt"
outputs = "outputs/score.txt"

def main():
    givenList = []
    givenWordList = []
    with open(standard_path, 'r') as f:
        for sentence in f.readlines():
            givenWordList = []
            line = sentence.split()
            for part in line:
                word = part.split('/')[0]  # 获得词
                word = re.sub('\[', '', word)  # 去除词中[
                # if (match_date(word)):  # 去除日期
                #     continue
                givenWordList.append(word)
            givenList.append(givenWordList)
        f.close()
    
    #FMM
    FMMList = []
    with open(seg_FMM, 'r') as f:
        for sentence in f.readlines():
            FMMWordList = []
            line = sentence.split()
            for part in line:
                word = part.split('/')[0]  # 获得词
                # if (match_date(word)):  # 去除日期
                #     continue
                FMMWordList.append(word)
            FMMList.append(FMMWordList)
        f.close()

    result1 = analysis(givenList, FMMList)
    print(result1)
    precision1 = result1[0] / result1[1]
    recall1 = result1[0] / result1[2]
    F1 = (2*precision1*recall1)/(precision1+recall1)

    #BMM
    BMMList = []
    with open(seg_BMM, 'r') as f:
        for sentence in f.readlines():
            BMMWordList = []
            line = sentence.split()
            for part in line:
                word = part.split('/')[0]  # 获得词
                BMMWordList.append(word)
            BMMList.append(FMMWordList)
        f.close()
    result2 = analysis(givenList, BMMList)
    print(result2)
    precision2 = result2[0] / result2[1]
    recall2 = result2[0] /  result2[2]
    F2 = (2 * precision2 * recall2) / (precision2 + recall2)

    with open(outputs, 'w') as w:
        w.write("FMM:\n")
        w.write("precision:"+ str(precision1)+"\n")
        w.write("recall:" + str(recall1) + "\n")
        w.write("F1:"+str(F1)+"\n\n")

        w.write("BMM:\n")
        w.write("precision:" + str(precision2) + "\n")
        w.write("recall:" + str(recall2) + "\n")
        w.write("F1:" + str(F2) + "\n")
        
        w.close()
    return

if __name__ == "__main__":
    main()