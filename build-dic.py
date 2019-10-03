# coding=utf-8
def readFile(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    f.close()
    return lines

def writeFile(path, dic):
    with open(path, 'w') as f:
        for word in dic:
            if(len(word) > 1):
                f.write(word[0] + " " + word[1] + " " +str(dic[word])+"\n")
    f.close()
    return 

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
            if fullword in words:
                dic[fullword] += 1
            else:
                words.add(fullword)
                dic[fullword] = 1
    sorted(dic.items(), key=lambda e: e[0][0], reverse = True)
    return dic

def main(segpath, dicpath):
    
    lines = readFile(segpath)
    dic = buildDic(lines)
    writeFile(dicpath, dic)


segpath = '199801_seg.txt'
dicpath = "199801_dic.txt"

if __name__ == "__main__":
    main(segpath, dicpath)
