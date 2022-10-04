import tkinter as tk
import tkinter.messagebox as tkm
import math

def button_click(event):
    a = event.widget
    txt = a["text"]
    entry.insert(tk.END,txt)


def cal(a):
    siki = entry.get()#getメソッドにはただ実行するだけで良い
    num = eval(siki)
    entry.delete(0,tk.END)
    entry.insert(tk.END,num)

def rm(a):
    entry.delete(0,tk.END)

def sin(a):
    siki = entry.get()
    num = eval(siki)
    msin = math.sin(math.radians(num))
    entry.delete(0,tk.END)
    entry.insert(tk.END,msin)

def fac(a):
    siki = entry.get()
    num = eval(siki)
    fac = num * num
    entry.delete(0,tk.END)
    entry.insert(tk.END,fac)

def fact(a):
    siki = entry.get()
    num = eval(siki)
    fact_num = 0
    for i in range(int(num)):
        fact_num += i+1
    entry.delete(0,tk.END)
    entry.insert(tk.END,fact_num)

root = tk.Tk()
root.geometry("500x500")
for i in range(4):
    for j in range(3):
        num = 9-(j+i*3)
        if num >= 0:
            button = tk.Button(root,text=num,font=("Times New Roman",30),width=4,height=1)
            button.bind("<1>",button_click)
            button.grid(column=j,row =i+1)
        elif num == -1:
            button = tk.Button(root,text="+",font=("Times New Roman",30),width=4,height=1)
            button.bind("<1>",button_click)
            button.grid(column=j,row =i+1)
        elif num == -2:
            button = tk.Button(root,text="=",font=("Times New Roman",30),width=4,height=1)
            button.bind("<1>",cal)
            button.grid(column=j,row =i+1)

dct = {"CA":rm,"**2":fac,"sin":sin}
for k,(i,j) in enumerate(dct.items(),0):

    if i == "CA":
        button = tk.Button(root,text=i,font=("Times New Roman",30),width=4,height=1,bg = 'blue')
    button = tk.Button(root,text=i,font=("Times New Roman",30),width=4,height=1)
    button.bind("<1>",j)
    button.grid(column=k,row =5)


button = tk.Button(root,text="!",font=("Times New Roman",30),width=4,height=1)
button.bind("<1>",fact)
button.grid(column=4,row =1)

dct2 = {"-","*","/","(",")"}
for i,j in enumerate(dct2,1):
    button = tk.Button(root,text=j,font=("Times New Roman",30),width=4,height=1)
    button.bind("<1>",button_click)
    button.grid(column=3,row =i)
    
entry = tk.Entry(justify="right",width=10,font=("TImes New Roman",40))
entry.grid(column=0,row=0,columnspan=30)


root.mainloop()