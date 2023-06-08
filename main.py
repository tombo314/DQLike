# セーブデータをロード
from json_data import json_data
json_data.select_save_data()

# クラスをインポート
from user_info import user_info
from map import map_

# 味方パーティーを設定
user_info.set_friend(["スライム", "ドラキー", "ギュメイ将軍"])

# マップを表示
map_.run()

"""
To Do

・ゲルニック将軍を実装する
    -> ルカナン
・味方パーティーをモンスターボックス内で編成できるようにする
・モンスター配合所を作る
    -> Fusionクラスを作る
・ゲーム終了ボタンを作る
    -> Escapeで画面が閉じないようにする
・エンカウントする敵をランダムにする
・倒した敵が一定の確率で仲間になるようにする
・ぴぽや倉庫から、モンスター配合所のような写真を持ってくる
"""
"""
メモ

・自傷ダメージのある攻撃は、range=singleのみ
・モンスター名の文字数の上限は、全角で8文字
"""