#!/usr/bin/env python3
# InfiniRoamGUI.py

import InfiniRoamWorld
import InfiniRoamSquare
import shutil
from tkinter import *
from PIL import Image
import os

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False
VIEW_DISTANCE = 7

def scaleImg(imgPath, newSize):
    """WARNING! THIS METHOD WILL OVERWRITE AN IMAGE!
    Takes a path to an image, and saves a scaled version over it with the dimensions 'newSize x newSize'.
    :param imgPath: The path to the image to resize.
    :param newSize: The new size will be newSize x newSize."""
    img = Image.open(imgPath).copy()
    img = img.resize((newSize, newSize))
    img.save(imgPath)

class GUI:
    def __init__(self):
        self.photos = []  # The currently loaded photos. Store them to keep from garbage-collecting, clear to (mostly) unload them.
        self.root = Tk()

        # Get screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        if screen_height < screen_width:
            screen_size = screen_height
        else:
            screen_size = screen_width

        # Determine game size
        self.gamePixelSize = 2 * screen_size // 3

        if DEBUGMODE:
            print('self.gamePixelSize', self.gamePixelSize)

        # Determine number of squares in game
        self.gameSquareSize = VIEW_DISTANCE * 2 + 1

        if DEBUGMODE:
            print('self.gameSquareSize', self.gameSquareSize)

        # Determine squares' pixel size
        self.squarePixelSize = self.gamePixelSize // self.gameSquareSize

        if DEBUGMODE:
            print('self.squarePixelSize', self.squarePixelSize)

        # Scale the images
        if not os.path.isdir(os.path.normpath(sys.path[0] + '/images/' + str(self.squarePixelSize))):  # If the images don't exist yet
            orig = os.path.normpath(sys.path[0] + '/images/originals')                                 # Copy the images...
            newDest = os.path.normpath(sys.path[0] + '/images/' + str(self.squarePixelSize))           # Into the folder...
            shutil.copytree(orig, newDest)                                                             # Where the new scaled ones will be kept

            for imageName in InfiniRoamSquare.SQUARE_SUBTYPES:                                         # Go through and...
                scaleImg(os.path.normpath(newDest + '/' + imageName + '.gif'), self.squarePixelSize)   # Scale each image

        # Images and screen measurements ready, make world
        self.world = InfiniRoamWorld.World(self.squarePixelSize)


        # Canvases. The gameCanvas should be square!
        self.buttonCanvas   = Canvas(self.root)
        self.gameCanvas     = Canvas(self.root, height=self.gamePixelSize, width=self.gamePixelSize)

        # Exit Button
        exitButton = Button(self.buttonCanvas, text = "Quit", command = exit)
        exitButton.pack()

        # 'Make' Entry
        self.makeEntry = Entry(self.buttonCanvas)
        self.makeEntry.pack()

        # 'Make' Button
        makeButton = Button(self.buttonCanvas, text = "Make", command = self.makeInput)
        makeButton.pack()

        # 'Response' Label
        self.responseText = StringVar()
        self.responseLabel = Label(self.buttonCanvas, textvariable=self.responseText)
        self.responseLabel.pack()

        # Player stats
        self.userStatText = StringVar()
        self.userStatText.set('Health:\t' + 'H'*self.world.userHealth + '\nFood:\t' + 'F'*self.world.userFood)
        self.playerStatLabel = Label(self.buttonCanvas, textvariable=self.userStatText, font=('Courier',), justify='left')  # No font size specified, add int to tuple to specify
        self.playerStatLabel.pack()

        self.buttonCanvas.pack()
        self.gameCanvas.pack()

        self.gameCanvas.focus_set()

        self.gameCanvas.bind('<Key>', self.keyPressed)
        self.makeEntry.bind('<Return>', self.makeInput) # Trigger make, like if the button is pressed

        self.updateGameCanvasContents()

        self.root.mainloop()

    def keyPressed(self, event):
        char = event.char
        c = char.lower()
        if DEBUGMODE:
            print('keyPressed', c)
        if c == 'w':
            interactLoc = (self.world.userPos[0], self.world.userPos[1] - 1)
            r = self.world.userInteract(interactLoc, char)
            self.responseText.set(r)
        elif c == 'a':
            interactLoc = (self.world.userPos[0] - 1, self.world.userPos[1])
            r = self.world.userInteract(interactLoc, char)
            self.responseText.set(r)
        elif c == 's':
            interactLoc = (self.world.userPos[0], self.world.userPos[1] + 1)
            r = self.world.userInteract(interactLoc, char)
            self.responseText.set(r)
        elif c == 'd':
            interactLoc = (self.world.userPos[0] + 1, self.world.userPos[1])
            r = self.world.userInteract(interactLoc, char)
            self.responseText.set(r)
        elif c == 'e':
            r = self.displayInventory(self.world.userInventory)
            self.responseText.set(r)
        elif c == 'r':
            self.makeEntry.focus_set()

        elif c == 'q':
            exit()

        self.updateGameCanvasContents()

        self.userStatText.set('Health:\t' + 'H'*self.world.userHealth + '\nFood:\t' + 'F'*self.world.userFood)


    def updateGameCanvasContents(self):
        """Update the contents of the gameCanvas."""
        self.photos = []  # Unload current photos

        pPos = self.world.userPos  # Player position
        leftEdge    = pPos[0] - VIEW_DISTANCE       # Left edge of area
        rightEdge   = pPos[0] + VIEW_DISTANCE + 1   # Right edge of area
        topEdge     = pPos[1] - VIEW_DISTANCE       # Top edge of area
        bottomEdge  = pPos[1] + VIEW_DISTANCE + 1   # Bottom edge of area

        sqX = 0
        sqY = 0

        for locY in range(topEdge, bottomEdge):
            for locX in range(leftEdge, rightEdge):
                location = self.world.getLocation((locX, locY))
                if DEBUGMODE:
                    print('Adding square', location.subType, 'to', locX, locY)
                self.addImage(sqX, sqY, location.imageName)
                sqX += 1
            sqX = 0
            sqY += 1


    def addImage(self, squareX, squareY, imageName):
        if DEBUGMODE:
            print('Adding image', imageName, 'at', squareX, squareY, '\n')
        pixelX = squareX * self.squarePixelSize
        pixelY = squareY * self.squarePixelSize
        photo = PhotoImage(file=imageName)  # Get photo
        self.photos.append(photo)  # Save photo into list to keep loaded
        self.gameCanvas.create_image(pixelX, pixelY, anchor='nw', image=photo)  # Add photo to canvas


    def displayInventory(self, inventory):
        output = ''
        countedItems = []
        inventory.sort()
        for item in inventory:
            if not item in countedItems:
                countedItems.append(item)
                output += str(inventory.count(item)) + ' ' + item + ', '

        if output == '':
            return 'Empty Inventory'
        else:
            return output[:-2]

    def makeInput(self, event=None):
        self.gameCanvas.focus_set() # Set focus back on the game
        makeText = self.makeEntry.get() # Get the text
        self.makeEntry.delete(0, END) # Clear the text
        rspnse = self.world.make(makeText)
        self.responseText.set(rspnse)



    #
    # def updateCanvasContents(self):
    #     """Update the contents of the buttonCanvas."""
    #     plrX = self.world.userPos[0]
    #     plrY = self.world.userPos[1]
    #     vd = VIEW_DISTANCE
    #
    #     self.loadedPhotos = []  # Init/unload loaded photos. Use this list to hold photos to keep from garbage collector
    #
    #     for y in range(plrY - vd, plrY + vd):           # Iterate through rows (top to bottom)
    #         for x in range(plrX - vd, plrX + vd):       # Iterate through columns (left to right)
    #             sqr = self.world.getLocation((x, y))    # Get the square at loc (i, j)
    #             p = PhotoImage(file='test.gif')       # TODO self.phto = PhotoImage(file='./'+sqr.subType+'.gif')
    #             self.loadedPhotos.append(p)                  # Keep the photo loaded
    #             self.addPhoto(p, (x, y))                # Add the photo to the buttonCanvas
    #
    # def addPhoto(self, photo, loc):
    #     """"Adds the given photo to the buttonCanvas at the given location"""
    #     x = loc[0] * self.squareSizePixels
    #     y = loc[1] * self.squareSizePixels
    #
    #     self.buttonCanvas.create_image(x, y, anchor='nw', image=photo)
