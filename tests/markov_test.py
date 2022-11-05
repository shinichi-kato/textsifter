import unittest
from collections import namedtuple
from textsifter import preprocess
from textsifter.dump.markov_dict import bot_markov_chain
import json

Args = namedtuple('Args', ['source', 'format'])


class TestMarkovDict(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = []
        with open("demo/lovecraft-l.txt") as f:
            cls.data = f.readlines()

        with open('tests/term.json') as f:
            cls.data = preprocess.morpho(cls.data, f)
            cls.data = preprocess.join_suffix(cls.data)
            cls.data = preprocess.join_ppa(cls.data)
            # cls.data = preprocess.join_kakujoshi(cls.data)

    def test_markov_chain(self):
        args = Args(source=['test'], format='surface')
        data = bot_markov_chain(TestMarkovDict.data, args)

        with open('dict.json', 'w') as f:
            json.dump(data,f,ensure_ascii=False)
    
    def test_text_generation(self):
        args = Args(source=['test'], format='text')
        data = bot_markov_chain(TestMarkovDict.data, args)
        print(data)


if __name__ == '__main__':
    unittest.main()
