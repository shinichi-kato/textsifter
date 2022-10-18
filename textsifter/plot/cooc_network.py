"""
共起ネットワーク
"""
import itertools
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx   
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')

def cooccurrence_network(nodeslist, top_most):

    """ 単語頻度 """
    counts = Counter([node for nodes in nodeslist for node in nodes])
    counts = counts.most_common()

    """ top_mostで足切り """
    if top_most <= 0:
        counts = counts[:top_most]



    """ jaccard距離 """
    vocab = [x[0] for x in counts]
    r_vocab = { node:index for index,node in enumerate(vocab)}
    size = len(vocab)
    cooc_mtx = np.zeros((size,size))
    
    for nodes in nodeslist:
        pairs = list(itertools.combinations(nodes,2)) if len(nodes) >=2 else []
        for x,y in pairs:
            cooc_mtx[r_vocab[x],r_vocab[y]] += 1
    
    cooc_mtx = (cooc_mtx + cooc_mtx.transpose())/2

    jac_dist = 1-cdist(cooc_mtx,cooc_mtx,'jaccard')

    """ グラフ化 """
    nodename = mk_node2name(counts)

    G = nx.Graph() 
    for node in vocab:
        G.add_node(nodename[node])
    
    pos = nx.spring_layout(G, seed=3068)
    nx.draw(G, pos=pos, with_labels=True)
    plt.show()


def mk_node2name(nodeslist):
    """ nodeslistを調べてsurfaceが重複するものがあった場合、
        surface(factor)という名前に、そうでない場合surfaceに変換する辞書を返す         """
    
    dict = {}
    for nodes in nodeslist:
        for node in nodes:
