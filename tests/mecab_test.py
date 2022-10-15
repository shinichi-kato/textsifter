import unittest
import MeCab


class TestTagger(unittest.TestCase):

    def test_tagger(self):
        tagger = MeCab.Tagger()
        nodes = tagger.parse("全自動化した立体的機動はよさそうだ。")
        for node in nodes.split('\n'):
            print(node.split('\t'))
        print("\n")

if __name__ == '__main__':
    unittest.main()