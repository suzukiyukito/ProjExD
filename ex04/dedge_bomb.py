
import pygame as pg
from pygame.locals import *

import random

import sys

width,height =  900,400

def main():
    screen = pg.display.set_mode((1600,900))
    pg.display.set_caption("逃げろ！こうかとん")#タイトル記入
    tori_pg = pg.image.load(".\ex04\pg_bg.jpg")
    rect_bg = tori_pg.get_rect()
    ###
    # tori_pgで背景画像をロードし、rect_bgで背景の大きさを取得している。

    t  =pg.image.load("ex04/fig/0.png")#鳥
    img = pg.transform.rotozoom(t,0,2.0)
    rect = img.get_rect()
    rect.center = (width,height)
    ###
    # 動く鳥の定義をしている。
    
    draw_scl = pg.Surface((20,20))#爆弾
    draw_scl.set_colorkey("black")#周りの黒い枠部分の透過
    pg.draw.circle(draw_scl,(255,0,0),(10,10),10)
    rect2 = draw_scl.get_rect()
    rect2.center = (random.randint(0,1600),random.randint(0,900))
    ###
    # 動く爆弾の定義をしている。
    x,y = 1,1
  

    while True:
        
        screen.blit(tori_pg,rect_bg)#背景表示
        screen.blit(img,rect)#鳥の表示
        if rect.y < 0:
            rect.y=0
        if rect.y >= 750:
            rect.y =750
        if rect.x < 0:
            rect.x =0
        if rect.x >=1500:
            rect.x = 1500
###
#鳥が枠内に収まるように条件の追加
###

        screen.blit(draw_scl,rect2)#爆弾表示
        if rect2.x <= 0 or rect2.x >= 1600-10:
            x = -x
        rect2.x += x
        if rect2.y <= 0 or rect2.y >= 900-10:
            y = -y    
        rect2.y += y
###
# 爆弾が画面の外に出ようとしてしまった時に、入力を反転させることによって画面内で
# 反転しながら動き回るようにする
###

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
###
# イベントに"x"が押された時などに終了する
###
        pressed_keys = pg.key.get_pressed()
        if pressed_keys[K_UP]:
            rect.move_ip(0,-1)
        elif pressed_keys[K_DOWN]:
            rect.move_ip(0,1) 
        elif pressed_keys[K_RIGHT]:
            rect.move_ip(1,0)
        elif pressed_keys[K_LEFT]:
            rect.move_ip(-1,0)
###
#pg.key.get_pressed()これ用いると押されている間ずっと更新かけているから、画面上の表示では
#ヌルヌル動いてるように見える
###

        if rect.colliderect(rect2):
            pg.quit()
            sys.exit()
###
# 鳥と爆弾が重なってしまった場合に、終了するような操作を導入する
# これにより、ゲームオーバーのような形になる。
###

        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    