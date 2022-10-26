"""
共起モードでのデータのファイル出力
vocabと共起行列
"""
import numpy as np

from textsifter.core import cooccurrence


def cooccurrence_matrix(nodeslist, args):
    """ 共起行列のファイル出力 """

    cooc = cooccurrence(nodeslist)

    np.save(args.outfile, {
        'vocab': cooc.vocab,
        'matrix': cooc.matrix
    })
