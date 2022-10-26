"""
main.py
====================
テキストファイルを読み込み、前処理、可視化及びマルコフ連鎖辞書の生成を行う。

以下の前処理をオプションで行う
* 〜化のような接尾辞を結合
* 助詞+動詞を結合

マルコフ連鎖生成では以下のプションが使える
* 逆順化
* 

"""
import sys
import argparse
from textsifter import preprocess


def squeeze(files, encoding):
    if len(files) == 1:
        with open(files[0], encoding=encoding) as f:
            return f.readlines()

    data = []
    for file in files:
        with open(file, encoding=encoding) as f:
            r = f.read()

            data.append(r.replace('\n', ''))
    return data


def plot(data, args):
    if 'common_central' in args:
        from textsifter.plot.common_central import common_central
        common_central(data, args.mode, args.common_central)
    elif 'network' in args:
        if args.mode == 'cooccurrence':
            from textsifter.plot.cooc_network import cooccurrence_network
            cooccurrence_network(data, args.network)
        elif args.mode == 'markov':
            from textsifter.plot.markov_network import markov_network
            markov_network(data, args.network)


def dump(data, args):
    if args.mode=='cooccurrence':
        from textsifter.dump.cooc_mtx import cooccurrence_matrix
        cooccurrence_matrix(data,args)
    print(args)


def main():
    parser = argparse.ArgumentParser(
        prog="sifter",
        description='''
            一つまたは複数のテキストファイルを処理し可視化やマルコフ連鎖化を行います。
            テキストファイルが一つの場合一行を共起単位とみなします。
            テキストファイルが複数の場合一ファイルを一行に変換し、共起単位とします。
            '''
    )
    parser.add_argument('source', nargs='+', type=str,
                        help='テキストファイル(複数可能)')
    parser.add_argument('-e', '--encoding', type=str, default="utf-8",
                        help='テキストの文字コードを指定')
    parser.add_argument('-t', '--term_file', type=str,
                        help="前処理: TERM_FILEで指定した語句をNode化し形態素解析で分割する")
    parser.add_argument('-ff', '--fix_fragment', action="store_true",
                        help="前処理: 名詞+接尾辞、名詞+格助詞を一つのノードに結合")
    parser.add_argument('-s', '--stopword', type=str,
                        help='前処理: 指定した語句を解析から除外する。STOPWORDには除外する形態素の表層形を一行一つ記載する')
    parser.add_argument('--mode', choices=['markov', 'cooccurrence'], default='cooccurrence',
                        help='markov:マルコフ連鎖, cooccurrence:共起性を計算します')

    subparsers = parser.add_subparsers()

    # plot - 可視化サブコマンド
    parser_plot = subparsers.add_parser('plot', help='可視化')
    parser_plot.add_argument('--common_central', type=int, default=argparse.SUPPRESS, nargs='?',
                             help='ノードの頻度-次数プロットを表示します。0以下の値を指定すると全表示します')
    parser_plot.add_argument('--network', type=int, default=argparse.SUPPRESS, nargs='?',
                             help='マルコフ連鎖または共起のネットワークを表示します。次数が上位X件のエッジに限定します')
    parser_plot.set_defaults(subcommand_func=plot)

    # dump - 辞書生成のサブコマンド
    parser_dump = subparsers.add_parser('dump',
                                        help='ファイル出力')
    parser_dump.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                             help="出力ファイルのパス(省略時は標準出力)")
    parser_dump.add_argument('-f', '--format', choices=['surface', 'feature'], default='surface',
                             help='surface:表層語彙を出力, feature:"表層語彙(品詞)"を出力')
    parser_dump.add_argument('-s', '--separator', choices=['comma', 'space'], default='space',
                             help="出力をの区切り文字を指定(省略時はスペース区切り)")
    parser_dump.set_defaults(subcommand_func=dump)

    args = parser.parse_args()

    mode = "マルコフ連鎖" if args.mode == 'markov' else "共起性"
    print(f"{mode}を計算します。")

    # sourceが複数ファイルなら一ファイルを一行にまとめる

    data = squeeze(args.source, args.encoding)

    # 前処理
    term_file = open(
        args.term_file, encoding=args.encoding) if args.term_file else None
    data = preprocess.morpho(data, term_file)

    if args.stopword:
        data = preprocess.exclude_stopword(data, open(
            args.stopword, encoding=args.encoding))

    if args.fix_fragment:
        data = preprocess.join_suffix(data)
        data = preprocess.join_kakujoshi(data)

    if args.subcommand_func:
        args.subcommand_func(data, args)
    else:
        parser.print_help()
        print(parser_plot.print_help())


if __name__ == '__main__':
    main()
