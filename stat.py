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

def run():
    outline(read_data('data/data.txt'))

if __name__ == "__main__":
    run()

