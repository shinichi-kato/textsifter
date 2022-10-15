"""
キャラクタごとの1-gram辞書を生成
"""
from collections import defaultdict, Counter
import json
import random
import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

s_data = [1, 2, 2, 8, 1, 5, 1, 1, 1, 1, 5, 1, 6, 1, 2, 1, 3, 2, 9,
          14, 4, 1, 1, 5, 7, 4, 14, 1, 2, 1, 1, 3, 2, 5, 1, 1, 2,
          1, 5, 9, 11, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 5, 1,
          1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 3, 1, 1, 6, 2, 2, 4, 2, 7, 1, 1, 6, 2, 1, 1, 1,
          7, 5, 1, 1, 1, 1, 1, 3, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1,
          1, 1, 1, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1,
          1, 1, 1, 1, 4, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


def historgram(data):
    count = [x*len(data[x]) for x in data]
    count = [len(x) for x in count]
    plt.xlabel("次候補の数")
    plt.ylabel("頻度")
    plt.hist(count, density=True, range=(1,100), bins=100, alpha=0.5, label="ATMOM-21kByte")
    plt.hist(s_data, density=True, range=(1,100), bins=100, alpha=0.5, label="ATMOM-927Byte")
    plt.legend(loc='upper right')
    plt.show()
    # plt.savefig('hist.svg')
    print(count)


def graph(data):
    G = nx.DiGraph()

    for src in data:
        dests = Counter(data[src])
        G.add_node(src, size=len(dests))
        for dest, weight in dests.items():

            G.add_edge(src, dest, weight=weight)

    pos = nx.spring_layout(G)
    node_keys = G.nodes()
    node_size = nx.get_node_attributes(G, "size")
    node_size = [node_size[n]*50 for n in node_keys]
    node_color = nx.degree_centrality(G)
    node_color = [(node_color[n]**0.5)*20+20 for n in node_keys]

    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_size,
        node_color=node_color,
        cmap='summer'
    )
    nx.draw_networkx_edges(
        G, pos,
        alpha=0.4,
        arrows=True
    )
    nx.draw_networkx_labels(
        G, pos,
        font_family="Noto Sans CJK JP",
    )
    plt.axis("off")
    plt.show()


def stringify(vocab):
    """ テスト文字出力 """
    c = "__head__"
    text = ""
    while c not in {'、', '。'}:
        cands = vocab[c]
        c = cands[random.randrange(len(cands))]
        text += c
    print(text)


def chr1gram(file):
    """
        文字列を一文字ずつ調べ、次にくる文字を格納した辞書を作る
        vocab={
            '理': ['由']
        }
    """
    vocab = defaultdict(list)
    prev = "\f"
    for line in file:
        for c in line:
            vocab[prev].append(c)
            prev = c

    print(json.dumps(vocab, ensure_ascii=False))
    return vocab


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(
            "chr1gram <input file> [-g]\n"
            "input fileを文字ごとの1gramに変換したjsonを出力します。\n"
            "-g: グラフとして可視化\n"
            "-h: ヒストグラム")

    with open(sys.argv[1]) as f:
        data = chr1gram(f)

    arg = sys.argv[2]
    with matplotlib.rc_context({
        'font.family': 'Noto Sans CJK JP'
    }):
        if arg == '-g':
            graph(data)

        elif arg == '-h':
            historgram(data)
