from time import sleep
from typing import Union
import tkinter as tk
import json
import math
import numpy as np
import random as rd

if 0:
    SHOW_DURATION = 1.5
    BATTLE_START_DURATION = 1
else:
    SHOW_DURATION = 0.3
    BATTLE_START_DURATION = 0.5
BATTLE_FINISH_DURATION = 2

class SelfInfo:
    def __init__(self) -> None:
        """
        プレイヤーに関する情報を持つ
        """
        self.friend = [None]*3

    def set_friend(self, friend: list[str]) -> None:
        """
        自分のパーティーを設定する
        """
        self.friend = friend

class Window:
    def __init__(self) -> None:
        """
        画面にUIを表示する
        """
        self.message_box = None
        self.message_text = None
        self.button = [None]*3
        self.enemy = [None]*3
    
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
    
    def show_message(self, message: str, is_fast: bool) -> None:
        """
        メッセージを表示（変更）する
        message: 表示するメッセージ
        is_fast: 表示間隔を短くするかどうか
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
        battle(self.enemy, self_info.friend)
    
    def make_three_buttons(self, text: list[str]) -> None:
        """
        前、左、右の三方向に進むボタンを表示する
        """
        for i in range(3):
            self.button[i] = tk.Button(
                app,
                text=text[i],
                font=("", 20),
                width=13,
                height=3
            )
            self.button[i].pack()
            self.button[i].place(x=230*i+100, y=200)
            # self.button[i].bind("<1>", self.encounter)
    
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

    def plot_image(self, name: str, is_friend: bool, path: str, x: int, y: int, i: int) -> None:
        """
        画像を表示
        name: モンスターの名前
        is_friend: 味方であるかどうか
        path: 画像のパス
        x: x座標
        y: y座標
        i: index
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
            width = 130+220*i
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 8
            self.plot_image(name, False, f"images/png_resized/{name}_resized.png", width, height, i)
            i += 1
        i = 0
        for name in self.friend:
            width = 130+220*i
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 520
            self.plot_image(name, True, f"images/png_resized/{name}_resized.png", width, height, 3+i)
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
        enemy_or_friend = None
        if is_friend==True:
            enemy_or_friend = "味方の"
        elif is_friend==False:
            enemy_or_friend = "敵の"
        window.show_message(f"{enemy_or_friend}{name}は力尽きた...", False)
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
        max_val = None
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

    def attack_on_monster(self, skill_name: str, offense_name: str, offense_is_friend: bool, defense_name: str, mp_consume: bool, show_fast: bool) -> Union[bool, None]:
        """
        モンスターからモンスターに攻撃する
        バトルを継続するときにTrue、終了するときにFalse、MPが足りない場合はNoneを返す
        skill_name: 技の名前
        offense_name: 攻撃側のモンスターの名前
        offense_is_friend: 攻撃側のモンスターが味方であるかどうか
        defense_name: 防御側のモンスターの名前
        mp_consume: MPを消費するかどうか（全体攻撃で最初の攻撃かどうか）
        show_fast: 表示間隔を短くするかどうか（全体攻撃かどうか）
        """
        if offense_is_friend==True:
            defense_is_friend = False
        elif offense_is_friend==False:
            defense_is_friend = True
        offensing_monster = {
            "attack": self.attack[offense_is_friend][offense_name],
            "magic_attack": self.magic_attack[offense_is_friend][offense_name]
        }
        defending_monster = {
            "name": defense_name,
            "defense": self.defense[defense_is_friend][defense_name],
            "attribute_damage_rate": monster[defense_name]["attribute_damage_rate"]
        }
        using_skill = skill[skill_name]
        # 攻撃時のメッセージを表示
        if mp_consume==True:
            enemy_or_friend = ""
            if offense_is_friend==True:
                enemy_or_friend = "味方の"
            elif offense_is_friend==False:
                enemy_or_friend = "敵の"
            window.show_message(enemy_or_friend+offense_name+using_skill["message"], False)
        # 攻撃側のMPが足りない場合は攻撃をキャンセル
        if mp_consume==True and self.mp[offense_is_friend][offense_name]<using_skill["mp_consumption"]:
            window.show_message("しかしMPが足りない！", False)
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
        if mp_consume==True:
            self.mp[offense_is_friend][offense_name] -= using_skill["mp_consumption"]
            # 攻撃側のMPの表示を変更する
            self.update_hp_mp_text(offense_name, offense_is_friend, "mp", self.mp[offense_is_friend][offense_name])
        # 防御側の被ダメージ時のメッセージを表示
        enemy_or_friend = ""
        if defense_is_friend==True:
            enemy_or_friend = "味方の"
        elif defense_is_friend==False:
            enemy_or_friend = "敵の"
        # 全体攻撃のときは表示間隔を短くする
        window.show_message(f"{enemy_or_friend}{defending_monster['name']}に{damage}のダメージ！", show_fast)
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
            window.show_message(f"{enemy_or_friend}{offense_name}に{self_damage}のダメージ！", False)
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
                offense_is_friend = None
                if offense_enemy_or_friend=="enemy":
                    offense_is_friend = False
                elif offense_enemy_or_friend=="friend":
                    offense_is_friend = True
                skill_name = self.select_skill(monster[offensing_monster]["skill_select_probability"][offense_enemy_or_friend])
                continue_ = None
                # 単体攻撃
                if skill[skill_name]["range"]=="single":
                    defending_monster = self.select_monster_at_random(deffense_enemy_or_friend)
                    # 防御側のパーティーが全滅したかどうか
                    continue_ = self.attack_on_monster(
                        skill_name,
                        offensing_monster,
                        offense_is_friend,
                        defending_monster,
                        True,
                        False
                    )
                # 全体攻撃
                elif skill[skill_name]["range"]=="all":
                    continue_tmp = []
                    defending_side = None
                    defense_is_friend = None
                    if offense_is_friend==True:
                        defense_is_friend = False
                        defending_side = self.enemy
                    elif offense_is_friend==False:
                        defense_is_friend = True
                        defending_side = self.friend
                    first_attack = True
                    # 防御側のパーティー全体に攻撃する
                    for defending_monster in defending_side:
                        # 死んでいたら攻撃の対象にならない
                        if self.dead[defense_is_friend][defending_monster]==True:
                            continue
                        is_continue = self.attack_on_monster(
                            skill_name,
                            offensing_monster,
                            offense_is_friend,
                            defending_monster,
                            first_attack,
                            True
                        )
                        if is_continue!=None:
                            first_attack = False
                        continue_tmp.append(is_continue)
                    sleep(SHOW_DURATION*0.5)
                    # 防御側のパーティーが全滅したかどうか
                    continue_ = all(judge!=False for judge in continue_tmp)
                # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
                if continue_==False:
                    if all([self.dead[0][name] for name in self.dead[0]]):
                        window.show_message("バトルに勝利した！", False)
                    elif all([self.dead[1][name] for name in self.dead[1]]):
                        window.show_message("全滅してしまった...", False)
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
    
    def fusion_monster(self, monster: list[str]) -> None:
        """
        モンスターを配合する
        """
        return 

