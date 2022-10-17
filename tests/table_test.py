import unittest
from textsifter import preprocess
from textsifter.plot.common_central import common_central
import json
import pprint

class TestTablePlot(unittest.TestCase):

    def test_most_central(self):
        data = []
        with open("demo/lovecraft.txt") as f:
            data = f.readlines()

        with open('tests/term.json') as f:
            data = preprocess.morpho(data,f)
            data = preprocess.join_suffix(data)
        
        common_central(data, "markov", 10)

        

if __name__ == '__main__':
    unittest.main()