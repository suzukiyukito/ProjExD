
import pygame as pg
from pygame.locals import *

import random

import sys


width,height,width2,height2 =  900,400,1000,500
a,b,c,d =random.randint(0,1600),random.randint(0,900),random.randint(0,1600),random.randint(0,900)
s,scls = 10,1
vx=vx1=vy=vy1 =2
bairitu = 2.0
#######################################
####爆弾


####動く爆弾の関数1
def move_scl1():             # 爆弾が画面の外に出ようとしてしまった時に、入力を反転させることによって
    global vx,vy,s,scls                 # 画面内で反転しながら動き回るようにする
    draw_scl = pg.Surface((80,80))     #爆弾の大きさ
    draw_scl.set_colorkey("black")     #周りの黒い枠部分の透過pg.draw.circle(d_s1,(255,0,0),(40,40),s)
    pg.draw.circle(draw_scl,(255,0,0),(40,40),30)
    
    rect1 = draw_scl.get_rect()
    rect1.center = (a,b)
    return draw_scl,rect1

####動く爆弾の関数2
def move_scl2():                     # 爆弾が画面の外に出ようとしてしまった時に、入力を反転させることによって
    global vx1,vy1,s,scls                      # 画面内で反転しながら動き回るようにする
    draw_scl = pg.Surface((80,80))     #爆弾の大きさ
    draw_scl.set_colorkey("black")     #周りの黒い枠部分の透過
    pg.draw.circle(draw_scl,(255,0,0),(40,40),30)
    rect2 = draw_scl.get_rect()
    rect2.center = (c,d)

    return draw_scl,rect2


#これを定義する事によって爆弾を表示させる
######################################






def main():
    

    screen = pg.display.set_mode((1600,900))
    pg.display.set_caption("逃げろ！こうかとん")#タイトル記入
    tori_pg = pg.image.load(".\ex04\pg_bg.jpg")
    rect_bg = tori_pg.get_rect()
# tori_pgで背景画像をロードし、rect_bgで背景の大きさを取得している。
    vx,vx1,vy,vy1=2,2,2,2 
    
    font = pg.font.Font(None,80)#ゲームオーバーに表示する文字設定

#######################################
#鳥
    t =pg.image.load("ex04/fig/0.png")    #鳥の画定義  
    img  = pg.transform.rotozoom(t,0,2.0) #動く鳥の定義
    rect = img.get_rect()
    rect.center = (width,height)
    #動くこうかとんの関数
    def move_rect(rct):                   ###
        if rct.y < 0:                     #鳥が枠内に収まるように条件の追加
            rct.y=0                       ###
        if rct.y >= 750:
            rct.y =750
        if rct.x < 0:
            rct.x =0
        if rct.x >=1500:
            rct.x = 1500


    t2 =pg.image.load("ex04/fig/1.png")   #GAME OVER時の鳥
######################################
    a,rect1 = move_scl1()
    b,rect2 = move_scl2()
###GAME OVERの時に表示させる関数
    def menu():
        global bairitu
        i,j =50,1
        screen.fill((255,i,0))
        if i >= 255:j*= -1
        elif i < 0:j*= -1 
        i += j
        text = font.render("GAME OVER",True,(255,255,255))
        screen.blit(text,[530,350])

        text2 = font.render("CONTINUE??",True,(255,255,255))
        text_rect2 = text2.get_rect(center=(1400//2,900//2))
        
        text2_1 = font.render("CONTINUE??",True,(0,0,0))
        text_rect2_1 = text2_1.get_rect(center=(1400//2-3,900//2-3))
        button1 = pg.Rect(1400//2-200,900//2-40,1600//4,900//10)
        pg.draw.rect(screen, (122,122,122),button1)
        screen.blit(text2_1,text_rect2_1)
        screen.blit(text2,text_rect2)

        img2 = pg.transform.rotozoom(t2,0,bairitu)            
        rect_img2 = img2.get_rect()
        #img_transpose = img.transpose(Image.FLIP_LEFT_RIGHT)
        rect_img2.center = (width2,height2)
        screen.blit(img2,rect_img2)
        pg.display.update(rect_img2)
        pg.time.wait(50)
        bairitu *= 1.1

    while True:
        screen.blit(tori_pg,rect_bg)       #背景表示

        screen.blit(img,rect)              #鳥の表示
        move_rect(rect)                    #鳥の処理
        
######################################
#爆弾の描写
        screen.blit(a,rect1)
        if rect1.x <= 0 or rect1.x >= 1600-40:
            vx *= -1
        rect1.x += vx
        if rect1.y <= 0 or rect1.y >= 900-40:
            vy *= -1    
        rect1.y += vy   

        screen.blit(b,rect2)
        if rect2.x <= 0 or rect2.x >= 1600-40:
            vx1 *= -1
        rect2.x += vx1
        if rect2.y <= 0 or rect2.y >= 900-40:
            vy1 *= -1    
        rect2.y += vy1     
######################################
# 
                     

        for event in pg.event.get():       ###
            if event.type == QUIT:         # イベントに"x"が押された時などに終了する
                pg.quit()                  ###
                sys.exit()

        pressed_keys = pg.key.get_pressed()###
        if pressed_keys[K_UP]:             #pg.key.get_pressed()これ用いると押されている間
            rect.move_ip(0,-2)             #ずっと更新かけているから、画面上の表示では      
        elif pressed_keys[K_DOWN]:         #ヌルヌル動いてるように見える
            rect.move_ip(0,2) 
        elif pressed_keys[K_RIGHT]:
            rect.move_ip(2,0)
        elif pressed_keys[K_LEFT]:
            rect.move_ip(-2,0)

        if rect.colliderect(rect1) or rect.colliderect(rect2):
            menu()
            

##
# 鳥と爆弾が重なってしまった場合に、終了するような操作を導入する
# これにより、ゲームオーバーのような形になる。
###

        pg.display.update()

if __name__ == "__main__":
    pg.init()
    main()
    