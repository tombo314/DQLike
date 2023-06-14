# debug
from pprint import pprint

# ライブラリをインポート
from time import sleep
from copy import deepcopy
import tkinter as tk

# クラスをインポート
from config import *
from json_data import json_data
from user_info import user_info
from numpy import base_repr

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
        # ログ
        self.log_text = [None]*15
        # モンスターの詳細に遷移するボタン
        self.button_monster = [None]*12
        # 次のページに進むボタン
        self.button_page_next = None
        # モンスターボックスのテキスト
        self.text_monster_box = None
        # 前のページに戻るボタン
        self.button_page_back = None
        # モンスターボックスを閉じるボタン
        self.close_button = None
        # 「パーティー編成」のボタン
        self.party_edit_button = None
        # 「決定」のボタン
        self.party_edit_end_button = None
        # 画像データ（モンスターボックス）
        self.image_monster_box = {name: [] for name in json_data.monster}
        # 敵パーティー
        self.enemy = None
        # 味方パーティー
        self.friend = None
        # 画像データ（バトル）
        self.image_battle = None
        # 「all」でモンスター一覧モード、「detail」でモンスター詳細モード、「edit」でパーティー編成モード
        self.monster_box_mode = None
        # モンスターボックスのモードの文字
        self.text_monster_box_mode = None
        # モンスターボックスのページ数
        self.page = None
        # パーティーの枠
        self.party_frame = [None]*3
        # パーティーの画像
        self.image_friend = [None]*3
        # 仮の味方パーティー
        self.friend_tmp = []
        # モンスターの名前ボタンのNORMAL・DISABLED
        self.monster_button_state = [tk.NORMAL]*1000
        # モンスターの詳細画面の画像
        self.monster_image_detail = None
        # モンスターの詳細画面のパラメータの文字のインスタンス
        self.text_monster_param_detail = {}
    
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

    def delete_all_ui(self) -> None:
        """
        すべてのUIを削除する
        """
        self.canvas.delete("all")
        if self.button_page_next is not None:
            self.button_page_next.destroy()
            self.button_page_next = None
        if self.button_page_back is not None:
            self.button_page_back.destroy()
            self.button_page_back = None
        for i in range(12):
            if self.button_monster[i] is not None:
                self.button_monster[i].destroy()
                self.button_monster[i] = None

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
    
    def make_close_button(self) -> None:
        # モンスターボックスを閉じるボタンを表示
        self.close_button = tk.Button(
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
        self.close_button.place(relx=left, rely=top)
        self.app.bind("<KeyPress>", self.listen_key)
    
    def party_edit_end(self) -> None:
        """
        パーティー編集モードを終了する
        """
        # パーティーを確定する
        user_info.friend = deepcopy(self.friend_tmp)
        # 「パーティー編成へ」のボタンを表示
        self.make_party_edit_button()
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
        if self.monster_box_mode=="all":
            text = "モンスター情報"
        elif self.monster_box_mode=="edit":
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
        # モンスターボックスモードを設定
        self.monster_box_mode = "all"
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
        self.monster_box_mode = "edit"
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
        
        # debug
        for i in range(self.page*12, min((self.page+1)*12, len(json_data.save_data["monster"]))):
            if self.monster_button_state[i]==tk.NORMAL:
                self.button_monster[i%12]["state"] = tk.NORMAL
            elif self.monster_button_state[i]==tk.DISABLED:
                self.button_monster[i%12]["state"] = tk.DISABLED

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
        キー入力を処理する
        """
        # eでモンスターボックスを閉じる
        if event.keysym=="e":
            self.close_monster_box()
        # →でモンスターボックスの次ページを表示
        elif self.monster_box_mode=="all" and event.keysym=="Right" and self.page<len(json_data.save_data["monster"])//12 and len(json_data.save_data["monster"])//12!=len(json_data.save_data["monster"])/12:
            self.show_next_page()
        # ←でモンスターボックスの前ページを表示
        elif event.keysym=="Left" and self.page>0:
            self.show_previous_page()
    
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
        self.page = 0
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
        self.monster_box_mode = "all"
        # Tkinterのウィンドウを表示
        self.make_tk_window("モンスターボックス")
        # 画面を閉じるボタンを表示
        self.make_close_button()
        # モンスターボックスの1ページ目を表示
        self.show_monster()

    def show_monster(self) -> None:
        """
        モンスターを1ページ分表示する
        """
        # 既存のUIを削除
        self.delete_all_ui()
        # パーティー編成モードに切り替えるボタンを表示
        if self.monster_box_mode=="all":
            self.make_party_edit_button()
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
            text = f"モンスターボックス（{self.page+1}／{page_all}）",
            font = ("", 22)
        )
        # パーティーの枠を表示
        self.make_party_edit_frame()
        # パーティーの画像を表示
        self.show_party_image()
        # モンスターの画像と詳細ボタンを表示
        for i in range(self.page*12, min((self.page+1)*12, len(json_data.save_data["monster"]))):
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
            if self.monster_box_mode=="all":
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
        if (self.page+1)*12<len(json_data.save_data["monster"]):
            self.button_page_next = tk.Button(
                self.app,
                text = ">",
                font=("", 18),
                width=2,
                height=7,
                command=self.show_next_page
            )
            self.button_page_next.pack()
            self.button_page_next.place(x=1140, y=240)
        # 最後のページだったら進むボタンを削除
        elif (self.page+1)*12>=len(json_data.save_data["monster"]) and self.button_page_next is not None:
            self.button_page_next.destroy()
        # 前のページに戻るボタンを表示
        if 0<self.page*12<len(json_data.save_data["monster"]):
            self.button_page_back = tk.Button(
                self.app,
                text = "<",
                font=("", 18),
                width=2,
                height=7,
                command=self.show_previous_page
            )
            self.button_page_back.pack()
            self.button_page_back.place(x=20, y=240)
        # 最初のページだったら進むボタンを削除
        elif self.page==0:
            if self.button_page_back is not None:
                self.button_page_back.destroy()
                self.button_page_back = None
        self.app.mainloop()

    def show_next_page(self) -> None:
        """
        次のページを表示する
        """
        self.page += 1
        self.show_monster()
    
    def show_previous_page(self) -> None:
        """
        前のページを表示する
        """
        self.page -= 1
        self.show_monster()

    def get_monster_info(self, event) -> dict:
        """
        押したボタンからモンスターの情報を得る
        event: ボタンを押したときのeventインスタンス
        """
        return json_data.save_data["monster"][str(int(event.widget["bg"][6], 16)+1+12*self.page)]

    def press_monster_name_button(self, event) -> None:
        """
        モンスターの名前が書かれたボタンを押す
        """
        # モンスターの情報のdict
        mons_info = self.get_monster_info(event)
        
        # モンスター情報モードのとき
        if self.monster_box_mode=="all":
            # モンスターの詳細情報を表示
            self.show_monster_info(mons_info)
        
        # パーティー編集モードのとき
        elif self.monster_box_mode=="edit":
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
    
    def show_monster_param_detail(self, name: str, level: int) -> None:
        """
        モンスター情報でモンスターのパラメータを表示する
        name: モンスターの名前
        level: モンスターのレベル
        """
        # モンスター情報の文字のインスタンスのdictを初期化する
        self.text_monster_param_detail.clear()
        # 文字の座標
        x, y = 150, 250
        # 文字の大きさ
        font_size = 18
        # 名前を表示
        self.text_monster_param_detail["name"] = self.canvas.create_text(
            x, y,
            font = ("helvetica", font_size),
            text = name
        )
        # 文字の座標
        x, y = 250, 250
        # 文字の大きさ
        font_size = 16
        # レベルを表示
        self.text_monster_param_detail["level"] = self.canvas.create_text(
            x+len(name)*5, y,
            font = ("helvetica", font_size),
            text = f"Lv. {level}"
        )
        # 使うデータを選択
        data = json_data.monster[name].copy()
        data.pop("name")
        data.pop("skill_select_probability")
        data.pop("attribute_damage_rate")
        data.pop("status_ailment_probability")
        # ループ変数
        i = 0
        # 文字の座標
        x, y = 160, 280
        # 文字の大きさ
        font_size = 18
        # 各パラメータを表示
        for key,val in data.items():
            if key=="hp":
                content_key = "HP"
            elif key=="mp":
                content_key = "MP"
            elif key=="attack":
                content_key = "攻撃力"
            elif key=="magic_attack":
                content_key = "賢さ"
            elif key=="defense":
                content_key = "守備力"
            elif key=="agility":
                content_key = "素早さ"
            self.text_monster_param_detail[f"{key}_key"] = self.canvas.create_text(
                x, y+30*i,
                font = ("helvetica", font_size),
                text = content_key
            )
            self.text_monster_param_detail[f"{val}_val"] = self.canvas.create_text(
                x+100, y+30*i,
                font = ("helvetica", font_size-2),
                text = val
            )
            i += 1
    
    def show_monster_info(self, mons_info) -> None:
        """
        モンスターの詳細情報を表示する
        mons_info: モンスター情報のdict
        """
        # UIを削除する
        self.delete_all_ui()
        self.party_edit_button.destroy()
        self.party_edit_button = None
        # モンスターの画像を表示する
        self.plot_image_monster_detail(mons_info["name"])
        # モンスターのパラメータを表示する
        self.show_monster_param_detail(mons_info["name"], mons_info["level"])
    
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
    
    def show_user_info(self) -> None:
        """
        自分の情報を表示する
        """
        # self.delete_all_ui()

    def close_monster_box(self) -> None:
        """
        モンスターボックスを閉じる
        """
        self.delete_all_ui()
        if self.party_edit_button is not None:
            self.party_edit_button.destroy()
            self.party_edit_button = None
        if self.party_edit_end_button is not None:
            self.party_edit_end_button.destroy()
            self.party_edit_end_button = None
        self.app.destroy()

ui = UI()