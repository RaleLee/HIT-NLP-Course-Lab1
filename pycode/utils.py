# coding=utf-8
def readFile(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    f.close()
    return lines

# use to write dic in part 3.1
def writeDic(path, dic):
    with open(path, 'w') as f:
        for word in dic:
            if(len(word[0]) > 1):
                f.write(word[0][0] + " " + word[0][1] + " " +str(word[1])+"\n")
    f.close()
    return 

# use to write seg result in part 3.2
def writeSeg(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            newline = ""
            for word in line:
                newline += word + "/" + " "
            f.write(newline)
            #print(newline)
            f.write("\n")
    f.close()
    return

# use to write analysis result in part 3.3
def writeList(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
            f.write("\n")
    f.close()
    return 

# use to write training & test dic in part 3.1
def writeTrainList(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            f.write(line)
    f.close()
    return

def binary_search(slis, key):
    left = 0
    right = len(slis) - 1
    while left < right:
        mid = int((left + right) / 2)
        if(key < slis[mid]):
            right = mid - 1
        elif(key > slis[mid]):
            left = mid + 1
        else:
            return True
    return False