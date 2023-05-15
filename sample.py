import pygame
from pygame.locals import *
from main import load_battle
def load_map():
    SCR_RECT = Rect(0, 0, 640, 480)
    ROW,COL = 15,20
    GS = 32
    map = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1],
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
    def load_image(filename, colorkey=None):
        image = pygame.image.load(filename)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image
    def draw_map(screen):
        """マップを描画する"""
        for r in range(ROW):
            for c in range(COL):
                if map[r][c] == 0:
                    screen.blit(grassImg, (c*GS,r*GS), (0,128,GS,GS))
                elif map[r][c] == 1:
                    screen.blit(sabakuImg, (c*GS,r*GS), (0,128,GS,GS))
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption("PyRPG 03 プレイヤーの移動")
    # イメージロード 
    playerImg = load_image("images/character.png", -1)  # プレイヤー
    grassImg = load_image("images/grass.png", -1)
    sabakuImg = load_image("images/dirt.png", -1)
    x,y = 0,0  # プレイヤーの位置（単位：マス）
    in_battle = False
    while True:
        draw_map(screen)  # マップ描画
        screen.blit(playerImg, (x*GS,y*GS), (0,0,GS,GS))  # プレイヤー描画
        pygame.display.update()
        # エンカウント
        if (x,y)==(2,1) and in_battle==False:
            in_battle = True
            load_battle()
        elif (x,y)!=(2,1):
            in_battle = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            # プレイヤーの移動処理
            if event.type == KEYDOWN and event.key == K_DOWN:
                y += 1
            if event.type == KEYDOWN and event.key == K_LEFT:
                x -= 1
            if event.type == KEYDOWN and event.key == K_RIGHT:
                x += 1
            if event.type == KEYDOWN and event.key == K_UP:
                y -= 1
load_map()