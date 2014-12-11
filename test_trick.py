# -*- coding: utf-8-*-
import unittest
from trick import prob


class test_trick(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_prob(self):
        self.assertEqual(1, 1)
 

def add_test(suite):
    suite.addTest(test_trick('test_prob'))

if __name__=='__main__':
    runner=unittest.TextTestRunner()

    suite=unittest.TestSuite()
    add_test(suite)

    runner.run(suite)
