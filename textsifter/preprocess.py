"""
preprocess.py
"""

from collections import namedtuple
import MeCab
import json
import re


Node = namedtuple('Node', ['surface', 'pos', 'factor'])
RE_TAG_BODY = re.compile(r'^([0-9]+)\t(.*)?$')
tagger = MeCab.Tagger()


def _segment(text):
    nodes = tagger.parse(text).rstrip().split('\n')
    nodes.pop()  # EOS除去
    nodes = [node.split('\t') for node in nodes]

    return [Node(node[0], node[4], frozenset({node[3]}))
            for node in nodes]


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
                ]                                                    """
    terms = []
    di_terms = {}

    if term_json:
        terms = json.load(term_json)
        di_terms = {
            t['surface']: {
                'index': index,
                'pos': t['pos'],
                'factor': t['factor']
            } for index, t in enumerate(terms)
        }

    nodeslist = []

    for line in text:
        # phase1 - 対象単語を「\f[i}\t」に置換
        for term in di_terms:
            if term in line:
                dt = di_terms[term]
                index = dt['index']
                line = line.replace(term, f'\f{index}\t')

        # phase 2
        elems = []
        es = line.split('\f')
        for e in es:
            match = RE_TAG_BODY.match(e)
            if match:
                t = terms[int(match.group(1))]
                elems.append(Node(
                    t['surface'],
                    t['pos'],
                    frozenset(t['factor'])
                ))
                if match.group(2):
                    elems.extend(_segment(match.group(2)))
            else:
                elems.extend(_segment(e))

        nodeslist.append(elems)
    return nodeslist


def joint_suffix(nodeslist):
    text = []
    buff = None
    for nodes in nodeslist:
        line = []
        for node in nodes:
            if node.pos.startswith('接尾辞'):
                if buff:
                    buff = Node(
                        f"{buff.surface}{node.surface}",
                        f"{buff.pos} {node.pos}",
                        node.factor | buff.factor)
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
