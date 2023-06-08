from json_import import import_json
import tkinter as tk

class JsonData:
    """
    JSONファイルを読み込む
    """
    def __init__(self) -> None:
        # JSONファイルのデータ
        self.save_data = None
        self.monster = None
        self.skill = None
        self.fusion_tree = None
        # tkinterのインスタンス
        self.app = None
        self.canvas = None
        # 文字のインスタンス
        self.text = None
        # ボタンのインスタンス
        self.button = [tk.Button]*3
    
    def load_json(self, event) -> None:
        """
        JSONファイルを読み込む
        save_data_id: セーブデータの番号
        """
        try:
            save_data_id = event.widget["text"]
            data = import_json(save_data_id)
            self.save_data = data["save_data"]
            self.monster = data["monster"]
            self.skill = data["skill"]
            self.fusion_tree = data["fusion_tree"]
            # tkinterのウィンドウを削除
            self.canvas.destroy()
            self.app.destroy()
        except:
            pass
    
    def select_save_data(self) -> None:
        """
        セーブデータ画面を表示する
        セーブデータをロードする
        """
        # tkinterのウィンドウを作成
        self.make_tk_window("セーブデータの作成・ロード")
        # 文字を表示
        left = 580
        top = 100
        text = "セーブデータを選択してください"
        self.text = self.canvas.create_text(
            left, top,
            font=("helvetica", 18),
            text=text
        )
        # ボタンを作成
        for i in range(3):
            self.button[i] = tk.Button(
                self.app,
                text=i+1,
                font=("", 18),
                width=10,
                height=2,
                bg="#ddd"
            )
            left = 0.2*i+0.22
            top = 0.4
            self.button[i].place(relx=left, rely=top)
            self.button[i].bind("<1>", self.load_json)
        self.app.mainloop()

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

json_data = JsonData()