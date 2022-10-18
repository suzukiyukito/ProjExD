import tkinter as tk

key = ""
cx,cy = 300,400
def key_down(event):#キーが押された時に呼びだされる関数
    global key
    key = event.keysym
   

def key_up(event):
    global key
    key =""
  
def main_proc():
    global cx,cy
    if key == "Up":
        cy -= 20
    elif key == "Down":
        cy += 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20
    canvas.coords(t,cx,cy)
    root.after(50,main_proc)
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷える肛門")
    root.geometry("1500x900")

    canvas = tk.Canvas(
        root,
        width=1500,
        height=900,
        bg="black"
    )

    tori = tk.PhotoImage(file="./ex03/fig/3.png")
    t = canvas.create_image(cx,cy,image=tori,tag="tori")
    canvas.pack()

    #キーが入力された時に反応する
    root.bind("<KeyPress>",key_down)
    #キーが話された時に反応する
    root.bind("<KeyRelease>",key_up)

    main_proc()

    root.mainloop()
