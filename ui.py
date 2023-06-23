# ライブラリをインポート
from time import sleep
from copy import deepcopy
from numpy import base_repr
import tkinter as tk

# クラスをインポート
from config import *
from json_data import json_data
from user_info import user_info

class UI:
    """
    UIを表示する
    """
    def __init__(self) -> None:
        """
        画面にUIを表示する
        """
        # Tkinterのインスタンス
        self.app = None
        self.canvas = None
        # UIのインスタンス
        self.message_box = None
        self.message_text = None
        # バトル時のログ
        self.log_text = [None]*15
        # モンスターボックスでモンスターの詳細に遷移するボタン
        self.button_monster = [None]*12
        # モンスターボックスで次のページに進むボタン
        self.button_page_next_monster_box = None
        # モンスターボックスのテキスト
        self.text_monster_box = None
        # モンスターボックスで前のページに戻るボタン
        self.button_page_back_monster_box = None
        # モンスターボックスを閉じるボタン
        self.close_button_monster_box = None
        # モンスターボックスの「パーティー編成」のボタン
        self.party_edit_button = None
        # モンスターボックスの「決定」のボタン
        self.party_edit_end_button = None
        # モンスターボックスの画像データ
        self.image_monster_box = {name: [] for name in json_data.monster}
        # バトル時の敵パーティー
        self.enemy = None
        # バトル時の味方パーティー
        self.friend = None
        # バトル時の画像データ
        self.image_battle = None
        # 「all」でモンスター一覧モード、「detail」でモンスター詳細モード、「edit」でパーティー編成モード、「fusion」で配合モード
        self.window_mode = None
        # モンスターボックスのモードの文字
        self.text_monster_box_mode = None
        # モンスターボックスのページ数（0-indexed）
        self.page_monster_box = None
        # モンスターボックスのパーティーの枠
        self.party_frame = [None]*3
        # モンスターボックスのパーティーのモンスターの画像
        self.image_friend = [None]*3
        # モンスターボックスの仮の味方パーティー
        self.friend_tmp = []
        # モンスターボックスのモンスターの名前ボタンのNORMAL・DISABLED
        self.monster_button_state = [tk.NORMAL]*3000
        # モンスター情報のモンスターの画像
        self.monster_image_detail = None
        # モンスター情報のパラメータの文字のインスタンス
        self.text_monster_detail = {}
        # モンスター情報のスキルと特性のボタン
        self.button_monster_detail = {}
        # モンスタのー情報のスキル説明の文字のインスタンス
        self.text_skill_description = None
        # モンスター情報の画面を閉じるボタンのインスタンス
        self.close_button_monster_detail = None
        # スキル説明の枠
        self.skill_description_box = None
        # 配合画面のモンスターの枠
        self.monster_frame_fusion = {"parent_1": None, "parent_2": None, "child": None}
        # 配合画面のモンスターの画像
        self.monster_image_fusion = {"parent_1": None, "parent_2": None, "child": None}
        # 配合画面の文字
        self.text_fusion = {"parent_1": None, "parent_2": None, "child": None}
        # 配合画面の線
        self.line_fusion = None
        # 配合画面のモンスターのボタン
        self.monster_button_fusion = [None]*10
        # 配合画面の配合ボタン
        self.button_fusion = None
        # 配合の親モンスターのid
        self.fusion_parent_id = []
        # 配合先の子モンスター
        self.fusion_child = None
        # 配合画面で次のページに進むボタン
        self.button_page_next_fusion = None
        # 配合画面で前のページに戻るボタン
        self.button_page_back_fusion = None
        # 配合画面のページ数（0-indexed）
        self.page_fusion = None
        # 配合画面を閉じるボタン
        self.close_button_fusion = None
        # 配合画面で子モンスターの候補を表示するボタン
        self.button_show_child_candidate_fusion = None
        # 子モンスターの候補の名前ボタン
        self.button_child_candidate_fusion = [None]*12
        # 子モンスター候補を閉じるボタン
        self.button_close_child_candidate_fusion = None
        # 子モンスター情報を閉じるボタン
        self.button_close_child_detail_fusion = None
    
    def init_all_button(self) -> None:
        """
        すべてのボタンをNoneで初期化する
        """
        self.party_edit_button = None
        self.party_edit_end_button = None
        self.button_page_next_monster_box = None
        self.button_page_back_monster_box = None
        self.close_button_monster_box = None
        self.close_button_monster_detail = None
        self.button_monster = [None]*12
    
    def set_party(self, enemy: list, friend: list) -> None:
        """
        バトル時の敵と味方のパーティーを設定する
        enemy: 敵パーティー
        friend: 味方パーティー
        """
        # 敵パーティー
        self.enemy = enemy
        # 味方パーティー
        self.friend = friend
        # 画像データ（バトル）
        self.image_battle = [
            {json_data.monster[mons["name"]]["name"]: 0 for mons in self.enemy},
            {json_data.monster[mons["name"]]["name"]: 0 for mons in self.friend},
        ]
    
    def plot_image_monster_box(self, name: str, x: int, y: int) -> None:
        """
        モンスターの画像を表示する（モンスターボックス）
        name: モンスターの名前
        x: x座標
        y: y座標
        """ 
        # 画像のパス
        path = f"images/png_resized/{name}_resized.png",
        # イメージを作成
        self.image_monster_box[name].append(tk.PhotoImage(file=path, width=130, height=130))
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_monster_box[name][-1], anchor=tk.NW)
    
    def plot_image_battle(self, name: str, is_friend: bool, x: int, y: int) -> None:
        """
        モンスターの画像を表示する（バトル）
        name: モンスターの名前
        is_friend: 味方かどうか
        x: x座標
        y: y座標
        """
        # 画像のパス
        path = f"images/png_resized/{name}_resized.png",
        # イメージを作成
        self.image_battle[is_friend][name] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_battle[is_friend][name], anchor=tk.NW)
    
    def plot_image_party(self, name: str, idx: int) -> None:
        """
        モンスターの画像を表示する（パーティー）
        name: モンスターの名前
        index: 左から何番目であるか（1~3）の値
        """
        # 画像の左上のxy座標
        x = idx*165+410
        if name=="ドラキー" or name=="ボストロール":
            x -= 20
        y = 37
        # 画像のパス
        path = f"images/png_resized/{name}_resized.png"
        # イメージを作成
        self.image_friend[idx] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_friend[idx], anchor=tk.NW)
    
    def plot_image_fusion(self, name: str, mode: str) -> None:
        """
        モンスターの画像を表示する（配合画面）
        name: モンスターの名前
        parent_or_child: 「parent_1」「parent_2」「child」のどれか
        """ 
        # 画像のパス
        path = f"images/png_resized/{name}_resized.png",
        # 画像の座標
        if mode=="parent_1":
            x, y = 125, 145
        elif mode=="parent_2":
            x, y = 130, 330
        elif mode=="child":
            x, y = 420, 230
        if name=="ドラキー" or name=="ボストロール":
            x -= 20
        # イメージを作成
        self.monster_image_fusion[mode] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.monster_image_fusion[mode], anchor=tk.NW)
    
    def plot_image_monster_detail(self, name: str) -> None:
        """
        モンスターの画像を表示する（モンスター情報）
        name: モンスターの名前
        """
        # 画像の左上のxy座標
        x = 150
        if name=="ドラキー" or name=="ボストロール":
            x -= 20
        y = 100
        # 画像のパス
        path = f"images/png_resized/{name}_resized.png"
        # イメージを作成
        self.monster_image_detail = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.monster_image_detail, anchor=tk.NW)
    
    def remove_image_party(self, name: str) -> None:
        """
        モンスターの画像を削除する（パーティー）
        name: モンスターの名前
        """
        for idx, mons in enumerate(self.friend_tmp):
            if mons["name"]==name:
                self.image_friend[idx] = None
        self.canvas.update()
    
    def remove_image_party_all(self) -> None:
        """
        すべてのモンスターの画像を削除する（パーティー）
        """
        for i in range(3):
            self.image_friend[i] = None
        self.canvas.update()
    
    def make_tk_window(self, window_title: str) -> None:
        """
        Tkinterの画面を描画する
        window_title: 画面の左上に表示するタイトル
        """
        self.app = tk.Tk()
        # ウィンドウをアクティブにする
        self.app.focus_force()
        self.app.title(window_title)
        width = 1200
        height = 620
        left = 60
        top = 30
        self.app.geometry(f"{width}x{height}+{left}+{top}")
        # 画面のサイズ変更を禁止
        self.app.resizable(0, 0)
        # canvasを描画
        self.canvas = tk.Canvas(
            self.app,
            width = width,
            height = height
        )
        self.canvas.pack()
        self.canvas.update()

    def delete_all_ui(self) -> None:
        """
        すべてのUIを削除する
        """
        self.canvas.delete("all")
        if self.button_page_next_monster_box is not None:
            self.button_page_next_monster_box.destroy()
            self.button_page_next_monster_box = None
        if self.button_page_back_monster_box is not None:
            self.button_page_back_monster_box.destroy()
            self.button_page_back_monster_box = None
        for i in range(12):
            if self.button_monster[i] is not None:
                self.button_monster[i].destroy()
                self.button_monster[i] = None

    def delete_all_ui_detail(self) -> None:
        """
        すべてのUIを削除する（モンスター情報）
        """
        self.canvas.delete("all")
        for key, button in self.button_monster_detail.items():
            button.destroy()
        self.button_monster_detail = {}
    
    def delete_all_ui_child_all(self) -> None:
        """
        すべてのUIを削除する（子モンスター候補）
        """
        for i in range(12):
            if self.button_child_candidate_fusion[i] is not None:
                self.button_child_candidate_fusion[i].destroy()
                self.button_child_candidate_fusion[i] = None

    def make_message_box(self) -> None:
        """
        メッセージボックスを生成する
        """
        start_x, start_y = 90, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_box = self.canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#eee",
            outline = "#777"
        )
        self.canvas.update()
    
    def show_message(self, message: str, is_fast: bool, log_list: list[str]) -> None:
        """
        メッセージを表示（変更）する
        message: 表示するメッセージ
        is_fast: 表示間隔を短くするかどうか
        log_list: 表示するログのリスト
        """
        # メッセージを表示する
        # すでにメッセージが書いてある場合は消去する
        if self.message_text is not None:
            self.canvas.delete(self.message_text)
        # メッセージを表示する
        start_x, start_y = 70, 275
        width, height = 700, 60
        end_x, end_y = start_x+width, start_y+height
        self.message_text = self.canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            font = ("helvetica", 18),
            text = message
        )
        # ログを表示する
        LOG_NUM = 15
        # すでにログが書いてある場合は削除する
        for i in range(LOG_NUM):
            self.canvas.delete(self.log_text[i])
        # ログを出力する
        if log_list is not None:
            log_list.append(message)
            if len(log_list)>LOG_NUM:
                log_list.pop(0)
            for i,content in enumerate(log_list):
                start_x, start_y = 950, 27*(i+1)
                width, height = 100, 30
                end_x, end_y = start_x+width, start_y+height
                self.log_text[i] = self.canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    font = ("helvetica", 12),
                    text = content
                )
        self.canvas.update()
        if is_fast==True:
            sleep(SHOW_DURATION*0.3)
        elif is_fast==False:
            sleep(SHOW_DURATION)
    
    def make_close_button_monster_box(self) -> None:
        # モンスターボックスを閉じるボタンを表示
        self.close_button_monster_box = tk.Button(
            self.app,
            text="x",
            font=("", 18),
            width=2,
            height=1,
            bg="#f44",
            command=self.close_monster_box
        )
        left = 0
        top = 0
        self.close_button_monster_box.place(relx=left, rely=top)
        self.app.bind("<KeyPress>", self.listen_key)
    
    def party_edit_end(self) -> None:
        """
        パーティー編集モードを終了する
        """
        # パーティーにモンスターが1体以上いる
        if len(self.friend_tmp)>=1:
            # パーティーを確定する
            user_info.friend = deepcopy(self.friend_tmp)
            # 「パーティー編成へ」のボタンを表示
            self.make_party_edit_button()
            # ウィンドウを閉じるボタンの色を変えて、状態をtk.NORMALにする
            self.close_button_monster_box["state"] = tk.NORMAL
            self.close_button_monster_box["bg"] = "#f44"
            # モンスターを1ページ分表示
            self.show_monster()
    
    def update_text_monster_box_mode(self) -> None:
        """
        モンスターボックスのモードの文字を更新
        """
        # モンスターボックスのモードの文字を削除
        if self.text_monster_box_mode is not None:
            self.canvas.delete(self.text_monster_box_mode)
        # モンスターボックスモードの文字を表示
        left = 200
        top = 120
        if self.window_mode=="all":
            text = "モンスター情報"
        elif self.window_mode=="edit":
            text = "パーティー編成"
        self.text_monster_box_mode = self.canvas.create_text(
            left, top,
            text=text,
            font=("", 20)
        )
    
    def make_party_edit_button(self) -> None:
        """
        「パーティー編成へ」のボタンを表示
        モンスター情報モードに移行する
        """
        # 「決定」のボタンを削除
        if self.party_edit_end_button is not None:
            self.party_edit_end_button.destroy()
            self.party_edit_end_button = None
        # モンスター情報のスキル（と特性（今はない））のボタンを削除
        for skill_name, id_ in self.button_monster_detail.items():
            id_.destroy()
        self.button_monster_detail = {}
        # モンスターボックスモードを設定
        self.window_mode = "all"
        # 「パーティー編成へ」のボタンを削除
        if self.party_edit_button is not None:
            self.party_edit_button.destroy()
            self.party_edit_button = None
        # 「パーティー編成へ」のボタンを表示
        self.party_edit_button = tk.Button(
            self.app,
            text="パーティー編成へ",
            font=("", 18),
            width=16,
            height=2,
            command=self.make_party_edit_end_button
        )
        left = 900
        top = 50
        self.party_edit_button.place(x=left, y=top)
        # モンスターボックスのモードの文字を更新
        self.update_text_monster_box_mode()
    
    def make_party_edit_end_button(self) -> None:
        """
        「決定」のボタンを表示
        パーティー編成モードに移行する
        """
        # 「パーティー編成へ」のボタンを削除
        if self.party_edit_button is not None:
            self.party_edit_button.destroy()
            self.party_edit_button = None
        # モンスターボックスモードを設定
        self.window_mode = "edit"
        # 「決定」のボタンを表示
        self.party_edit_end_button = tk.Button(
            self.app,
            text="決定",
            font=("", 18),
            width=16,
            height=2,
            command=self.party_edit_end
        )
        left = 900
        top = 50
        self.party_edit_end_button.place(x=left, y=top)
        # モンスターボックスのモードの文字を更新
        self.update_text_monster_box_mode()
        # 仮の味方パーティーを設定
        self.friend_tmp = deepcopy(user_info.friend)
        # 編成されているモンスターのボタンの状態をtk.DISABLEDにする
        for i in range(self.page_monster_box*12, min((self.page_monster_box+1)*12, len(json_data.save_data["monster"]))):
            if self.monster_button_state[i]==tk.NORMAL:
                self.button_monster[i%12]["state"] = tk.NORMAL
            elif self.monster_button_state[i]==tk.DISABLED:
                self.button_monster[i%12]["state"] = tk.DISABLED
        # ウィンドウを閉じるボタンの色を変えて、状態をtk.DISABLEDにする
        self.close_button_monster_box["state"] = tk.DISABLED
        self.close_button_monster_box["bg"] = "#ddd"

    def make_party_edit_frame(self) -> None:
        """
        パーティー編成の枠を表示
        """
        for i in range(3):
            start_x, start_y = 165*(i-1)+550, 20
            width, height = 140, 120
            end_x, end_y = start_x+width, start_y+height
            self.party_frame[i] = self.canvas.create_rectangle(
                start_x, start_y,
                end_x, end_y,
                fill = "#eee",
                outline = "#777",
                width=3
            )
    
    def listen_key(self, event) -> None:
        """
        キー入力を受け取る
        """
        if event.keysym=="e":
            # eでモンスターボックスを閉じる
            if self.window_mode=="all":
                self.close_monster_box()
            # eでモンスター情報を閉じる
            elif self.window_mode=="detail":
                # モンスターボックスからのとき
                self.close_monster_detail()
            elif self.window_mode=="child_all":
                # 親モンスター選択からのとき
                self.close_monster_candidate_child()
            elif self.window_mode=="child_detail":
                # 子モンスター候補からのとき
                self.close_monster_detail_child()
        # fでモンスター配合所を閉じる
        if event.keysym=="f" and self.window_mode=="fusion":
            self.close_fusion_screen()
        # →でモンスターボックスの次ページを表示
        elif event.keysym=="Right" and (self.window_mode=="all" or self.window_mode=="edit") and self.page_monster_box<len(json_data.save_data["monster"])//12 and len(json_data.save_data["monster"])//12!=len(json_data.save_data["monster"])/12:
            self.show_next_page_monster_box()
        # ←でモンスターボックスの前ページを表示
        elif event.keysym=="Left" and (self.window_mode=="all" or self.window_mode=="edit") and self.page_monster_box>0:
            self.show_previous_page_monster_box()
        # →でモンスター配合所の次ページを表示
        elif event.keysym=="Right" and self.window_mode=="fusion" and self.page_fusion<len(json_data.save_data["monster"])//10 and len(json_data.save_data["monster"])//12!=len(json_data.save_data["monster"])/12:
            self.show_next_page_fusion()
        # ←でモンスター配合所の前ページを表示
        elif event.keysym=="Left" and self.window_mode=="fusion" and self.page_fusion>0:
            self.show_previous_page_fusion()
    
    def show_party_image(self) -> None:
        """
        パーティーの画像を表示する
        """
        for idx, mons in enumerate(self.friend_tmp):
            self.plot_image_party(mons["name"], idx)
    
    def open_monster_box(self) -> None:
        """
        自分が持っているモンスターを表示する
        """
        # モンスターボックスのページ数を初期化
        self.page_monster_box = 0
        # すべてのボタンを初期化
        self.init_all_button()
        # 仮の味方パーティーを初期化
        self.friend_tmp = deepcopy(user_info.friend)
        # モンスターの名前のボタンの状態を初期化
        for idx in json_data.save_data["monster"]:
            mons = json_data.save_data["monster"][idx]
            # そのモンスターがパーティーに含まれていたら
            if mons in self.friend_tmp:
                self.monster_button_state[int(idx)-1] = tk.DISABLED
            # そのモンスターがパーティーに含まれていなかったら
            else:
                self.monster_button_state[int(idx)-1] = tk.NORMAL
        # モンスターボックスのモードを設定
        self.window_mode = "all"
        # Tkinterのウィンドウを表示
        self.make_tk_window("モンスターボックス")
        # 画面を閉じるボタンを表示
        self.make_close_button_monster_box()
        # 「パーティー編成へ」のボタンを表示
        self.make_party_edit_button()
        # モンスターボックスの1ページ目を表示
        self.show_monster()

    def show_monster(self) -> None:
        """
        モンスターを1ページ分表示する
        """
        # 既存のUIを削除
        self.delete_all_ui()
        # モンスターボックスのモードの文字を更新
        self.update_text_monster_box_mode()
        # 「モンスターボックス」の文字を表示
        start_x, start_y = 60, 30
        width, height = 300, 60
        end_x, end_y = start_x+width, start_y+height
        # 文字が設定してあれば削除する
        if self.text_monster_box is not None:
            self.canvas.delete(self.text_monster_box)
        if len(json_data.save_data["monster"])//12==len(json_data.save_data["monster"])/12:
            page_all = len(json_data.save_data["monster"])//12
        else:
            page_all = len(json_data.save_data["monster"])//12+1
        # 「モンスターボックス」の文字とページ数を表示
        self.text_monster_box = self.canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"モンスターボックス（{self.page_monster_box+1}／{page_all}）",
            font = ("", 22)
        )
        # パーティーの枠を表示
        self.make_party_edit_frame()
        # パーティーの画像を表示
        self.show_party_image()
        # モンスターの画像と詳細ボタンを表示
        for i in range(self.page_monster_box*12, min((self.page_monster_box+1)*12, len(json_data.save_data["monster"]))):
            name = json_data.save_data["monster"][str(i+1)]["name"]
            # 画像を表示
            width = 247*(i%4)+190
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = (150*(i//4)+140)%450+10
            self.plot_image_monster_box(name, width, height)
            # モンスターの名前のボタンを表示
            # ボタンの色によってボタンを区別する
            color = f"#eeeee{base_repr(i%12, 16)}"
            # モンスターの名前ボタンのNORMAL・DISABLED
            if self.window_mode=="all":
                button_state = tk.NORMAL
            else:
                button_state = self.monster_button_state[i]
            self.button_monster[i%12] = tk.Button(
                self.app,
                text=f"{name} Lv.{json_data.save_data['monster'][str(i+1)]['level']}",
                font=("", 18),
                width=16,
                height=1,
                bg=color,
                state=button_state
            )
            self.button_monster[i%12].pack()
            left = 0.21*(i%4)+0.1
            top = (0.24*(i//4))%0.72+0.4
            # ボタンを配置
            self.button_monster[i%12].place(relx=left, rely=top)
            # ボタンを押したときの処理
            self.button_monster[i%12].bind("<ButtonPress>", self.press_monster_name_button)
        # 次のページに進むボタンを表示
        if (self.page_monster_box+1)*12<len(json_data.save_data["monster"]):
            self.button_page_next_monster_box = tk.Button(
                self.app,
                text = ">",
                font=("", 18),
                width=2,
                height=7,
                command=self.show_next_page_monster_box
            )
            self.button_page_next_monster_box.pack()
            self.button_page_next_monster_box.place(x=1140, y=240)
        # 最後のページだったら進むボタンを削除
        elif (self.page_monster_box+1)*12>=len(json_data.save_data["monster"]) and self.button_page_next_monster_box is not None:
            if self.button_page_next_monster_box is not None:
                self.button_page_next_monster_box.destroy()
                self.button_page_next_monster_box = None
        # 前のページに戻るボタンを表示
        if 0<self.page_monster_box*12<len(json_data.save_data["monster"]):
            self.button_page_back_monster_box = tk.Button(
                self.app,
                text = "<",
                font=("", 18),
                width=2,
                height=7,
                command=self.show_previous_page_monster_box
            )
            self.button_page_back_monster_box.pack()
            self.button_page_back_monster_box.place(x=20, y=240)
        # 最初のページだったら進むボタンを削除
        elif self.page_monster_box==0:
            if self.button_page_back_monster_box is not None:
                self.button_page_back_monster_box.destroy()
                self.button_page_back_monster_box = None
        self.app.mainloop()

    def show_next_page_monster_box(self) -> None:
        """
        次のページを表示する
        """
        self.page_monster_box += 1
        # 「パーティー編成へ」のボタンを表示
        if self.window_mode=="all":
            self.make_party_edit_button()
        self.show_monster()
    
    def show_previous_page_monster_box(self) -> None:
        """
        前のページを表示する
        """
        self.page_monster_box -= 1
        # 「パーティー編成へ」のボタンを表示
        if self.window_mode=="all":
            self.make_party_edit_button()
        self.show_monster()

    def get_monster_info(self, event) -> dict:
        """
        押したボタンからモンスターの情報を得る
        event: ボタンを押したときのeventインスタンス
        """
        return json_data.save_data["monster"][str(int(event.widget["bg"][6], 16)+1+12*self.page_monster_box)]

    def press_monster_name_button(self, event) -> None:
        """
        モンスターの名前が書かれたボタンを押す
        """
        # モンスターの情報のdict
        mons_info = self.get_monster_info(event)
        
        # モンスター情報モードのとき
        if self.window_mode=="all":
            # モンスター情報を表示
            self.show_monster_info(mons_info)
            # モンスター情報を閉じるボタンを表示
            self.make_close_button_monster_detail()
        
        # パーティー編集モードのとき
        elif self.window_mode=="edit":
            # そのモンスターが選択されていないとき
            if event.widget["state"]==tk.NORMAL:
                # 同じ種類のモンスターを、2体以上パーティに入れることはできない
                ok = True
                name = event.widget["text"].split()[0]
                for mons in self.friend_tmp:
                    if mons["name"]==name:
                        ok = False
                if not ok:
                    return None
                # モンスターの枠が空いているなら、モンスターを追加できる
                if len(self.friend_tmp)<=2:
                    # そのモンスターをパーティーに追加する
                    self.add_or_remove_monster(mons_info, "add")
                    # ボタンの有効・無効を切り替える
                    event.widget["state"] = tk.DISABLED
                    self.monster_button_state[mons_info["id"]-1] = tk.DISABLED
                
            # そのモンスターが既に選択されているとき
            elif event.widget["state"]==tk.DISABLED:
                # そのモンスターをパーティーから削除する
                self.add_or_remove_monster(mons_info, "remove")
                # ボタンの有効・無効を切り替える
                event.widget["state"] = tk.NORMAL
                self.monster_button_state[mons_info["id"]-1] = tk.NORMAL
    
    def show_monster_detail(self, name: str, level: int) -> None:
        """
        モンスター情報でモンスターのパラメータを表示する
        name: モンスターの名前
        level: モンスターのレベル
        """
        # モンスター情報の文字のインスタンスのdictを初期化する
        self.text_monster_detail.clear()

        # 文字の座標
        x, y = 150, 240
        # 文字の大きさ
        font_size = 18
        # 名前を表示
        self.text_monster_detail["name"] = self.canvas.create_text(
            x, y,
            font = ("helvetica", font_size),
            text = name
        )
        
        # 文字の座標
        x, y = 250, 240
        # 文字の大きさ
        font_size = 16
        # レベルを表示
        self.text_monster_detail["level"] = self.canvas.create_text(
            x+len(name)*5, y,
            font = ("helvetica", font_size),
            text = f"Lv. {level}"
        )
        
        # 使うデータを選択
        data = deepcopy(json_data.monster[name])
        data.pop("name")
        data.pop("skill_select_probability")
        data.pop("attribute_damage_rate")
        data.pop("status_ailment_probability")
        # ループ変数
        i = 0
        # 文字の座標
        x, y = 160, 290
        # 文字の大きさ
        font_size = 18
        # パラメータに合わせて文字を設定
        for param, val in data.items():
            if param=="hp":
                key_content = "HP"
            elif param=="mp":
                key_content = "MP"
            elif param=="attack":
                key_content = "攻撃力"
            elif param=="magic_attack":
                key_content = "賢さ"
            elif param=="defense":
                key_content = "守備力"
            elif param=="agility":
                key_content = "素早さ"
            # パラメータを表示
            self.text_monster_detail[f"{param}_key"] = self.canvas.create_text(
                x, y+35*i,
                font = ("helvetica", font_size),
                text = key_content
            )
            self.text_monster_detail[f"{param}_val"] = self.canvas.create_text(
                x+100, y+35*i,
                font = ("helvetica", font_size-2),
                text = val
            )
            i += 1
        
        # 使うデータを選択
        data = deepcopy(json_data.monster[name])["skill_select_probability"]["friend"]
        # ループ変数
        i = 0
        # 「スキル」の文字を表示
        x, y = 450, 100
        self.text_monster_detail["スキル"] = self.canvas.create_text(
            x, y,
            font = ("helvetica", font_size),
            text = "スキル"
        )
        # 覚えているスキルを表示
        for skill_name, prob in data.items():
            # 使う可能性のあるスキルだけを表示
            if prob>0:
                # 覚えているスキルを表示
                self.button_monster_detail[skill_name] = tk.Button(
                    self.app,
                    text=skill_name,
                    font=("", 18),
                    width=12,
                    height=1
                )
                # ボタンの座標
                x, y = 360, 50*i+150
                self.button_monster_detail[skill_name].place(x=x, y=y)
                self.button_monster_detail[skill_name].bind("<ButtonPress>", self.show_skill_description)
                i += 1
        
        # 使うデータを選択
        data = deepcopy(json_data.monster[name])["attribute_damage_rate"]
        # ループ変数
        i = 0
        # 文字の大きさ
        font_size = 18
        # 文字の座標
        x, y = 830, 100
        # 「耐性」の文字を表示
        self.text_monster_detail["耐性"] = self.canvas.create_text(
            x, y,
            font = ("helvetica", font_size),
            text = "耐性"
        )
        # 属性耐性を表示
        for attribute, damage_rate in data.items():
            if damage_rate<=0:
                val_content = "無効"
            elif 0<damage_rate<0.4:
                val_content = "激減"
            elif 0.4<=damage_rate<=0.6:
                val_content = "半減"
            elif 0.6<damage_rate<=0.9:
                val_content = "軽減"
            elif 0.9<damage_rate<1.1:
                val_content = "普通"
            elif 1.1<=damage_rate:
                val_content = "弱点"
            # 文字の座標
            x, y = 650, 40*i+150
            # 属性耐性を表示
            self.text_monster_detail[f"{attribute}_key"] = self.canvas.create_text(
                x, y,
                font = ("helvetica", font_size),
                text = attribute
            )
            self.text_monster_detail[f"{attribute}_val"] = self.canvas.create_text(
                x+100, y,
                font = ("helvetica", font_size),
                text = val_content
            )
            i += 1
        
        # 使うデータを選択
        data = deepcopy(json_data.monster[name])["status_ailment_probability"]
        # ループ変数
        i = 0
        # 状態異常耐性を表示
        for ailment, prob in data.items():
            if prob<=0:
                val_content = "無効"
            elif 0<prob<0.3:
                val_content = "激減"
            elif 0.3<=prob<0.5:
                val_content = "半減"
            elif 0.5<=prob<0.7:
                val_content = "軽減"
            elif 0.7<=prob<0.9:
                val_content = "普通"
            elif 0.9<=prob:
                val_content = "弱点"
            # 文字の座標
            x, y = 930, 40*i+150
            # 状態異常を表示
            self.text_monster_detail[f"{ailment}_key"] = self.canvas.create_text(
                x, y,
                font = ("helvetica", font_size),
                text = ailment
            )
            self.text_monster_detail[f"{ailment}_val"] = self.canvas.create_text(
                x+130, y,
                font = ("helvetica", font_size),
                text = val_content
            )
            i += 1

    def show_skill_description(self, event) -> None:
        """
        スキルの説明を表示する
        """
        # スキルの名前を取得する
        skill_name = event.widget["text"]
        # 前の表示を削除する
        if self.text_skill_description is not None:
            self.canvas.delete(self.text_skill_description)
            self.text_skill_description = None
        # 文字のxy座標
        x, y = 350, 480
        # 文字の大きさ
        font_size = 18
        # 文を改行する
        content = list(json_data.skill[skill_name]["description"])
        chars_per_line = 30
        tmp = []
        for idx, char in enumerate(content):
            tmp.append(char)
            if idx%chars_per_line==0 and idx>0:
                tmp.append("\n")
        content = "".join(tmp)
        # スキルの説明を表示する
        self.text_skill_description = self.canvas.create_text(
            x, y,
            font = ("helvetica", font_size),
            text = content,
            anchor=tk.NW
        )

    def make_close_button_monster_detail(self) -> None:
        """
        モンスター情報の画面を閉じるボタンを表示する
        """
        # モンスターボックスを閉じるボタンを削除する
        if self.close_button_monster_box is not None:
            self.close_button_monster_box.destroy()
            self.close_button_monster_box = None
        # モンスター情報の画面を閉じるボタンを表示する
        self.close_button_monster_detail = tk.Button(
            self.app,
            text="x",
            font=("", 18),
            width=2,
            height=1,
            bg="#f44",
            command=self.close_monster_detail
        )
        x, y = 0, 0
        self.close_button_monster_detail.place(x=x, y=y)
    
    def make_skill_description_box(self) -> None:
        """
        スキル説明の枠を表示する
        """
        start_x, start_y = 340, 470
        width, height = 730, 100
        end_x, end_y = start_x+width, start_y+height
        self.skill_description_box = self.canvas.create_rectangle(
            start_x, start_y,
            end_x, end_y,
            fill = "#eee",
            outline = "#777",
            width=3
        )
    
    def show_monster_info(self, mons_info: dict) -> None:
        """
        モンスターの詳細情報を表示する（モンスターボックスから）
        mons_info: モンスター情報のdict {"name": name, "level": level}
        """
        # UIを削除する
        self.delete_all_ui()
        # 「パーティー編成へ」のボタンを削除する
        if self.party_edit_button is not None:
            self.party_edit_button.destroy()
            self.party_edit_button = None
        # モンスターボックスのモードを変更する
        self.window_mode = "detail"
        # モンスターの画像を表示する
        self.plot_image_monster_detail(mons_info["name"])
        # モンスターのパラメータを表示する
        self.show_monster_detail(mons_info["name"], mons_info["level"])
        # スキル説明の枠を表示する
        self.make_skill_description_box()
    
    def show_monster_info_child(self, mons_info: dict) -> None:
        """
        モンスター情報を表示する（子モンスターの候補から）
        mons_info: モンスター情報のdict {"name": name, "level": level}
        """
        # UIを削除する
        self.delete_all_ui()
        self.delete_all_ui_child_fusion()
        # ウィンドウモードを変更する
        self.window_mode = "child_detail"
        # モンスターの画像を表示する
        self.plot_image_monster_detail(mons_info["name"])
        # モンスターのパラメータを表示する
        self.show_monster_detail(mons_info["name"], mons_info["level"])
        # スキル説明の枠を表示する
        self.make_skill_description_box()
        # 子モンスター候補を閉じるボタンを削除する
        if self.button_close_child_candidate_fusion is not None:
            self.button_close_child_candidate_fusion.destroy()
            self.button_close_child_candidate_fusion = None
        # 子モンスター情報を閉じるボタンを表示する
        self.make_close_button_child_detail()
    
    def add_or_remove_monster(self, mons: dict, add_or_remove: str) -> None:
        """
        モンスターをパーティーに追加したり、パーティーから削除したりする
        mons: モンスターの情報
        add_or_remove: 「add」「remove」のいずれか
        """
        if add_or_remove=="add":
            self.plot_image_party(mons["name"], len(self.friend_tmp))
            self.friend_tmp.append(mons)
        elif add_or_remove=="remove":
            self.remove_image_party(mons["name"])
            self.friend_tmp.remove(mons)
            self.remove_image_party_all()
            self.show_party_image()
    
    def get_makable_monster(self, parents: list[str]) -> list:
        """
        配合先のモンスターの候補を表示する
        parent: 親モンスター
        """
        # 子モンスターの候補
        candidate = set()
        # 親モンスターをソートする
        parents.sort()
        # 各親モンスターについて
        for parent in parents:
            # 子モンスターの候補
            childs = json_data.fusion_tree[parent]
            # 子モンスターと、そのモンスターを作るのに必要な親モンスター
            for child, needed_parents in childs.items():
                # 必要な親モンスターにparent自身を加える
                needed_parents = needed_parents.copy()
                needed_parents.append(parent)
                # 必要な親モンスターをソートする
                needed_parents.sort()
                # 指定した親モンスターと必要なモンスターが一致しているか
                if needed_parents==parents:
                    # 子モンスターを候補に加える
                    candidate.add(child)
        # 子モンスターの候補を返す
        return list(candidate)
    
    def show_text_fusion(self) -> None:
        """
        文字を表示する（配合画面）
        """
        modes = ["parent_1", "parent_2", "child"]
        for mode in modes:
            if mode=="parent_1":
                x, y = 170, 110
                content = "親1"
            elif mode=="parent_2":
                x, y = 170, 290
                content = "親2"
            elif mode=="child":
                x, y = 450, 195
                content = "子"
            # 文字を表示する
            self.text_fusion[mode] = self.canvas.create_text(
                x, y,
                font = ("helvetica", 18),
                text = content
            )
    
    def show_monster_frame_fusion(self) -> None:
        """
        モンスターの枠と線を表示する（配合画面）
        """
        # 線を表示する
        start_x, start_y = 255, 280
        diff_x, diff_y = 100, 0
        end_x, end_y = start_x+diff_x, start_y+diff_y
        self.line_fusion = self.canvas.create_line(
            start_x, start_y,
            end_x, end_y,
            fill="#999",
            width=5
        )
        self.canvas.update()
        # モンスターの枠を表示する
        modes = ["parent_1", "parent_2", "child"]
        for mode in modes:
            if mode=="parent_1":
                start_x, start_y = 100, 130
            elif mode=="parent_2":
                start_x, start_y = 100, 310
            elif mode=="child":
                start_x, start_y = 380, 215
            width, height = 140, 120
            end_x, end_y = start_x+width, start_y+height
            self.monster_frame_fusion[mode] = self.canvas.create_rectangle(
                start_x, start_y,
                end_x, end_y,
                fill="#eee",
                outline="#777",
                width=3
            )
    
    def delete_monster_image_fusion(self) -> None:
        """
        モンスターの画像を削除する（配合画面）
        """
        self.monster_image_fusion = {}
    
    def add_or_remove_parent_fusion(self, event) -> None:
        """
        配合の親を設定する
        """
        # モンスターの画像を削除する
        self.delete_monster_image_fusion()
        # モンスターの名前を取得する
        monster_id = int("".join(event.widget["bg"][2::2]), 16)+1
        # 配合の親を追加する
        if event.widget["state"]==tk.NORMAL:
            if len(self.fusion_parent_id)<json_data.save_data["max_num_fusion_parent"]:
                self.fusion_parent_id.append(monster_id)
                event.widget["state"] = tk.DISABLED
        elif event.widget["state"]==tk.DISABLED:
            self.fusion_parent_id.remove(monster_id)
            event.widget["state"] = tk.NORMAL
        # モンスターの画像を表示する
        for idx, id_ in enumerate(self.fusion_parent_id):
            name = json_data.save_data["monster"][str(id_)]["name"]
            if idx==0:
                mode = "parent_1"
            elif idx==1:
                mode = "parent_2"
            elif idx==2:
                mode = "child"
            self.plot_image_fusion(name, mode)
        # 子モンスターの候補を取得する
        parents = []
        for id_ in self.fusion_parent_id:
            parents.append(json_data.save_data["monster"][str(id_)]["name"])
        # 「候補を見る」のボタンのstateを更新する
        if len(self.fusion_parent_id)>=2 and len(self.get_makable_monster(parents))>0:
            self.button_show_child_candidate_fusion["state"] = tk.NORMAL
        else:
            self.button_show_child_candidate_fusion["state"] = tk.DISABLED
    
    def delete_monster_button_fusion(self) -> None:
        """
        モンスターのボタンが表示されているときに、モンスターのボタンを削除する（配合画面）
        """
        for i in range(10):
            if self.monster_button_fusion[i] is not None:
                self.monster_button_fusion[i].destroy()
                self.monster_button_fusion[i] = None
    
    def init_all_button_fusion(self) -> None:
        """
        すべてのボタンを初期化する（配合画面）
        """
        self.monster_button_fusion = [None]*10
        self.button_page_next_fusion = None
        self.button_page_back_fusion = None
    
    def show_monster_fusion(self) -> None:
        """
        モンスターを1ページ分表示する（配合画面）
        """
        # 1ページに表示するモンスターの数
        mons_per_page = 10
        # モンスターのボタンを削除する
        self.delete_monster_button_fusion()
        # 次のページに進むボタンを削除する
        if self.button_page_next_fusion is not None:
            self.button_page_next_fusion.destroy()
            self.button_page_next_fusion = None
        # 前のページに戻るボタンを削除する
        if self.button_page_back_fusion is not None:
            self.button_page_back_fusion.destroy()
            self.button_page_back_fusion = None
        # 次のページに進むボタンを表示する
        if self.page_fusion<len(json_data.save_data["monster"])//mons_per_page:
            self.show_next_page_button_fusion()
        # 前のページに戻るボタンを表示する
        if self.page_fusion>0:
            self.show_previous_page_button_fusion()
        # モンスターを1ページ分表示する
        for i in range(self.page_fusion*mons_per_page, min(self.page_fusion*mons_per_page+10, len(json_data.save_data["monster"]))):
            # モンスターの連想配列を取得する
            mons = json_data.save_data["monster"][str(i+1)]
            # 背景色にidの役割を持たせる
            color = "{:03x}".format(int(base_repr(i, 16), 16))
            color = f"#e{color[0]}e{color[1]}e{color[2]}"
            # idからボタンの状態を取得する
            if i+1 in self.fusion_parent_id:
                state = tk.DISABLED
            elif i+1 not in self.fusion_parent_id:
                state = tk.NORMAL
            # モンスターのボタンを表示する
            self.monster_button_fusion[i%mons_per_page] = tk.Button(
                self.app,
                text=f"{mons['name']} Lv.{mons['level']}",
                font=("", 18),
                width=16,
                height=2,
                bg=color,
                state=state
            )
            # 1行に表示するモンスターの数
            mons_per_line = 2
            # ボタンのxy座標
            x, y = 250*((i%mons_per_page)%mons_per_line)+630, 100*((i%mons_per_page)//mons_per_line)+100
            # ボタンを表示する
            self.monster_button_fusion[i%mons_per_page].place(x=x, y=y)
            # ボタンにイベントを設定する
            self.monster_button_fusion[i%mons_per_page].bind("<ButtonPress>", self.add_or_remove_parent_fusion)
    
    def show_next_page_button_fusion(self) -> None:
        """
        次のページに進むボタンを表示する（配合画面）
        """
        self.button_page_next_fusion = tk.Button(
            self.app,
            text = ">",
            font=("", 18),
            width=2,
            height=7,
            command=self.show_next_page_fusion
        )
        x, y = 1140, 240
        self.button_page_next_fusion.place(x=x, y=y)

    def show_next_page_fusion(self) -> None:
        """
        次のページに進む（配合画面）
        """
        self.page_fusion += 1
        self.show_monster_fusion()

    def show_previous_page_button_fusion(self) -> None:
        """
        前のページに戻るボタンを表示する（配合画面）
        """
        self.button_page_back_fusion = tk.Button(
            self.app,
            text = "<",
            font=("", 18),
            width=2,
            height=7,
            command=self.show_previous_page_fusion
        )
        x, y = 550, 240
        self.button_page_back_fusion.place(x=x, y=y)
    
    def show_previous_page_fusion(self) -> None:
        """
        前のページに戻る（配合画面）
        """
        self.page_fusion -= 1
        self.show_monster_fusion()
    
    def fusion(self) -> None:
        """
        配合する
        """
        # tk.DISABLEDなら何もしない
        if self.button_fusion["state"]==tk.DISABLED:
            return None
    
    def show_fusion_button(self) -> None:
        """
        配合ボタンを表示する
        """
        self.button_fusion = tk.Button(
            self.app,
            text="配合する",
            font=("", 18),
            width=10,
            height=3,
            state=tk.DISABLED,
            command=self.fusion
        )
        x, y = 150, 450
        self.button_fusion.place(x=x, y=y)
    
    def show_fusion_screen(self) -> None:
        """
        配合画面を表示する
        """
        # ページ数を初期化する
        self.page_fusion = 0
        # 配合の親を初期化する
        self.fusion_parent_id = []
        # ウィンドウモードを更新する
        self.window_mode = "fusion"
        # ボタンを初期化する
        self.init_all_button_fusion()
        # キー入力を受け付ける
        self.app.bind("<KeyPress>", self.listen_key)
        # モンスターの親と子の枠を作る
        self.show_monster_frame_fusion()
        # 「親1」「親2」「子」の文字を表示する
        self.show_text_fusion()
        # モンスターを1ページ分表示する
        self.show_monster_fusion()
        # 閉じるボタンを表示する
        self.make_close_button_fusion()
        # 「候補を見る」のボタンを表示する
        self.make_show_child_candidate_button_fusion()
        # 配合ボタンを表示する
        self.show_fusion_button()
        # 画面を表示する
        self.app.mainloop()
    
    def delete_all_ui_fusion(self) -> None:
        """
        すべてのUIを削除する（子モンスターの候補を表示する）
        """
        # モンスターのボタンを削除する
        for i in range(10):
            if self.monster_button_fusion[i] is not None:
                self.monster_button_fusion[i].destroy()
                self.monster_button_fusion[i] = None
        # 次のページに進むボタンを削除する
        if self.button_page_next_fusion is not None:
            self.button_page_next_fusion.destroy()
            self.button_page_next_fusion = None
        # 前のページに戻るボタンを削除する
        if self.button_page_back_fusion is not None:
            self.button_page_back_fusion.destroy()
            self.button_page_back_fusion = None
        # 「候補を見る」のボタンを削除する
        if self.button_show_child_candidate_fusion is not None:
            self.button_show_child_candidate_fusion.destroy()
            self.button_show_child_candidate_fusion = None
        # モンスターの枠と文字を削除する
        self.canvas.delete("all")
    
    def delete_all_ui_child_fusion(self) -> None:
        """
        子モンスターの候補の画面のUIをすべて削除する
        """
        # 子モンスターの名前ボタンを削除する
        for i in range(12):
            if self.button_child_candidate_fusion[i] is not None:
                self.button_child_candidate_fusion[i].destroy()
                self.button_child_candidate_fusion[i] = None
    
    def show_child_candidate_fusion(self) -> None:
        """
        子モンスターの候補を表示する
        """
        # ウィンドウモードを更新する
        self.window_mode = "child_all"
        # 配合画面を閉じるボタンを削除する
        if self.close_button_fusion is not None:
            self.close_button_fusion.destroy()
            self.close_button_fusion = None
        # 配合ボタンを削除する
        if self.button_fusion is not None:
            self.button_fusion.destroy()
            self.button_fusion = None
        # 子モンスター候補を閉じるボタンを表示する
        self.make_close_button_child_all()
        # 状態がtk.DISABLEDなら候補を表示しない
        if self.button_show_child_candidate_fusion is not None and self.button_show_child_candidate_fusion["state"]==tk.DISABLED:
            return None
        # すべてのUIを削除する
        self.delete_all_ui_fusion()
        if self.close_button_fusion is not None:
            self.close_button_fusion.destroy()
            self.close_button_fusion = None
        # 親モンスターのidから名前を得る
        parents = []
        for id_ in self.fusion_parent_id:
            name = json_data.save_data["monster"][str(id_)]["name"]
            parents.append(name)
        # 子モンスターの候補を得る
        candidate = self.get_makable_monster(parents)
        # モンスターの画像と詳細ボタンを表示する
        for idx, name in enumerate(candidate):
            # 画像を表示
            width = 247*(idx%4)+190
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = (150*(idx//4)+140)%450+10
            self.plot_image_monster_box(name, width, height)
            # モンスターの名前のボタンを表示
            self.button_child_candidate_fusion[idx] = tk.Button(
                self.app,
                text=f"{name} Lv.1",
                font=("", 18),
                width=16,
                height=1,
                command=lambda: self.show_monster_info_child({"name": name, "level": 1})
            )
            self.button_child_candidate_fusion[idx].pack()
            left = 0.21*(idx%4)+0.1
            top = (0.24*(idx//4))%0.72+0.4
            # ボタンを配置する
            self.button_child_candidate_fusion[idx].place(relx=left, rely=top)
    
    def make_show_child_candidate_button_fusion(self) -> None:
        """
        「候補を見る」のボタンを表示する
        """
        self.button_show_child_candidate_fusion = tk.Button(
            self.app,
            text="候補を見る",
            font=("", 18),
            width=10,
            height=3,
            state=tk.DISABLED,
            command=self.show_child_candidate_fusion
        )
        x, y = 350, 450
        self.button_show_child_candidate_fusion.place(x=x, y=y)
    
    def make_close_button_fusion(self) -> None:
        """
        閉じるボタンを表示する（配合画面）
        """
        # モンスター配合所を閉じるボタンを削除する
        if self.close_button_fusion is not None:
            self.close_button_fusion.destroy()
            self.close_button_fusion = None
        # モンスター配合所を閉じるボタンを表示する
        self.close_button_fusion = tk.Button(
            self.app,
            text="x",
            font=("", 18),
            width=2,
            height=1,
            bg="#f44",
            command=self.close_fusion_screen
        )
        x, y = 0, 0
        self.close_button_fusion.place(x=x, y=y)
    
    def make_close_button_child_all(self) -> None:
        """
        閉じるボタンを表示する（子モンスター候補）
        """
        self.button_close_child_candidate_fusion = tk.Button(
            self.app,
            text="x",
            font=("", 18),
            width=2,
            height=1,
            bg="#f44",
            command=self.close_monster_candidate_child
        )
        # ボタンのxy座標
        x, y = 0, 0
        # ボタンを表示する
        self.button_close_child_candidate_fusion.place(x=x, y=y)
    
    def make_close_button_child_detail(self) -> None:
        """
        閉じるボタンを表示する（子モンスター情報）
        """
        self.button_close_child_detail_fusion = tk.Button(
            self.app,
            text="x",
            font=("", 18),
            width=2,
            height=1,
            bg="#f44",
            command=self.close_monster_detail_child
        )
        # ボタンのxy座標
        x, y = 0, 0
        # ボタンを表示する
        self.button_close_child_detail_fusion.place(x=x, y=y)
    
    def close_fusion_screen(self) -> None:
        """
        モンスター配合所を閉じる
        """
        # モンスター配合所を閉じるボタンを削除する
        if self.close_button_fusion is not None:
            self.close_button_fusion.destroy()
            self.close_button_fusion = None
        # canvasを削除する
        if self.canvas is not None:
            self.canvas.destroy()
            self.canvas = None
        # appを削除する
        if self.app is not None:
            self.app.destroy()
            self.app = None
    
    def close_monster_box(self) -> None:
        """
        モンスターボックスを閉じる
        """
        # モンスター一覧を表示しているときだけ、閉じることができる
        if self.window_mode=="all":
            # UIを削除する
            self.delete_all_ui()
            if self.party_edit_button is not None:
                self.party_edit_button.destroy()
                self.party_edit_button = None
            if self.party_edit_end_button is not None:
                self.party_edit_end_button.destroy()
                self.party_edit_end_button = None
            # Tkinterのインスタンスを削除する
            if self.app is not None:
                self.app.destroy()
                self.app = None

    def close_monster_detail(self) -> None:
        """
        モンスター情報を閉じる
        """
        # モンスター情報を閉じるボタンを削除する
        if self.close_button_monster_detail is not None:
            self.close_button_monster_detail.destroy()
            self.close_button_monster_detail = None
        # モンスターボックスのモードを変更する
        self.window_mode = "all"
        # モンスターボックスを閉じるボタンを表示する
        self.make_close_button_monster_box()
        # 「パーティー編成へ」のボタンを表示
        self.make_party_edit_button()
        # モンスターを1ページ分表示する
        self.show_monster()

    def close_monster_candidate_child(self) -> None:
        """
        子モンスター候補を閉じる
        """
        # すべてのUIを削除する
        self.delete_all_ui_detail()
        self.delete_all_ui_child_all()
        # 配合画面を表示する
        self.show_fusion_screen()

    def close_monster_detail_child(self) -> None:
        """
        子モンスター情報を閉じる
        """
        # すべてのUIを削除する
        self.delete_all_ui_detail()
        # 子モンスターの候補を表示する
        self.show_child_candidate_fusion()

ui = UI()