import pygame as pg
import sys
from random import randint

class Screen:
    y = 0
    def __init__(self, title, wh, bgimg):
        # 練習1
        pg.display.set_caption(title)

        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()

        self.bg_sfc = pg.image.load(bgimg)
        self.bg_rct = self.bg_sfc.get_rect()

        self.y = wh[0]

    def blit(self):
        Screen.y = (Screen.y+3)%self.y
        self.sfc.blit(self.bg_sfc,[Screen.y-self.y,0])
        self.sfc.blit(self.bg_sfc,[Screen.y,0])

class Bird:
    key_delta = {
        pg.K_UP:    [0, -3],
        pg.K_DOWN:  [0, +3],
        pg.K_LEFT:  [-3 , 0],
        pg.K_RIGHT: [+3, 0],
    }

    def __init__(self, img, zoom, xy):
        # 練習3
        sfc = pg.image.load(img)
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_states[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
                # 練習7
                if check_bound(self.rct, scr.rct) != (+1, +1):
                    self.rct.centerx -= delta[0]
                    self.rct.centery -= delta[1]
        self.blit(scr)

class Life:
  
    def __init__(self,img,zoom,ly=1):
        sfc = pg.image.load(img) # ハート画像の読み込み
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) # ハート画像の倍率変更
        self.rct = self.sfc.get_rect() # ハートのrect取得
        self.y = ly

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,brd:Bird,scr:Screen):
        x,y = brd.rct.midtop
            
        self.rct.center = x-60+30*self.y,y-30
        self.blit(scr)
        

class Bomb:
    def __init__(self, color, radius, vxy, fx, fy):
        self.sfc = pg.Surface((radius*2, radius*2)) # 空のSurface
        self.sfc.set_colorkey((0, 0, 0)) # 四隅の黒い部分を透過させる
        pg.draw.circle(self.sfc, color, (radius,radius), radius) # 円を描く
        self.rct = self.sfc.get_rect()
        self.rct.centerx = fx
        self.rct.centery = fy
        self.vx, self.vy = vxy
        self.bound = 0 # 跳ね返りカウント

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        if yoko == -1 or tate == -1: # もし跳ね返ったら
            self.count_bound() # 跳ね返りカウントを呼び出す

        self.blit(scr)

    def count_bound(self): # 跳ね返りカウント関数
        self.bound += 1 # 跳ね返りのカウントを増やす

        
class Enemy: # 敵クラス
    def __init__(self, img, zoom, xy, vxy):
        """
        img：敵画像
        zoom：敵画像の拡大倍率
        xy：初期位置の座標のタプル
        vxy：敵のx,y移動の大きさのタプル
        """
        sfc = pg.image.load(img) # 敵画像の読み込み
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) # 敵画像の倍率変更
        self.rct = self.sfc.get_rect() # 敵のrect取得
        # 敵の初期位置
        self.rct.center = xy
        self.vx, self.vy = vxy 
        

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.move_ip(self.vx, self.vy) # 敵の移動
        yoko, tate = check_bound(self.rct, scr.rct) # 壁判定
        self.vy *= tate
        self.blit(scr)


class Attack: # 攻撃クラス
    def __init__(self,image,zoom, vxy, fx, fy):
        """
        color：玉の色
        radius：玉の半径
        vxy：玉の移動のタプル
        fx：玉のx軸初期位置
        fy：玉のy軸初期位置
        """
        self.sfc = pg.image.load(image)
        self.sfc = pg.transform.rotozoom(self.sfc,90,zoom)
        self.rct  =self.sfc.get_rect()
        # 初期位置
        self.rct.centerx = fx
        self.rct.centery = fy
        # 移動の変数
        self.vx, self.vy = vxy[0] * 0.05 , vxy[1] * 0.05
        self.move = 0 # 玉の移動距離

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr:Screen):
        self.rct.centerx += self.vx
        self.rct.centery += self.vy # 玉の移動
        # 壁判定
        self.move += 1 # 玉の移動距離
        self.blit(scr)





