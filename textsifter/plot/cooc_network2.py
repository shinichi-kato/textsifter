"""
共起ネットワーク
"""
import itertools
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

from textsifter.plot import mk_node2name, FONT_FAMILY

matplotlib.use('TkAgg')

def cooccurrence_network(nodeslist, top_most):
    """ 共起ネットワークを表示する。
        degree_centralityをnodeの色で、頻度をnodeの大きさで、
        2つのノード間の共起性の高さをjaccard距離で表したものをedgeの太さで表現する。
        top_mostで数を指定した場合、edgeのjaccard距離の上位top_most件を表示し、
        孤立したnodeは非表示にする。                                                 """
    
    """ グラフ化 """
    nodename = mk_node2name(nodeslist)
    with matplotlib.rc_context({
        'font.family': FONT_FAMILY
    }):
        G = nx.Graph()
        for node in vocab:
            G.add_node(
                nodename.get(node, node.surface), count=counts[node]
            )
