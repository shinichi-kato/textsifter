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
import MeCab

matplotlib.use('TkAgg')
tagger = MeCab.Tagger()

s_data = [
    1, 7, 2, 140, 9, 67, 4, 6, 21, 14, 191, 19, 114, 1, 6, 3,
    44, 5, 72, 132, 70, 99, 21, 16, 103, 77, 339, 1, 3, 4, 2,
    45, 38, 99, 6, 3, 6, 2, 127, 136, 149, 29, 20, 6, 1, 66,
    44, 3, 3, 8, 6, 1, 45, 143, 1, 17, 73, 22, 56, 10, 13, 15,
    4, 1, 2, 4, 26, 5, 5, 5, 2, 38, 8, 8, 227, 2, 5, 47, 7,
    187, 8, 5, 56, 12, 2, 13, 2, 59, 116, 9, 2, 4, 9, 3, 31,
    38, 31, 5, 6, 3, 1, 29, 13, 35, 3, 2, 10, 3, 3, 109, 50,
    2, 12, 8, 4, 1, 3, 23, 15, 5, 29, 30, 2, 13, 3, 9, 10,
    12, 15, 4, 5, 11, 4, 7, 5, 1, 43, 10, 17, 2, 7, 26, 3, 4, 3,
    2, 1, 2, 8, 6, 3, 3, 4, 1, 4, 15, 25, 30, 13, 3, 6, 1, 15, 1,
    1, 4, 1, 2, 2, 2, 3, 1, 8, 2, 2, 20, 4, 6, 5, 3, 27, 10, 9,
    6, 1, 6, 19, 3, 1, 1, 1, 8, 8, 7, 4, 13, 7, 9, 2, 2, 1, 2,
    5, 2, 1, 1, 1, 4, 2, 1, 10, 4, 4, 8, 5, 3, 2, 26, 2, 42, 3,
    2, 2, 4, 4, 5, 2, 13, 8, 9, 2, 4, 1, 5, 1, 1, 13, 20,
    19, 2, 2, 5, 6, 1, 5, 4, 13, 4, 1, 4, 9, 1, 14, 1, 1, 1,
    1, 3, 1, 30, 1, 8, 2, 2, 1, 14, 13, 32, 3, 2, 14, 2, 1,
    6, 7, 30, 17, 34, 12, 16, 13, 14, 2, 17, 9, 3, 7, 11, 6,
    2, 4, 10, 6, 5, 1, 1, 12, 5, 14, 16, 1, 11, 12, 1, 1, 1, 4,
    22, 1, 22, 2, 6, 7, 1, 4, 11, 9, 12, 3, 6, 1, 1, 4, 2, 4, 8,
    6, 7, 11, 1, 2, 6, 3, 9, 8, 4, 10, 1, 5, 3, 3, 3, 2, 4, 2,
    1, 3, 1, 1, 4, 2, 1, 1, 1, 1, 2, 3, 6, 3, 1, 7, 4, 9, 5,
    1, 1, 4, 2, 6, 3, 3, 2, 8, 1, 2, 1, 21, 10, 5, 2, 15, 5,
    10, 12, 2, 1, 3, 6, 3, 5, 10, 5, 7, 2, 4, 2, 1, 4, 5, 11,
    4, 5, 9, 1, 3, 4, 1, 3, 11, 5, 5, 1, 5, 8, 6, 1, 7, 8, 2, 3,
    1, 4, 9, 2, 4, 1, 3, 1, 3, 12, 4, 3, 6, 10, 5, 10, 7, 13, 15,
    4, 8, 1, 8, 4, 2, 4, 1, 10, 1, 7, 1, 3, 2, 2, 2, 3, 2, 1, 8,
    6, 3, 2, 3, 2, 1, 5, 8, 2, 1, 3, 2, 2, 1, 1, 8, 1, 1, 3, 1, 1,
    2, 2, 5, 2, 4, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 4, 5, 1, 3,
    8, 4, 1, 8, 6, 2, 1, 2, 3, 1, 2, 2, 1, 2, 1, 3, 1, 2, 5, 1, 8,
    2, 3, 1, 1, 1, 2, 2, 1, 2, 3, 4, 2, 1, 1, 1, 1, 1, 4, 1, 15,
    11, 3, 3, 1, 10, 4, 3, 3, 1, 2, 5, 19, 2, 2, 9, 2, 4, 1, 6, 1,
    12, 2, 2, 2, 4, 1, 2, 4, 1, 6, 4, 6, 2, 12, 1, 1, 1, 1, 2, 1, 2,
    1, 2, 5, 2, 1, 3, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 10, 6, 2, 1, 1,
    7, 2, 5, 3, 2, 1, 1, 1, 3, 7, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1,
    3, 1, 2, 5, 2, 3, 5, 6, 2, 1, 2, 1, 2, 1, 1, 2, 1, 1, 2, 3, 3,
    1, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 4, 1, 1, 7, 1, 2, 3, 1, 3,
    2, 1, 1, 1, 1, 1, 4, 3, 3, 2, 3, 3, 2, 3, 3, 4, 1, 1, 2, 1, 1,
    4, 5, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 1, 2, 2, 2, 7, 1, 1, 1,
    1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3,
    1, 1, 1, 4, 2, 1, 2, 1, 4, 1, 3, 1, 1, 1, 2, 2, 1, 1, 3, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 5, 1, 2, 1, 1, 2, 1, 14, 1,
    0, 18, 27, 14, 13, 1, 10, 10, 2, 12, 2, 3, 6, 3, 2, 9, 2, 2, 2,
    2, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1,
    1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2,
    2, 1, 1, 3, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1, 1, 1,
    1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 1, 3, 1, 1, 1, 1, 1, 1,
    2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1, 1, 1, 1, 1, 1
]


