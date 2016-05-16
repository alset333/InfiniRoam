#!/usr/bin/env python3

from tkinter import *
import time

__author__ = 'Peter Maar'
__version__ = '0.1.0'

def guiInput(tkObj, promptText):

    c = Canvas(tkObj)
    c.pack()

    confirmButton = Button(c, text='Confirm')
    confirmButton.pack()

    l = Label(c, text=promptText)
    l.pack()


    time.sleep(10)


print(guiInput(Tk(), 'Prompt'))