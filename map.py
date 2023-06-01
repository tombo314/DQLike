# ライブラリのインポート
from pygame.locals import *
import pygame
import random as rd
from time import sleep

# クラスのインポート
from battle import battle
from ui import ui

# ライブラリの初期設定
pygame.init()

KEY_INPUT_DURATION = 0.1

class Map:
    """
    マップを表示する
    """
    def __init__(self) -> None:
        self.scr_rect = Rect(0, 0, 640, 480)
        self.row, self.col = 15,20
        self.gs = 32
        self.bitmap = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1],
            [1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,1,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]
        self.screen = pygame.display.set_mode(self.scr_rect.size)
        pygame.display.set_caption("フィールドマップ")
        # イメージロード
        self.playerImg = self.load_image("images/character.png", -1)  # プレイヤー
        self.grassImg = self.load_image("images/grass.png", -1)
        self.sabakuImg = self.load_image("images/dirt.png", -1)
        # プレイヤーの位置（単位：マス）
        self.x, self.y = 0, 0
        # Trueでキーを押せない
        self.key_in_use = False
        # エンカウントする確率
        self.encounter_prob = 0
        # 移動した回数
        self.move_cnt = 0
    
    def load_image(self, filename, colorkey=None):
        image = pygame.image.load(filename)
        image = image.convert()
        if colorkey is not None:
            if colorkey==-1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image

    def draw_map(self, screen):
        """マップを描画する"""
        for r in range(self.row):
            for c in range(self.col):
                if self.bitmap[r][c]==0:
                    screen.blit(self.grassImg, (c*self.gs, r*self.gs), (0, 128, self.gs, self.gs))
                elif self.bitmap[r][c]==1:
                    screen.blit(self.sabakuImg, (c*self.gs, r*self.gs), (0, 128, self.gs, self.gs))
    
    def can_move_to(self, direction: str) -> bool:
        """
        その場所に移動することができるか
        direction: 「x+」「x-」「y+」「y-」のいずれか
        """
        if direction=="x+":
            if self.x+1<len(self.bitmap[0]) and self.bitmap[self.y][self.x+1]==1:
                return True
        elif direction=="x-":
            if self.x-1>=0 and self.bitmap[self.y][self.x-1]==1:
                return True
        elif direction=="y+":
            if self.y+1<len(self.bitmap) and self.bitmap[self.y+1][self.x]==1:
                return True
        elif direction=="y-":
            if self.y-1>=0 and self.bitmap[self.y-1][self.x]==1:
                return True
        return False
    
    def is_n_percent(self, prob: int) -> bool:
        """
        probパーセントの確率でTrueを返す
        prob: Trueが返ってくる確率(0~100)
        """
        r = rd.randint(1, 100)
        if r<=prob:
            return True
        return False

    def show_monster_box(self) -> None:
        ui.make_tk_window()
        ui.show_all_monster()

    def encounter_judge(self, enemy: list):
        """
        エンカウントするか判定する
        enemy: 敵パーティー
        """
        is_encountered = self.is_n_percent(self.encounter_prob)
        # エンカウントする
        if is_encountered==True and self.in_use==False:
            self.in_use = True
            self.encounter_prob = 0
            self.move_cnt = 0
            # バトルを開始する
            # battle.start_battle(enemy)
            # モンスターボックスを開く
            self.show_monster_box()
        # エンカウントしない
        else:
            # 確率を調整する
            if self.move_cnt<3:
                pass
            elif 3<=self.move_cnt<=5:
                self.encounter_prob += 1
            elif self.move_cnt<=8:
                self.encounter_prob += 2
            elif self.move_cnt<=10:
                self.encounter_prob += 7
            elif self.move_cnt>=11:
                self.encounter_prob += 15
            self.move_cnt += 1

    def run(self) -> None:
        """
        マップを表示する
        """
        key_inputted = False
        while True:
            # マップを描画する
            self.draw_map(self.screen)
            # プレイヤーの座標を更新する
            self.screen.blit(self.playerImg, (self.x*self.gs, self.y*self.gs), (0, 0, self.gs, self.gs))
            pygame.display.update()
            # キーの入力間隔を空ける
            if key_inputted==True:
                sleep(KEY_INPUT_DURATION)
                key_inputted = False
            # 敵パーティーを設定
            # 出てくるモンスターの種類を指定して、その中からランダムに選ぶ
            enemy = ["スライム", "ゴースト", "ゲルニック将軍"]
            # キーの入力を受け取る
            for event in pygame.event.get():
                if event.type==QUIT:
                    exit()
                # Escapeで画面を閉じる
                elif event.type==KEYDOWN and event.key==K_ESCAPE:
                    exit()
                # プレイヤーが移動する
                # 下
                elif event.type==KEYDOWN and event.key==K_DOWN and self.can_move_to("y+"):
                    self.y += 1
                    self.encounter_judge(enemy)
                    key_inputted = True
                # 左
                elif event.type==KEYDOWN and event.key==K_LEFT and self.can_move_to("x-"):
                    self.x -= 1
                    self.encounter_judge(enemy)
                    key_inputted = True
                # 右
                elif event.type==KEYDOWN and event.key==K_RIGHT and self.can_move_to("x+"):
                    self.x += 1
                    self.encounter_judge(enemy)
                    key_inputted = True
                # 上
                elif event.type==KEYDOWN and event.key==K_UP and self.can_move_to("y-"):
                    self.y -= 1
                    self.encounter_judge(enemy)
                    key_inputted = True
                break

map_ = Map()