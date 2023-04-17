from pprint import pprint
import tkinter as tk
import json

class Battle:
    def __init__(self) -> None:
        self.name_box = [0]*3
        self.name_text = [0]*3
        self.hp_box = [0]*3
        self.hp_text = [0]*3
        self.mp_box = [0]*3
        self.mp_text = [0]*3
    
    def make_element(self, monster: list, type_: str, is_enemy: bool) -> None:
        """
        monster: 敵か味方のモンスター3体の要素の配列
        type: 「名前」「HP」「MP」のいずれか
        is_enemy: 敵の要素であるかどうか
        """
        if type_=="名前":
            y = 100
        elif type_=="HP":
            y = 160
        elif type_=="MP":
            y = 220
        if is_enemy==True:
            color = "#f33"
        elif is_enemy==False:
            color = "#3f3"
            y += 250
        i = 0
        for name in monster:
            start_x, start_y = 220*i+100, y
            width, height = 160, 40
            end_x, end_y = start_x+width, start_y+height
            if type_=="名前":
                self.name_box[i] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                self.name_text[i] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = name
                )
            elif type_=="HP":
                self.hp_box[i] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                hp = monster[name]["hp"]
                self.hp_text[i] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = f"{hp} / {hp}"
                )
            elif type_=="MP":
                self.mp_box[i] = canvas.create_rectangle(
                    start_x, start_y,
                    end_x, end_y,
                    fill = "#ddd",
                    outline = color
                )
                mp = monster[name]["mp"]
                self.mp_text[i] = canvas.create_text(
                    (start_x+end_x)/2, (start_y+end_y)/2,
                    text = f"{mp} / {mp}"
                )
            i += 1
            

with open("monster.json", encoding="utf-8") as f:
    data = json.load(f)
    monster = data["monster"]

app = tk.Tk()

canvas = tk.Canvas(
    app,
    width = 850,
    height = 600
)
canvas.pack()

def battle():
    btl = Battle()
    btl.make_element(monster, "名前", True)
    btl.make_element(monster, "HP", True)
    btl.make_element(monster, "MP", True)
    btl.make_element(monster, "名前", False)
    btl.make_element(monster, "HP", False)
    btl.make_element(monster, "MP", False)

battle()

app.mainloop()
