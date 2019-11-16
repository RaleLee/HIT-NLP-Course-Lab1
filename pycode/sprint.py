# -*- coding: utf-8 -*-
# take snownlp as a reference
#  
import sys
import gzip
import marshal
import codecs
import datetime
from math import log



class CharacterBasedGenerativeModel(object):

    def __init__(self):
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.status = ('b', 'm', 'e', 's')
        self.uni = BaseProb()
        self.bi = BaseProb()
        self.tri = BaseProb()

    def save(self, fname, iszip=True):
        d = {}
        for k, v in self.__dict__.items():
            if hasattr(v, '__dict__'):
                d[k] = v.__dict__
            else:
                d[k] = v
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            marshal.dump(d, open(fname, 'wb'))
        else:
            f = gzip.open(fname, 'wb')
            f.write(marshal.dumps(d))
            f.close()

    def load(self, fname, iszip=True):
        if sys.version_info[0] == 3:
            fname = fname + '.3'
        if not iszip:
            d = marshal.load(open(fname, 'rb'))
        else:
            try:
                f = gzip.open(fname, 'rb')
                d = marshal.loads(f.read())
            except IOError:
                f = open(fname, 'rb')
                d = marshal.loads(f.read())
            f.close()
        for k, v in d.items():
            if hasattr(self.__dict__[k], '__dict__'):
                self.__dict__[k].__dict__ = v
            else:
                self.__dict__[k] = v

    def div(self, v1, v2):
        if v2 == 0:
            return 0
        return float(v1)/v2

    def train(self, data):
        for sentence in data:
            now = [('', 'BOS'), ('', 'BOS')]
            self.bi.add((('', 'BOS'), ('', 'BOS')), 1)
            self.uni.add(('', 'BOS'), 2)
            for word, tag in sentence:
                now.append((word, tag))
                self.uni.add((word, tag), 1)
                self.bi.add(tuple(now[1:]), 1)
                self.tri.add(tuple(now), 1)
                now.pop(0)
        tl1 = 0.0
        tl2 = 0.0
        tl3 = 0.0
        samples = sorted(self.tri.samples(), key=lambda x: self.tri.get(x)[1])
        for now in samples:
            c3 = self.div(self.tri.get(now)[1]-1, self.bi.get(now[:2])[1]-1)
            c2 = self.div(self.bi.get(now[1:])[1]-1, self.uni.get(now[1])[1]-1)
            c1 = self.div(self.uni.get(now[2])[1]-1, self.uni.getsum()-1)
            if c3 >= c1 and c3 >= c2:
                tl3 += self.tri.get(now)[1]
            elif c2 >= c1 and c2 >= c3:
                tl2 += self.tri.get(now)[1]
            elif c1 >= c2 and c1 >= c3:
                tl1 += self.tri.get(now)[1]
        self.l1 = self.div(tl1, tl1+tl2+tl3)
        self.l2 = self.div(tl2, tl1+tl2+tl3)
        self.l3 = self.div(tl3, tl1+tl2+tl3)

    def log_prob(self, s1, s2, s3):
        uni = self.l1*self.uni.freq(s3)
        bi = self.div(self.l2*self.bi.get((s2, s3))[1], self.uni.get(s2)[1])
        tri = self.div(self.l3*self.tri.get((s1, s2, s3))[1],
                       self.bi.get((s1, s2))[1])
        if uni+bi+tri == 0:
            return float('-inf')
        return log(uni+bi+tri)

    def tag(self, data):
        now = [((('', 'BOS'), ('', 'BOS')), 0.0, [])]
        for w in data:
            stage = {}
            not_found = True
            for s in self.status:
                if self.uni.freq((w, s)) != 0:
                    not_found = False
                    break
            if not_found:
                for s in self.status:
                    for pre in now:
                        stage[(pre[0][1], (w, s))] = (pre[1], pre[2]+[s])
                now = list(map(lambda x: (x[0], x[1][0], x[1][1]),
                               stage.items()))
                continue
            for s in self.status:
                for pre in now:
                    p = pre[1]+self.log_prob(pre[0][0], pre[0][1], (w, s))
                    if (not (pre[0][1],
                             (w, s)) in stage) or p > stage[(pre[0][1],
                                                            (w, s))][0]:
                        stage[(pre[0][1], (w, s))] = (p, pre[2]+[s])
            now = list(map(lambda x: (x[0], x[1][0], x[1][1]), stage.items()))
        return zip(data, max(now, key=lambda x: x[1])[2])

