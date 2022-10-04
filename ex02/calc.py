import tkinter as tk
import tkinter.messagebox as tkm

def button_click(event):
    a = event.widget
    txt = a["text"]
    tkm.showinfo(txt,f"{txt}ボタンが押されました")

root = tk.Tk()
root.geometry("300x580")
for i in range(4):
    for j in range(3):
        num = 9-(j+i*3)
        if num >= 0:
            button = tk.Button(root,text=num,font=("Times New Roman",30),width=4,height=2)
            button.bind("<1>",button_click)
            button.grid(column=j,row =i+1)


entry = tk.Entry(justify="right",width=10,font=("TImes New Roman",40))
entry.grid(column=0,row=0,columnspan=3)



root.mainloop()