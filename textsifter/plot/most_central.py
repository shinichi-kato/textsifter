"""
most_central.py
"""
from collections import defaultdict, Counter
from textsifter.preprocess import Node


def most_central(nodeslist, mode, top_most):
    """
    modeが='markov'の場合はマルコフ連鎖を、'cooccurrence'の場合は共起性を計算します。
    
    形態素解析済みのnodeslistを受取り、上位top_most個の単語について
    マルコフ連鎖の場合は

    node    c   next_nodes
    -----------------------------
    の      5   で,島,
    を      3   

    共起性の場合は

    node    c   co_occured_nodes
    -----------------------------
    の      5   で,島,
    を      3   

    のような表を表示します。

    """
    node = nodeslist[0][0]
    if isinstance(node, Node):
        
        if mode == 'markov':
            data = _most_central_node_markov(nodeslist)
        elif mode == 'cooccurrence':
            data = _most_central_node_cooccur(nodeslist)

    elif isinstance(node, str):
        if mode == 'markov':
            data =  _most_central_surf_markov(nodeslist)
        elif mode == 'cooccurrence':
            data = _most_central_surf_cooccur(nodeslist)

    """ top_mostのスライス"""

    top_most = top_most or 10

    print(f"表示件数指定:{top_most}件 / 全単語{len(data)}")

    if top_most>0:
        data = data[:top_most]
    

    """ table 整形 """

    value_label = "next_nodes" if mode == 'markov' else 'co_occurred_nodes'
    label = f'surface,  count, {value_label}'

    print(label)
    for node,nexts in data:
        print(f'{node:12},  {len(nexts):3},  {nexts}')


def _most_central_node_markov(nodeslist):
    vocab = defaultdict(list)
    
    for nodes in nodeslist:
        prev = '\f'
        for node in nodes:
            vocab[prev].append(node.surface)
            prev = node.surface

    vcount = Counter({node: len(nexts) for node, nexts in vocab.items()})

    return [(n[0], vocab[n[0]]) for n in vcount.most_common()]


def _most_central_surf_markov(nodeslist):
    vocab = defaultdict(set)

    for nodes in nodeslist:
        prev = '\f'
        for node in nodes:
            vocab[prev].append(node)
            prev = node

    vcount = Counter({node: len(nexts) for node, nexts in vocab.items()})

    return [(n, vocab[n]) for n in vcount.most_common()]



def _most_central_node_cooccur(nodeslist):
    return []


def _most_central_surf_cooccur(nodeslist):
    return [] 

