# -*- coding: utf-8-*-

import os
from trick import read_data, freq_of_problem
from util import top1, cutting_line

header = """\
    |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  10 |  11 |  12 |  13 |  14 |  15 |  16 |  17 |  18 |  19 |  20
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
"""
sp = ' | '


def match_top1(known, target_answer, target_year):
    count = ['count']
    choice = ['choice']

    single_top1 = []
    eq = []
    for i, item in zip(range(20), freq_of_problem(known)):
        num, answer = top1(item)
        count.append(str(num))
        choice.append('/'.join(answer))
        if 1 == len(answer):
            single_top1.append(i)
        if target_answer[i] in answer:
            eq.append(i)

    content = sp.join(count) + '\n' + sp.join(choice) + '\n' 
    return single_top1, eq, content


def trend_top1(full_data):
    end = len(full_data)
    f = open('detail.md', 'w')
    for target_idx in range(end-1, 4, -1):
        target_year, target_answer = full_data[target_idx]
        topn = []

        print cutting_line(target_year)
        f.write('\n')
        f.write('\n')
        f.write(header)
        f.write(target_year + sp + sp.join(target_answer))
        f.write('\n')

        for group in range(target_idx, 4, -1):
            single_top1, eq, content = match_top1(full_data[target_idx-group: target_idx], target_answer, target_year)

            f.write(content)

            print single_top1
            print len(single_top1), set(eq) & set(single_top1)
    f.close()


def run():
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, 'data/data.txt')
    full_data = read_data(filename)
    trend_top1(full_data)



if __name__ == "__main__":
    run()
