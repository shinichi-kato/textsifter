from textsifter.preprocess import Node
import pandas as pd
from matplotlib import font_manager


def mk_node2name(nodeslist):
    """ nodeslistを調べて
        surfaceが同一でfactorが異なる場合は
            surface = なる(成る)
            surface = なる(為る)

        surfaceが異なりfactorが同一の場合は
            surface = MLCC|積層セラミックコンデンサ

        となるようなnode->surface辞書を生成して返す      """

    node2name = {}

    data = [[n.surface, n.pos, n.factor] for nodes in nodeslist for n in nodes]
    df = (pd.DataFrame(data, columns=['surface', 'pos', 'factor'])
          .drop_duplicates())

    """ surfaceが同一でfactorが異なるnode """
    dfs = df[df.duplicated('surface', keep=False)]
    for row in dfs.itertuples():
        factors = _squeeze_factor(row.factor)
        node2name[Node(row.surface, row.pos, row.factor)
                  ] = f'{row.surface}({"-".join(factors)})'

    """ factorが同一でsurfaceが異なるnode """
    dff = df[df.duplicated('factor', keep=False)]
    for row in dff.itertuples():
        factors = _squeeze_factor(row.factor)
        node2name[Node(row.surface, row.pos, row.factor)
                  ] = f'{row.surface}({"-".join(factors)})'

    return node2name


def _squeeze_factor(factor):
    factors = [factor[-1]]
    if len(factor) == 2:
        factors.extend(list(factor[0]))
    return factors


def find_font():
    fonts = {f.name for f in font_manager.fontManager.ttflist}
    knowns = {'Noto Sans CJK JP', 'Meiryo'}
    for k in knowns:
        if k in fonts:
            return k


FONT_FAMILY = find_font()