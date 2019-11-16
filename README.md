# HIT-NLP-Course-Lab1

## 文件说明

### 3.1

生成词典使用的是build_dic.py。 想要重新生成词典可以运行该文件。生成的词典文件存放在outputs文件夹中,文件名dic.txt。运行该文件同时将会生成3.5中使用的unigram词典 LMdic.txt 和bigram词典 bidic.txt

3.1中还对词典组成进行了实验，如要复现实验过程，则可以首先运行cut_dic.py将词典切分成训练集和验证集。然后使用build_train_dic.py从训练集中生成不同的词典，生成的词典在train文件夹中，文件名类似xxxtrainDic.txt。接下来使用FMM_train.py对所有的情况进行测试，测试结果在train文件夹中，文件名类似seg_xxx.txt。然后使用analysis_one.py来得到F1，正确率，召回率等结果。这里运行的时候需要进到analysis_one.py中手动修改seg文件的path和存放结果的score文件的path。最终的测试结果存放在train文件夹中，文件名类似score_xxx.txt

### 3.2

对文件进行正反向最大匹配分词请运行 FMM+BMM.py，这里面查找算法使用的是二分查找，因为顺序查找太慢，运行一次时间过长（大于10分钟），所以不提供顺序查找版本。二分查找运行约3分钟，请耐心等待，生成的结果是相同的。最后分词结果输出到outputs文件夹中，正向最大匹配分词结果文件名seg_FMM.txt，反向最大匹配分词结果文件名是seg_BMM.txt。分词输出采用'/ '分割，如果要获得每行分词后的结果可以直接使用split('/ ')，还要注意判断split后得到的列表最后一个是否为空。

### 3.3

结果输出在outputs文件夹中，文件名是score.txt

个人使用的分词评价函数是 analysis.py

### 3.4

速度优化代码为FMM_fast.py，这里选择对FMM优化。使用了二分查找和HashSet，二分查找代码在utils.py中，HashSet版本为HashSetL，在HashSet.py中(Line 156开始)。结果输出在outputs文件夹中，文件名是TimeCost.txt

### 3.5

一元文法 LM_one_gram.py

使用的词典是LMdic.txt，分词结果保存在outputs/seg_withLM1.txt，分词得分保存在outputs/score_LM1.txt

二元文法 LM_two_gram.py

使用的词典是LMdic.txt和bidic.txt，分词结果保存在outputs/seg_withLM2.txt，分词得分保存在outputs/score_LM2.txt

隐马尔可夫模型 HMM.py

使用的是199801_seg&pos进行训练，训练结果保存在outputs/save.pkl，分词结果保存在outputs/seg_HMM.txt，分词得分保存在outputs/score_HMM.txt

一元文法结合隐马尔可夫模型未登录词LM_onegram+OOV.py

使用的是199801_seg&pos进行训练，训练结果保存在outputs/save.pkl，使用的词典是LMdic.txt，分词结果保存在outputs/seg_withLM1OOV.txt，分词得分保存在outputs/score_LM1OOV.txt

性能冲刺 sprint.py

采用基于二阶隐马尔可夫模型改进的Character Based Generative Model，详见报告以及
论文Wang, Kun, Chengqing Zong, and Keh-Yih Su. "Which is More Suitable for Chinese Word Segmentation, the Generative Model or the Discriminative One?." PACLIC. 2009.

该模型结合了N-gram文法和HMM的方法，能够实现高召回的词典词和高召回的未登录词。

使用的是199801_seg&pos进行训练，会将输入的seg&pos还有sent从GBK编码转化为UTF-8编码。保存在outputs文件夹下199801_seg&pos_utf8.txt和199801_sent_utf8.txt。标注结果保存在outputs/BMESdata.txt，分词结果保存在outputs/seg_sprint.txt，分词得分保存在outputs/score_sprint.txt

如果要使用性能冲刺代码对别的文件进行分词，请修改以下路径(sprint.py Line 260开始)：

textpath -- 待分词的文件路径，GBK编码

text_utf8_path -- 将待分词的文件转成UTF-8编码存放路径

segpath -- 存放最终的分词结果，GBK编码，格式为199801_seg&pos

程序运行需要的时间很长，使用199801_seg&pos训练时长约2分钟，分标准文件199801_sent需要10分钟。

还请耐心等待，thanks!
