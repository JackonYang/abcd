# -*- coding: utf-8-*-
import unittest
from trick import freq


class test_trick(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_freq(self):
        test_data = [('CBACBADADBCADCDBCDA', [5, 4, 5, 5]),
                     ('CBACBCDADBACDDABDAB', [5, 5, 4, 5]),
                     ('AA', [2, 0, 0, 0]),
                     ]
        i = 0
        for one_answer, expt in test_data:
            self.assertEqual(freq(one_answer), expt)
 

def add_test(suite):
    suite.addTest(test_trick('test_freq'))

if __name__=='__main__':
    runner=unittest.TextTestRunner()

    suite=unittest.TestSuite()
    add_test(suite)

    runner.run(suite)
