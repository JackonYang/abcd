# -*- Encoding: utf-8 -*-
from util import print_cutting_line
import matplotlib.pyplot as plt

def read_data(file_name):
    data = dict()
    with open(file_name) as f:
        for line in f.readlines():
            year, cloze, read_a, read_b = line.strip().split(' ')
            item = list(cloze)
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
    return [res['A'], res['B'], res['C'], res['D']]

@print_cutting_line
def outline(data):
    for year, answer in sort_dict(data):
        print year, 'total: ', prob(answer[:40]),\
            '\tcloze: ', prob(answer[:20]),\
            '\tread_a: ', prob(answer[20:40])

def calc_freq(data):
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
def freq(data):
    count = calc_freq(data)
    for answer, fq in sort_dict(count):
        print answer, fq

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
    outline(read_data('data/data.txt'))
    freq(read_data('data/data.txt'))
    most_freq_trend(read_data('data/data.txt'))

if __name__ == "__main__":
    run()

