import unittest
from textsifter import preprocess
from textsifter.plot import cooc_network

class TestCooc(unittest.TestCase):

    def test_cooc_graph(self):
        data = []
        with open("demo/lovecraft.txt") as f:
            data = f.readlines()

        with open('tests/term.json') as f:
            data = preprocess.morpho(data,f)
            data = preprocess.join_suffix(data)
            data = preprocess.join_kakujoshi(data)
        
        cooc_network.cooccurrence_network(data, 10)

        

if __name__ == '__main__':
    unittest.main()