def historgram(data):
    count = [x[0]*len(data[x]) for x in data]
    count = [len(x) for x in count]
    plt.xlabel("次候補の数")
    plt.ylabel("頻度")
    plt.hist(count, density=True, range=(1, 100), color='tab:green',
             bins=100, alpha=0.5, label="形態素")
    plt.hist(s_data, density=True, range=(1, 100), color='tab:blue',
             bins=100, alpha=0.5, label=f"文字")
    plt.legend(loc='upper right')
    plt.show()
    # plt.savefig('hist.svg')
    # print(count)


def count(data):
    count = Counter({k:len(v) for k,v in data.items()}).most_common()
    
    print(count)
    y = [x[0] for x in count]
    width = [x[1] for x in count]
    plt.ylabel("次候補の数")
    plt.barh(y,width)
    plt.show()


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
    node_color = [(node_color[n]**0.5)*40+20 for n in node_keys]

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


def mor1gram(file):
    """
        文字列を形態素解析し、次にくる形態素を格納した辞書を作る
    """
    vocab = defaultdict(list)

    prev = "\f"
    for line in file:
        l = line.strip()
        nodes = tagger.parse(l).strip().split('\n')
        nodes.pop()

        for node in nodes:
            n = node.split('\t')
            vocab[prev].append(n[0])
            prev = n[0]

    return vocab


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(
            "mor1gram <input file> [-g]\n"
            "input fileを形態素ごとの1gramに変換したjsonを出力します。\n"
            "-g: グラフとして可視化\n"
            "-h: ヒストグラム")

    with open(sys.argv[1]) as f:
        data = mor1gram(f)
    print(json.dumps(data, ensure_ascii=False))
    args = sys.argv[2:]
    with matplotlib.rc_context({
        'font.family': 'Noto Sans CJK JP'
    }):
        while((arg := args.pop()) if args else False):
            if arg == '-g':
                graph(data)
            elif arg == '-c':
                count(data)
            elif arg == '-h':
                historgram(data)
