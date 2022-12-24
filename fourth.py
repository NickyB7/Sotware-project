# Import the required Libraries
from tkinter import *

import downloads as downloads
from PIL import Image, ImageTk

# Create an instance of tkinter frame
win = Tk()

# Set the geometry of tkinter frame


# Create a canvas
canvas = Canvas(win, width=1000, height=1000)
canvas.pack()

# Load an image in the script
img = ImageTk.PhotoImage(Image.open("../../../downloads/unnamed_3.png"))

# Add image to the Canvas Items
canvas.create_image(10, 10, anchor=NW, image=img)

win.mainloop()
