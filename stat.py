# -*- Encoding: utf-8 -*-
from util import print_cutting_line

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

@print_cutting_line
def freq(data):
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

    for answer, fq in sort_dict(count):
        print answer, fq

def run():
    outline(read_data('data/data.txt'))
    freq(read_data('data/data.txt'))

if __name__ == "__main__":
    run()

