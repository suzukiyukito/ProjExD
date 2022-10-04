import tkinter as tk
import tkinter.messagebox as tkm
root = tk.Tk()
root.geometry("300x500")
for i in range(4):
    for j in range(3):
        num = 9-(j+i*3)
        if num >= 0:
            button = tk.Button(root,text=num,font=("Times New Roman",30),width=4,height=2)
            button.grid(column=j,row =i)
root.mainloop()