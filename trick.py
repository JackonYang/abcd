# -*- Encoding: utf-8 -*-
import os
import matplotlib.pyplot as plt

from util import print_cutting_line
import util

BASE_DIR = os.path.dirname(__file__)


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
    return util.sort_dict(data)


def prob(one_answer):
    """ 统计一组答案中, 各选项出现概率 """
    res = dict()

    def add(ch):
        if ch in res:
            res[ch] += 1
        else:
            res[ch] = 1

    for ch in one_answer:
        add(ch)
    output = ['A', 'B', 'C', 'D']
    return [res.get(ch, 0) for ch in output]


def calc_freq(data):
    """ 历年各题目各选项出现次数统计 """
    count = dict()

    def add(ch, i):
        def _wrap():
            if ch not in count:
                count[ch] = [0] * len(answer)
            count[ch][i] += 1
        _wrap()

    for year, answer in data:
        for i in range(len(answer)):
            add(answer[i], i)
    return count

@print_cutting_line
def outline(datafile):
    """ 45 个选择题总体分布率 """
    data = read_data(datafile, has_reading=True)

    print util.cutting_line('历年答案 ABCD 比例分布')

    def fmt(lst):
        return str(lst).strip('[]')

    print 'year | total | Cloze | Reading A'
    for year, answer in data:
        print '%s | %s | %s | %s' % (year, fmt(prob(answer[:40])), fmt(prob(answer[:20])), fmt(prob(answer[20:40])))

    print util.cutting_line('完型各选项出现次数统计')
    count = calc_freq(data)
    for answer, fq in util.sort_dict(count):
        print answer, fq[:20]


class Cloze:
    """ 完型填空分析与预测 """

    def __init__(self, data=read_data('data/data.txt')):
        self.probs = 20  # len(data.values()[0]) 20 个完型填空题
        self.std_answer = data
        self.most_freq()

    def predict(self, my_answer, fig=None):
        scores = [util.calc_score(my_answer, one_answer) for year, one_answer in self.std_answer]

        if fig:
            plt.sca(fig)
        else:
            plt.figure()
        plt.plot(scores)
        plt.title('avg score: %.2f' % (sum(scores) / len(scores)))
        if not fig:
            plt.show()

    def most_freq(self):
        count = calc_freq(self.std_answer)
        self.trend_freq = [0] * self.probs
        self.trend_answer_head = ['Z'] * self.probs
        self.trend_answer_tail = ['Z'] * self.probs
        for answer, fq in util.sort_dict(count):
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

    plt.cla()
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

    save_name = os.path.join(BASE_DIR, 'figures/predict_by_most_freq.png')
    plt.savefig(save_name, dpi=96)
    print 'figure saved in %s' % save_name

    # plt.show()  # for debug

@print_cutting_line
def predict_by_most_freq_total(p):
    plt.cla()
    head_plot = plt.subplot(121)
    tail_plot = plt.subplot(122)

    p.predict(p.trend_answer_head, head_plot)
    p.predict(p.trend_answer_tail, tail_plot)

    save_name = os.path.join(BASE_DIR, 'figures/predict_by_most_freq_total.png')
    plt.savefig(save_name, dpi=96)
    print 'figure saved in %s' % save_name

    # plt.show()  # for debug

    print util.cutting_line('完型填空历年出现频率最高选项与次数')
    header = '题号 | 次数 | 选项'
    print header
    for i in range(20):
        if p.trend_answer_head[i] == p.trend_answer_tail[i]:
            print '%s | %s | %s' % (i+1, p.trend_freq[i], p.trend_answer_head[i])
        else:
            print '%s | %s | %s' % (i+1, p.trend_freq[i], '%s/%s' % (p.trend_answer_head[i], p.trend_answer_tail[i]))


def predict_by_random(p):
    ans1 = util.gen_answer()
    ans2 = util.gen_answer()
    ans3 = util.gen_answer()
    ans4 = util.gen_answer()

    plt.cla()
    ans1_plot = plt.subplot(221)
    ans2_plot = plt.subplot(222)
    ans3_plot = plt.subplot(223)
    ans4_plot = plt.subplot(224)

    p.predict(ans1, ans1_plot)
    p.predict(ans2, ans2_plot)
    p.predict(ans3, ans3_plot)
    p.predict(ans4, ans4_plot)

    print util.cutting_line('random 产生答案')
    print ', '.join(ans1)
    print ', '.join(ans2)
    print ', '.join(ans3)
    print ', '.join(ans4)
    #plt.show()

def calc_avg_score(full_data, step):
    avg = []

    groups = len(full_data) + 1 - step
    for start in range(groups):
        p = Cloze(full_data[start:start+step])
        avg.append(0.5*sum(p.trend_freq)/step)
    return avg

def avg_trend(filename):
    avgs = []
    orig_data = read_data(filename)
    for i in range(1, len(orig_data)+1):
        avgs.append(util.mean(calc_avg_score(orig_data, i)))
    plt.cla()
    plt.plot(avgs, '-*')
    plt.title('avg trend with years of source data')
    save_name = os.path.join(BASE_DIR, 'figures/avg_trend_by_years.png')
    plt.savefig(save_name, dpi=96)

def best_accuracy(full_data, step):
    groups = len(full_data) - step
    scores = []
    for start in range(groups-1, -1, -1):
        p = Cloze(full_data[start:start+step])
        # plt.cla()
        # head_plot = plt.subplot(121)
        # tail_plot = plt.subplot(122)
        score = 0
        year, std_answer = full_data[start+step]
        for std, ans1, ans2 in zip(std_answer, p.trend_answer_head, p.trend_answer_tail):
            score += (std == ans1 or std == ans2)
        scores.append(score*0.5)

    return scores

@print_cutting_line
def best_accuracy_trend(full_data):
    for step in range(3, 10):
        print '%s years a group, scores: %s' % (step, str(best_accuracy(full_data, step)).strip('[]'))



def run():

    filename = os.path.join(BASE_DIR, 'data/data.txt')
    full_data = read_data(filename)
    #outline(filename)

    # p = Cloze()
    # predict_by_most_freq(p)
    # predict_by_random(p)

    # avg_trend(filename)

    best_accuracy_trend(full_data)

if __name__ == "__main__":
    run()
