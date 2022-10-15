"""
キャラクタごとの2-gram辞書を生成
"""
from collections import defaultdict, Counter
import json
import random
import sys
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import mor1gram

matplotlib.use('TkAgg')


def historgram(data):
    count = [x[0]*len(data[x]) for x in data]
    count = [len(x) for x in count]
    plt.xlabel("次候補の数")
    plt.ylabel("頻度")
    plt.hist(count, density=True, range=(1, 100),  bins=100,
             alpha=0.5, color='tab:red', label="bi-gram")
    plt.hist(mor1gram.s_data, density=True, range=(1, 100), bins=100,
             alpha=0.5, color='tab:blue', label="uni-gram")
    plt.legend(loc='upper right')
    plt.show()
    # plt.savefig('hist.svg')
    print(count)


def chr2gram(file):
    vocab = defaultdict(list)
    prev = "\f\f"
    for line in file:
        nl = f"\f\f{line}"
        for i in range(1, len(nl)):
            vocab[prev].append(nl[i])
            prev = nl[i-1:i+1]

    return vocab


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(
            "chr1gram <input file> [-g]\n"
            "input fileを文字ごとの2gramに変換したjsonを出力します。\n"
            "-s: 出現頻度とグラフとして可視化\n"
            "-h: ヒストグラム")

    with open(sys.argv[1]) as f:
        data = chr2gram(f)

    arg = sys.argv[2]
    with matplotlib.rc_context({
        'font.family': 'Noto Sans CJK JP'
    }):
        # if arg == '-g':
        #     graph(data)

        print(data)

        if arg == '-h':
            historgram(data)
