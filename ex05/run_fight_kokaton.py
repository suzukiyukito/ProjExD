import pygame as pg
import sys
from random import randint,random

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


class Screen:
    def __init__(self, title, wh, bgimg):
        pg.display.set_caption(title) #逃げろ！こうかとん
        self.sfc = pg.display.set_mode(wh) #(1600, 900)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(bgimg) #"fig/pg_bg.jpg"
        self.bgi_rct = self.bgi_sfc.get_rect()
        
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)

class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img, zoom, xy):
        sfc = pg.image.load(img) # "fig/6.png"
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) # 2.0
        self.rct = self.sfc.get_rect()
        self.rct.center = xy # 900, 400

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]*5
                self.rct.centery += delta[1]*5
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]*5
                    self.rct.centery -= delta[1]*5
        self.blit(scr) # =scr.sfc.blit(self.sfc, self.rct)

#爆弾の関数
class Bomb:
    def __init__(self, color, radius, vxy, scr:Screen):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius, radius), radius) # 爆弾用の円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = randint(0, scr.rct.width)
        self.rct.centery = randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr) # =scr.sfc.blit(self.sfc, self.rct)
#第2の敵の敵キャラ
class Enemy():
    ran = random()
    def __init__(self,image,angle,xy):
        self.sfc = pg.image.load(image)
        self.angle = angle
        self.sfc2 = pg.transform.rotozoom(self.sfc,self.angle,Enemy.ran)
        self.rct = self.sfc2.get_rect()
        self.rct.center = xy
        

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc2, self.rct)

    def update(self,scr:Screen):
        self.sfc2 = pg.transform.rotozoom(self.sfc,self.angle,Enemy.ran)
        self.sfc_w = self.sfc.get_width()
        self.sfc_h = self.sfc.get_height()
        ### 回転角度設定
        if self.angle > -359:
            self.angle -= 1
        else:
            self.angle  = 0
        self.blit(scr)
"""敵キャラがブレブレになりながら、回転している関数"""


#Continueを押させる気のないGAMEOVER画面
class END:
    bairitu = 2.0
    def __init__(self,img,xy):
        self.font = pg.font.Font(None,80)#ゲームオーバーに表示する文字設定
        self.img = pg.image.load(img)#画像読み込み
        self.wid2,self.ht2 = xy #画像の中心
    
    def blit(self,moji,rct,scr:Screen):
        scr.sfc.blit(moji, rct)

    def end(self,scr:Screen):
        scr.sfc.fill((255,0,0))

        #GAME OVERの文字
        text = self.font.render("GAME OVER",True,(255,255,255))
        self.blit(text,[530,350],scr)
        #CONTINUE??の追加
        text2 = self.font.render("CONTINUE??",True,(255,255,255))
        text_rect2 = text2.get_rect(center=(1400//2,900//2))
        
        text2_1 = self.font.render("CONTINUE??",True,(0,0,0))
        text_rect2_1 = text2_1.get_rect(center=(1400//2-3,900//2-3))
        """２つの文字を少しずらして張り付けることで、立体的に見せることができる"""
        #枠の作成
        button1 = pg.Rect(1400//2-200,900//2-40,1600//4,900//10)
        pg.draw.rect(scr.sfc, (122,122,122),button1)#ボタン枠の作成

        self.blit(text2_1,text_rect2_1,scr)#文字の張り付け
        self.blit(text2,text_rect2,scr)
        
        #徐々にこうかとんがこちらに近づいてContinueを押させないように邪魔してくるある意味敵キャラ
        img2 = pg.transform.rotozoom(self.img,0,END.bairitu)            
        rect_img2 = img2.get_rect()
        rect_img2.center = (self.wid2,self.ht2)
        self.blit(img2,rect_img2,scr)
        pg.display.update(rect_img2)
        END.bairitu *= 1.1
        """
        徐々にこうかとんが拡大してGAMEOVER時のContinueボタンを押させないように邪魔する。
        bairituで徐々に画像を拡大する
        """


"""
敵を出現させるクラスを作成する。
初期インスタンスは敵の画像を生成し、初めにScreenのxy座標に位置される。

"""

def main():

    scr = Screen("逃げろ！こうかとん", (1600, 900), "fig/pg_bg.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    bkd = Bomb((255, 0, 0), 10, (+5, +5), scr)

    ene = Enemy("fig/enemy.png",0,(200,500))
    ene2 = Enemy("fig/enemy.png",0,(900,900))
    ene3 = Enemy("fig/enemy.png",0,(1300,200))
    end = END("fig/1.png",(1000,500))

    clock = pg.time.Clock() # 練習1
    while True:
        scr.blit() # 練習2
        
        for event in pg.event.get(): # 練習2
            if event.type == pg.QUIT:
                return
        
        ene.update(scr)
        ene2.update(scr)
        ene3.update(scr)
        kkt.update(scr)        
        bkd.update(scr)



        # 練習8
        if kkt.rct.colliderect(bkd.rct) or kkt.rct.colliderect(ene.rct) or  kkt.rct.colliderect(ene2.rct) or kkt.rct.colliderect(ene3.rct): # こうかとんrctが爆弾rctと重なったら
            end.end(scr)

        pg.display.update() #練習2
        clock.tick(2000)


if __name__ == "__main__":
    pg.init() # 初期化
    main()    # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()