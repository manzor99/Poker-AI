import random
import math
import sys
import numpy as np
from scipy import stats


# Random function: choose an element randomly based on your probability vector
def rand(pk):
    if sum(pk) == 0:
        return 5
    pk = [pk[i]/sum(pk) for i in range(len(pk))]
    x = random.uniform(0, 1)
    result = -1
    while x > 0:
        result += 1
        x = x - pk[result]
    return result


class Solver:
    def __init__(self):
        # List of part_of_speech
        self.part_of_speech = ['adj', 'adv', 'adp', 'conj', 'det', 'noun', 'num', 'pron', 'prt', 'verb', 'x', '.']
        # Length of part_of_speech
        self.pos_len = len(self.part_of_speech)
        # Initial probability
        self.init_num = {self.part_of_speech[i]: 0 for i in range(self.pos_len)}
        self.init_prob = [0 for i in range(self.pos_len)]
        # Transition probability
        # Example: trans_prob[s2][s1] = prob(s1|s2)
        self.trans_num = [[0 for i in range(self.pos_len)] for i in range(self.pos_len)]
        self.trans_prob = [[0 for i in range(self.pos_len)] for i in range(self.pos_len)]
        # Emission probability
        self.emi_num = [{} for i in range(self.pos_len)]
        self.emi_prob = [{} for i in range(self.pos_len)]
        # State|Word
        self.sw_num = {}
        self.sw_prob = {}

    # Calculate the log of the posterior probability of a given sentence with a given part-of-speech labeling
    def posterior(self, sentence, label):
        result = 0
        for i in range(len(sentence)):
            try:
                result += math.log(self.sw_prob[sentence[i]][self.part_of_speech.index(label[i])])
            except Exception:
                pass
        return result

    # Train data to compute the probability
    def train(self, data):
        for (words, pos) in data:
            for i in range(len(pos) - 1):
                self.init_num[pos[i]] += 1
                self.trans_num[self.part_of_speech.index(pos[i])][self.part_of_speech.index(pos[i + 1])] += 1
                try:
                    self.emi_num[self.part_of_speech.index(pos[i])][words[i]] += 1
                except KeyError:
                    self.emi_num[self.part_of_speech.index(pos[i])][words[i]] = 1
            # Last word in the sentence
            self.init_num[pos[-1]] += 1
            try:
                self.emi_num[self.part_of_speech.index(pos[-1])][words[-1]] += 1
            except KeyError:
                self.emi_num[self.part_of_speech.index(pos[-1])][words[-1]] = 1

        # Compute initial probability
        sum_pos = sum(self.init_num.values())
        for i in range(self.pos_len):
            self.init_prob[i] = self.init_num[self.part_of_speech[i]] * 1.0 / sum_pos
        # Compute transition probability
        for i in range(self.pos_len):
            sum_trans = sum(self.trans_num[i])
            for j in range(self.pos_len):
                self.trans_prob[i][j] = self.trans_num[i][j] * 1.0 / sum_trans
        # Compute emission probability
        for i in range(self.pos_len):
            sum_emi = sum(self.emi_num[i].values())
            for j in self.emi_num[i].keys():
                self.emi_prob[i][j] = self.emi_num[i][j] * 1.0 / sum_emi

        # Compute State|Word
        for (words, pos) in data:
            for i in range(len(words)):
                try:
                    self.sw_num[words[i]][self.part_of_speech.index(pos[i])] += 1
                except KeyError:
                    self.sw_num[words[i]] = [0 for ii in range(self.pos_len)]
                    self.sw_num[words[i]][self.part_of_speech.index(pos[i])] += 1
        for i in self.sw_num.keys():
            sum_emi = sum(self.sw_num[i])
            self.sw_prob[i] = [0 for ii in range(self.pos_len)]
            for j in range(self.pos_len):
                self.sw_prob[i][j] = self.sw_num[i][j] * 1.0 / sum_emi

    # Naive inference
    def naive(self, sentence):
        result = []
        for w in sentence:
            max_prob = -1
            # Set noun as default because of the frequency of appearance
            r = 'noun'
            for i in range(self.pos_len):
                try:
                    # Record the part of speech if it has a larger probability
                    if self.sw_prob[w][i] > max_prob:
                        max_prob = self.sw_prob[w][i]
                        r = self.part_of_speech[i]
                except KeyError:
                    pass
            result.append(r)
        return [[result], []]

    # Viterbi inference
    def viterbi(self, sentence):
        path = [str(i) for i in range(self.pos_len)]
        path_prob = [0] * self.pos_len
        # First word in the sentence
        for i in range(self.pos_len):
            try:
                path_prob[i] = math.log(self.emi_prob[i][sentence[0]]) + math.log(self.init_prob[i])
            except KeyError:
                path_prob[i] = -1000000000.00 + math.log(self.init_prob[i])
                if i == 5:
                    path_prob[i] = -1000000.00 + math.log(self.init_prob[i])
        # Inference continue
        for i in range(1, len(sentence)):
            new_path = [''] * self.pos_len
            new_prob = [0] * self.pos_len
            # For each state in step n
            for j in range(self.pos_len):
                best = -sys.maxint
                state = -1
                # For each state in step n-1
                for jj in range(self.pos_len):
                    try:
                        p = math.log(self.trans_prob[jj][j]) + math.log(self.emi_prob[j][sentence[i]]) + path_prob[jj]
                    except ValueError:
                        p = -sys.maxint
                    except KeyError:
                        p = -1000000000.00 + math.log(self.trans_prob[jj][j]) + path_prob[jj]
                        if j == 5:
                            p = -1000000.00 + math.log(self.trans_prob[jj][j]) + path_prob[jj]
                    if p > best:
                        best = p
                        state = jj
                new_path[j] = path[state] + ',' + str(j)
                new_prob[j] = best
            path = new_path[:]
            path_prob = new_prob[:]

        r = path[path_prob.index(max(path_prob))].split(',')
        result = []
        for index in r:
            result.append(self.part_of_speech[int(index)])
        return [[result], []]

    def solve(self, algo, sentence):
        if algo == "Naive":
            return self.naive(sentence)
        elif algo == "MAP":
            return self.viterbi(sentence)
        else:
            print "Unknown algo!"
