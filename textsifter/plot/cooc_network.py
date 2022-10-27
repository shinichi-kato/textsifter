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
from textsifter.core.cooccurrence import cooccurrence

matplotlib.use('TkAgg')


def cooccurrence_network(nodeslist, top_most):
    """ 共起ネットワークを表示する。
        degree_centralityをnodeの色で、頻度をnodeの大きさで、
        2つのノード間の共起性の高さをjaccard距離で表したものをedgeの太さで表現する。
        top_mostで数を指定した場合、edgeのjaccard距離の上位top_most件を表示し、
        孤立したnodeは非表示にする。                                                 """

    # """ 単語頻度 """
    # counts = Counter([node for nodes in nodeslist for node in nodes])
    # commons = counts.most_common()

    # """ jaccard距離 """
    # vocab = [x[0] for x in commons]
    # r_vocab = {node: index for index, node in enumerate(vocab)}
    # size = len(vocab)
    # cooc_mtx = np.zeros((size, size))

    # for nodes in nodeslist:
    #     pairs = itertools.combinations(nodes, 2) if len(nodes) >= 2 else []
    #     for x, y in pairs:
    #         cooc_mtx[r_vocab[x], r_vocab[y]] += 1
    cooc = cooccurrence(nodeslist)

    jac_dist = 1-cdist(cooc.matrix, cooc.matrix, 'jaccard')

    """ jaccard距離のTOP_MOSTで足切り """

    jac_distl = np.tril(jac_dist)
    num_of_edges = np.count_nonzero(jac_distl)

    if top_most is None:
        top_most = 50
    if top_most > 0:
        rank = np.unique(jac_distl, axis=None)
        limit = rank[-top_most] if len(rank)>top_most else 0.0
        jac_dist = jac_dist*np.where(jac_distl > limit, 1, 0)

    view_edges = np.count_nonzero(jac_dist)
    print(f"Jaccard距離が上位{top_most}番までのedge({num_of_edges}本中{view_edges}本)を表示します")


    """ グラフ化 """
    nodename = mk_node2name(nodeslist)
    with matplotlib.rc_context({
        'font.family': FONT_FAMILY
    }):
        G = nx.Graph()
        for node in cooc.vocab:
            G.add_node(
                nodename.get(node, node.surface), count=cooc.counts[node]
            )

        for x in range(len(cooc.vocab)):
            x_name = nodename[vx] if (
                vx := cooc.vocab[x]) in nodename else vx.surface
            for y in range(x):
                weight = jac_dist[x, y]
                if weight > 0:
                    y_name = nodename[vy] if (
                        vy := cooc.vocab[y]) in nodename else vy.surface
                    G.add_edge(
                        x_name, y_name,
                        weight=weight,
                    )

        """ 孤立ノードを削除 """
        G.remove_nodes_from(list(nx.isolates(G)))

        """ デザイン """
        edge_color = [d['weight']*10 for (u, v, d) in G.edges(data=True)]
        node_color = np.fromiter(nx.degree_centrality(G).values(), float)
        node_size = [
            10+(x**0.5)*100 for x in nx.get_node_attributes(G, "count").values()]
        edge_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('half',
                                                                        plt.cm.binary(np.linspace(0.2, 0.8, 256)))

        pos = nx.spring_layout(G, seed=3068, k=0.5)
        nx.draw_networkx_nodes(G, pos,
                               node_color=node_color, cmap=plt.cm.summer, node_size=node_size)
        nx.draw_networkx_labels(G, pos,
                                font_size=10,
                                font_family=FONT_FAMILY)
        nx.draw_networkx_edges(G, pos=pos, node_size=node_size,
                               edge_color=edge_color, edge_cmap=edge_cmap,width=1)

        sm = plt.cm.ScalarMappable(cmap=plt.cm.summer,
                            norm=plt.Normalize(vmin=node_color.min(), vmax=node_color.max()))
        sm.set_array([])
        plt.colorbar(sm, label="全graphにおけるjaccard距離")
        plt.axis('off')
        plt.show()


def _filter_tril_top(matrix, top_most):
    """ matrixの値の上位top_most件のみをのこし、それ以外を0にして返す """
    if top_most is None:
        top_most = 50
    if top_most <= 0:
        return matrix

    m = np.tril(matrix)
    limit = np.unique(m, axis=None)[-top_most]
    return matrix*np.where(m > limit, 1, 0)

