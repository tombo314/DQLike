# ライブラリのインポート
from pygame.locals import *
from PIL import Image
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
        # プレイヤー
        self.playerImg = self.load_image("images/character_split/character_front_1.png", -1)
        # 草
        self.grassImg = self.load_image("images/grass_split/grass.png", -1)
        # 土
        self.sabakuImg = self.load_image("images/dirt_split/dirt.png", -1)
        # プレイヤーの位置（単位：マス）
        self.x, self.y = 0, 0
        # エンカウントする確率
        self.encounter_prob = 0
        # 移動した回数（エンカウントしたら初期化）
        self.move_cnt = 0
        # Tkinterのウィンドウを開いているか
        self.tk_opening = False
        # キャラクターがその向きに移動した回数（向きを変えたら初期化）
        self.move_cnt_direct = 0
    
    def update_player_image(self, direct: str) -> None:
        """
        プレイヤーの画像を更新する
        direct: プレイヤーの向き 「front」「back」「left」「right」のいずれか
        """
        self.playerImg = self.load_image(f"images/character_split/character_{direct}_{self.move_cnt_direct+1}.png", -1)
        self.move_cnt_direct += 1
        self.move_cnt_direct %= 4
    
    def load_image(self, filename, colorkey=None) -> pygame.surface.Surface:
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
        """
        モンスターボックスを表示する
        """
        ui.open_monster_box()

    def encounter_judge(self, enemy: list[dict]):
        """
        エンカウントするか判定する
        enemy: 敵パーティー
        """
        is_encountered = self.is_n_percent(self.encounter_prob)
        # エンカウントする
        if is_encountered==True:
            self.encounter_prob = 0
            self.move_cnt = 0
            # バトルを開始する
            self.tk_opening = True
            battle.start_battle(enemy)
            self.tk_opening = False
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
            enemy = [
                {"name": "スライム", "level": 1, "gear": None},
                {"name": "ゴースト", "level": 1, "gear": None},
                {"name": "ゲルニック将軍", "level": 1, "gear": None}
            ]
            # キーの入力を受け取る
            for event in pygame.event.get():
                # よく分かっていない
                if event.type==QUIT:
                    return None
                # Escapeで画面を閉じる
                elif event.type==KEYDOWN and event.key==K_ESCAPE:
                    return None
                # プレイヤーが移動する
                # 下
                elif event.type==KEYDOWN and (event.key==K_DOWN or event.key==K_s) and self.can_move_to("y+"):
                    # プレイヤーの座標を更新する
                    self.y += 1
                    # プレイヤーの画像を更新する
                    self.update_player_image("front")
                    # エンカウントの判定をする
                    self.encounter_judge(enemy)
                    # キーの入力間隔を空ける
                    key_inputted = True
                # 左
                elif event.type==KEYDOWN and (event.key==K_LEFT or event.key==K_a) and self.can_move_to("x-"):
                    # プレイヤーの座標を更新する
                    self.x -= 1
                    # プレイヤーの画像を更新する
                    self.update_player_image("left")
                    # エンカウントの判定をする
                    self.encounter_judge(enemy)
                    # キーの入力間隔を空ける
                    key_inputted = True
                # 右
                elif event.type==KEYDOWN and (event.key==K_RIGHT or event.key==K_d) and self.can_move_to("x+"):
                    # プレイヤーの座標を更新する
                    self.x += 1
                    # プレイヤーの画像を更新する
                    self.update_player_image("right")
                    # エンカウントの判定をする
                    self.encounter_judge(enemy)
                    # キーの入力間隔を空ける
                    key_inputted = True
                # 上
                elif event.type==KEYDOWN and (event.key==K_UP or event.key==K_w) and self.can_move_to("y-"):
                    # プレイヤーの座標を更新する
                    self.y -= 1
                    # プレイヤーの画像を更新する
                    self.update_player_image("back")
                    # エンカウントの判定をする
                    self.encounter_judge(enemy)
                    # キーの入力間隔を空ける
                    key_inputted = True
                # モンスターボックスを開く
                elif event.type==KEYDOWN and event.key==K_e and self.tk_opening==False:
                    # モンスターボックスを表示する
                    self.tk_opening = True
                    self.show_monster_box()
                    self.tk_opening = False
                # モンスター配合所を開く
                elif event.type==KEYDOWN and event.key==K_f and self.tk_opening==False:
                    self.tk_opening = True
                    # 配合画面を表示する
                    ui.init_parent_child()
                    ui.show_fusion_screen(None)
                    self.tk_opening = False
                    # ウィンドウモードを更新する
                    ui.window_mode = None
                break

map_ = Map()