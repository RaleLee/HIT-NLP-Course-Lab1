# HIT-NLP-Course-Lab1

## 文件说明

### 3.1

生成词典使用的是build_dic.py。 想要重新生成词典可以运行该文件。生成的词典文件存放在outputs文件夹中,文件名dic.txt。运行该文件同时将会生成3.5中使用的onegram词典和bigram词典

3.1中还对词典组成进行了实验，如要复现实验过程，则可以首先运行cut_dic.py将词典切分成训练集和验证集。然后使用build_train_dic.py从训练集中生成不同的词典，生成的词典在train文件夹中，文件名类似xxxtrainDic.txt。接下来使用FMM_train.py对所有的情况进行测试，测试结果在train文件夹中，文件名类似seg_xxx.txt。然后使用analysis_one.py来得到F1，正确率，召回率等结果。这里运行的时候需要进到analysis_one.py中手动修改seg文件的path和存放结果的score文件的path。最终的测试结果存放在train文件夹中，文件名类似score_xxx.txt

### 3.2

对文件进行正反向最大匹配分词请运行FMM+BMM.py，这里面查找算法使用的是二分查找，因为顺序查找太慢，运行一次时间过长，建议不要轻易直接运行，需要等待很久，生成的结果是相同的。最后分词结果输出到outputs文件夹中，正向最大匹配分词结果文件名seg_FMM.txt，反向最大匹配分词结果文件名是seg_BMM.txt。分词输出采用
'/ '分割，如果要获得每行分词后的结果可以直接使用split('/ ')，还要注意判断split后得到的列表最后一个是否为空。

### 3.3

结果输出在outputs文件夹中，文件名是score.txt

### 3.4

速度优化代码为FMM_fast.py，这里选择对FMM优化。使用了二分查找和HashSet，二分查找代码在utils.py中，HashSet版本为HashSetL，在HashSet.py中。结果输出在outputs文件夹中，文件名是TimeCost.txt

### 3.5

一元文法 LM_one_gram.py

二元文法 LM_two_gram.py 

隐马尔可夫模型 HMM.py 

一元文法结合隐马尔可夫模型未登录词LM_onegram+OOV.py 

二元文法结合隐马尔可夫模型未登录词LM_twogram+OOV.py