class BaseProb(object):

    def __init__(self):
        self.d = {}
        self.total = 0.0
        self.none = 0

    def exists(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def get(self, key):
        if not self.exists(key):
            return False, self.none
        return True, self.d[key]

    def freq(self, key):
        return float(self.get(key)[1])/self.total

    def samples(self):
        return self.d.keys()

    def add(self, key, value):
        if not self.exists(key):
            self.d[key] = 0
        self.d[key] += value
        self.total += value

class Seg(object):

    def __init__(self):
        self.segger = CharacterBasedGenerativeModel()

    def save(self, fname, iszip=True):
        self.segger.save(fname, iszip)

    def load(self, fname, iszip=True):
        self.segger.load(fname, iszip)

    def train(self, fname):
        fr = codecs.open(fname, 'r', 'utf-8')
        data = []
        for i in fr:
            line = i.strip()
            if not line:
                continue
            tmp = map(lambda x: x.split('/'), line.split())
            data.append(tmp)
        fr.close()
        self.segger.train(data)

    def seg(self, sentence):
        ret = self.segger.tag(sentence)
        tmp = ''
        for i in ret:
            if i[1] == 'e':
                yield tmp+i[0]
                tmp = ''
            elif i[1] == 'b' or i[1] == 's':
                if tmp:
                    yield tmp
                tmp = i[0]
            else:
                tmp += i[0]
        if tmp:
            yield tmp


def generateBMESData(lines, save_path):
    bmeslist = []
    size = len(lines)
    for i in range(size):
        wordlist = []
        bmes = []
        if len(lines[i]) == 0:
            continue
        linewords = lines[i].strip().split()[1:]
        for word in linewords:
            if(word == " "):
                continue
            fullword = tuple(word.strip().split("/"))
            if(len(fullword[0]) == 0 or len(fullword[1]) == 0):
                continue
            copy = fullword
            if fullword[0][0] == "[" and len(fullword[0]) > 1:
                fullword = (fullword[0][1:], copy[1])
            copy = fullword[0]
            wordlist.append(copy)
        if len(wordlist) == 0:
            continue
        for word in wordlist:
            chs = len(word)
            if chs == 1:
                bmes.append(word + "/s")
            elif chs > 1:
                for j in range(chs):
                    if j == 0:
                        bmes.append(word[j] + "/b")
                    elif j == chs-1:
                        bmes.append(word[j] + "/e")
                    else:
                        bmes.append(word[j] + "/m")
            else:
                assert False, "Something wrong!"
        str_bmes = bmes[0]
        size_bmes = len(bmes)
        for j in range(1, size_bmes):
            str_bmes += " " + bmes[j]
        bmeslist.append(str_bmes)
    f = codecs.open(save_path, 'w', 'utf-8')
    for st_bmes in bmeslist:
        f.write(st_bmes + "\n")
    f.close()
    return


standard_path = "dataset/199801_seg&pos.txt"
standard_utf8_path = "outputs/199801_seg&pos_utf8.txt"
save_path = "outputs/BMESdata.txt"

'''
上面的路径请不要修改！
请修改以下路径
textpath -- 待分词的文件路径，GBK编码
text_utf8_path -- 将待分词的文件转成UTF-8编码存放路径
segpath -- 存放最终的分词结果， GBK编码
程序运行需要的时间很长，分标准文件199801_sent需要10分钟
还请耐心等待，thanks!
'''

textpath = "dataset/199801_sent.txt"
text_utf8_path = "outputs/199801_sent_utf8.txt"
segpath = "outputs/seg_sprint.txt"

if __name__ == '__main__':
    print("Start to load BMES data.")
    f = codecs.open(standard_path, 'r', 'gbk')    
    context = f.read()
    f.close()
    utf = codecs.open(standard_utf8_path, 'w', 'utf-8')
    utf.write(context)
    utf.close()
    st = codecs.open(standard_utf8_path, 'r', 'utf-8', 'ignore')
    lines = st.readlines()
    st.close()
    generateBMESData(lines, save_path)
    print("Finish generate BMES data.") 
    seg = Seg()
    print("Start to train, please wait a moment.")
    seg.train(save_path)
    print("Finish train! Start to load utf-8 199801_sent...")
    f = codecs.open(textpath, 'r', 'gbk')    
    context = f.read()
    f.close()
    utf = codecs.open(text_utf8_path, 'w', 'utf-8')
    utf.write(context)
    utf.close()
    st = codecs.open(text_utf8_path, 'r', 'utf-8', 'ignore')
    lines = st.readlines()
    st.close()

    
    textsize = len(lines)
    print(datetime.datetime.now())
    print("Start to seg...")
    gbkf = codecs.open(segpath, 'w', 'gbk')
    for i in range(textsize):
        sen = lines[i].strip()
        if len(sen) == 0:
            gbkf.write("\n")
            continue
        linebegin = sen[:19]
        sen = sen[19:]
        sen_seg = linebegin + "/ " + "/ ".join(seg.seg(sen)) + "/ " + "\n"
        gbkf.write(sen_seg)
        if(i % 1000 == 0):
            print(datetime.datetime.now())
    gbkf.close()

    print('/ '.join(seg.seg('主要是用来放置一些简单快速的中文分词和词性标注的程序')))