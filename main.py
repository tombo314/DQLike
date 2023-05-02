from pprint import pprint
from time import sleep
from json import load
import tkinter as tk
import math
import numpy as np
import random as rd

SHOW_DURATION = 0.01
BATTLE_FINISH_DURATION = 3

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
        sleep(SHOW_DURATION)

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
        # 画像データ
        self.image = [0]*6
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
        # 敵と味方の名前、HP、MPを表示する
        self.make_party(enemy, "name", False)
        self.make_party(enemy, "hp", False)
        self.make_party(enemy, "mp", False)
        self.make_party(friend, "name", True)
        self.make_party(friend, "hp", True)
        self.make_party(friend, "mp", True)
        # 敵と味方の画像を表示する
        self.plot_image_all()
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

    def plot_image(self, path: str, x: int, y: int, i: int) -> None:
        """
        画像を表示
        path: 画像のパス
        x: x座標
        y: y座標
        i: index
        """
        # イメージ作成
        self.image[i] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        canvas.create_image(x, y, image=self.image[i], anchor=tk.NW)

    def plot_image_all(self) -> None:
        """
        敵と味方のパーティーの画像を表示
        """
        i = 0
        for name in self.enemy:
            width = 130+220*i
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 8
            self.plot_image(f"images/png_resized/{name}_resized.png", width, height, i)
            i += 1
        i = 0
        for name in self.friend:
            width = 130+220*i
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 520
            self.plot_image(f"images/png_resized/{name}_resized.png", width, height, 3+i)
            i += 1
        canvas.update()

    def kill_monster(self, name: str, is_friend: bool) -> None:
        """
        モンスターが死亡する
        name: モンスターの名前
        is_friend: 味方であるかどうか
        """
        # メッセージを表示
        enemy_or_friend = None
        if is_friend==True:
            enemy_or_friend = "味方の"
        elif is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(f"{enemy_or_friend}{name}は力尽きた...")
        # deadフラグを更新
        self.dead[is_friend][name] = True
        # 名前を削除
        canvas.delete(self.name_box[is_friend][name])
        canvas.delete(self.name_text[is_friend][name])
        # 画像を削除
        # debug
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
        is_friend: 味方かどうか
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
        elem = canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"{param} / {monster[name][type_]}",
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
            while mons==None or self.dead[0][mons]==True:
                mons = rd.choice(self.enemy)
            return mons
        elif enemy_or_friend=="friend":
            while mons==None or self.dead[1][mons]==True:
                mons = rd.choice(self.friend)
            return mons

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
        # 攻撃時のメッセージを表示
        enemy_or_friend = ""
        if offense_is_friend==True:
            enemy_or_friend = "味方の"
        elif offense_is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(enemy_or_friend+offense_name+using_skill["message"])
        # 攻撃側のMPが足りない場合は攻撃をキャンセル
        if self.mp[offense_is_friend][offense_name]<using_skill["mp_consumption"]:
            window.show_message("しかしMPが足りない！")
            return None
        # 攻撃側の与ダメージと自傷ダメージを計算する
        damage = self.calc_damage(
            skill_name,
            offensing_monster["attack"],
            offensing_monster["magic_attack"],
            defending_monster["defense"],
            defending_monster["attribute_damage_rate"]
        )
        self_damage = max(0, math.ceil(damage*using_skill["self_damage_ratio_to_calc_damage"]))
        # 防御側のHPと攻撃側のMPを減らす
        self.hp[defense_is_friend][defense_name] = max(self.hp[defense_is_friend][defense_name]-damage, 0)
        self.mp[offense_is_friend][offense_name] -= using_skill["mp_consumption"]
        # 攻撃側のMPの表示を変更する
        self.update_hp_mp_text(offense_name, offense_is_friend, "mp", self.mp[offense_is_friend][offense_name])
        # 防御側の被ダメージ時のメッセージを表示
        enemy_or_friend = ""
        if defense_is_friend==True:
            enemy_or_friend = "味方の"
        elif defense_is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(f"{enemy_or_friend}{defending_monster['name']}に{damage}のダメージ！")
        # 防御側のHPの表示を変更する
        self.update_hp_mp_text(defense_name, defense_is_friend, "hp", self.hp[defense_is_friend][defense_name])
        # 防御側のdeadフラグを更新して、死亡時のメッセージを表示
        if self.hp[defense_is_friend][defense_name]==0:
            self.kill_monster(defense_name, defense_is_friend)
        # 自傷ダメージ
        if self_damage>0:
            # 攻撃側のHPを減らす
            self.hp[offense_is_friend][offense_name] -= self_damage
            self.update_hp_mp_text(offense_name, offense_is_friend, "hp", self.hp[offense_is_friend][offense_name])
            # 攻撃側の被ダメージ時のメッセージを表示
            if offense_is_friend==True:
                enemy_or_friend = "味方の"
            elif offense_is_friend==False:
                enemy_or_friend = "敵の"
            window.show_message(f"{enemy_or_friend}{offense_name}に{self_damage}のダメージ！")
            # 攻撃側のHPの表示を変更する
            self.update_hp_mp_text(offense_name, offense_is_friend, "hp", self.hp[offense_is_friend][offense_name])
            # 攻撃側のdeadフラグを更新して、死亡時のメッセージを表示
            if self.hp[offense_is_friend][offense_name]==0:
                self.kill_monster(offense_name, offense_is_friend)
        # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
        # Falseで終了
        if any([self.dead[0][name]==False for name in self.enemy]) and any([self.dead[1][name]==False for name in self.friend]):
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
                is_friend = None
                if offense_enemy_or_friend=="enemy":
                    is_friend = False
                elif offense_enemy_or_friend=="friend":
                    is_friend = True
                if self.dead[is_friend][name]==True:
                    continue
                # 攻撃する
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
                continue_ = self.attack_on_monster(
                    skill_name,
                    offensing_monster,
                    offense_is_friend,
                    defensing_monster
                )
                # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する                
                if continue_==False:
                    if all([self.dead[0][name] for name in self.dead[0]]):
                        window.show_message("バトルに勝利した！")
                    elif all([self.dead[1][name] for name in self.dead[1]]):
                        window.show_message("全滅してしまった...")
                    sleep(BATTLE_FINISH_DURATION)
                    break_ = True
                    break
            if break_:
                break

def battle(party_enemy: list, party_friend: list) -> None:
    """
    バトルを行う
    party_enemy: 敵のパーティーの配列
    party_friend: 味方のパーティーの配列
    """
    btl = Battle(party_enemy, party_friend)
    btl.battle_start_auto()

def param_level_up(param: int, is_mp: bool) -> int:
    """
    レベルアップ後のパラメータを返す
    param: 強化される前の値
    is_mp: MPかどうか
    """
    if is_mp and param==0:
        return 2
    if is_mp:
        return max(999, math.ceil(param*1.05))
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
    height = 670
)
canvas.pack()

# システムウィンドウのインスタンス
window = Window()
window.make_message_box()

# debug
if 1:
    battle(
        ["スライム", "おばけキノコ", "ボストロール"],
        ["ドラキー", "スライム", "ボストロール"]
    )
    app.mainloop()

"""
メモ

・パーティー内のモンスターの重複禁止
"""
