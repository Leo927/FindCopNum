import tkinter as tk
import tree


def build(app):
    canvas1 = tk.Canvas(app, width = 1024, height = 600)
    canvas1.pack()

    label1 = tk.Label(app, text= 'Enter number of vertices', fg='green', font=('helvetica', 12, 'bold'))

    input1 = tk.Entry(app, bg='white')

    button1 = tk.Button(text='Generate')
    button1.bind("<ButtonPress-1>", lambda data: tree.generateGraph(input1.get()))
    autoGenBtn = tk.Button(text='AutoGenrate 30,60,90,120,150 vertices graphs',command=tree.autoGenGraph)
    tex = tk.Text(master=app)
    bop = tk.Frame()
    canvas1.create_window(512, 500, window=tex)
    canvas1.create_window(512, 250, window = autoGenBtn)
    canvas1.create_window(512, 200, window=button1)
    canvas1.create_window(512, 120, window=label1)
    canvas1.create_window(512, 150, window=input1)

def printOut(output:str):
    tex.insert(tk.END,output+'\n')
    tex.see(tk.END)