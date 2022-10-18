import tkinter as tk

from maze_maker import *
from PIL import Image,ImageTk
key = ""
def key_down(event):#キーが押された時に呼びだされる関数
    global key
    key = event.keysym
   

def key_up(event):
    global key
    key =""
  
def main_proc():
    global cx,cy,mx,my
    if key == "Up" and mz[my-1][mx] == 0:
        cy -= 100
        my -= 1
    elif key == "Down"and mz[my+1][mx]  == 0:
        cy += 100
        my += 1
    elif key == "Left"and mz[my][mx-1]  == 0:
        cx -= 100
        mx -= 1
    elif key == "Right"and mz[my][mx+1] == 0:
        cx += 100
        mx += 1
    canvas.coords(t,cx,cy)
    root.after(100,main_proc)
    
def start_end():
    str = canvas.create_rectangle(100, 100, 200, 200, fill="red")   
    end = canvas.create_rectangle(1300, 700, 1400, 800, fill="green")   

if __name__ == "__main__":
    cx,cy = 150,150
    mx,my = 1,1
    root = tk.Tk()
    root.title("迷えるこうかとん")
    root.geometry("1500x900")

    canvas = tk.Canvas(
        root,
        width=1500,
        height=900,
        bg="black"
    )

    mz = make_maze(15,9)
    show_maze(canvas,mz)

    str_en = start_end()

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
    
    main_proc()
    #キーが入力された時に反応する
    root.bind("<KeyPress>",key_down)
    #キーが話された時に反応する
    root.bind("<KeyRelease>",key_up)
    
    root.mainloop()
