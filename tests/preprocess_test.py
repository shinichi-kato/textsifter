import unittest
from textsifter import preprocess
import json
import pprint

class TestTagger(unittest.TestCase):

    def test_morpho(self):
        data = []
        with open("demo/lovecraft.txt") as f:
            data = f.readlines()

        with open('tests/term.json') as f:
            data = preprocess.morpho(data,f)
            data = preprocess.joint_suffix(data)
        
        pp = pprint.PrettyPrinter()
        with open('tests/result.txt', 'wt') as f:
            f.writelines(pp.pformat(data))
        
        

if __name__ == '__main__':
    unittest.main()