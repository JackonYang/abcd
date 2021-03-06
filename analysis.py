# -*- coding: utf-8-*-

import os
from trick import read_data, freq_of_problem
from util import top1, cutting_line, bottom1

header = """\
    |  1  |  2  |  3  |  4  |  5  |  6  |  7  |  8  |  9  |  10 |  11 |  12 |  13 |  14 |  15 |  16 |  17 |  18 |  19 |  20
--- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---
"""
sp = ' | '


def match_top1(known, target_answer, target_year, cmp_func):
    count = ['count']
    choice = ['choice']

    single_top1 = []
    eq = []
    for i, item in zip(range(20), freq_of_problem(known)):
        num, answer = cmp_func(item)
        count.append(str(num))
        choice.append('/'.join(answer))
        if 1 == len(answer) and num == 1:
            single_top1.append(i)
        if target_answer[i] in answer:
            eq.append(i)

    content = sp.join(count) + '\n' + sp.join(choice) + '\n' 
    return single_top1, eq, content


def trend_top1(full_data, cmp_func):
    end = len(full_data)
    f = open('detail_%s.md' % cmp_func.__name__, 'w')
    for target_idx in range(end-1, 5, -1):
        target_year, target_answer = full_data[target_idx]
        topn = []

        print cutting_line(target_year)
        f.write('\n')
        f.write('\n')
        f.write(header)
        f.write(target_year + sp + sp.join(target_answer))
        f.write('\n')

        for group in range(target_idx, 5, -1):
            single_top1, eq, content = match_top1(full_data[target_idx-group: target_idx], target_answer, target_year, cmp_func)

            f.write(content)

            print single_top1
            print len(single_top1), set(eq) & set(single_top1)
    f.close()


def top1_2015(full_data, cmp_func):
    end = len(full_data)
    target_year, target_answer = '2015', ['Z'] * 20
    topn = []

    f = open('predict_2015%s.md' % cmp_func.__name__, 'w')
    f.write(header)
    for group in range(end, 4, -1):
        single_top1, eq, content = match_top1(full_data[end-group: end], target_answer, target_year, cmp_func)

        f.write(content)

        print len(single_top1), single_top1
    f.close()


def run():
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, 'data/data.txt')
    full_data = read_data(filename)

    print cutting_line('drop by top')
    trend_top1(full_data, top1)

    print cutting_line('drop by bottom')
    trend_top1(full_data, bottom1)

    print cutting_line('predict 2015. top')
    top1_2015(full_data, top1)
    print cutting_line('predict 2015. bottom')
    top1_2015(full_data, bottom1)



if __name__ == "__main__":
    run()
