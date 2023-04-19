from pprint import pprint
from random import randint, uniform
from time import sleep
from math import ceil
from json import load
from numpy.random import choice
import tkinter as tk

class Battle:
    def __init__(self, enemy:list, friend: list) -> None:
        """
        バトルのインスタンスを生成する
        enemy: 敵のパーティー
        friend: 味方のパーティー
        """
        self.enemy = enemy
        self.friend = friend
        # 0がenemyのUI, 1がfriendのUI
        self.name_box = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        self.name_text = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        self.hp_box = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        self.hp_text = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        self.mp_box = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        self.mp_text = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend}
        ]
        # モンスタ―とUIの座標の対応関係
        # (monster_name, is_friend): (start_x, start_y)
        self.elem_coord = {}
        # 敵と味方のUIを生成する
        self.__make_party(enemy, "name", False)
        self.__make_party(enemy, "hp", False)
        self.__make_party(enemy, "mp", False)
        self.__make_party(friend, "name", True)
        self.__make_party(friend, "hp", True)
        self.__make_party(friend, "mp", True)
        # バトル時のパラメータ
        self.hp = [
            {monster[name]["name"]: monster[name]["hp"] for name in enemy},
            {monster[name]["name"]: monster[name]["hp"] for name in friend}
        ]
        self.mp = [
            {monster[name]["name"]: monster[name]["mp"] for name in enemy},
            {monster[name]["name"]: monster[name]["mp"] for name in friend}
        ]
        self.attack = [
            {monster[name]["name"]: monster[name]["attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["attack"] for name in friend}
        ]
        self.magic_attack = [
            {monster[name]["name"]: monster[name]["magic_attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["magic_attack"] for name in friend}
        ]
        self.deffense = [
            {monster[name]["name"]: monster[name]["deffense"] for name in enemy},
            {monster[name]["name"]: monster[name]["deffense"] for name in friend}
        ]
        self.agility = [
            {monster[name]["name"]: monster[name]["agility"] for name in enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in friend}
        ]
        self.dead = [
            {monster[name]["name"]: False for name in enemy},
            {monster[name]["name"]: False for name in friend}
        ]
    
    def __make_party(self, party: list[str], type_: str, is_friend: bool) -> None:
        """
        UIを生成する
        party: 敵か味方のモンスター3体
        type: 「name」「hp」「mp」のいずれか
        is_friend: 敵の要素であるかどうか
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
        for name in party:
            start_x, start_y = 220*i+100, y
            # モンスター名とモンスターの敵・味方の区分と、UIの座標を対応付ける
            self.elem_coord.update({(name, type_, is_friend): (start_x, start_y)})
            width, height = 160, 40
            end_x, end_y = start_x+width, start_y+height
            # 四角形を表示する
            self.name_box[is_friend][monster[name][type_]] = canvas.create_rectangle(
                start_x, start_y,
                end_x, end_y,
                fill = "#ddd",
                outline = color
            )
            content = ""
            if type_=="name":
                content = monster[name][type_]
            elif type_=="hp" or type_=="mp":
                content = f"{monster[name][type_]} / {monster[name][type_]}"
            # テキストを表示する
            self.name_text[is_friend][monster[name][type_]] = canvas.create_text(
                (start_x+end_x)/2, (start_y+end_y)/2,
                text = content
            )
            i += 1

    def __kill_monster(self, monster_name: str, is_friend: bool) -> None:
        """
        モンスターが死亡する
        monster_name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        canvas.update()
        sleep(1)
        self.dead[is_friend][monster_name] = True
        canvas.delete(self.name_box[is_friend][monster_name])
        canvas.delete(self.name_text[is_friend][monster_name])
    
    def __revive_monster(self, name: str, is_friend: bool) -> None:
        """
        モンスターが復活する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        canvas.update()
        sleep(1)
        self.dead[is_friend][name] = False
        width, height = 160, 40
        start_x, start_y = self.elem_coord[(name, "name", is_friend)]
        end_x, end_y = start_x+width, start_y+height
        if is_friend:
            color = "#3f3"
        else:
            color = "#f33"
        # 四角形を表示する
        self.name_box[is_friend][name] = canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#ddd",
            outline = color
        )
        # テキストを表示する
        self.name_text[is_friend][name] = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = name
        )

    def battle_start_auto(self) -> None:
        """
        バトルを開始する（自動）
        """
        # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
        while any([self.dead[0][monster[name]["name"]]==False for name in self.enemy]) and any([self.dead[1][monster[name]["name"]]==False for name in self.friend]):
            # 各ターンの処理
            order = []
            for name in self.enemy:
                r = uniform(0.8, 1.2)
                order.append([r*monster[name]["agility"], monster[name]["name"], "enemy"])
            for name in self.friend:
                order.append([r*monster[name]["agility"], monster[name]["name"], "friend"])
            order.sort(reverse=True)
            break
    
    def battle_start_manual(self) -> None:
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
    return choice(list(skill.keys()), p=list(skill.values()))

def param_level_up(param: int) -> int:
    """
    パラメータを強化する
    """
    return ceil(param*1.05)

with open("data.json", encoding="utf-8") as f:
    data = load(f)
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

if 1:
    battle(
        ["スライム", "ドラキー", "ゴースト"],
        ["スライム", "ドラキー", "ボストロール"]
    )
    app.mainloop()

"""
メモ

・モンスターの重複禁止
"""

