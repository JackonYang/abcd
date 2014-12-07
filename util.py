# -*- Encoding: utf-8 -*-

def cutting_line(desc, length=26):
    half_len = int((length - len(desc) - 2) / 2)
    return '-'*half_len + ' ' + desc + ' ' + '-'*half_len

line_length = 60
def print_cutting_line(func):
    def _wrap(*args, **kwargs):
        print cutting_line(func.__name__, line_length)
        return func(*args, **kwargs)
    return _wrap


def calc_score(my_answer, std_answer):
    score = 0
    for i, ch in my_answer:
        score += (std_answer[i] == ch)
    return 10.0*score/len(my_answer)
