"""
log2script.py
ログ→スクリプト変換

ログファイルをチャットボットのスクリプトに変換する。
ログファイルはJ-TOCC20220829の形式に対応する。
http://nakamata.info/database/

 n行をIN、n+1行をoutとするスクリプトとして出力
"""

def log2scipt(data):
    """ 前処理 """
    for line in data:
        print(line)

