from battle import start_battle
from user_info import UserInfo
from window import Window
from fusion import Fusion
from map import Map

import tkinter as tk

# クラスをインスタンス化する
user_info = UserInfo()
window = Window
fusion = Fusion()
map = Map()


# Tkinterの初期設定
app = tk.Tk()
app.title("DQLike")
width = 1200
height = 620
left = 60
top = 30
app.geometry(f"{width}x{height}+{left}+{top}")
# 画面のサイズ変更を禁止
app.resizable(0, 0)
canvas = tk.Canvas(
    app,
    width = width,
    height = height
)
canvas.pack()

"""
To Do

"""
"""
Memo

"""