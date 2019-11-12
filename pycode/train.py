from utils import readFile, writeList
def analysis(standard_path, my_seg_path):
    F1 = 0
    Precision = 0
    Recall = 0
    word_true = 0   # true seg word num
    word_cor = 0    # predict correct word num
    word_pre = 0    # predict word num

    standard_seg = readFile(standard_path)
    my_seg = readFile(my_seg_path)
    # remove blank lines in standard & my_seg
    tmp_list = []
    for line in standard_seg:
        if line == "" or line == "\n": #or line == "\n\r": #or line == "\r\n":
            continue
        else:
            tmp_list.append(line.strip())
    standard_seg = tmp_list
    tmp_list = []
    for line in my_seg:
        if line == "" or line == "\n":
            continue
        else:
            tmp_list.append(line[:-1])
    my_seg = tmp_list

    len_stand = len(standard_seg)
    len_my = len(my_seg)
    length = 0
    # if len not equal, throw a exception
    if(len_my != len_stand):
        raise Exception("Length error", len_stand, len_my)
    else:
        length = len(standard_seg)
    
    for i in range(length):
        standard_words = standard_seg[i].split(" ")[1:]
        tmp_words = []
        for word in standard_words:
            if(word == " " or word == ""):
                continue
            fullword = word.strip().split("/")[0]
            if "[" in fullword:
                fullword = fullword[1:]
            tmp_words.append(fullword)
        standard_words = tmp_words
        my_words = my_seg[i].split("/ ")[1:]
        if my_words[len(my_words) - 1] == "":
            my_words = my_words[:-1]
        for word in my_words:
            if word in standard_words:
                word_cor += 1
        word_true += len(standard_words)
        word_pre += len(my_words)

    Precision = word_cor / word_pre
    Recall = word_cor / word_true
    F1 = 2 * Precision * Recall / (Precision + Recall)      
    ret = []
    ret.append("Precision: " + str(Precision*100) + "%")
    ret.append("Recall: " + str(Recall*100) + "%")
    ret.append("F1: " + str(F1*100) + "%")
    ret.append("correct: " + str(word_cor))
    ret.append("All: " + str(word_true))
    ret.append("Predict: " + str(word_pre))
    return ret
    
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

standard_path = "dataset/199801_seg.txt"
seg_LM = "outputs/seg_FMM_test.txt"
output_file = "outputs/score_FMM_test2.txt"   # including precision, recall, F1

def main():
    output_LM = analysis(standard_path, seg_LM)
    output_LM.insert(0, "FMM_test: ")
    writeList(output_file, output_LM)
    return

if __name__ == "__main__":
    main()