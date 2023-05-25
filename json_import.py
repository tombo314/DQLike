# ライブラリのインポート
import json

# JSONデータを読み込む
with open("data/monster.json", encoding="utf-8") as data:
    monster = json.load(data)
with open("data/user.json", encoding="utf-8") as data:
    user = json.load(data)
with open("data/skill.json", encoding="utf-8") as data:
    skill = json.load(data)
with open("data/fusion_tree.json", encoding="utf-8") as data:
    fusion_tree = json.load(data)