import unittest
from textsifter import preprocess
from textsifter.plot import cooc_network,markov_network

class TestNetwork(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = []
        with open("demo/lovecraft.txt") as f:
            cls.data = f.readlines()

        with open('tests/term.json') as f:
            cls.data = preprocess.morpho(cls.data,f)
            cls.data = preprocess.join_suffix(cls.data)
            cls.data = preprocess.join_kakujoshi(cls.data)
        
    def test_cooc_graph(self):
        
        cooc_network.cooccurrence_network(TestNetwork.data, 10)

    def test_markov_graph(self):
        
        markov_network.markov_network(TestNetwork.data, 10)
        

if __name__ == '__main__':
    unittest.main()