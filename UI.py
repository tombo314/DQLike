# ライブラリのインポート
from time import sleep
import tkinter as tk

# クラスのインポート
from config import *
from json_import import *
from battle_system import battle

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
        # 画像データ
        self.image = {name: [] for name in monster}
        # モンスタ―とUIの座標の対応関係
        # (monster_name, is_friend): (start_x, start_y)
        self.elem_coord = {}
    
    def draw_battle_ui(self) -> None:
        """
        UIを描画する
        """
        # Tkinterのインスタンスを生成
        self.make_tk_window()
        # UIを削除
        self.canvas.delete("all")
        # メッセージボックスを作成
        ui.make_message_box()
        # 敵と味方の名前、HP、MPを表示する
        self.make_party(battle.enemy, "name", False)
        self.make_party(battle.enemy, "hp", False)
        self.make_party(battle.enemy, "mp", False)
        self.make_party(battle.friend, "name", True)
        self.make_party(battle.friend, "hp", True)
        self.make_party(battle.friend, "mp", True)
        # 敵と味方の画像を表示する
        self.plot_image_all()
        self.canvas.update()
        
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
            elem = self.canvas.create_rectangle(
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
            elem = self.canvas.create_text(
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
        self.canvas.update()
    
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
        self.canvas.create_image(x, y, image=self.image[name][-1], anchor=tk.NW)
    
    def plot_image_all(self) -> None:
        """
        敵と味方のパーティーの画像を表示
        """
        i = 0
        for name in battle.enemy:
            width = 212*i+175
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 8
            self.plot_image(name, False, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        i = 0
        for name in battle.friend:
            width = 222*i+170
            if name=="ドラキー" or name=="ボストロール":
                width -= 13
            height = 520
            self.plot_image(name, True, f"images/png_resized/{name}_resized.png", width, height)
            i += 1
        self.canvas.update()
    
    def make_tk_window(self) -> None:
        """
        Tkinterの画面を描画する
        """
        self.app = tk.Tk()
        self.app.title("DQLike")
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
        if self.button_page_back is not None:
            self.button_page_back.destroy()
        for i in range(12):
            if self.button_monster[i] is not None:
                self.button_monster[i].destroy()

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
            relx = 0.2*(i%4)+0.12
            rely = (0.27*(i//4))%0.81+0.3
            self.button_monster[i%12].place(relx=relx, rely=rely)
            # debug
            # self.button_monster[i].bind("<1>", self.show_monster_info)
            i += 1
        # 次のページに進むボタンを表示
        if (self.page+1)*12<len(user["monster"]):
            self.button_page_next = tk.Button(
                self.app,
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
                self.app,
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
        self.canvas.update()

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

ui = UI()