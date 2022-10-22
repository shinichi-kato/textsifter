"""
マルコフ連鎖ネットワーク
"""
from collections import Counter, defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from textsifter.preprocess import Node
from textsifter.plot import mk_node2name, FONT_FAMILY

matplotlib.use('TkAgg')


def markov_network(nodeslist, top_most):
    """ マルコフ連鎖ネットワークを表示する。
        degree_centralityをnodeの色で、頻度をnodeの大きさで、
        2つのノード間の遷移頻度をedgeの太さで表現する。
        top_mostで数を指定した場合、ノードの次数が上位top_most位までの
        ノードに限定する                                                  """

    """ markov連鎖 """
    chain = defaultdict(list)

    prev = None
    for nodes in nodeslist:
        for node in nodes:
            if prev:
                chain[prev].append(node)
            prev = node

    """ グラフ化 """
    nodename = mk_node2name(nodeslist)

    G = nx.DiGraph()
    for node in chain:
        dests = Counter(chain[node])
        node_name = nodename.get(node, node.surface)
        G.add_node(
            node_name, count=len(dests)
        )

        for dest, weight in dests.items():
            dest_name = nodename.get(dest, dest.surface)
            G.add_edge(node_name, dest_name, weight=weight)
    
    """ top_mostで足切り """

    number_of_all_nodes = G.number_of_nodes()

    if top_most is None:
        top_most = 10
    if top_most >0:
        d = np.fromiter(dict(G.degree()).values(),int)
        limit = np.unique(d,axis=None)[-top_most]
        to_be_removed=[n for n in G.nodes() if G.degree(n)<limit]
        G.remove_nodes_from(to_be_removed)
        view_nodes = G.number_of_nodes()
        print(f"次数が上位{top_most}番までのnode({number_of_all_nodes}個中{view_nodes}個)を表示します")


    """ デザイン """
    node_color = np.fromiter(nx.degree_centrality(G).values(), float)
    edge_color = [d['weight']**0.5 for (u, v, d) in G.edges(data=True)]
    node_size = np.fromiter(nx.get_node_attributes(G, "count").values(), float)
    node_size = 10+(node_size**0.5)*100
    edge_cmap = matplotlib.colors.LinearSegmentedColormap.from_list('half',
        plt.cm.binary(np.linspace(0.3,max(edge_color),256)))

    pos = nx.spring_layout(G, seed=228270, k=0.5)
    nx.draw_networkx_nodes(G, pos,
                           node_color=node_color, cmap=plt.cm.summer, node_size=node_size)
    nx.draw_networkx_labels(G, pos,
                            font_size=10,
                            font_family=FONT_FAMILY)
    nx.draw_networkx_edges(G, pos, 
                            edge_color=edge_color, edge_vmin=1, edge_cmap=edge_cmap,
                            width=1.5,
                            node_size=node_size)
    plt.axis('off')
    plt.show()

