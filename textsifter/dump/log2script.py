"""
log2script.py
ログ→スクリプト変換

ログファイルをチャットボットのスクリプトに変換する。
ログファイルはJ-TOCC20220829の形式に対応する。
http://nakamata.info/database/

n行をIN、n+1行をoutとするスクリプトとして出力する。
dataは前処理により代名詞のposが{I}や{YOU}となっている。
in,outともに表層語彙の代わりに{I}や{YOU}を用いる
"""
import datetime
import re
import json
from .. import DI_PRONOUN

RE_PROMPT = re.compile(r'（[A-Z]-[0-9]+-[0-9A-Za-z]+：[^) ]+）')

SETTINGS_TEMPLATE = {
    "description": "",
    "updatedAt": "",
    "creator": "",
    "avatarDir": "",  # biomeセルでは利用しない
    "backgroundColor": "",  # biomeセルでは利用しない
    "encoder": "LogEncoder",
    "stateMachine": "EnterlessStateMachine",
    "decoder": "HarvestDecoder",
    "precision": 0.5,
    "retention": 0.7,
    "convolution": 0.3,
    "memory": {
        "{BOT_NAME}":["アルファ"],
    },
    "biome": [],
    "script": []
}


def log2script(data, args):
    """ J-TOCC形式の会話ログを読む

        J-TOCC形式では以下のように話者名と本文が全角コロンで区切られ、
        
        ```
        W-302-1F：ゲームのほうが【人名：１人称】はこれまだあれかも。
        W-302-2F：うんうんうん。
        W-302-1F：ゲームキューブ、Wii、（W-302-2F：うん）、DS。
        ```
        本文で用いられる表記には以下のような対応をする。
        【人名：１人称】 : →{MY_NAME}に置き換える
        【人名：２人称】 : →{YOUR_NAME}に置き換える
        【人名：３人称】 : 任意の人名。そのまま
        【地名】【学校名】: ふせられた固有名詞。そのまま
        （W-302-2F：うん）: 発話中に重なった相づち→削除
        ● : 聞き取れなかった語句→そのまま
        〓一度〓: 確信が持てなかった部分→〓を削除　          """

    script = []
    prev = None
    for line in data:

        surface = "".join(
            [n.pos if n.pos in DI_PRONOUN else n.surface for n in line])

        """ 行頭の発言者IDを削除"""
        surface = "".join(surface.split('：', 1)[1])

        """ 人称を置き換え """
        surface = (surface
                   .replace('【人名：１人称】', '{MY_NAME}')
                   .replace('【人名：２人称】', '{YOUR_NAME}')
                   .replace('〓', '')
                   )

        """ 相槌を削除"""
        surface = RE_PROMPT.sub('', surface)

        if prev:
            script.append({
                'in': [prev],
                'out': [surface]
            })
        prev = surface

    today = datetime.datetime.today()
    today = today.strftime('%Y/%m/%d %H:%M:%S')
    SETTINGS_TEMPLATE['updatedAt'] = today
    SETTINGS_TEMPLATE['memory'] = {k:list(v) for k,v in DI_PRONOUN}
    SETTINGS_TEMPLATE['script'] = script

    settings = json.dumps(SETTINGS_TEMPLATE, ensure_ascii=False)
    return settings
