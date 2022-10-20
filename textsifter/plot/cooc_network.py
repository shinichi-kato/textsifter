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

from textsifter.preprocess import Node
from textsifter.plot.font import FONT_FAMILY

matplotlib.use('TkAgg')


def cooccurrence_network(nodeslist, top_most):
    """ 単語頻度 """
    counts = Counter([node for nodes in nodeslist for node in nodes])
    commons = counts.most_common()

    # """ top_mostで足切り """
    # top_most = top_most or 10
    # if top_most <= 0:
    #     commons = commons[:top_most]

    """ jaccard距離 """
    vocab = [x[0] for x in commons]
    r_vocab = {node: index for index, node in enumerate(vocab)}
    size = len(vocab)
    cooc_mtx = np.zeros((size, size))

    for nodes in nodeslist:
        pairs = itertools.combinations(nodes, 2) if len(nodes) >= 2 else []
        for x, y in pairs:
            cooc_mtx[r_vocab[x], r_vocab[y]] += 1

    cooc_mtx = (cooc_mtx + cooc_mtx.transpose())/2

    jac_dist = 1-cdist(cooc_mtx, cooc_mtx, 'jaccard')

    """ jaccard距離のTOP_MOSTで足切り """
     
    jac_dist = _filter_triu_top(jac_dist, top_most)

    """ グラフ化 """
    nodename = _mk_node2name(nodeslist)
    with matplotlib.rc_context({
        'font.family': FONT_FAMILY
    }):
        G = nx.Graph()
        for node in vocab:
            G.add_node(
                nodename.get(node, node.surface), count=counts[node]
            )

        for x in range(size):
            x_name = nodename[vx] if (
                vx := vocab[x]) in nodename else vx.surface
            for y in range(x):
                weight = jac_dist[x, y]
                if weight > 0:
                    y_name = nodename[vy] if (
                        vy := vocab[y]) in nodename else vy.surface
                    print(x_name,y_name,weight)
                    G.add_edge(
                        x_name, y_name,
                        weight=weight,
                    )

        width = [d['weight']*10 for (u, v, d) in G.edges(data=True)]
        node_color = np.fromiter(nx.degree_centrality(G).values(), float)
        node_size = [
            10+(x**0.5)*200 for x in nx.get_node_attributes(G, "count").values()]

        pos = nx.spring_layout(G, seed=3068, weight=None)
        nx.draw_networkx_nodes(G, pos,
                               node_color=node_color, cmap=plt.cm.summer, node_size=node_size)
        nx.draw_networkx_labels(G, pos,
                                font_size=10,
                                font_family=FONT_FAMILY)
        nx.draw_networkx_edges(G, pos=pos, alpha=0.2,
                               edge_color='#332300', width=width)
        plt.axis('off')
        plt.show()


def _filter_triu_top(matrix, top_most):
    """ matrixの値の上位top_most件のみをのこし、それ以外を0にして返す """
    if top_most is None:
        top_most=50
    if top_most <=0:
        return matrix

    m = np.tril(matrix)
    limit = np.unique(m,axis=None)[-top_most]
    return matrix*np.where(m>limit,1,0)


def _mk_node2name(nodeslist):
    """ nodeslistを調べて
        surfaceが同一でfactorが異なる場合は
            surface = なる(成る)
            surface = なる(為る)

        surfaceが異なりfactorが同一の場合は
            surface = MLCC|積層セラミックコンデンサ

        となるようなnode->surface辞書を生成して返す      """

    node2name = {}

    data = [[n.surface, n.pos, n.factor] for nodes in nodeslist for n in nodes]
    df = (pd.DataFrame(data, columns=['surface', 'pos', 'factor'])
          .drop_duplicates())

    """ surfaceが同一でfactorが異なるnode """
    dfs = df[df.duplicated('surface', keep=False)]
    for row in dfs.itertuples():
        factors = _squeeze_factor(row.factor)
        node2name[Node(row.surface, row.pos, row.factor)
                  ] = f'{row.surface}({"-".join(factors)})'

    """ factorが同一でsurfaceが異なるnode """
    dff = df[df.duplicated('factor', keep=False)]
    for row in dff.itertuples():
        factors = _squeeze_factor(row.factor)
        node2name[Node(row.surface, row.pos, row.factor)
                  ] = f'{row.surface}({"-".join(factors)})'

    return node2name


def _squeeze_factor(factor):
    factors=[factor[-1]]
    if len(factor) == 2:
        factors.extend(list(factor[0]))
    return factors
