import tkinter as tk

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
cx,cy = 300,400
canvas.create_image(cx,cy,image=tori,tag="tori")
canvas.pack()
root.mainloop()
