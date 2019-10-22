# coding=utf-8
import sys

class Node:
    def __init__(self, word):
        self.word = word
        self.endOfWord = False
        self.childs = []

class DoubleArrayTrie:
    def __init__(self):
        self.root = Node('\0')
    
    def __getUnicode(self, word):
        return ord(word)
    
    def add(self, words):
        node = self.root
        for word in words:
            insertIndex = 0
            length = len(node.childs)
            for id in range(length):
                if(self.__getUnicode(word) == self.__getUnicode(node.childs[id].word)):
                    insertIndex = -1
                    tmpnode = node.childs[id]
                    node = tmpnode
                    break
                elif(self.__getUnicode(word) < self.__getUnicode(node.childs[id].word)):
                    insertIndex = id
                    break
                elif(id == length - 1):
                    insertIndex = length
                    break

            if(insertIndex == -1):
                continue

            tmpnode = Node(word)
            if(insertIndex == length):
                node.childs.append(tmpnode)
            else:
                node.childs.insert(0, tmpnode)
            node = tmpnode
        
        node.endOfWord = True
        return True 

    def __contains__(self, words):
        node = self.root
        for word in words:
            for child in node.childs:
                if(child.word == word):
                    node = child
                    break
                elif(child == node.childs[len(node.childs) - 1]):
                    return False
        if(node.endOfWord == True):
            return True
        else:
            return False
