# -*- Encoding: utf-8 -*-
from util import print_cutting_line
import util

import matplotlib.pyplot as plt

def read_data(file_name, has_reading=False):
    data = dict()
    with open(file_name) as f:
        for line in f.readlines():
            year, cloze, read_a, read_b = line.strip().split(' ')
            item = list(cloze)
            if has_reading:
                item.extend(read_a)
                item.extend(read_b)
            data[year] = item
    return data

def sort_dict(orig):
    return sorted(orig.iteritems(), key=lambda item:item[0])

def prob(item):
    res = dict()

    def add(ch):
        if ch in res:
            res[ch] += 1
        else:
            res[ch] = 1

    for ch in item:
        add(ch)
    return [res.get('A', 0), res.get('B', 0), res.get('C', 0), res.get('D', 0)]

def calc_freq(data):
    """ 历年各题目各选项出现次数统计 """
    count = dict()

    def add(ch, i):
        def _wrap():
            if ch not in count:
                count[ch] = [0] * len(answer)
            count[ch][i] += 1
        _wrap()

    for answer in data.values():
        for i in range(len(answer)):
            add(answer[i], i)
    return count

@print_cutting_line
def outline(datafile):
    data = read_data(datafile, has_reading=True)

    print util.cutting_line('历年答案 ABCD 比例分布')
    for year, answer in sort_dict(data):
        print year, 'total: ', prob(answer[:40]),\
            '\tcloze: ', prob(answer[:20]),\
            '\tread_a: ', prob(answer[20:40])

    print util.cutting_line('历年各题目各选项出现次数统计')
    count = calc_freq(data)
    for answer, fq in sort_dict(count):
        print answer, fq


class Cloze:

    def __init__(self, datafile):
        self.probs = 20  # len(data.values()[0])
        self.std_answer = read_data(datafile)
        self.most_freq()

    def predict(self, my_answer, fig=None):
        scores = [util.calc_score(my_answer, one_answer) for year, one_answer in sort_dict(self.std_answer)]

        if fig:
            plt.sca(fig)
        plt.plot(scores)
        if not fig:
            plt.show()

    def most_freq(self):
        count = calc_freq(self.std_answer)
        self.trend_freq = [0] * self.probs
        self.trend_answer_head = ['Z'] * self.probs
        self.trend_answer_tail = ['Z'] * self.probs
        for answer, fq in sort_dict(count):
            for i in range(self.probs):
                if fq[i] > self.trend_freq[i]:
                    self.trend_freq[i] = fq[i]
                    self.trend_answer_head[i] = answer
                    self.trend_answer_tail[i] = answer
                if fq[i] == self.trend_freq[i]:
                    self.trend_answer_tail[i] = answer

@print_cutting_line
def predict_by_most_freq(p):

    answer = [(i, p.trend_answer_head[i])
            for i in range(p.probs)
            if p.trend_answer_head[i] == p.trend_answer_tail[i]]

    plt.figure(1)
    score_plot = plt.subplot(221)
    same_trend_plot = plt.subplot(222)
    tail_plot = plt.subplot(223)
    head_plot = plt.subplot(224)

    p.predict(answer, score_plot)
    plt.sca(same_trend_plot)
    x = [i for i, ch in answer]
    y = [util.ch2int(ch) for i, ch in answer]
    plt.plot(x, y, 'r-*')
    plt.sca(tail_plot)
    plt.plot([util.ch2int(i)  for i in p.trend_answer_tail[:40]], 'b*-')
    plt.sca(head_plot)
    plt.plot([util.ch2int(i)  for i in p.trend_answer_head[:40]], 'r*-')
    plt.savefig('figures/predict_by_most_freq.png', dpi=96)
    # plt.show()  # for debug


def run():
    filename = 'data/data.txt'
    outline(filename)

    p = Cloze(filename)

    predict_by_most_freq(p)


if __name__ == "__main__":
    run()

