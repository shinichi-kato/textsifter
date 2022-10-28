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
            chain[prev].append(extractor(node))
            prev = extractor(node)
        
    del chain['。']

    """ タグでないinに番号を割り当てる """
    index=0
    index_dict={}
    for key in chain.keys():
        if not key.startswith('{') or not key.endswith('}'):
            index_dict[key] = index
            index += 1
    
    """ valueの"理由を" → "理由を{name_node0}"に、
        keyの"理由を"→"{name_node0}"に変換          """
    
    script = []
    for key, values in chain.items():
        outs=[]
        for value in values:
            if value in index_dict:
                outs.append(f'{value}{"{"}{header}_node{index_dict[value]}{"}"}')
            else:
                outs.append(value)

        ins = None
        if not key.startswith('{') or not key.endswith('}'):
            ins=[f'{"{"}{header}_node{index_dict[key]}{"}"}']
        else:
            ins=[key]
            
        script.append({'in':ins,'out':outs})

    return script



