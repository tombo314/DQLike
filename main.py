from pprint import pprint
from time import sleep
from json import load
import tkinter as tk
import math
import numpy as np
import random as rd

class Window:
    def __init__(self) -> None:
        self.message_box = None
        self.message_text = None
    
    def make_message_box(self) -> None:
        """
        メッセージボックスを生成する
        """
        start_x, start_y = 70, 275
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
    
    def show_message(self, message: str) -> None:
        """
        メッセージを表示（変更）する
        message: 表示するメッセージ
        """
        start_x, start_y = 70, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        # すでにメッセージが書いてある場合は消去する
        if self.message_text!="":
            canvas.delete(self.message_text)
        # メッセージを表示する
        self.message_text = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            font = ("helvetica", 18),
            text = message
        )
        canvas.update()

    def delete_message(self) -> None:
        """
        メッセージを削除する
        """
        if self.message_text!=None:
            canvas.delete(self.message_text)
            canvas.update()

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
        self.make_party(enemy, "name", False)
        self.make_party(enemy, "hp", False)
        self.make_party(enemy, "mp", False)
        self.make_party(friend, "name", True)
        self.make_party(friend, "hp", True)
        self.make_party(friend, "mp", True)
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
        self.defense = [
            {monster[name]["name"]: monster[name]["defense"] for name in enemy},
            {monster[name]["name"]: monster[name]["defense"] for name in friend}
        ]
        self.agility = [
            {monster[name]["name"]: monster[name]["agility"] for name in enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in friend}
        ]
        self.dead = [
            {monster[name]["name"]: False for name in enemy},
            {monster[name]["name"]: False for name in friend}
        ]
    
    def make_party(self, party: list[str], type_: str, is_friend: bool) -> None:
        """
        UIを生成する
        party: 敵か味方のモンスター3体
        type: 「name」「hp」「mp」のどれか
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
            content = ""
            if type_=="name":
                content = name
            elif type_=="hp" or type_=="mp":
                content = f"{monster[name][type_]} / {monster[name][type_]}"
            elem = canvas.create_text(
                (start_x+end_x)/2, (start_y+end_y)/2,
                text = content
            )
            if type_=="name":
                self.name_text[is_friend][name] = elem
            elif type_=="hp":
                self.hp_text[is_friend][name] = elem
            elif type_=="mp":
                self.mp_text[is_friend][name] = elem
            i += 1
        canvas.update()

    def kill_monster(self, name: str, is_friend: bool) -> None:
        """
        モンスターが死亡する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        self.dead[is_friend][name] = True
        canvas.delete(self.name_box[is_friend][name])
        canvas.delete(self.name_text[is_friend][name])
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
            text = name
        )
        canvas.update()

    def update_hp_mp(self, name: str, is_friend: bool, type_: str, param: int) -> None:
        """
        hpまたはmpの表示を更新する
        name: モンスターの名前
        is_friend: 味方かどうか
        type_: 「hp」「mp」のどちらか
        param: 更新したあとの数字
        """
        if type_=="hp":
            canvas.delete(self.hp_text[is_friend][name])
        elif type_=="mp":
            canvas.delete(self.mp_text[is_friend][name])
        start_x, start_y = self.elem_coord[(name, type_, is_friend)]
        width, height = 160, 40
        end_x, end_y = start_x+width, start_y+height
        # テキストを表示する
        elem = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"{param} / {monster[name][type_]}"
        )
        if type_=="hp":
            self.hp_text[is_friend][monster[name][type_]] = elem
        elif type_=="mp":
            self.mp_text[is_friend][monster[name][type_]] = elem
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
        if enemy_or_friend=="enemy":
            return rd.choice(self.enemy)
        elif enemy_or_friend=="friend":
            return rd.choice(self.friend)

    def calc_damage(self, skill_name: str, attack: int, magic_attack: int, defense: int, attribute_damage_rate: dict) -> int:
        """
        ダメージを計算する
        skill_name: 使うスキルの名前
        attack: 攻撃側の物理攻撃力
        magic_attack: 攻撃側の呪文攻撃力
        defense: 防御側の物理防御力
        attribute_damage_rate: 防御側の属性耐性 {属性: ダメージ倍率}
        """
        physics_damage = 0
        magic_damage = 0
        damage_rate = 1
        using_skill = skill[skill_name]
        if using_skill["type"]=="physics":
            physics_damage += attack-defense//2
        elif using_skill["type"]=="magic":
            magic_damage += magic_attack
        damage_rate *= using_skill["damage_rate"]
        if using_skill["attribute"]!="無" and using_skill["attribute"]!="null":
            damage_rate *= attribute_damage_rate[using_skill["attribute"]]
        damage = (physics_damage+magic_damage)*damage_rate*rd.uniform(0.95, 1.05)
        return max(0, math.ceil(damage))

    def attack_on_monster(self, skill_name: str, offense_name: str, offense_is_friend: bool, defense_name: str) -> None:
        """
        モンスターからモンスターに攻撃する
        skill_name: 技の名前
        offense_name: 攻撃側のモンスターの名前
        offense_is_friend: 攻撃側のモンスターが味方であるかどうか
        defense_name: 防御側のモンスターの名前
        defense_is_friend: 防御側のモンスターが味方であるかどうか
        """
        offensing_monster = monster[offense_name]
        defending_monster = monster[defense_name]
        using_skill = skill[skill_name]
        if offense_is_friend==True:
            defense_is_friend = False
        elif offense_is_friend==False:
            defense_is_friend = True
        # メッセージを表示
        enemy_or_friend = ""
        if offense_is_friend==True:
            enemy_or_friend = "味方の"
        elif offense_is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(enemy_or_friend+offense_name+skill[skill_name]["message"])
        sleep(1.2)
        # MPが足りない場合はキャンセル
        if self.mp[offense_is_friend][offense_name]<using_skill["mp_consumption"]:
            window.show_message("しかしMPが足りない！")
            return False
        # ダメージの処理とHP・MPの減少
        damage = self.calc_damage(
            skill_name,
            offensing_monster["attack"],
            offensing_monster["magic_attack"],
            defending_monster["defense"],
            defending_monster["attribute_damage_rate"]
        )
        self_damage = max(0, math.ceil(damage*using_skill["self_damage_ratio_to_calc_damage"]))
        self.hp[defense_is_friend][defense_name] -= damage
        self.mp[offense_is_friend][offense_name] -= skill[skill_name]["mp_consumption"]
        self.update_hp_mp(defense_name, defense_is_friend, "hp", self.hp[defense_is_friend][defense_name])
        # メッセージを表示
        enemy_or_friend = ""
        if defense_is_friend==True:
            enemy_or_friend = "味方の"
        elif defense_is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(f"{enemy_or_friend}{defending_monster['name']}に{damage}のダメージ！")
        sleep(1.2)
        # 自傷ダメージ
        if self_damage>0:
            self.hp[offense_is_friend][offense_name] -= self_damage
            self.update_hp_mp(offense_name, offense_is_friend, "hp", self.hp[offense_is_friend][offense_name])
            # メッセージを表示
            window.show_message(f"自分に{self_damage}のダメージ！")
            sleep(1.2)
    
    def battle_start_auto(self) -> None:
        """
        バトルを開始する（自動）
        """
        # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
        while any([self.dead[0][monster[name]["name"]]==False for name in self.enemy]) and any([self.dead[1][monster[name]["name"]]==False for name in self.friend]):
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
                deffense_enemy_or_friend = ""
                if offense_enemy_or_friend=="enemy":
                    deffense_enemy_or_friend = "friend"
                elif offense_enemy_or_friend=="friend":
                    deffense_enemy_or_friend = "enemy"
                offensing_monster = name
                defensing_monster = self.select_monster_at_random(deffense_enemy_or_friend)
                offense_is_friend = None
                if offense_enemy_or_friend=="enemy":
                    offense_is_friend = False
                elif offense_enemy_or_friend=="friend":
                    offense_is_friend = True
                skill_name = self.select_skill(monster[offensing_monster]["skill_select_probability"][offense_enemy_or_friend])
                self.attack_on_monster(
                    skill_name,
                    offensing_monster,
                    offense_is_friend,
                    defensing_monster
                )
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

def param_level_up(param: int, is_mp) -> int:
    """
    レベルアップ後のパラメータを返す
    param: 強化される前の値
    is_mp: MPかどうか
    """
    if is_mp and param==0:
        return 2
    return math.ceil(param*1.05)

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

# システムウィンドウのインスタンス
window = Window()
window.make_message_box()

# debug
if 1:
    battle(
        ["スライム", "ドラキー", "ゴースト"],
        ["スライム", "ドラキー", "ボストロール"]
    )
    app.mainloop()

"""
メモ

・パーティー内のモンスターの重複禁止
・MP不足はそのターンにMPを減少させられた場合にのみ起こり得る。
"""
