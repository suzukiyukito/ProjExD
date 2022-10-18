import tkinter as tk
from tkinter import messagebox

from maze_maker import *
from PIL import Image,ImageTk

import sys

import time

key = ""
def key_down(event):#キーが押された時に呼びだされる関数
    global key
    key = event.keysym

    if key == "Escape":#Escapeキーが押された時の処理
        messagebox.showinfo("なんや","ようこんな機能があるのに気づいたな")
        ask = messagebox.askquestion("いいのか？","ゴールしちまうけどええんか？")
        if ask =="yes":#メッセージボックスのyesが押された時
            canvas.delete("tori")
            canvas.create_image(1350, 750,image=tori,tag="tori")
            canvas.pack()
            ret = messagebox.showinfo("ゴール",f"おめでとう\n君はズルをした・.・")
            if ret == "ok":#メッセージボックスのokが押された時
                sys.exit()

def key_up(event):
    global key
    key =""


  
def main_proc():
    global cx,cy,mx,my,jid,mz
    if key == "Up" and (mz[my-1][mx] == 0 or mz[my-1][mx] ==2):
        cy -= 100
        my -= 1
    elif key == "Down"and (mz[my+1][mx]  == 0 or mz[my+1][mx]  == 2):
        cy += 100
        my += 1
    elif key == "Left"and (mz[my][mx-1]  == 0 or mz[my][mx-1]  == 2):
        cx -= 100
        mx -= 1
    elif key == "Right"and (mz[my][mx+1] == 0 or mz[my][mx+1] == 2) :
        cx += 100
        mx += 1

        

    canvas.coords(t,cx,cy)
    jid = root.after(100,main_proc)
    #ゴールに到達したときの処理
    if mz[my][mx] == mz[7][13]:
        root.after_cancel(jid)
        t2 = time.time()#ゴールした時の時間の記録
        jid = None
        pop_message(t2)#ゴールした時間を渡す
    
def start_end():
    canvas.create_rectangle(100, 100, 200, 200, fill="red")#スタートの床を赤に設定   
    canvas.create_rectangle(1300, 700, 1400, 800, fill="green")#ゴールの床を赤に設定

#メッセージ表示
def pop_message(time):
    global t1 
    #メッセージを表示するとともにクリア時間を表示させる
    ret = messagebox.showinfo("ゴール",f"おめでとう\nクリアタイムは{int(time-t1)}秒やで")
    if ret == "ok":
        sys.exit()

if __name__ == "__main__":
    cx,cy = 150,150#こうかとんの初期位置
    mx,my = 1,1#ピクセルの初期設定
    root = tk.Tk()
    root.title("迷えるこうかとん")#タイトル
    root.geometry("1500x900")#画面のサイズ
    canvas = tk.Canvas(
        root,
        width=1500,
        height=900,
        bg="black"
    )#画面設定

    #迷路の呼び出し
    mz = make_maze(15,9)
    show_maze(canvas,mz)
    mz[7][13] = 2


    str_en = start_end()#こうかとんのスタートとゴールの場所の装飾関数の呼び出し

    #スタートの地点を画像で表示
    img = Image.open("./ex03/start.png")
    st = ImageTk.PhotoImage(image=img.resize((int(img.width/5),int(img.height/5))))
    canvas.create_image(150,125,image=st)
    canvas.pack()

    #ゴールの地点を画像で表示
    img2 = Image.open("./ex03/goal.png")
    st2 = ImageTk.PhotoImage(image=img2.resize((int(img2.width/5),int(img2.height/5))))
    canvas.create_image(1350, 725,image=st2)
    canvas.pack()


    #こうかとんの画像処理
    tori = tk.PhotoImage(file="./ex03/fig/3.png")
    t = canvas.create_image(cx,cy,image=tori,tag="tori")
    canvas.pack()

    t1 = time.time()#ゲーム開始時の時間記録

    main_proc()
    #キーが入力された時に反応する
    root.bind("<KeyPress>",key_down)
    #キーが話された時に反応する
    root.bind("<KeyRelease>",key_up)

    root.mainloop()
