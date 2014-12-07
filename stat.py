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

    def predict(self, my_answer):
        scores = [util.calc_score(my_answer, one_answer) for year, one_answer in sort_dict(self.std_answer)]

        plt.plot(scores)
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
def most_freq_trend(data):
    count = calc_freq(data)
    probs = len(data.values()[0])
    trend_freq = [0] * probs
    trend_answer_head = ['Z'] * probs
    trend_answer_tail = ['Z'] * probs
    for answer, fq in sort_dict(count):
        for i in range(probs):
            if fq[i] > trend_freq[i]:
                trend_freq[i] = fq[i]
                trend_answer_head[i] = answer
                trend_answer_tail[i] = answer
            if fq[i] == trend_freq[i]:
                trend_answer_tail[i] = answer
    print ', '.join(trend_answer_head)
    print ', '.join(trend_answer_tail)
    print trend_freq

    print ', '.join(['%2d' % (i+1) for i in range(probs) if trend_answer_head[i] == trend_answer_tail[i]])
    print ', '.join(['%2d' % trend_freq[i] for i in range(probs) if trend_answer_head[i] == trend_answer_tail[i]])
    print ', '.join([' %s' % trend_answer_head[i] for i in range(probs) if trend_answer_head[i] == trend_answer_tail[i]])
    print prob(trend_answer_head), prob(trend_answer_tail)

    plt.figure(1)
    plt.plot([ord(i) - ord('A') + 1 for i in trend_answer_tail[:40]], 'b*-')
    plt.savefig('figures/most_freq_trend_tail.png', dpi=96)
    plt.cla()
    plt.figure(2)
    plt.plot([ord(i) - ord('A') + 1 for i in trend_answer_head[:40]], 'r*-')
    plt.savefig('figures/most_freq_trend_head.png', dpi=96)
    # plt.show()


def run():
    filename = 'data/data.txt'
    outline(filename)

    p = Cloze(filename)

    answer = [(i, p.trend_answer_head[i])
            for i in range(p.probs)
            if p.trend_answer_head[i] == p.trend_answer_tail[i]]

    p.predict(answer)

if __name__ == "__main__":
    run()

