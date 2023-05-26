# ライブラリをインポート
from time import sleep
from typing import Union
import pygame
import math
import numpy as np
import random as rd

# クラスをインポート
from json_import import *
from config import *
from ui import ui
from user_info import user_info

# ライブラリの初期設定
pygame.init()

class Battle:
    """
    バトルを行う
    """
    def __init__(self) -> None:
        self.enemy = None
        self.friend = None
        # バトル時のログ
        self.log_list = []
        # モンスタ―とUIの座標の対応関係
        self.elem_coord = {}
    
    def set_enemy(self, enemy: list) -> None:
        """
        敵パーティーを設定する
        """
        self.enemy = enemy
        # パーティー内でモンスターの重複があったら強制終了
        if len(set(self.enemy))<=2:
            print("敵パーティー内でモンスターが重複しています。")
            exit()

    def set_friend(self) -> None:
        """
        味方パーティーを設定する
        """
        self.friend = user_info.friend
    
    def init_param(self) -> None:
        """
        モンスターの情報を初期化する
        """
        # バトル時のパラメータ
        self.hp = [
            {monster[name]["name"]: monster[name]["hp"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["hp"] for name in self.friend}
        ]
        self.hp_init = [
            {monster[name]["name"]: monster[name]["hp"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["hp"] for name in self.friend}
        ]
        self.mp = [
            {monster[name]["name"]: monster[name]["mp"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["mp"] for name in self.friend}
        ]
        self.mp_init = [
            {monster[name]["name"]: monster[name]["mp"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["mp"] for name in self.friend}
        ]
        self.attack = [
            {monster[name]["name"]: monster[name]["attack"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["attack"] for name in self.friend}
        ]
        self.attack_init = [
            {monster[name]["name"]: monster[name]["attack"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["attack"] for name in self.friend}
        ]
        self.magic_attack = [
            {monster[name]["name"]: monster[name]["magic_attack"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["magic_attack"] for name in self.friend}
        ]
        self.magic_attack_init = [
            {monster[name]["name"]: monster[name]["magic_attack"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["magic_attack"] for name in self.friend}
        ]
        self.defense = [
            {monster[name]["name"]: monster[name]["defense"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["defense"] for name in self.friend}
        ]
        self.defense_init = [
            {monster[name]["name"]: monster[name]["defense"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["defense"] for name in self.friend}
        ]
        self.agility = [
            {monster[name]["name"]: monster[name]["agility"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in self.friend}
        ]
        self.agility_init = [
            {monster[name]["name"]: monster[name]["agility"] for name in self.enemy},
            {monster[name]["name"]: monster[name]["agility"] for name in self.friend}
        ]
        self.dead = [
            {monster[name]["name"]: False for name in self.enemy},
            {monster[name]["name"]: False for name in self.friend}
        ]
        # レベルに合わせてパラメータを変更する
        for name in self.enemy:
            self.reflect_level(name, False, monster[name]["level"])
        for name in self.friend:
            self.reflect_level(name, True, monster[name]["level"])
    
    def init_ui(self) -> None:
        # 0がenemyのUI, 1がfriendのUI
        self.name_box = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        self.name_text = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        self.hp_box = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        self.hp_text = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        self.mp_box = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        self.mp_text = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend}
        ]
        # 画像データ
        self.image = [
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend},
        ]
    
    def plot_image_battle(self) -> None:
        """
        敵と味方のパーティーの画像を表示
        """
        i = 0
        for name in self.enemy:
            width = 212*i+175
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 8
            ui.plot_image(name, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        i = 0
        for name in self.friend:
            width = 222*i+170
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 520
            ui.plot_image(name, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        ui.canvas.update()
    
    def draw_battle_ui(self) -> None:
        """
        UIを描画する
        """
        # Tkinterのインスタンスを生成
        ui.make_tk_window()
        # UIを削除
        ui.canvas.delete("all")
        # メッセージボックスを作成
        ui.make_message_box()
        # 敵と味方の名前、HP、MPを表示する
        self.make_party(self.enemy, "name", False)
        self.make_party(self.enemy, "hp", False)
        self.make_party(self.enemy, "mp", False)
        self.make_party(self.friend, "name", True)
        self.make_party(self.friend, "hp", True)
        self.make_party(self.friend, "mp", True)
        # 敵と味方の画像を表示する
        self.plot_image_battle()
        ui.canvas.update()
    
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
            elem = ui.canvas.create_rectangle(
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
            elem = ui.canvas.create_text(
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
        ui.canvas.update()

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
            ui.canvas.delete(self.hp_text[is_friend][name])
        elif type_=="mp":
            ui.canvas.delete(self.mp_text[is_friend][name])
        start_x, start_y = self.elem_coord[(name, type_, is_friend)]
        width, height = 160, 40
        end_x, end_y = start_x+width, start_y+height
        # テキストを表示する
        if type_=="hp":
            max_val = self.hp_init[is_friend][name]
        elif type_=="mp":
            max_val = self.mp_init[is_friend][name]
        elem = ui.canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"{param} / {max_val}",
            font = ("", 12)
        )
        if type_=="hp":
            self.hp_text[is_friend][name] = elem
        elif type_=="mp":
            self.mp_text[is_friend][name] = elem
        ui.canvas.update()
    
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
        ui.show_message(message, False, self.log_list)
        # deadフラグを更新
        self.dead[is_friend][name] = True
        # 画像を削除
        self.delete_image(name, is_friend)
        ui.canvas.update()
    
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
        self.name_box[is_friend][name] = ui.canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#ddd",
            outline = color
        )
        # テキストを表示する
        self.name_text[is_friend][name] = ui.canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = name,
            font = ("", 12)
        )
        ui.canvas.update()

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

    def attack_on_monster(self, skill_name: str, offense_name: str, offense_is_friend: bool, defense_name: str) -> Union[bool, None]:
        """
        モンスターからモンスターに攻撃する
        バトルを継続するときにTrue、終了するときにFalse、MPが足りない場合はNoneを返す
        skill_name: 技の名前
        offense_name: 攻撃側のモンスターの名前
        offense_is_friend: 攻撃側のモンスターが味方であるかどうか
        defense_name: 防御側のモンスターの名前
        """
        # 使うスキルを設定
        using_skill = skill[skill_name]
        # 全体攻撃かどうか
        if using_skill["range"]=="all":
            is_all = True
        elif using_skill["range"]=="single" or using_skill["range"]==None:
            is_all = False
        # ダメージが逓減するかどうか
        if using_skill["is_decreasing"]==True:
            is_decreasing = True
        elif using_skill["is_decreasing"]==False:
            is_decreasing = False
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
        # 攻撃時のメッセージを表示
        if offense_is_friend==True:
            enemy_or_friend = "味方の"
        elif offense_is_friend==False:
            enemy_or_friend = "敵の"
        message = enemy_or_friend+offense_name+using_skill["message"]
        ui.show_message(message, False, self.log_list)
        # 攻撃側のMPが足りない場合は攻撃をキャンセル
        if self.mp[offense_is_friend][offense_name]<using_skill["mp_consumption"]:
            message = "しかしMPが足りない！"
            ui.show_message(message, False, self.log_list)
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
        # ダメージが逓減する割合
        damage_decreasing_rate = 1
        # 攻撃する
        for defending_monster in defending_side:
            # skill「ミス」を使用する
            # 攻撃がミスする
            if skill_name=="ミス" or self.is_n_percent(using_skill["miss_probability"]*100)==True:
                message = f"ミス！{enemy_or_friend}{defending_monster['name']}はダメージを受けない！"
                ui.show_message(message, show_fast, self.log_list)
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
                    ui.show_message(message, False, self.log_list)
                elif using_skill["type"]=="magic" and is_first_attack==True:
                    message = f"{offense_name}の魔力が暴走した！"
                    ui.show_message(message, False, self.log_list)
            # 攻撃側の与ダメージと自傷ダメージを計算する
            damage = self.calc_damage(
                skill_name,
                offensing_monster["attack"],
                offensing_monster["magic_attack"],
                defending_monster["defense"],
                defending_monster["attribute_damage_rate"],
                is_critical,
            )*damage_decreasing_rate
            damage = math.ceil(damage)
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
                ui.show_message(message, show_fast, self.log_list)
            # ダメージを無効化した、または攻撃を回避した
            else:
                message = f"ミス！{enemy_or_friend}{defending_monster['name']}はダメージを受けない！"
                ui.show_message(message, show_fast, self.log_list)
            # 防御側のHPの表示を変更する
            self.update_hp_mp_text(defending_monster["name"], defense_is_friend, "hp", self.hp[defense_is_friend][defending_monster["name"]])
            # 防御側のdeadフラグを更新して、死亡時のメッセージを表示
            if self.hp[defense_is_friend][defending_monster["name"]]==0:
                self.kill_monster(defending_monster["name"], defense_is_friend)
            is_first_attack = False
            # ダメージを減少させる
            decreasing_rate_of_decreasing_rate = 0.25
            if is_decreasing==True:
                damage_decreasing_rate -= decreasing_rate_of_decreasing_rate
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
            ui.show_message(message, False, self.log_list)
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
    
    def turns_process(self) -> None:
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
                        defending_monster
                    )
                # 全体攻撃
                elif skill[skill_name]["range"]=="all":
                    # 防御側のパーティーが全滅したかどうか
                    continue_ = self.attack_on_monster(
                        skill_name,
                        offensing_monster,
                        offense_is_friend,
                        None
                    )
                # 両方のチームで1体以上のモンスターが生きている場合、バトルを継続する
                if continue_==False:
                    if all([self.dead[0][name] for name in self.dead[0]]):
                        message = "バトルに勝利した！"
                        winner = "friend"
                        ui.show_message(message, False, self.log_list)
                    elif all([self.dead[1][name] for name in self.dead[1]]):
                        message = "全滅してしまった..."
                        winner = "enemy"
                        ui.show_message(message, False, self.log_list)
                    sleep(BATTLE_FINISH_DURATION)
                    break_ = True
                    break
            # 戦闘が終了した
            if break_:
                # 戦闘BGMを停止する
                pygame.mixer.music.stop()
                # 戦闘終了BGMを流す
                if winner=="friend":
                    pygame.mixer.music.load("music/勝利.mp3")
                elif winner=="enemy":
                    pygame.mixer.music.load("music/全滅.mp3")
                pygame.mixer.music.play()
                break

    def play_music(self, file_name: str) -> None:
        """
        音声を再生する
        file_name: ファイル名
        """
        pygame.mixer.music.load(file_name)
        pygame.mixer.music.play(-1)

    def is_n_percent(self, prob: int) -> bool:
        """
        probパーセントの確率でTrueを返す
        prob: Trueが返ってくる確率(0~100)
        """
        r = rd.randint(1, 100)
        if r<=prob:
            return True
        return False

    def start_battle(self, enemy: list) -> None:
        """
        バトルを行う
        enemy: 敵パーティー
        """
        # 味方パーティーを設定
        self.set_friend()
        # 敵パーティーを設定
        self.set_enemy(enemy)
        # モンスターのパラメータを初期化
        self.init_param()
        # モンスターのUIを初期化
        self.init_ui()
        # UIを表示
        self.draw_battle_ui()
        # 戦闘BGMを再生
        self.play_music("music/戦闘.mp3")
        # メッセージを表示
        ui.show_message("魔物の群れが現れた！", False, None)
        # 開始まで間隔を空ける
        sleep(BATTLE_START_DURATION)
        # ターンを開始する
        self.turns_process()
        # Tkinterのインスタンスを削除する
        ui.app.destroy()

battle = Battle()