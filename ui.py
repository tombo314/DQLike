# ライブラリをインポート
from time import sleep
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
        # 「info」でモンスター情報モード、「edit」でパーティー編成モード
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
        self.friend_tmp = [None]*3
    
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
    
    def plot_image_monster_box(self, name: str, path: str, x: int, y: int) -> None:
        """
        モンスターの画像を表示（モンスターボックス）
        name: モンスターの名前
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージを作成
        self.image_monster_box[name].append(tk.PhotoImage(file=path, width=130, height=130))
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_monster_box[name][-1], anchor=tk.NW)
    
    def plot_image_battle(self, name: str, is_friend: bool, path: str, x: int, y: int) -> None:
        """
        モンスターの画像を表示（バトル）
        name: モンスターの名前
        is_friend: 味方かどうか
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージを作成
        self.image_battle[is_friend][name] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_battle[is_friend][name], anchor=tk.NW)
    
    def plot_image_party(self, name: str, idx: int) -> None:
        """
        モンスターの画像を表示（パーティー）
        name: モンスターの名前
        path: 画像のパス
        index: 左から何番目であるか（1~3）の値
        """
        x = idx*162+405
        y = 37
        path = f"images/png_resized/{name}_resized.png"
        # イメージを作成
        self.image_friend[idx] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_friend[idx], anchor=tk.NW)
    
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
        # # パーティーを確定する
        # user_info.friend = self.friend_tmp.copy()
        # 「パーティー編成へ」のボタンを表示
        self.make_party_edit_button()
    
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
        if self.monster_box_mode=="info":
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
        """
        # 「決定」のボタンを削除
        if self.party_edit_end_button is not None:
            self.party_edit_end_button.destroy()
            self.party_edit_end_button = None
        # モンスターボックスモードを設定
        self.monster_box_mode = "info"
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
        モンスターボックス内で、パーティー編成モードとモンスター情報モードを切り替える
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
        self.friend_tmp = user_info.friend.copy()
    
    def make_party_edit_frame(self) -> None:
        """
        パーティー編成の枠を表示
        """
        for i in range(3):
            start_x, start_y = 160*(i-1)+550, 20
            width, height = 120, 120
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
        elif event.keysym=="Right" and self.page<len(json_data.save_data["monster"])//12 and len(json_data.save_data["monster"])//12!=len(json_data.save_data["monster"])/12:
            self.show_next_page()
        # ←でモンスターボックスの前ページを表示
        elif event.keysym=="Left" and self.page>0:
            self.show_previous_page()
    
    def show_party_image(self) -> None:
        """
        パーティーの画像を表示する
        """
        for idx, mons in enumerate(user_info.friend):
            self.plot_image_party(mons["name"], idx)
    
    def open_monster_box(self) -> None:
        """
        自分が持っているモンスターを表示する
        """
        # モンスターボックスのページ数
        self.page = 0
        # モンスターボックスのモードを設定
        self.monster_box_mode = "info"
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
        if self.monster_box_mode=="info":
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
            self.plot_image_monster_box(name, f"images/png_resized/{name}_resized.png", width, height)
            # モンスターの名前のボタンを表示
            # ボタンの色によってボタンを区別する
            color = f"#eeeee{base_repr(i%12, 16)}"
            self.button_monster[i%12] = tk.Button(
                self.app,
                text=f"{name} Lv.{json_data.save_data['monster'][str(i+1)]['level']}",
                font=("", 18),
                width=16,
                height=1,
                bg=color
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

    def get_monster_info(self, event) -> None:
        """
        押したボタンからモンスターの情報を得る
        event: ボタンを押したときのeventインスタンス
        """
        return json_data.save_data["monster"][str(int(event.widget["bg"][6], 16)+1)]

    def press_monster_name_button(self, event) -> None:
        """
        モンスターの名前が書かれたボタンを押す
        """
        print(self.get_monster_info(event))
        # モンスター情報モードのとき
        if self.monster_box_mode=="info":
            # モンスターの詳細情報を表示
            self.show_monster_info()
        # パーティー編集モードのとき
        elif self.monster_box_mode=="edit":
            # そのモンスターをパーティーに追加するか、パーティーから削除する
            self.add_or_remove_monster()
        # ボタンの有効・無効を切り替える
        if event.widget["state"]==tk.NORMAL:
            event.widget["state"] = tk.DISABLED
        elif event.widget["state"]==tk.DISABLED:
            event.widget["state"] = tk.NORMAL
    
    def show_monster_info(self) -> None:
        """
        モンスターの詳細情報を表示する
        """
    
    def add_or_remove_monster(self) -> None:
        """
        モンスターをパーティーに追加したり、パーティーから削除したりする
        """
    
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