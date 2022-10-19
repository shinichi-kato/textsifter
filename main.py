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


def compile(data, args):

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
    parser.add_argument('-m', '--morpho', action="store_true",
                        help="前処理: 形態素解析")
    parser.add_argument('-t', '--term_file', type=open,
                        help="前処理: TERM_FILEで指定した語句をNode化し形態素解析で分割する")
    parser.add_argument('-ff', '--fix_fragment', action="store_true",
                        help="前処理: 名詞+接尾辞、名詞+格助詞を一つのノードに結合")
    parser.add_argument('-s', '--stopword', type=open,
                        help='前処理: 指定した語句を解析から除外する。STOPWORDには除外する形態素の表層形を一行一つ記載する')
    parser.add_argument('--mode', choices=['markov','cooccurrence'], default='markov',
                   help='markov:マルコフ連鎖, cooccurrence:共起性を計算します')

    subparsers = parser.add_subparsers()

    # plot - 可視化サブコマンド
    parser_plot = subparsers.add_parser('plot', help='可視化')
    parser_plot.add_argument('--common_central', type=int, default=argparse.SUPPRESS, nargs='?',
                             help='ノードの頻度-次数プロットを表示します。0以下の値を指定すると全表示します')
    parser_plot.add_argument('--network', type=int, default=argparse.SUPPRESS, nargs='?',
        help='指定した数のノードを')
    parser_plot.set_defaults(subcommand_func=plot)

    # compile - 辞書生成のサブコマンド
    parser_compile = subparsers.add_parser('compile',
                                           help='ファイル出力')
    cgroup = parser_compile.add_mutually_exclusive_group()
    cgroup.add_argument('-f', '--feature', action='store_true',
                        help="表層+品詞を出力")
    cgroup.add_argument('-s', '--surface', action='store_true',
                        help="表層形を出力")
    parser_compile.add_argument('-c', '--comma', action='store_true',
                                help="出力をカンマ区切りに(省略時はスペース区切り)")
    parser_compile.set_defaults(subcommand_func=compile)

    args = parser.parse_args()

    mode = "マルコフ連鎖" if args.mode == 'markov' else "共起性"
    print(f"{mode}を計算します。")

    # sourceが複数ファイルなら一ファイルを一行にまとめる

    data = squeeze(args.source, args.encoding)

    # 前処理
    if args.morpho or args.term_file or args.fix_fragment or args.stopword:
        data = preprocess.morpho(data, args.term_file)

    if args.stopword:
        data = preprocess.exclude_stopword(data, args.stopword)

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
