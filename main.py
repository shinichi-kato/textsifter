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

            data.append(r.replace('\n', '')
                        )
    return data


def plot(args):
    print("Execute visualize command")
    print(args)


def compile(args):

    print("Execute markov command")
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
    parser.add_argument('-js', '--joint_suffix', action="store_true",
                        help="前処理: 名詞+接尾辞を一つのノードに結合")
    parser.add_argument('-s', '--stopword', type=open,
                        help='前処理: 指定した語句を解析から除外する。STOPWORDには除外する形態素の表層形を一行一つ記載する')

    subparsers = parser.add_subparsers()

    # plot - 可視化サブコマンド
    parser_plot = subparsers.add_parser('plot', help='可視化')
    parser_plot.add_argument('--bar', type=str, help='bar help')
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

    print(args)

    # sourceが複数ファイルなら一ファイルを一行にまとめる

    data = squeeze(args.source, args.encoding)

    # 前処理
    if args.morpho or args.term_file or args.joint_suffix or args.stopword:
        data = preprocess.morpho(data, args.term_file)

    if args.stopword:
        data = preprocess.exclude_stopword(data, args.stopword)

    if args.joint_suffix:
        data = preprocess.joint_suffix(data)

    if args.subcommand_func:
        args.subcommand_func(args)
    else:
        parser.print_help()
        print(parser_plot.print_help())


if __name__ == '__main__':
    main()
