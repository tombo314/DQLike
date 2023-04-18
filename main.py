from pprint import pprint
from random import randint, uniform
import tkinter as tk
import json
import numpy as np

class Battle:
    def __init__(self, enemy:list, friend: list) -> None:
        """
        バトルのインスタンスを生成する
        enemy: 敵のパーティー
        friend: 味方のパーティー
        """
        self.enemy = enemy
        self.friend = friend
        # UIを生成する
        # 0がenemy, 1がfriend
        self.name_box = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.name_text = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.hp_box = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.hp_text = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.mp_box = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.mp_text = [
            {mons["name"]: 0 for mons in enemy},
            {mons["name"]: 0 for mons in friend}
        ]
        self.__make_element(enemy, "name", False)
        self.__make_element(enemy, "hp", False)
        self.__make_element(enemy, "mp", False)
        self.__make_element(friend, "name", True)
        self.__make_element(friend, "hp", True)
        self.__make_element(friend, "mp", True)
        # バトル時のパラメータ
        self.hp = [
            {mons["name"]: mons["hp"] for mons in enemy},
            {mons["name"]: mons["hp"] for mons in friend}
        ]
        self.mp = [
            {mons["name"]: mons["mp"] for mons in enemy},
            {mons["name"]: mons["mp"] for mons in friend}
        ]
        self.attack = [
            {mons["name"]: mons["attack"] for mons in enemy},
            {mons["name"]: mons["attack"] for mons in friend}
        ]
        self.magic_attack = [
            {mons["name"]: mons["magic_attack"] for mons in enemy},
            {mons["name"]: mons["magic_attack"] for mons in friend}
        ]
        self.deffense = [
            {mons["name"]: mons["deffense"] for mons in enemy},
            {mons["name"]: mons["deffense"] for mons in friend}
        ]
        self.agility = [
            {mons["name"]: mons["agility"] for mons in enemy},
            {mons["name"]: mons["agility"] for mons in friend}
        ]
        self.dead = [
            {mons["name"]: False for mons in enemy},
            {mons["name"]: False for mons in friend}
        ]
    
    def __make_element(self, party: list, type_: str, is_friend: bool) -> None:
        """
        敵と味方のUIを生成する
        party: 敵か味方のモンスター3体
        type: 「name」「hp」「mp」のいずれか
        is_enemy: 敵の要素であるかどうか
        """
        y = -1
        color = ""
        if type_=="name":
            y = 100
        elif type_=="hp":
            y = 160
        elif type_=="mp":
            y = 220
        if is_friend==True:
            color = "#3f3"
            y += 250
        elif is_friend==False:
            color = "#f33"
        i = 0
        # パーティーのモンスターのUIを表示する
        for mons in party:
            start_x, start_y = 220*i+100, y
            width, height = 160, 40
            end_x, end_y = start_x+width, start_y+height
            # 四角形を表示する
            self.name_box[is_friend][mons[type_]] = canvas.create_rectangle(
                start_x, start_y,
                end_x, end_y,
                fill = "#ddd",
                outline = color
            )
            content = ""
            if type_=="name":
                content = mons[type_]
            elif type_=="hp" or type_=="mp":
                content = f"{mons[type_]} / {mons[type_]}"
            # テキストを表示する
            self.name_text[is_friend][mons[type_]] = canvas.create_text(
                (start_x+end_x)/2, (start_y+end_y)/2,
                text = content
            )
            i += 1

    def battle_start_auto(self):
        """
        バトルを開始する（自動）
        """
        # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
        while any([self.dead[0][mons["name"]]==False for mons in self.enemy]) and any([self.dead[1][mons["name"]]==False for mons in self.friend]):
            # 各ターンの処理
            order = []
            for mons in self.enemy:
                r = uniform(0.8, 1.2)
                order.append([r*mons["agility"], mons["name"]])
            for mons in self.friend:
                order.append([r*mons["agility"], mons["name"]])
            order.sort(reverse=True)
            
    
    def battle_start_manual(self):
        """
        バトルを開始する（手動）
        """

def battle(party_enemy: list, party_friend: list) -> None:
    """
    バトルを行う
    party_enemy: 敵のパーティーの配列
    party_friend: 味方のパーティーの配列
    """
    btl = Battle(party_enemy, party_friend)
    btl.battle_start_auto()

def is_n_percent(prob: int) -> bool:
    """
    probパーセントの確率でTrueを返す
    prob: Trueが返ってくる確率(0~100)
    """
    r = randint(1, 100)
    if r<=prob:
        return True
    return False

def select_skill(skill: dict) -> str:
    """
    スキルを選択する
    skill: keyにスキル名、valueに確率
    """
    return np.random.choice(list(skill.keys()), p=list(skill.values()))

def calc_damage(skill_name: str, attack: int, magic_attack: int, deffense: int, attribute_damage: dict, is_physics: bool) -> int:
    """
    ダメージを計算する
    skill_name: スキル名
    attack: 物理攻撃力
    magic_attack: 呪文攻撃力
    deffense: 物理防御力
    attribute_damage: 属性耐性
    is_physics: 物理攻撃かどうか
    """

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
    monster = data["monster"]
    skill = data["skill"]

# Tkinterの初期設定
app = tk.Tk()
app.title("DQLike")
canvas = tk.Canvas(
    app,
    width = 850,
    height = 600
)
canvas.pack()

battle([
        monster["スライム"],
        monster["ドラキー"],
        monster["ゴースト"]
    ],
    [
        monster["スライム"],
        monster["ドラキー"],
        monster["ボストロール"]
    ]
)

app.mainloop()