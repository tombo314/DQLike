# ライブラリのインポート
import tkinter as tk

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
