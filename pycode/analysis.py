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
        my_words = my_seg[i].split("/ ")
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
    return ret


standard_path = "dataset/199801_seg.txt"
seg_FMM = "outputs/seg_FMM.txt"
seg_BMM = "outputs/seg_BMM.txt"
output_file = "outputs/score.txt"   # including precision, recall, F1

def main():
    output_FMM = analysis(standard_path, seg_FMM)
    output_BMM = analysis(standard_path, seg_BMM)
    ret = []
    ret.append("FMM: ")
    ret.extend(output_FMM)
    ret.append("BMM: ")
    ret.extend(output_BMM)
    writeList(output_file, ret)
    return

if __name__ == "__main__":
    main()