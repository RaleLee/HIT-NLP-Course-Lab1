# coding=utf-8
# Take jieba and pdf as references
from utils import readFile, writeList
import time

class HMM():
    # init
    def __init__(self):
        # state list, B means begin of a word, M means middle of a word
        # E means end of a word, S means a single word
        self.state = ["B", "M", "E", "S"]
        self.start_p = {}   # state start probability
        self.trans_p = {}   # state transition probability
        self.emit_p = {}    # emit probability

        self.save_model_path = "outputs/model.pkl"
        self.train_vaild = False
    
    # make label for the training data
    @staticmethod
    def __make_label(word):
        seg_with_label = []
        if len(word) == 1:
            seg_with_label = ["S"]
        else:
            seg_with_label += ["B"] + ["M"]*(len(word) - 2) + ["E"]
        return seg_with_label

    def train(self, train_data, save_model_path = None):
        if save_model_path == None:
            save_model_path = self.save_model_path
            print(save_model_path)
        
        # load training data
        lines = readFile(train_data)

        # count for the start state
        state_dic = {}

        # init parameters
        for state in self.state:
            self.start_p[state] = 0.0
            self.trans_p[state] = {s : 0.0 for s in self.state}
            self.emit_p[state] = {}
            state_dic[state] = 0
        line_nb = 0

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            line_nb += 1
            # get words and don't need the first time
            linewords = line.split(" ")[1:]
            word_list = []
            words_list = []
            # get words from each lines, split by /, don't need POS
            for word in linewords:
                if(word == " "):
                    continue
                fullword = word.strip().split("/")[0]
                if len(fullword) == 0:
                    continue
                if fullword[0] == "[":
                    fullword = fullword[1:]
                words_list.append(fullword)
                for w in fullword:
                    word_list.append(w)
            
            line_state = []
            for word in words_list:
                line_state.extend(self.__make_label(word))

            # make sure no mistake in adding state
            assert len(line_state) == len(word_list), str(line_state) + str(word_list)

            for i, v in enumerate(line_state):
                state_dic[v] += 1

                if i == 0:
                    self.start_p[v] += 1
                else:
                    self.trans_p[line_state[i-1]][v] += 1
                    self.emit_p[line_state[i]][word_list[i]] = self.emit_p[line_state[i]].get(word_list[i], 0) + 1.0

        self.start_p = {k : v * 1.0 / line_nb for k, v in self.start_p.items()}
        self.trans_p = {k : {k1 : v1 / state_dic[k1] for k1, v1 in v0.items()} for k, v0 in self.trans_p.items()}
        self.emit_p = {k : {k1 : (v1 + 1) / state_dic.get(k1, 1.0) for k1, v1 in v0.items()} for k, v0 in self.emit_p.items()}

        with open(save_model_path, "wb") as f:
            import pickle
            pickle.dump(self.start_p, f)
            pickle.dump(self.trans_p, f)
            pickle.dump(self.emit_p, f)
        f.close()
        self.train_vaild = True
        print("Done. Training complete, model save at ", save_model_path)

    # load model
    def load(self, model_path):
        import pickle
        with open(model_path, "rb") as f:
            self.start_p = pickle.load(f)
            self.trans_p = pickle.load(f)
            self.emit_p = pickle.load(f)
        f.close()
        self.train_vaild = True
        print("Done. Finish load training data!")

    # viterbi algorithm to calculate the best path
    def __viterbi(self, text, states, start_p, trans_p, emit_p):
        V = [{}]
        path = {}
        for state in states:
            V[0][state] = start_p[state] * emit_p[state].get(text[0], 1.0)
            path[state] = [state]

        for t in range(1, len(text)):
            V.append({})
            new_path = {}

            for y in states:
                emitp = emit_p[y].get(text[t], 1.0)
                (prob, state) = max([(V[t-1][y0] * trans_p[y0].get(y, 0) * emitp, y0) for y0 in states if V[t-1][y0] > 0])
                V[t][y] = prob
                new_path[y] = path[state] + [y]
            path = new_path

        if emit_p["M"].get(text[-1], 0) > emit_p["S"].get(text[-1], 0):
            (prob, state) = max([(V[len(text)-1][y], y) for y in ("E", "M")])
        else:
            (prob, state) = max([(V[len(text)-1][y], y) for y in states])

        return (prob, path[state])

    # to seg the sentence
    def seg(self, text):
        if not self.train_vaild:
            print("Error! Not trained!")
            return

        _, pos_list = self.__viterbi(text, self.state, self.start_p, self.trans_p, self.emit_p)
        begin, next = 0, 0
        
        for i, char in enumerate(text):
            pos = pos_list[i]
            if pos == "B":
                begin = i
            elif pos == "E":
                yield text[begin : i + 1]
                next = i + 1
            elif pos == "S":
                yield char
                next = i + 1
        
        if next < len(text):
            yield text[next : ]            

# to return all the seg result in a list
def seg_HMM(model, test_set):
    seg = []
    lines = readFile(test_set)
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            tmp_seg = "/ ".join(model.seg(line))
            tmp_seg += "/ "
            seg.append(tmp_seg)
    return seg

# need to cut
train_set = "dataset/199801_seg.txt"
test_set = "dataset/199801_sent.txt"
save_model_path = "outputs/save.pkl"
fine_model_path = "dataset/hmm_model.pkl"
seg_path = "outputs/seg_HMM.txt"
fine_seg_path = "outputs/seg_fine_HMM.txt"

def main():
    # count time
    startTime = time.time()
    model = HMM()
    # model.train(train_set, save_model_path)
    # model.load(save_model_path)
    model.load(fine_model_path)
    #seg = seg_HMM(model, test_set)
    endTime = time.time()
    print((endTime - startTime) * 1000)
    # writeList(seg_path, seg)
    #writeList(fine_seg_path, seg)
    text = "新华社报道，近日出现重大问题。"
    print('/'.join(model.seg(text)))

if __name__ == "__main__":
    main()
