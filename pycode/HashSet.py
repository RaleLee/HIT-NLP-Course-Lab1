# version 1.0 - linear probing

class HashSet: 
    def __len__(self):
        return self.numItems
    
    # init
    def __init__(self,contents=[]):
        self.items = [None] * 10
        self.numItems = 0
 
        for item in contents:
            self.add(item)    
 
    def __hash(self, word):
        word_hash = 0
        for ch in word:
            byte_ch = ch.encode("gbk")
            if(len(byte_ch) < 2):
                ch_hash = (byte_ch[0] - 0xB0) * 94
            else:
                ch_hash = (byte_ch[0] - 0xB0) * 94 + (byte_ch[1] - 0xA1)
            word_hash = word_hash * 114 + ch_hash
        return int((word_hash & 0x7FFFFFFF))

    def __add(self, item, items):
        idx = self.__hash(item) % len(items)
        loc = -1
 
        while items[idx] != None:
            if items[idx] == item:
                # item already in set
                return False
 
            if loc < 0 and type(items[idx]) == HashSet.__Placeholder:
                loc = idx
 
            idx = (idx + 1) % len(items)
 
        if loc < 0:
            loc = idx
 
        items[loc] = item
        return True
    
    def __rehash(self, oldList, newList):
        for x in oldList:
            if x != None and type(x) != self.__Placeholder:
                self.__add(x,newList)
 
        return newList
 
    def add(self, item):
        if self.__add(item,self.items):
            self.numItems += 1
            load = self.numItems / len(self.items)
            if load >= 0.75:
                self.items = self.__rehash(self.items,[None]*2*len(self.items))
 
    class __Placeholder:
        def __init__(self):
            pass
 
        def __eq__(self,other):
            return False

    # use find method can call this method to find a item in set
    def __contains__(self, item):
        idx = self.__hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return True
 
            idx = (idx + 1) % len(self.items)
 
        return False

# version 2.0 - zipper method with list, wrong version!!!
class HashSetZ:
    class __Node:
        load = False
        words = []

        # init of Node
        def __init__(self, word):
            self.words.append(word)
            if(word != ""):
                self.load = True

        def empty(self):
            return self.load

        # add word to Node
        def add(self, word):
            self.words.append(word)
        
        # find a word in zipper list
        def __contains__(self, word):
            if(self.words.count(word) > 0):
                return True
            return False

    Hashset = []
    length = 0
    # hash_function = my_hash
    __Place = __Node("")
    # ch_encoder = ch_gbk_encode

    def __init__(self, length):
        self.length = length
        for i in range(self.length):
            self.Hashset.append(self.__Place)

    def __hash(self, word):
        word_hash = 0
        for ch in word:
            byte_ch = ch.encode("gbk")
            if(len(byte_ch) < 2):
                ch_hash = (byte_ch[0] - 0xB0) * 94
            else:
                ch_hash = (byte_ch[0] - 0xB0) * 94 + (byte_ch[1] - 0xA1)
            word_hash = word_hash * 114 + ch_hash
        return int((word_hash & 0x7FFFFFFF))

    # add word into hashset
    def add(self, word):
        val = self.__hash(word) % self.length
        newNode = self.__Node(word)
        if self.Hashset[val].empty:
            self.Hashset[val] = newNode
        else:
            self.Hashset[val].add(word)
        return True

    # use find method can call this method to find a item in set
    def __contains__(self, word):
        val = self.__hash(word) % self.length
        if self.Hashset[val].empty():
            return False
        else:
            return word in self.Hashset[val]

class linkListNode:
    word = None
    next = None
    
    # init
    def __init__(self, word):
        self.word = word

    # add
    def add(self, next):
        self.next = next 


# version 3.0 - zipper method with linkedList
class HashSetL:
    Hashset = []
    length = 0
    __Place = linkListNode("")

    def __init__(self, length):
        self.length = length
        for i in range(self.length):
            self.Hashset.append(self.__Place)

    def __hash(self, word):
        word_hash = 0
        for ch in word:
            byte_ch = ch.encode("gbk")
            if(len(byte_ch) < 2):
                ch_hash = (byte_ch[0] - 0xB0) * 94
            else:
                ch_hash = (byte_ch[0] - 0xB0) * 94 + (byte_ch[1] - 0xA1)
            word_hash = word_hash * 114 + ch_hash
        return int((word_hash & 0x7FFFFFFF))
    
    def add(self, word):
        val = hash(word) % self.length
        newNode = linkListNode(word)
        if self.Hashset[val] == self.__Place:
            self.Hashset[val] = newNode
        else:
            curNode = self.Hashset[val]
            while curNode.next is not None:
                if curNode.word == word:
                    return False
                curNode = curNode.next
            curNode.add(newNode)
            return True

    def __contains__(self, word):
        val = hash(word) % self.length
        if self.Hashset[val] == self.__Place:
            return False
        else:
            curNode = self.Hashset[val]
            while curNode.word != word:
                curNode = curNode.next
                if(curNode == None):
                    return False
            return True