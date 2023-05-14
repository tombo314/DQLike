from time import sleep
from typing import Union
from threading import Thread
from playsound import playsound
import tkinter as tk
import json
import math
import numpy as np
import random as rd

mode = "debug"
if mode=="release":
    SHOW_DURATION = 1.7
    BATTLE_START_DURATION = 1
elif mode=="debug":
    SHOW_DURATION = 0.3
    BATTLE_START_DURATION = 0.5
BATTLE_FINISH_DURATION = 2

class UserInfo:
    def __init__(self) -> None:
        """
        プレイヤーに関する情報を持つ
        """
        self.friend = [None]*3
        # モンスターの詳細に遷移するボタン
        self.button_monster = [None]*12
        # 画像データ
        self.image = {name: [] for name in monster}
        # 次のページに進むボタン
        self.button_page_next = None
        # 前のページに戻るボタン
        self.button_page_back = None
        # モンスター一覧のページ数
        self.page = 0
        # モンスターボックスのテキスト
        self.text_monster_box = None

    def delete_all_ui(self) -> None:
        """
        すべてのUIを削除する
        """
        canvas.delete("all")
        if self.button_page_next is not None:
            self.button_page_next.destroy()
        if self.button_page_back is not None:
            self.button_page_back.destroy()
        for i in range(12):
            if self.button_monster[i] is not None:
                self.button_monster[i].destroy()

    def set_friend(self, friend: list[str]) -> None:
        """
        自分のパーティーを設定する
        """
        self.friend = friend
    
    def plot_image(self, name: str, path: str, x: int, y: int) -> None:
        """
        画像を表示
        name: モンスターの名前
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージ作成
        self.image[name].append(tk.PhotoImage(file=path, width=130, height=130))
        # キャンバスにイメージを表示
        canvas.create_image(x, y, image=self.image[name][-1], anchor=tk.NW)
        
    def show_all_monster(self) -> None:
        """
        自分が持っているモンスターを表示する
        """
        self.page = 0
        self.show_monster()

    def show_monster(self) -> None:
        """
        モンスターを1ページ分表示する
        """
        self.delete_all_ui()
        # テキストを表示
        start_x, start_y = 425, 20
        width, height = 300, 60
        end_x, end_y = start_x+width, start_y+height
        # テキストが設定してあれば削除する
        if self.text_monster_box is not None:
            canvas.delete(self.text_monster_box)
        if len(user["monster"])//12==len(user["monster"])/12:
            page_all = len(user["monster"])//12
        else:
            page_all = len(user["monster"])//12+1
        self.text_monster_box = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"モンスターボックス（{self.page+1}／{page_all}）",
            font = ("", 22)
        )
        for i in range(self.page*12, min((self.page+1)*12, len(user["monster"]))):
            name = user["monster"][i]["name"]
            # 画像を表示
            width = 240*(i%4)+180
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = (170*(i//4)+90)%510
            self.plot_image(name, f"images/png_resized/{name}_resized.png", width, height)
            # 詳細ボタンを表示
            self.button_monster[i%12] = tk.Button(
                app,
                text=name,
                font=("", 18),
                width=12,
                height=1
            )
            self.button_monster[i%12].pack()
            relx = 0.2*(i%4)+0.12
            rely = (0.27*(i//4))%0.81+0.3
            self.button_monster[i%12].place(relx=relx, rely=rely)
            # debug
            # self.button_monster[i].bind("<1>", self.show_monster_info)
            i += 1
        # 次のページに進むボタンを表示
        if (self.page+1)*12<len(user["monster"]):
            self.button_page_next = tk.Button(
                app,
                text = ">",
                font=("", 18),
                width=2,
                height=7
            )
            self.button_page_next.pack()
            self.button_page_next.place(x=1140, y=240)
            self.button_page_next.bind("<1>", self.show_next_page)
        # 最後のページだったら進むボタンを削除
        elif (self.page+1)*12>=len(user["monster"]):
            self.button_page_next.destroy()
        # 前のページに戻るボタンを表示
        if 0<self.page*12<len(user["monster"]):
            self.button_page_back = tk.Button(
                app,
                text = "<",
                font=("", 18),
                width=2,
                height=7
            )
            self.button_page_back.pack()
            self.button_page_back.place(x=20, y=240)
            self.button_page_back.bind("<1>", self.show_previous_page)
        # 最初のページだったら進むボタンを削除
        elif self.page==0:
            if self.button_page_back is not None:
                self.button_page_back.destroy()
        canvas.update()

    def show_next_page(self, event) -> None:
        """
        次のページを表示する
        """
        self.page += 1
        self.show_monster()
    
    def show_previous_page(self, event) -> None:
        """
        前のページを表示する
        """
        self.page -= 1
        self.show_monster()

    def show_monster_info(self, event) -> None:
        """
        自分が持っているモンスターの詳細を表示する
        """
    
    def show_user_info(self) -> None:
        """
        自分の情報を表示する
        """
        self.delete_all_ui()

class Window:
    def __init__(self) -> None:
        """
        画面にUIを表示する
        """
        self.message_box = None
        self.message_text = None
        self.button = [None]*3
        self.enemy = [None]*3
        self.log_text = [None]*15
    
    def make_message_box(self) -> None:
        """
        メッセージボックスを生成する
        """
        start_x, start_y = 90, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_box = canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#eee",
            outline = "#777"
        )
        canvas.update()
    
    def delete_message_box(self) -> None:
        """
        メッセージボックスを削除する
        """
        if self.message_box!=None:
            canvas.delete(self.message_box)
            canvas.update()
    
    def show_message(self, message: str, is_fast: bool, log_list: list[str]) -> None:
        """
        メッセージを表示（変更）する
        message: 表示するメッセージ
        is_fast: 表示間隔を短くするかどうか
        log_list: 表示するログのリスト
        """
        # メッセージ
        # すでにメッセージが書いてある場合は消去する
        if self.message_text is not None:
            canvas.delete(self.message_text)
        # メッセージを表示する
        start_x, start_y = 70, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_text = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            font = ("helvetica", 18),
            text = message
        )
        # ログ
        LOG_NUM = 15
        # すでにログが書いてある場合は削除する
        for i in range(LOG_NUM):
            canvas.delete(self.log_text[i])
        # ログを出力する
        if log_list is not None:
            log_list.append(message)
            if len(log_list)>LOG_NUM:
                log_list.pop(0)
            for i,content in enumerate(log_list):
                start_x, start_y = 950, 27*(i+1)
                width, height = 100, 30
                end_x, end_y = start_x+width, start_y+height
                self.log_text[i] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    font = ("helvetica", 12),
                    text = content
                )
        canvas.update()
        if is_fast==True:
            sleep(SHOW_DURATION*0.3)
        elif is_fast==False:
            sleep(SHOW_DURATION)

    def delete_message(self) -> None:
        """
        メッセージを削除する
        """
        if self.message_text!=None:
            canvas.delete(self.message_text)
            canvas.update()
    
    def set_enemy(self, enemy: list[str]) -> None:
        """
        敵のパーティーを設定する
        """
        self.enemy = enemy
    
    def encounter(self, event) -> None:
        """
        敵と遭遇する
        """
        # ボタンを削除する
        for i in range(3):
            self.button[i].destroy()
        # バトルを開始する
        start_battle(self.enemy)
            
    def make_three_buttons(self, text: list[str]) -> None:
        """
        前、左、右の三方向に進むボタンを表示する
        """
        canvas.delete("all")
        for i in range(3):
            self.button[i] = tk.Button(
                app,
                text=text[i],
                font=("", 20),
                width=13,
                height=3
            )
            self.button[i].pack()
            self.button[i].place(x=230*i+130, y=200)
            # debug
            self.button[i].bind("<1>", self.encounter)
    
    def make_yes_no_buttons(self) -> None:
        """
        「はい」と「いいえ」のボタンを表示する
        """
    
    def delete_yes_no_buttons(self) -> None:
        """
        「はい」と「いいえ」のボタンを削除する
        """

class Battle:
    def __init__(self, enemy:list, friend: list) -> None:
        """
        バトルを行う
        enemy: 敵のパーティー
        friend: 味方のパーティー
        """
        self.enemy = enemy
        self.friend = friend
        # バトル時のログ
        self.log_list = []
        canvas.delete("all")
        # メッセージボックスを作成
        window.make_message_box()
        # パーティー内でモンスターの重複があったら終了
        is_deplicated = False
        if len(set(enemy))<=2:
            is_deplicated = True
            print("敵パーティー内でモンスターが重複しています。")
        if len(set(friend))<=2:
            is_deplicated = True
            print("味方パーティー内でモンスターが重複しています。")
        if is_deplicated:
            exit()
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
        # 画像データ
        self.image = [
            {monster[name]["name"]: 0 for name in enemy},
            {monster[name]["name"]: 0 for name in friend},
        ]
        # モンスタ―とUIの座標の対応関係
        # (monster_name, is_friend): (start_x, start_y)
        self.elem_coord = {}
        # バトル時のパラメータ
        self.hp = [
            {monster[name]["name"]: monster[name]["hp"] for name in enemy},
            {monster[name]["name"]: monster[name]["hp"] for name in friend}
        ]
        self.hp_init = [
            {monster[name]["name"]: monster[name]["hp"] for name in enemy},
            {monster[name]["name"]: monster[name]["hp"] for name in friend}
        ]
        self.mp = [
            {monster[name]["name"]: monster[name]["mp"] for name in enemy},
            {monster[name]["name"]: monster[name]["mp"] for name in friend}
        ]
        self.mp_init = [
            {monster[name]["name"]: monster[name]["mp"] for name in enemy},
            {monster[name]["name"]: monster[name]["mp"] for name in friend}
        ]
        self.attack = [
            {monster[name]["name"]: monster[name]["attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["attack"] for name in friend}
        ]
        self.attack_init = [
            {monster[name]["name"]: monster[name]["attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["attack"] for name in friend}
        ]
        self.magic_attack = [
            {monster[name]["name"]: monster[name]["magic_attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["magic_attack"] for name in friend}
        ]
        self.magic_attack_init = [
            {monster[name]["name"]: monster[name]["magic_attack"] for name in enemy},
            {monster[name]["name"]: monster[name]["magic_attack"] for name in friend}
        ]
        self.defense = [
            {monster[name]["name"]: monster[name]["defense"] for name in enemy},
            {monster[name]["name"]: monster[name]["defense"] for name in friend}
        ]
        self.defense_init = [
            {monster[name]["name"]: monster[name]["defense"] for name in enemy},
            {monster[name]["name"]: monster[name]["defense"] for name in friend}
        ]
        self.agility = [
            {monster[name]["name"]: monster[name]["agility"] for name in enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in friend}
        ]
        self.agility_init = [
            {monster[name]["name"]: monster[name]["agility"] for name in enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in friend}
        ]
        self.dead = [
            {monster[name]["name"]: False for name in enemy},
            {monster[name]["name"]: False for name in friend}
        ]
        # レベルに合わせてパラメータを変更する
        for name in enemy:
            self.reflect_level(name, False, monster[name]["level"])
        for name in friend:
            self.reflect_level(name, True, monster[name]["level"])
        # 敵と味方の名前、HP、MPを表示する
        self.make_party(enemy, "name", False)
        self.make_party(enemy, "hp", False)
        self.make_party(enemy, "mp", False)
        self.make_party(friend, "name", True)
        self.make_party(friend, "hp", True)
        self.make_party(friend, "mp", True)
        # 敵と味方の画像を表示する
        self.plot_image_all()
        canvas.update()
    
    def make_party(self, party: list[str], type_: str, is_friend: bool) -> None:
        """
        UIを生成する
        party: 敵か味方のモンスター3体
        type: 「name」「hp」「mp」のどれか
        is_friend: 敵の要素であるかどうか
        """
        y = -1
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
            start_x, start_y = 220*i+140, y
            # モンスター名とモンスターの敵・味方の区分と、UIの座標を対応付ける
            self.elem_coord.update({(name, type_, is_friend): (start_x, start_y)})
            width, height = 160, 40
            end_x, end_y = start_x+width, start_y+height
            # 四角形を表示する
            elem = canvas.create_rectangle(
                start_x, start_y,
                end_x, end_y,
                fill = "#ddd",
                outline = color
            )
            if type_=="name":
                self.name_box[is_friend][name] = elem
            elif type_=="hp":
                self.hp_box[is_friend][name] = elem
            elif type_=="mp":
                self.mp_box[is_friend][name] = elem
            # テキストを表示する
            if type_=="name":
                content = name
            elif type_=="hp":
                content = f"{self.hp[is_friend][name]} / {self.hp_init[is_friend][name]}"
            elif type_=="mp":
                content = f"{self.mp[is_friend][name]} / {self.mp_init[is_friend][name]}"
            elem = canvas.create_text(
                (start_x+end_x)/2, (start_y+end_y)/2,
                text = content,
                font = ("", 12)
            )
            if type_=="name":
                self.name_text[is_friend][name] = elem
            elif type_=="hp":
                self.hp_text[is_friend][name] = elem
            elif type_=="mp":
                self.mp_text[is_friend][name] = elem
            i += 1
        canvas.update()

    def plot_image(self, name: str, is_friend: bool, path: str, x: int, y: int) -> None:
        """
        画像を表示
        name: モンスターの名前
        is_friend: 味方であるかどうか
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージ作成
        self.image[is_friend][name] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        canvas.create_image(x, y, image=self.image[is_friend][name], anchor=tk.NW)

    def plot_image_all(self) -> None:
        """
        敵と味方のパーティーの画像を表示
        """
        i = 0
        for name in self.enemy:
            width = 212*i+175
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 8
            self.plot_image(name, False, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        i = 0
        for name in self.friend:
            width = 222*i+170
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 520
            self.plot_image(name, True, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        canvas.update()

    def delete_image(self, name: str, is_friend) -> None:
        """
        画像を削除する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        self.image[is_friend][name] = None

    def reflect_level(self, name: str, is_friend: bool, level: int) -> None:
        """
        モンスターのレベルを、パラメータに反映させる
        name: モンスターの名前
        is_friend: 味方であるかどうか
        level: モンスターのレベル
        """
        for _ in range(level-1):
            self.hp_init[is_friend][name] = self.param_level_up(self.hp_init[is_friend][name], False)
            self.mp_init[is_friend][name] = self.param_level_up(self.mp_init[is_friend][name], True)
            self.attack_init[is_friend][name] = self.param_level_up(self.attack_init[is_friend][name], False)
            self.magic_attack_init[is_friend][name] = self.param_level_up(self.magic_attack_init[is_friend][name], False)
            self.defense_init[is_friend][name] = self.param_level_up(self.defense_init[is_friend][name], False)
            self.agility_init[is_friend][name] = self.param_level_up(self.agility_init[is_friend][name], False)
        self.hp[is_friend][name] = self.hp_init[is_friend][name]
        self.mp[is_friend][name] = self.mp_init[is_friend][name]
        self.attack[is_friend][name] = self.attack_init[is_friend][name]
        self.magic_attack[is_friend][name] = self.magic_attack_init[is_friend][name]
        self.defense[is_friend][name] = self.defense_init[is_friend][name]
        self.agility[is_friend][name] = self.agility_init[is_friend][name]

    def param_level_up(self, param: int, is_mp: bool) -> int:
        """
        レベルの上昇に伴って、パラメータを強化する
        param: 強化前のパラメータ
        is_mp: パラメータの種類がMPであるかどうか
        """
        if is_mp and param==0:
            return 2
        if is_mp:
            return min(999, math.ceil(param*1.05))
        return math.ceil(param*1.05)

    def kill_monster(self, name: str, is_friend: bool) -> None:
        """
        モンスターが死亡する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        # メッセージを表示
        if is_friend==True:
            enemy_or_friend = "味方の"
        elif is_friend==False:
            enemy_or_friend = "敵の"
        message = f"{enemy_or_friend}{name}は力尽きた..."
        window.show_message(message, False, self.log_list)
        # deadフラグを更新
        self.dead[is_friend][name] = True
        # 画像を削除
        self.delete_image(name, is_friend)
        canvas.update()
    
    def revive_monster(self, name: str, is_friend: bool) -> None:
        """
        モンスターが復活する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
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
            text = name,
            font = ("", 12)
        )
        canvas.update()

    def update_hp_mp_text(self, name: str, is_friend: bool, type_: str, param: int) -> None:
        """
        hpまたはmpの表示を更新する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        type_: 「hp」「mp」のどちらか
        param: 更新したあとの数字
        """
        # 前のテキストを削除する
        if type_=="hp":
            canvas.delete(self.hp_text[is_friend][name])
        elif type_=="mp":
            canvas.delete(self.mp_text[is_friend][name])
        start_x, start_y = self.elem_coord[(name, type_, is_friend)]
        width, height = 160, 40
        end_x, end_y = start_x+width, start_y+height
        # テキストを表示する
        if type_=="hp":
            max_val = self.hp_init[is_friend][name]
        elif type_=="mp":
            max_val = self.mp_init[is_friend][name]
        elem = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"{param} / {max_val}",
            font = ("", 12)
        )
        if type_=="hp":
            self.hp_text[is_friend][name] = elem
        elif type_=="mp":
            self.mp_text[is_friend][name] = elem
        canvas.update()

    def is_n_percent(self, prob: int) -> bool:
        """
        probパーセントの確率でTrueを返す
        prob: Trueが返ってくる確率(0~100)
        """
        r = rd.randint(1, 100)
        if r<=prob:
            return True
        return False

    def select_skill(self, skill: dict) -> str:
        """
        スキルを選択する
        skill: keyにスキル名、valueに確率
        """
        return np.random.choice(list(skill.keys()), p=list(skill.values()))

    def select_monster_at_random(self, enemy_or_friend: str) -> str:
        """
        パーティーの中からランダムに1体選ぶ
        enemy_or_friend: 「enemy」「friend」のどちらか
        """
        mons = None
        if enemy_or_friend=="enemy":
            # 死んでいたら攻撃の対象にならない
            while mons==None or self.dead[0][mons]==True:
                mons = rd.choice(self.enemy)
            return mons
        elif enemy_or_friend=="friend":
            # 死んでいたら攻撃の対象にならない
            while mons==None or self.dead[1][mons]==True:
                mons = rd.choice(self.friend)
            return mons

    def calc_damage(self, skill_name: str, attack: int, magic_attack: int, defense: int, attribute_damage_rate: dict, is_critical: bool) -> int:
        """
        ダメージを計算する
        skill_name: 使うスキルの名前
        attack: 攻撃側の物理攻撃力
        magic_attack: 攻撃側の呪文攻撃力
        defense: 防御側の物理防御力
        attribute_damage_rate: 防御側の属性耐性 {属性: ダメージ倍率}
        is_critical: 会心の一撃かどうか
        """
        physics_damage = 0
        magic_damage = 0
        damage_rate = 1
        using_skill = skill[skill_name]
        # 物理ダメージ
        if using_skill["type"]=="physics":
            # 会心の一撃が発生する
            if is_critical==True:
                # 相手の物理防御力を無視
                physics_damage += attack
                # ダメージが増える
                damage_rate *= rd.uniform(1.4, 1.6)
            # 会心の一撃が発生しない
            else:
                physics_damage += attack-defense//2
        # 呪文ダメージ
        elif using_skill["type"]=="magic":
            magic_damage += magic_attack
            # 会心の一撃が発生する
            if is_critical==True:
                # ダメージが増える
                damage_rate *= rd.uniform(1.4, 1.6)
        damage_rate *= using_skill["damage_rate"]
        # 属性耐性を計算する
        if using_skill["attribute"]!="無" and using_skill["attribute"] is not None:
            # 会心の一撃発生時、属性貫通率が増える
            if is_critical==True:
                damage_rate *= attribute_damage_rate[using_skill["attribute"]]+0.2
            # 会心の一撃が発生しない
            elif is_critical==False:
                damage_rate *= attribute_damage_rate[using_skill["attribute"]]
        # ダメージを計算する
        damage = (physics_damage+magic_damage)*damage_rate*rd.uniform(0.95, 1.05)
        # ダメージは0以上
        # 小数点以下切り上げ
        return max(0, math.ceil(damage))

    def attack_on_monster(self, skill_name: str, offense_name: str, offense_is_friend: bool, defense_name: str, is_all: bool) -> Union[bool, None]:
        """
        モンスターからモンスターに攻撃する
        バトルを継続するときにTrue、終了するときにFalse、MPが足りない場合はNoneを返す
        skill_name: 技の名前
        offense_name: 攻撃側のモンスターの名前
        offense_is_friend: 攻撃側のモンスターが味方であるかどうか
        defense_name: 防御側のモンスターの名前
        is_all: 全体攻撃かどうか
        """
        # 攻撃側と防御側を設定
        if offense_is_friend==True:
            defense_is_friend = False
        elif offense_is_friend==False:
            defense_is_friend = True
        # 攻撃を受ける相手のモンスターを設定
        if is_all==True: 
            if offense_is_friend==True:
                defending_side = self.enemy.copy()
            elif offense_is_friend==False:
                defending_side = self.friend.copy()
        elif is_all==False:
            defending_side = [defense_name]
        # 攻撃側の情報を設定
        offensing_monster = {
            "attack": self.attack[offense_is_friend][offense_name],
            "magic_attack": self.magic_attack[offense_is_friend][offense_name]
        }
        # 防御側の情報を設定
        for i,name in enumerate(defending_side):
            defending_side[i] = {
                "name": name,
                "defense": self.defense[defense_is_friend][name],
                "attribute_damage_rate": monster[name]["attribute_damage_rate"]
            }
        # 使うスキルを設定
        using_skill = skill[skill_name]
        # 攻撃時のメッセージを表示
        if offense_is_friend==True:
            enemy_or_friend = "味方の"
        elif offense_is_friend==False:
            enemy_or_friend = "敵の"
        message = enemy_or_friend+offense_name+using_skill["message"]
        window.show_message(message, False, self.log_list)
        # 攻撃側のMPが足りない場合は攻撃をキャンセル
        if self.mp[offense_is_friend][offense_name]<using_skill["mp_consumption"]:
            message = "しかしMPが足りない！"
            window.show_message(message, False, self.log_list)
            return None
        # 防御側の被ダメージ時のメッセージを表示
        if defense_is_friend==True:
            enemy_or_friend = "味方の"
        elif defense_is_friend==False:
            enemy_or_friend = "敵の"
        self_damage = 0
        # 全体攻撃のときは、表示速度を速くする
        show_fast = is_all
        is_first_attack = True
        is_critical = None
        for defending_monster in defending_side:
            # skill「ミス」を使用する
            # 攻撃がミスする
            if skill_name=="ミス" or self.is_n_percent(using_skill["miss_probability"]*100)==True:
                message = f"ミス！{enemy_or_friend}{defending_monster['name']}はダメージを受けない！"
                window.show_message(message, show_fast, self.log_list)
                continue
            # 死んでいる場合は攻撃の対象にならない
            if self.dead[defense_is_friend][defending_monster["name"]]==True:
                continue
            # 会心の一撃かどうかを判定する
            # 会心の一撃が出る可能性のあるスキルの、typeとrangeは以下の通り
            # ・type=physics range=single
            # ・type=magic range=single
            # ・type=magic range=all
            if is_critical is None:
                is_critical = self.is_n_percent(using_skill["critical_probability"]*100)
            # 会心の一撃発生時に、メッセージを表示
            if is_critical==True:
                if using_skill["type"]=="physics" and is_all==False:
                    message = "会心の一撃！"
                    window.show_message(message, False, self.log_list)
                elif using_skill["type"]=="magic" and is_first_attack==True:
                    message = f"{offense_name}の魔力が暴走した！"
                    window.show_message(message, False, self.log_list)
            # 攻撃側の与ダメージと自傷ダメージを計算する
            damage = self.calc_damage(
                skill_name,
                offensing_monster["attack"],
                offensing_monster["magic_attack"],
                defending_monster["defense"],
                defending_monster["attribute_damage_rate"],
                is_critical,
            )
            self_damage = max(0, math.ceil(damage*using_skill["self_damage_ratio_to_calc_damage"]))
            # 防御側のHPと攻撃側のMPを減らす
            self.hp[defense_is_friend][defending_monster["name"]] = max(self.hp[defense_is_friend][defending_monster["name"]]-damage, 0)
            if is_first_attack==True:
                self.mp[offense_is_friend][offense_name] -= using_skill["mp_consumption"]
            # 攻撃側のMPの表示を変更する
            self.update_hp_mp_text(offense_name, offense_is_friend, "mp", self.mp[offense_is_friend][offense_name])
            # 全体攻撃のときは表示間隔を短くする
            if damage>0:
                message = f"{enemy_or_friend}{defending_monster['name']}に{damage}のダメージ！"
                window.show_message(message, show_fast, self.log_list)
            # ダメージを無効化した、または攻撃を回避した
            else:
                message = f"ミス！{enemy_or_friend}{defending_monster['name']}はダメージを受けない！"
                window.show_message(message, show_fast, self.log_list)
            # 防御側のHPの表示を変更する
            self.update_hp_mp_text(defending_monster["name"], defense_is_friend, "hp", self.hp[defense_is_friend][defending_monster["name"]])
            # 防御側のdeadフラグを更新して、死亡時のメッセージを表示
            if self.hp[defense_is_friend][defending_monster["name"]]==0:
                self.kill_monster(defending_monster["name"], defense_is_friend)
            is_first_attack = False
        if is_all==True:
            sleep(SHOW_DURATION*0.7)
        # 自傷ダメージ
        if self_damage>0 and is_all==False:
            # 攻撃側のHPを減らす
            self.hp[offense_is_friend][offense_name] -= self_damage
            self.update_hp_mp_text(offense_name, offense_is_friend, "hp", self.hp[offense_is_friend][offense_name])
            # 攻撃側の被ダメージ時のメッセージを表示
            if offense_is_friend==True:
                enemy_or_friend = "味方の"
            elif offense_is_friend==False:
                enemy_or_friend = "敵の"
            message = f"{enemy_or_friend}{offense_name}に{self_damage}のダメージ！"
            window.show_message(message, False, self.log_list)
            # 攻撃側のHPの表示を変更する
            self.update_hp_mp_text(offense_name, offense_is_friend, "hp", self.hp[offense_is_friend][offense_name])
            # 攻撃側のdeadフラグを更新して、死亡時のメッセージを表示
            if self.hp[offense_is_friend][offense_name]==0:
                self.kill_monster(offense_name, offense_is_friend)
        # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
        # Falseで終了
        if any(self.dead[0][name]==False for name in self.enemy) and any(self.dead[1][name]==False for name in self.friend):
            return True
        return False
    
    def battle_start_auto(self) -> None:
        """
        バトルを開始する（自動）
        """
        break_ = False
        while True:
            # 各ターンの処理
            order = []
            for name in self.enemy:
                r = rd.uniform(0.8, 1.2)
                order.append([r*monster[name]["agility"], monster[name]["name"], "enemy"])
            for name in self.friend:
                order.append([r*monster[name]["agility"], monster[name]["name"], "friend"])
            order.sort(reverse=True)
            for mons in order:
                agility, name, offense_enemy_or_friend = mons
                # 死んでいたら行動できない
                if offense_enemy_or_friend=="enemy":
                    is_friend = False
                elif offense_enemy_or_friend=="friend":
                    is_friend = True
                if self.dead[is_friend][name]==True:
                    continue
                # 攻撃する
                if offense_enemy_or_friend=="enemy":
                    deffense_enemy_or_friend = "friend"
                elif offense_enemy_or_friend=="friend":
                    deffense_enemy_or_friend = "enemy"
                offensing_monster = name
                if offense_enemy_or_friend=="enemy":
                    offense_is_friend = False
                elif offense_enemy_or_friend=="friend":
                    offense_is_friend = True
                skill_name = self.select_skill(monster[offensing_monster]["skill_select_probability"][offense_enemy_or_friend])
                # 単体攻撃
                if skill[skill_name]["range"]=="single" or skill[skill_name]["range"] is None:
                    defending_monster = self.select_monster_at_random(deffense_enemy_or_friend)
                    # 防御側のパーティーが全滅したかどうか
                    continue_ = self.attack_on_monster(
                        skill_name,
                        offensing_monster,
                        offense_is_friend,
                        defending_monster,
                        False
                    )
                # 全体攻撃
                elif skill[skill_name]["range"]=="all":
                    # 防御側のパーティーが全滅したかどうか
                    continue_ = self.attack_on_monster(
                        skill_name,
                        offensing_monster,
                        offense_is_friend,
                        None,
                        True
                    )
                # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
                if continue_==False:
                    if all([self.dead[0][name] for name in self.dead[0]]):
                        message = "バトルに勝利した！"
                        window.show_message(message, False, self.log_list)
                    elif all([self.dead[1][name] for name in self.dead[1]]):
                        message = "全滅してしまった..."
                        window.show_message(message, False, self.log_list)
                    sleep(BATTLE_FINISH_DURATION)
                    break_ = True
                    break
            if break_:
                break

class Fusion:
    def __init__(self) -> None:
        """
        モンスターの配合に関する情報を持つ
        """
    
    def show_fusion_screen(self) -> None:
        """
        配合画面を表示する
        """
    
    def get_makeable_monster(self, monster: str) -> None:
        """
        モンスターの配合候補を返す
        monster: 親の片方となるモンスター
        """
        return fusion_tree[monster]

def start_battle(party_enemy: list[str]) -> None:
    """
    バトルを行う
    party_enemy: 敵のパーティー
    """
    # 再生を2回試行する
    try:
        play_music("交える死闘.mp3", 0)
    except:
        play_music("交える死闘.mp3", 0)
    battle = Battle(party_enemy, user_info.friend)
    window.show_message("魔物の群れが現れた！", False, None)
    sleep(BATTLE_START_DURATION)
    battle.battle_start_auto()

def game_start() -> None:
    """
    ゲーム全体を開始する
    """

def play_music(file_name: str, play_duration: int) -> None:
    """
    音声を再生する
    file_name: ファイル名
    play_duration: 再生時間
    """
    music = Thread(target=lambda: playsound(file_name), daemon=True)
    music.start()
    sleep(play_duration+1)

# JSONデータを読み込む
with open("data/monster.json", encoding="utf-8") as data:
    monster = json.load(data)
with open("data/skill.json", encoding="utf-8") as data:
    skill = json.load(data)
with open("data/fusion_tree.json", encoding="utf-8") as data:
    fusion_tree = json.load(data)
with open("data/user.json", encoding="utf-8") as data:
    user = json.load(data)

# Tkinterの初期設定
app = tk.Tk()
app.title("DQLike")
width = 1200
height = 620
left = 60
top = 30
app.geometry(f"{width}x{height}+{left}+{top}")
# 画面のサイズ変更を禁止
app.resizable(0, 0)
canvas = tk.Canvas(
    app,
    width = width,
    height = height
)
canvas.pack()

# UIのインスタンス
window = Window()

# 自分の情報のインスタンス
user_info = UserInfo()

# debug
user_info.set_friend(["スライム", "ドラキー", "ギュメイ将軍"])

# debug print

# debug
# user_info.show_all_monster()

# debug
window.set_enemy(["スライム", "ボストロール", "ゲルニック将軍"])
window.make_three_buttons([1,2,3])

# 画面を表示
app.mainloop()

"""
To Do

・ゲルニック将軍を実装する
    ・ルカナン
・is_decreasingを見ていない
    -> さみだれ斬りが減衰しない
・バトル時のログを表示する
"""
"""
メモ

・毎バトル終了後に、味方モンスターのHPとMPが全回復してもいいかもしれない？
・パーティー内のモンスターの重複禁止
・自傷ダメージのある攻撃は、range=singleのみ
"""
