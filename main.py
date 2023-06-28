# セーブデータをロード
from json_data import json_data
json_data.select_save_data()

# クラスをインポート
from user_info import user_info
from map import map_

# 味方パーティーを設定
user_info.set_friend([
    {"id": 1, "name": "スライム", "level": 1, "gear": None, "valid": True},
    {"id": 3, "name": "ゴーレム", "level": 1, "gear": None, "valid": True},
    {"id": 20, "name": "ギュメイ将軍", "level": 1, "gear": None, "valid": True}
])

# マップを表示
map_.run()

"""
To Do

"""
"""
メモ

・rangeはsingleかallのどちらか
・自傷ダメージのある攻撃は、range=singleのみ
・モンスター名の文字数の上限は、全角で8文字
・任意の親の組み合わせから、配合で作られる子モンスターの候補数は12以下
"""