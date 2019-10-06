class HashSet: 
    def __str__(self):
        lst = []
        for x in self:
            lst.append(x)
 
        lst = sorted(lst)
 
        return str(lst)
 
    def __len__(self):
        return self.numItems
    
    def __iter__(self):
        for i in range(len(self.items)):
            if self.items[i] != None and type(self.items[i]) != HashSet.__Placeholder:
                yield self.items[i]
    
 
    #初始化
    def __init__(self,contents=[]):
        self.items = [None] * 10
        self.numItems = 0
 
        for item in contents:
            self.add(item)    
 
    def __add(self, item,items):
        idx = hash(item) % len(items)
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
 
    def __contains__(self, item):
        idx = hash(item) % len(self.items)
        while self.items[idx] != None:
            if self.items[idx] == item:
                return True
 
            idx = (idx + 1) % len(self.items)
 
        return False