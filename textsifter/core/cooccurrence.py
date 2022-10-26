from collections import Counter, namedtuple
import numpy as np
import itertools

CoocMtx = namedtuple('CoocMtx', ['counts', 'vocab','matrix'])

def cooccurrence(nodeslist):
    """ nodeslistから共起行列とvocabを計算して返す """
    counts = Counter([node for nodes in nodeslist for node in nodes])

    vocab = list(counts.keys())
    r_vocab = {node: index for index, node in enumerate(vocab)}
    size = len(vocab)
    cooc_mtx = np.zeros((size, size))

    for nodes in nodeslist:
        pairs = itertools.combinations(nodes, 2) if len(nodes) >= 2 else []
        for x, y in pairs:
            cooc_mtx[r_vocab[x], r_vocab[y]] += 1

    cooc_mtx = (cooc_mtx + cooc_mtx.transpose())/2

    return CoocMtx(counts=counts,vocab=vocab,matrix=cooc_mtx)