def battle(party_enemy: list[str], party_friend: list[str]) -> None:
    """
    バトルを行う
    party_enemy: 敵のパーティーの配列
    party_friend: 味方のパーティーの配列
    """
    battle_ = Battle(party_enemy, party_friend)
    window.show_message("魔物の群れが現れた！", False)
    sleep(BATTLE_START_DURATION)
    battle_.battle_start_auto()

def game_start() -> None:
    """
    ゲーム全体を開始する
    """

# JSONデータを読み込む
with open("data/monster.json", encoding="utf-8") as data:
    monster = json.load(data)
with open("data/skill.json", encoding="utf-8") as data:
    skill = json.load(data)
with open("data/fusion_tree.json", encoding="utf-8") as data:
    fusion_tree = json.load(data)

# Tkinterの初期設定
app = tk.Tk()
app.title("DQLike")
canvas = tk.Canvas(
    app,
    width = 850,
    height = 670
)
canvas.pack()

# UIのインスタンス
window = Window()

# 自分の情報のインスタンス
self_info = SelfInfo()
self_info.set_friend(["スライム", "ドラキー", "ゴーレム"])

# debug
window.set_enemy(["スライム", "ボストロール", "おばけキノコ"])
window.make_three_buttons(["左", "前", "右"])

app.mainloop()

"""
To Do

・ゲルニック将軍を実装する
    ・ルカナン
    ・ドルマ
"""
"""
メモ

・パーティー内のモンスターの重複禁止
・自傷ダメージのある攻撃は、range=singleのみ
"""