###こうかとんが３回当たった時の処理(GAME OVER時の処理)
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
    
        #CONTINUE??の追加
        text2 = self.font.render("CONTINUE??",True,(255,255,255))
        text_rect2 = text2.get_rect(center=(1400//2,900//2))
        
        text2_1 = self.font.render("CONTINUE??",True,(0,0,0))
        text_rect2_1 = text2_1.get_rect(center=(1400//2-3,900//2-3))
        """２つの文字を少しずらして張り付けることで、立体的に見せることができる"""

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            #枠の作成
            button1 = pg.Rect(1400//2-200,900//2-40,1600//4,900//10)
            pg.draw.rect(scr.sfc, (122,122,122),button1)#ボタン枠の作成
            self.blit(text,[530,350],scr)
            self.blit(text2_1,text_rect2_1,scr)#文字の張り付け
            self.blit(text2,text_rect2,scr)
            
            #徐々にこうかとんがこちらに近づいてContinueを押させないように邪魔してくるある意味敵キャラ
            img2 = pg.transform.rotozoom(self.img,0,END.bairitu)            
            rect_img2 = img2.get_rect()
            rect_img2.center = (self.wid2,self.ht2+430)
            self.blit(img2,rect_img2,scr)
            pg.display.update(rect_img2)
            END.bairitu *= 1.05
            """
            徐々にこうかとんが拡大してGAMEOVER時のContinueボタンを押させないように邪魔する。
            bairituで徐々に画像を拡大する
            """

def check_bound(obj_rct, scr_rct):
    """
    obj_rct：こうかとんrct，または，爆弾rct
    scr_rct：スクリーンrct
    領域内：+1／領域外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left: 
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom: 
        tate = -1
    return yoko, tate


def main():
    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")
    kkt = Bird("fig/3.png", 1.0, (900, 400))
    end = END("last_enemy.png",(1000,500))

    # Bombクラスインスタンスのリスト
    bkd = []

    # Enemyクラスインスタンスのリスト
    ene = [Enemy("fig/1.png", 1.0, (30  ,randint(0,900)), (randint(-2,2),randint(-2,2)))]

    # Attackクラスインスタンスのリスト
    atk = []

    hrt = [Life("heart.png",0.05),Life("heart.png",0.05,2),Life("heart.png",0.05,3)]

    clock = pg.time.Clock()
    count = 0
    while True:
        scr.blit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        for heart in hrt:
            heart.update(kkt,scr)
        for attack in atk: # attackはAttackクラスインスタンス
            if attack.move >= 100: # 玉の移動距離が100を超えた場合
                atk.remove(attack) # リストから玉を消す

            attack.update(scr) # 玉の更新
                 
        if randint(0,100) == 0: # ランダムに
            # 敵の追加
            ene.append(Enemy("fig/1.png", 1.0, (0,randint(0,900)),(randint(-2,2),randint(-2,2))))

        for enemy in ene: # enemyはEnemyクラスインスタンス
            enemy.update(scr) # 敵の更新
            if kkt.rct.colliderect(enemy.rct):
                count +=1
                ene = []
                bkd =[]
                hrt.pop()
                if count ==3:
                    # もしこうかとんが敵とぶつかったら終了
                        return end.end(scr)
                    

            if randint(0,300) == 0: # ランダムに
                # 爆弾を出す（敵の攻撃）
                bkd.append(Bomb((255,0,0), 10, (randint(-3,3),randint(-3,3)), enemy.rct.centerx, enemy.rct.centery))

            for attack in atk: # attackはAttackクラスインスタンス
                if enemy.rct.colliderect(attack.rct):
                    # 攻撃が敵にあったたら敵を消す
                    ene.remove(enemy)
                    break

        for bomb in bkd: # bombは# Bombクラスインスタンス
            bomb.update(scr) # 爆弾の更新
            if bomb.bound == 3: # もし3回跳ね返ったら
                # 爆弾が消える
                bkd.remove(bomb)
                break

            if kkt.rct.colliderect(bomb.rct):
                count +=1
                ene = []
                bkd =[]
                hrt.pop()
                if count ==3:
                    return end.end(scr)

        key_states = pg.key.get_pressed()
        if key_states[pg.K_SPACE] and int(pg.time.get_ticks())%15 == 0: # スペースキーを押している間
            # 全方位に攻撃が出る
            atk.append(Attack("egg.png", 0.5, (-1000,0), kkt.rct.centerx, kkt.rct.centery))

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init() # 初期化
    main() # ゲームの本体
    pg.quit() # 初期化の解除
    sys.exit()