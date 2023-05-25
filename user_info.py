# クラスのインポート
from json_import import *
from screen import canvas

class UserInfo:
    """
    プレイヤーの情報を管理する
    """
    def __init__(self) -> None:
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
        # パーティー内でモンスターの重複があったら終了
        if len(set(self.friend))<=2:
            print("味方パーティー内でモンスターが重複しています。")
            exit()
    
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

user_info = UserInfo()