"""
common_central.py


"""
import itertools
from collections import Counter, defaultdict
import pandas as pd
from textsifter.preprocess import Node
import matplotlib.pyplot as plt
import matplotlib


def common_central(nodeslist, mode, top_most):
    """ 
    modeが'markov'の場合はnodeslistからマルコフ連鎖を計算し、単語について頻度vs次数を
    上位top_most件の単語についてプロットします。
    modeが'cooccurrence'の場合はnodeslistから共起行列を計算し、単語について頻度vs次数を
    上位top_most件の単語についてプロットします。

    """

    node = nodeslist[0][0]
    if isinstance(node, Node):

        if mode == 'markov':
            df = _node_markov(nodeslist)
        elif node == 'cooccurrence':
            df = _node_cooccurrence(nodeslist)

    # elif isinstance(node, str):W

    """ top_mostのスライス"""

    top_most = top_most or 10

    print(f"表示件数指定:{top_most}件 / 全単語{len(df)}")

    if top_most > 0:
        df = df.head(top_most)

    """ リスト表示 """
    print(df)

    """ 散布図描画 """

    with matplotlib.rc_context({
        'font.family': 'Noto Sans CJK JP'
    }):
        fig, ax = plt.subplots()

        df.plot.scatter('freq', 'centrality', ax=ax)

        for _, row in df.iterrows():
            ax.annotate(row['node'], (row['freq'], row['centrality']))

        plt.show()


def _node_markov(nodeslist):
    """ markov連鎖を生成し、以下を計算
        commons: 各表層形の頻度(markov連鎖の場合は次候補数と同じ)
        centrals: 各表層形の次数(ユニークな次候補の数)             
        commonsはリスト、centralsはCounterとする                      """

    vocab = defaultdict(list)

    for nodes in nodeslist:
        prev = '\f'
        for node in nodes:
            vocab[prev].append(node.surface)
            prev = node.surface

    commons = Counter({node: len(nexts) for node, nexts in vocab.items()})
    commons = [(n[0], n[1], vocab[n[0]]) for n in commons.most_common()]

    centrals = Counter({node: len(set(nexts))
                       for node, nexts in vocab.items()})
    centrals = [(node, cnt) for node, cnt in centrals.items()]

    df = pd.DataFrame(commons, columns=['node', 'freq', 'nexts'])
    df2 = pd.DataFrame(centrals, columns=['node', 'centrality'])
    df = pd.merge(df, df2, on='node')

    return df


def _node_cooccurrence(nodeslist):
    """ 共起行列を生成し、以下を計算
        commons: 各ノードの頻度
        centrals: 各ノードの次数
        commonsはリスト、centralsはCounterとする                      """

    commons = Counter([node for nodes in nodeslist for node in nodes])
    commons = [(n[0], n[1]) for n in commons.most_common()]

    pairslist = [frozenset(itertools.combinations(nodes, 2))
                 for nodes in nodeslist if len(nodes) >= 2]

    centrals = Counter([p for pairs in pairslist for p in pairs])
    centrals = [(node, cnt) for node, cnt in centrals.items()]

    df = pd.DataFrame(commons, columns=['node', 'freq', 'nexts'])
    df2 = pd.DataFrame(centrals, columns=['node', 'centrality'])
    df = pd.merge(df, df2, on='node')

    return df
