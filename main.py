# クラスをインポート
from user_info import user_info
from map import map

# 味方パーティーを設定
user_info.set_friend(["スライム", "ドラキー", "ギュメイ将軍"])

# マップを表示
map.run()

"""
To Do

・ゲルニック将軍を実装する
    -> ルカナン
"""
"""
メモ

・自傷ダメージのある攻撃は、range=singleのみ
"""