"""
preprocess.py

preprocessではテキストを形態素解析した後、各形態素を
Node(
    surface,  # 表層形(str)
    pos,      # 品詞(str)
    factor    # (基本形)または(frozenset({基本形, ...}),基本形)
)
というノード単位で扱う。
形態素解析直後、factorは形態素の基本形を格納したtupleである。
その後のテキスト処理でいくつかの形態素を結合して一つのNodeにする場合がある。
例えば「地震火災保険」の場合先行する地震と火災は順番があまり影響せず、
末尾の「保険」は位置を交換できない。つまり末尾が主概念で、その他がこれに従う
という関係とみなせる。これを、
( frozenset({従概念,従概念,...}), 主概念)
というデータ形式で表現する。tupleとfrozensetのみを使うことでNodeはhashableとなる。

"""

from collections import namedtuple
import MeCab
import json
import re


Node = namedtuple('Node', ['surface', 'pos', 'factor'])
RE_TAG_BODY = re.compile(r'^([0-9]+)\t(.*)?$')
tagger = MeCab.Tagger()


def morpho(text, term_json):
    """ テキストを読んでterm_jsonで定義された単語をNodeに変換し、
        それ以外の部分を形態素解析してnodeslistを生成する。各Nodeは
        以下のnamedtupleとする。

        Node(surface,pos,factor)

        termsは以下のように記述する。
                [
                    {
                        "surface": 表層形,
                        "pos": 
                        "factor": 基本形のリスト
                    },...
                ]

        なお、factorは基本形のリストで、基本形が複数ある場合は
        末尾の一つが主、その他が従とみなす                            """

    terms = []
    di_terms = {}

    if term_json:
        terms = json.load(term_json)
        terms = [Node(
            t['surface'],
            t['pos'],
            (tf[0],) if len(tf := t['factor']) == 1 else (frozenset(tf[:-1]), tf[-1]))
            for t in terms]
        di_terms = { t.surface: index for index, t in enumerate(terms) }

    nodeslist = []

    for line in text:
        # phase1 - 対象単語を「\f[i}\t」に置換
        for term in di_terms:
            if term in line:
                index = di_terms[term]
                line = line.replace(term, f'\f{index}\t')

        # phase 2
        elems = []
        es = line.split('\f')
        for e in es:
            match = RE_TAG_BODY.match(e)
            if match:
                elems.append(terms[int(match.group(1))])
                if match.group(2):
                    elems.extend(_segment(match.group(2)))
            else:
                elems.extend(_segment(e))

        nodeslist.append(elems)
    return nodeslist


def join_suffix(nodeslist):
    text = []
    buff = None
    for nodes in nodeslist:
        line = []
        for node in nodes:
            if node.pos.startswith('接尾辞'):
                if buff:
                    buff = Node(
                        surface=f"{buff.surface}{node.surface}",
                        pos=f"{buff.pos} {node.pos}",
                        factor=_merge_suffix(buff.factor, node.factor))
                    continue
                line.append(node)
            else:
                if buff:
                    line.append(buff)
            buff = node

        if buff:
            line.append(buff)
        text.append(line)

    return text


def _merge_suffix(node_factor, suffix_factor):
    """ node_factorにsuffix_factorを結合した新しいfactorを返す。
        (小型,) (化,) → (小型化,)
        (frozenset({豚骨}),しょうゆ) (味,) → (frozenset({豚骨}),しょうゆ味)
        のように、末尾のfactor飲みを結合する                                 """

    if len(node_factor) == 1:
        return (f"{node_factor[0]}{suffix_factor[0]}",)
    else:
        return (node_factor[0], f"{node_factor[1]}{suffix_factor[0]}")

# ---------------------------------------------------------------------------------------
#
# join_kakujoshi
#
# ---------------------------------------------------------------------------------------


def join_kakujoshi(nodeslist):
    """ 助詞の「が」、「と」、「から」はいずれも格助詞と接続助詞の両方がある。
        鳥が/が(助詞-格助詞) 捕まったが/が(助詞-接続助詞)
        姉と/と(助詞-格助詞) 春になると/と(助詞-接続助詞)
        駅から/から(助詞-格助詞) 歩くから/から(助詞-接続助詞)
        これらを区別するため、
        体言(名詞、代名詞)＋格助詞の並びを結合し
        
        Node(鳥が, 主語, (frozenset({鳥})),が)
        
        とする。なお、join_kakujoshiはlex/concept.pyに吸収予定            """
    
    text = []
    buff = None
    for nodes in nodeslist:
        line = []
        for node in nodes:
            if node.pos == '助詞-格助詞':
                if buff:
                    buff = Node(
                        surface=f"{buff.surface}{node.surface}",
                        pos=f"{buff.pos} {node.pos}",
                        factor=_merge_left(buff.factor, node.factor))
                    continue
                line.append(node)
            else:
                if buff:
                    line.append(buff)
            buff = node

        if buff:
            line.append(buff)
        text.append(line)

    return text


def _merge_left(newbie, oldie):
    """ oldie ファクターにne_factorwbieファクターの内容を結合した新しいfactorを返す
        (しょうゆ, ) (ラーメン,) → (frozenset({しょうゆ}), ラーメン)
        (豚骨,) (frozenset({しょうゆ}),ラーメン) → (frozenset({豚骨,しょうゆ}),ラーメン)
        のように、"""

    if len(oldie) == 1:
        if len(newbie) == 1:
            return (frozenset({newbie[0]}), oldie[0])
        else:
            return (newbie[0] | frozenset({newbie[1]}), oldie[0])
    else:
        if len(newbie) == 1:
            return (frozenset({newbie[0]}) | oldie[0], oldie[1])
        else:
            return (newbie[0] | frozenset({newbie[1]}) | oldie[0], oldie[1])


# -----------------------------------------------------------------------------
#
# excluse_stopword
#
# -----------------------------------------------------------------------------

def exclude_stopword(nodeslist, stop_word):
    """ 形態素解析後のnodeslistを検査し、表層形がstopwordに含まれる
        場合その単語を除外する。stopwordは表層形を一行一単語で
        保存したものとする。#で始まる行はコメント行として扱う       """

    stopwords = stop_word.readlines()
    stopwords = {x.strip() for x in stopwords if not x.startswith('#')}

    return [
        [n for n in nodes if n.surface not in stopwords]
        for nodes in nodeslist
    ]


def filter():
    """ セリフ部分のみ、または地の文のみを抽出する"""
    pass


def filter_nva(nodeslist):
    """ 名詞、動詞、形容詞、形状詞のみを残す """
    return [
        [n for n in nodes if n.pos.split('詞',1)[0] in {'名','動','形容','形状'}]
        for nodes in nodeslist
    ]


def _segment(text):
    nodes = tagger.parse(text).rstrip().split('\n')
    nodes.pop()  # EOS除去
    nodes = [node.split('\t') for node in nodes]

    return [Node(node[0], node[4], (node[3],))
            for node in nodes]
