# ライブラリのインポート
import json

def import_json(save_data_id: int) -> None:
    """
    JSONデータを読み込む
    save_data_id: セーブデータの番号(1～3)
    """
    with open(f"data/save_data/save_data_{save_data_id}.json", encoding="utf-8") as data:
        save_data = json.load(data)
    with open("data/monster.json", encoding="utf-8") as data:
        monster = json.load(data)
    with open("data/skill.json", encoding="utf-8") as data:
        skill = json.load(data)
    with open("data/fusion_tree.json", encoding="utf-8") as data:
        fusion_tree = json.load(data)
    return {
        "save_data": save_data,
        "monster": monster,
        "skill": skill,
        "fusion_tree": fusion_tree
    }