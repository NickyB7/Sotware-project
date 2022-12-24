# Import Module
from tkinter import *

# create root window
root = Tk()

# root window title and dimension
root.title("Welcome to GeekForGeeks")
# Set geometry (widthxheight)
root.geometry('350x200')

kill = Label(root, text = "Are you a Geek?")
kill.grid(column=0,row = 0)

sam = Label(root,text = "Are you a loving?")
sam.grid(column=0,row = 3)

def clicked():
    sam.configure(text="I just got clicked")


# button widget with red color text
# inside
btn = Button(root, text="Click me",
             fg="red", command=clicked)
# set Button grid
btn.grid(column=1, row=3)
# all widgets will be here
# Execute Tkinter
root.mainloop()