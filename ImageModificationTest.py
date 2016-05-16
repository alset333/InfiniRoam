from PIL import ImageTk
import PIL.Image
import os
import sys
from tkinter import *

root = Tk()

#p = PhotoImage(file='test.gif')
img = PIL.Image.open('test.gif').copy()
for i in range(img.width//2):
    for j in range(img.height//2):
        img.putpixel((j*2,i*2), 0)
p = ImageTk.PhotoImage(img)

canvas = Canvas()

canvas.create_image(0, 0, anchor='nw', image=p) 

canvas.pack()
