# ライブラリをインポート
from time import sleep
import tkinter as tk

# クラスをインポート
from config import *
from json_import import *

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
        self.button = [None]*3
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
        # 画像データ（モンスターボックス）
        self.image_monster_box = {name: [] for name in monster}
        # 敵パーティー
        self.enemy = None
        # 味方パーティー
        self.friend = None
        # 画像データ（バトル）
        self.image_battle = None
    
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
            {monster[name]["name"]: 0 for name in self.enemy},
            {monster[name]["name"]: 0 for name in self.friend},
        ]
    
    def plot_image(self, name: str, path: str, x: int, y: int) -> None:
        """
        画像を表示
        name: モンスターの名前
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージ作成
        self.image_monster_box[name].append(tk.PhotoImage(file=path, width=130, height=130))
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_monster_box[name][-1], anchor=tk.NW)
    
    def plot_image_battle(self, name: str, is_friend: bool, path: str, x: int, y: int) -> None:
        """
        画像を表示
        name: モンスターの名前
        is_friend: 味方かどうか
        path: 画像のパス
        x: x座標
        y: y座標
        """
        # イメージ作成
        self.image_battle[is_friend][name] = tk.PhotoImage(file=path, width=130, height=130)
        # キャンバスにイメージを表示
        self.canvas.create_image(x, y, image=self.image_battle[is_friend][name], anchor=tk.NW)
    
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
        self.app.bind("<KeyPress>", self.key_listen_to_close_monster_box)
    
    def make_edit_button(self) -> None:
        """
        """
    
    def key_listen_to_close_monster_box(self, event) -> None:
        """
        eキーでモンスターボックスを閉じる
        """
        if event.keysym=="e":
            self.close_monster_box()
    
    def show_all_monster(self) -> None:
        """
        自分が持っているモンスターを表示する
        """
        self.page = 0
        self.make_tk_window("モンスターボックス")
        self.make_close_button()
        self.show_monster()

    def show_monster(self) -> None:
        """
        モンスターを1ページ分表示する
        """
        # 既存のUIを削除
        self.delete_all_ui()
        # テキストを表示
        start_x, start_y = 425, 20
        width, height = 300, 60
        end_x, end_y = start_x+width, start_y+height
        # テキストが設定してあれば削除する
        if self.text_monster_box is not None:
            self.canvas.delete(self.text_monster_box)
        if len(user["monster"])//12==len(user["monster"])/12:
            page_all = len(user["monster"])//12
        else:
            page_all = len(user["monster"])//12+1
        self.text_monster_box = self.canvas.create_text(
            (start_x+end_x)/2, (start_y+end_y)/2,
            text = f"モンスターボックス（{self.page+1}／{page_all}）",
            font = ("", 22)
        )
        # モンスターの画像を表示
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
                self.app,
                text=name,
                font=("", 18),
                width=12,
                height=1
            )
            self.button_monster[i%12].pack()
            left = 0.2*(i%4)+0.12
            top = (0.27*(i//4))%0.81+0.3
            self.button_monster[i%12].place(relx=left, rely=top)
            # # モンスターの詳細情報を表示
            # self.button_monster[i].bind("<1>", self.show_monster_info)
        # 次のページに進むボタンを表示
        if (self.page+1)*12<len(user["monster"]):
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
        elif (self.page+1)*12>=len(user["monster"]) and self.button_page_next is not None:
            self.button_page_next.destroy()
        # 前のページに戻るボタンを表示
        if 0<self.page*12<len(user["monster"]):
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

    def show_monster_info(self) -> None:
        """
        自分が持っているモンスターの詳細を表示する
        """
        self.delete_all_ui()
    
    def show_user_info(self) -> None:
        """
        自分の情報を表示する
        """
        self.delete_all_ui()

    def close_monster_box(self) -> None:
        """
        モンスターボックスを閉じる
        """
        self.delete_all_ui()
        self.app.destroy()

ui = UI()