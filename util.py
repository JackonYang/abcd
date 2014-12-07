# -*- Encoding: utf-8 -*-
import random

def cutting_line(desc, length=60):
    half_len = int((length - len(desc) - 2) / 2)
    return '-'*half_len + ' ' + desc + ' ' + '-'*half_len

line_length = 60
def print_cutting_line(func):
    def _wrap(*args, **kwargs):
        desc = func.__name__
        if func.__doc__:
            desc = func.__doc__
        print cutting_line(desc, line_length)
        return func(*args, **kwargs)
    return _wrap


def calc_score(my_answer, std_answer):
    score = 0
    if isinstance(my_answer[0], str):
        for i, ch in zip(range(len(my_answer)), my_answer):
            score += (std_answer[i] == ch)
    else:
        for i, ch in my_answer:
            score += (std_answer[i] == ch)
    return 10.0*score/len(my_answer)

def ch2int(ch):
    return ord(ch) - ord('A') + 1

def int2ch(digit):
    return chr(ord('A') + digit - 1)

def gen_answer():
    answer = []
    for i in range(20):
        answer.append(int2ch(random.randrange(1, 5, 1)))
    return answer
