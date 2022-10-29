"""
マルコフ連鎖辞書の出力

"""
import os
from collections import defaultdict


def bot_markov_chain(nodeslist, args):
    """ チャットボット用にマルコフ連鎖辞書を生成する。
        args.source : マルコフ辞書のidとしてファイル名の一部を使う
        args.format :'surface' or 'feature'
        args.outfile: 出力ファイル

        マルコフ連鎖辞書にはテキスト生成の起点がある。

        outfileの形式はjsonで以下の形式。
        "script": [
            {
                "in": [
                    "こんにちは"
                ],
                "out": [
                    "こんにちは"
                ]
            },
            {
                "in": ["{NOP}"],
                "out":["{NOP}"]
            },
        ]                                                     """

    """ markov連鎖 """

    chain = defaultdict(list)
    extractor = None

    def surface_extractor(node):
        return node.surface

    def feature_extractor(node):
        return f'{node.surface}({node.pos})'

    if args.format == 'surface':
        extractor = surface_extractor
    elif args.format == 'feature':
        extractor = feature_extractor

    header = args.source[0]
    header = os.path.splitext(os.path.basename(header))[0]
    headers = []

    for index, nodes in enumerate(nodeslist):
        prev = f'{"{"}{header}{index}{"}"}'
        headers.append(prev)

        for node in nodes:
            feat = extractor(node)
            chain[prev].append(feat)
            prev = feat

    chain['{start}'] = headers

    """ 次数が1のノードが連続したら一つにまとめる
        実装試験中                                  """

    dropping_keys = set()
    new_chain = {}

    for key in list(chain.keys()):
        if key in dropping_keys:
            continue

        if len(values := chain[key]) == 1:
            cursor = values[0]

            if (len(chain[cursor]) == 1):
                next = chain[cursor][0]
                dropping_keys |= {cursor, next}
                new_node = cursor+chain[cursor][0]
                new_chain[key] = [new_node]
                new_chain[new_node] = chain[next]
            else:
                new_chain[key] = values

        else:
            new_chain[key] = chain[key]

    """ チャットボット辞書に変換 """
    """ タグでないinに番号を割り当てる """

    index = 0
    index_dict = {}
    for key in new_chain.keys():
        if not key.startswith('{') or not key.endswith('}'):
            index_dict[key] = index
            index += 1

    """ valueの"理由を" → "理由を{name_node0}"に、
        keyの"理由を"→"{name_node0}"に変換          """

    script = []
    for key, values in new_chain.items():
        outs = []
        for value in values:
            if value in index_dict:
                outs.append(
                    f'{value}{"{"}{header}_node{index_dict[value]}{"}"}')
            else:
                outs.append(value)

        ins = None
        if not key.startswith('{') or not key.endswith('}'):
            ins = [f'{"{"}{header}_node{index_dict[key]}{"}"}']
        else:
            ins = [key]

        script.append({'in': ins, 'out': outs})

    return script
