def readFile(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    f.close()
    return lines

def writeDic(path, dic):
    with open(path, 'w') as f:
        for word in dic:
            if(len(word[0]) > 1):
                f.write(word[0][0] + " " + word[0][1] + " " +str(word[1])+"\n")
    f.close()
    return 

def writeSeg(path, lines):
    with open(path, 'w') as f:
        for line in lines:
            newline = ""
            for word in line:
                newline += word + "/" + " "
            f.write(newline)
            #print(newline)
            f.write("\n")
    f.close
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