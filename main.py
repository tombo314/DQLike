# クラスのインポート
from user_info import user_info
from window import window
from battle import battle
from fusion import fusion
from map import map

# 味方パーティーを設定
user_info.set_friend(["スライム", "ドラキー", "ギュメイ将軍"])

# 味方パーティーを設定
battle.set_friend(user_info.friend)
# # 敵パーティーを設定
# battle.set_enemy(["スライム", "ゴースト", "ゲルニック将軍"])
# battle.init_param()
# battle.draw_ui()

# マップを表示
map.run()

"""
To Do

"""
"""
Memo

"""