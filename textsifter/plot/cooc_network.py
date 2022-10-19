"""
共起ネットワーク
"""
import itertools
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib

from textsifter.preprocess import Node

matplotlib.use('TkAgg')


def cooccurrence_network(nodeslist, top_most):
    """ 単語頻度 """
    counts = Counter([node for nodes in nodeslist for node in nodes])
    counts = counts.most_common()

    """ top_mostで足切り """
    top_most = top_most or 10
    if top_most <= 0:
        counts = counts[:top_most]

    """ jaccard距離 """
    vocab = [x[0] for x in counts]
    r_vocab = {node: index for index, node in enumerate(vocab)}
    size = len(vocab)
    cooc_mtx = np.zeros((size, size))

    for nodes in nodeslist:
        pairs = list(itertools.combinations(nodes, 2)
                     ) if len(nodes) >= 2 else []
        for x, y in pairs:
            cooc_mtx[r_vocab[x], r_vocab[y]] += 1

    cooc_mtx = (cooc_mtx + cooc_mtx.transpose())/2

    jac_dist = 1-cdist(cooc_mtx, cooc_mtx, 'jaccard')

    """ グラフ化 """
    nodename = mk_node2name(nodeslist)
    with matplotlib.rc_context({
        'font.family': 'Noto Sans CJK JP'
    }):
        G = nx.Graph()
        for node in vocab:
            G.add_node(
                nodename.get(node, node.surface),
                )
        
        for x in range(size):
            x_name = nodename[vx] if (vx:=vocab[x]) in nodename else vx.surface
            for y in range(x):
                y_name = nodename[vy] if (vy:=vocab[y]) in nodename else vy.surface
                G.add_edge(
                    x_name,y_name,
                    weight=jac_dist[x,y],
                    )

        pos = nx.spring_layout(G, seed=3068)
        nx.draw_networkx_nodes(G, pos=pos )
        nx.draw_networkx_labels(G, pos=pos, font_family='Noto Sans CJK JP')
        nx.draw_networkx_edges(G, pos=pos, alpha=0.2)
        plt.show()


def mk_node2name(nodeslist):
    """ nodeslistを調べて
        surfaceが同一でfactorが異なる場合は
            surface = なる(成る)
            surface = なる(為る)

        surfaceが異なりfactorが同一の場合は
            surface = MLCC|積層セラミックコンデンサ

        となるようなnode->surface辞書を生成して返す      """
    
    node2name={}

    data = [[n.surface,n.pos,n.factor] for nodes in nodeslist for n in nodes]
    df = (pd.DataFrame(data, columns=['surface', 'pos', 'factor'])
          .drop_duplicates())

    """ surfaceが同一でfactorが異なるnode """
    dfs = df[df.duplicated('surface',keep=False)]
    for row in dfs.itertuples():
        node2name[Node(row.surface,row.pos,row.factor)] = f'{row.surface}({"-".join(row.factor)})'

    """ factorが同一でsurfaceが異なるnode """
    dff = df[df.duplicated('factor',keep=False)]
    for row in dff.itertuples():
        node2name[Node(row.surface,row.pos,row.factor)] = f'{row.surface}({"-".join(row.factor)})'
    
    return node2name