# -*- coding: utf-8-*-
import unittest

import os
from trick import freq, read_data, freq_of_problem
from util import top1


class test_trick(unittest.TestCase):

    def setUp(self):
        BASE_DIR = os.path.dirname(__file__)
        filename = os.path.join(BASE_DIR, 'data/data.txt')
        self.full_data = read_data(filename)

        self.count = [
            {'A': 4, 'C': 2, 'B': 4},
            {'A': 2, 'B': 4, 'D': 4},
            {'A': 3, 'C': 2, 'B': 2, 'D': 3},
            {'A': 2, 'C': 4, 'B': 3, 'D': 1},
            {'A': 2, 'C': 5, 'B': 2, 'D': 1},
            {'A': 4, 'C': 1, 'B': 4, 'D': 1},
            {'A': 2, 'C': 1, 'B': 3, 'D': 4},
            {'A': 3, 'C': 2, 'B': 2, 'D': 3},
            {'A': 2, 'C': 2, 'B': 3, 'D': 3},
            {'A': 3, 'C': 3, 'B': 2, 'D': 2},
            {'A': 2, 'C': 3, 'B': 2, 'D': 3},
            {'A': 3, 'C': 3, 'B': 2, 'D': 2},
            {'A': 3, 'C': 2, 'B': 2, 'D': 3},
            {'A': 1, 'C': 5, 'D': 4},
            {'A': 2, 'C': 1, 'B': 4, 'D': 3},
            {'A': 2, 'C': 3, 'B': 2, 'D': 3},
            {'A': 3, 'C': 3, 'B': 2, 'D': 2},
            {'A': 3, 'C': 5, 'D': 2},
            {'A': 4, 'C': 1, 'B': 4, 'D': 1},
            {'A': 1, 'C': 3, 'B': 2, 'D': 4},
            ]


    def tearDown(self):
        self.full_data = None

    def test_freq(self):
        test_data = [('CBACBADADBCADCDBCDA', [5, 4, 5, 5]),
                     ('CBACBCDADBACDDABDAB', [5, 5, 4, 5]),
                     ('AA', [2, 0, 0, 0]),
                     ]
        i = 0
        for one_answer, expt in test_data:
            self.assertEqual(freq(one_answer), expt)

    def test_freq_of_problem(self):
        self.assertEqual(freq_of_problem(self.full_data), self.count)

    def test_top1(self):
        expts = [
            (4, ['A', 'B']), (4, ['B', 'D']), (3, ['A', 'D']),
            (4, ['C']), (5, ['C']), (4, ['A', 'B']), (4, ['D']),
            (3, ['A', 'D']), (3, ['B', 'D']), (3, ['A', 'C']),
            (3, ['C', 'D']), (3, ['A', 'C']), (3, ['A', 'D']),
            (5, ['C']), (4, ['B']), (3, ['C', 'D']),
            (3, ['A', 'C']), (5, ['C']), (4, ['A', 'B']),
            (4, ['D'])]
        for item, expt in zip(self.count, expts):
            self.assertEqual(top1(item), expt)


def add_test(suite):
    suite.addTest(test_trick('test_freq'))
    suite.addTest(test_trick('test_freq_of_problem'))

    suite.addTest(test_trick('test_top1'))


if __name__=='__main__':
    runner=unittest.TextTestRunner()

    suite=unittest.TestSuite()
    add_test(suite)

    runner.run(suite)
