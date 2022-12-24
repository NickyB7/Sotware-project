from tkinter import *
from tkinter.ttk import *

from time import strftime

root = Tk()
root.title("clock")

def time():
    string = strftime('%H:%M:%S %p')
    label.config(text=string)
    label.after(1000, time)

label = Label(root, font=(200), background="white")
label.pack(padx=20,pady=20)
time()

mainloop()