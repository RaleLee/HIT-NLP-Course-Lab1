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

def binary_search(slis, key):
    left = 0
    right = len(slis) - 1
    while left < right:
        mid = int((left + right) / 2)
        if(key < slis[mid]):
            right = mid - 1
        elif(ley > slis[mid]):
            left = mid + 1
        else:
            return mid
    return False