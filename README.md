# Textsifter

テキストをチャットボット用のマルコフ連鎖型辞書に変換

## Description

テキストやログの内容をマルコフ連鎖に変換し、チャットボットで使用できる辞書にします。
深層学習のような方法で作られた辞書は人間可読性が低く、不適切な発言を削除したり
チャットボットの反応を追加するといった作業が困難です。
そこで比較的可読性のあるマルコフ連鎖を用い、さらに以下のような処理を行うことで
拡張性や編集性の高い辞書を生成します。

* 助詞と動詞の結合 
* 文末から文頭に向かうマルコフ連鎖生成 
* セリフと地の文の区別


■文末からのマルコフ連鎖生成
日本語では「犬が好き」「りんごが好き」のように主語や目的語より後ろに動詞が現れます。
文頭からのマルコフ連鎖では
犬→が, りんご→が, が→好き
のようになります。一方文末からのマルコフ連鎖では 
好き
この方法で作られた辞書は人間が拡張したり不適切な反応を除去しやすいことが望ましい

■文末からのマルコフ連鎖辞書生成
日本語では「犬が好き」「ネコが好き」のように

■ 助詞を分離しない
日本語では「犬が好き」「ネコが好き」のように

## Getting Started

### Prerequisities

* python 3.8


### Installing

```
python -m venv .venv
```
次に`source .venv/bin/activate`でvenvを有効化する。
vscodeの場合は`Ctrl-Shift-p` で Python: Select Interpreterを選び、.venvが有効なインタプリタを選ぶ

ターミナルで(.venv)が表示された状態になっているのを確認し、以下のコマンドを実行
```
pip -m requirements.txt
sudo apt-get install python3-tk
```

### Executing program

* How to run the program
* Step-by-step bullets
```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)