from pprint import pprint
from random import randint
import tkinter as tk
import json
import numpy as np

class Battle:
    def __init__(self, enemy:list, friend: list) -> None:
        """
        バトルのインスタンスを生成する
        enemy: 敵のパーティーの配列
        friend: 味方のパーティーの配列
        """
        # UIを生成する
        # 0がenemy, 1がfriend
        self.name_box = [[0, 0]]*3
        self.name_text = [[0, 0]]*3
        self.hp_box = [[0, 0]]*3
        self.hp_text = [[0, 0]]*3
        self.mp_box = [[0, 0]]*3
        self.mp_text = [[0, 0]]*3
        self.__make_element(enemy, "名前", False)
        self.__make_element(enemy, "HP", False)
        self.__make_element(enemy, "MP", False)
        self.__make_element(friend, "名前", True)
        self.__make_element(friend, "HP", True)
        self.__make_element(friend, "MP", True)
        # バトル時のパラメータ
        self.
    
    def __make_element(self, party: list, type_: str, is_friend: bool) -> None:
        """
        敵と味方のUIを生成する
        party: 敵か味方のモンスター3体の要素の配列
        type: 「名前」「HP」「MP」のいずれか
        is_enemy: 敵の要素であるかどうか
        """
        y = -1
        color = ""
        if type_=="名前":
            y = 100
        elif type_=="HP":
            y = 160
        elif type_=="MP":
            y = 220
        if is_friend==True:
            color = "#f33"
        elif is_friend==False:
            color = "#3f3"
            y += 250
        i = 0
        for mons in party:
            start_x, start_y = 220*i+100, y
            width, height = 160, 40
            end_x, end_y = start_x+width, start_y+height
            if type_=="名前":
                self.name_box[i][is_friend] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                self.name_text[i][is_friend] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = mons["name"]
                )
            elif type_=="HP":
                self.hp_box[i][is_friend] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                hp = mons["hp"]
                self.hp_text[i][is_friend] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = f"{hp} / {hp}"
                )
            elif type_=="MP":
                self.mp_box[i][is_friend] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                mp = mons["mp"]
                self.mp_text[i][is_friend] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = f"{mp} / {mp}"
                )
            i += 1

    def battle_start():
        

def battle(party_enemy: list, party_friend: list) -> None:
    """
    バトルを行う
    party_enemy: 敵のパーティーの配列
    party_friend: 味方のパーティーの配列
    """
    btl = Battle(party_enemy, party_friend)

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
    skill: keyにスキル、valueに確率を取る連想配列
    """
    return np.random.choice(list(skill.keys()), p=list(skill.values()))

with open("data.json", encoding="utf-8") as f:
    data = json.load(f)
    monster = data["monster"]
    skill = data["skill"]

app = tk.Tk()

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