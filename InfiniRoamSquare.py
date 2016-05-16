#!/usr/bin/env python3
# InfiniRoamSquare.py

import hashlib
import random
from PIL import Image
import os
import sys

__author__ = 'Peter Maar'
__version__ = '0.1.0'

DEBUGMODE = False

# More organised
SQUARE_TYPES_SUBTYPES = \
    {'user':         ('user',),
     'player':       ('player',),
     'ground':       ('stone', 'dirt', 'sand'),
     'living':       ('animal', 'monster'),
     'growing':      ('crop', 'bush', 'tree'),
     'spreading':    ('grass', 'fungus'),
     'water':        ('water', 'ice'),
     'fire':         ('fire', 'lava'),
     'food':         ('food',),
     'ore':          ('ore',),
     'man-made':     ('material', 'bricks', 'glass', 'wood')}

# More useful
SQUARE_SUBTYPES_TYPES = {}
for key in SQUARE_TYPES_SUBTYPES:
    for item in SQUARE_TYPES_SUBTYPES[key]:
        SQUARE_SUBTYPES_TYPES[item] = key

if DEBUGMODE:
    print(SQUARE_SUBTYPES_TYPES)

SQUARE_SUBTYPES = \
    {'user': 0, 'player': 0,     # User != player. 'user' is this, 'player' is other players (for future multi-player)
     'stone': 30, 'dirt': 45, 'sand': 30,    # Ground
     'animal': 5, 'monster': 5,        # Living creatures
     'crop': 5, 'bush': 7, 'tree': 10,     # Growing stuff
     'grass': 20, 'fungus': 1,          # Spreading stuff
     'water': 40, 'ice': 5,             # Water
     # no air - not 3d right now     'air': 100,                      # Air
     'fire': 1, 'lava': 1,             # Fire
     'food': 10,                     # Food
     'ore': 10,          # Ore is unprocessed material.
     'material': 0, 'bricks': 0, 'glass': 0, 'wood': 0}  # Man-made. Material is processed ore.

WEIGHTED_SQUARE_SUBTYPES = []
for item in SQUARE_SUBTYPES:
    weight = SQUARE_SUBTYPES[item]
    for i in range(weight):
        WEIGHTED_SQUARE_SUBTYPES.append(item)

WEIGHTED_SQUARE_SUBTYPES.sort()  # Dictionaries are in a random order, so sort the resulting list to account for this


class Square:
    def __init__(self, loc, sqPxSize, setSubType = 'random'):
        # set 'self.locIntHash' - a (ideally) unique hash for the location
        locStr = str(loc)  # Get a string from it
        locEncoded = locStr.encode('utf-8')  # Encode the string to utf-8
        locHashObj = hashlib.sha512(locEncoded)  # Make a hash object for the utf-8 string
        locHexHash = locHashObj.hexdigest()  # Get the hash in hex
        self.locIntHash = int(locHexHash, 16)  # Convert the hex to an int (allows for adding to easily adjust random #s)

        # Random generator based on location's hash, used for setting attributes:
        atrbRand = random.Random(self.locIntHash)


        # set 'self.locIntHash' - a (ideally) unique hash for the area the location is in
        areaStr = str(loc[0]//10) + str(loc[1]//10)
        areaEncoded = areaStr.encode('utf-8')  # Encode the string to utf-8
        areaHashObj = hashlib.sha512(areaEncoded)  # Make a hash object for the utf-8 string
        areaHexHash = areaHashObj.hexdigest()  # Get the hash in hex
        self.areaIntHash = int(areaHexHash, 16)  # Convert the hex to an int (allows for adding to easily adjust random #s)

        # Random generator based on area's hash, used for affecting square subtypes by area:
        areaRand = random.Random(self.areaIntHash)

        # Set the type prevelant in this area based on the area
        areaType = areaRand.choice(WEIGHTED_SQUARE_SUBTYPES)

        # Determine whether the individual square (so use atrbRand) should be the area type or not
        isAreaType = atrbRand.randint(0, 1) == 1


        # # # # # Start of setting attributes # # # # #




        # Subtype and type
        if setSubType == 'random':
            if isAreaType:
                self.subType = areaType
            else:
                self.subType = atrbRand.choice(WEIGHTED_SQUARE_SUBTYPES)
        else:
            self.subType = setSubType
        self.type = SQUARE_SUBTYPES_TYPES[self.subType]

        # Prepare color modification values
        rChg = 0  # Danger level
        gChg = 0  # Helpfulness level
        bChg = 0  # Other attributes

        # Height
        self.height = atrbRand.randint(0, 100)
        #bChg += self.height

        # Wood count if tree
        if self.subType == 'tree':
            self.woodCount = atrbRand.randint(3, 10)
            gChg += self.woodCount*10

        # Food points if food
        if self.type == 'food':
            self.foodPoints = atrbRand.randint(5, 10)
            gChg += self.foodPoints*10

        # Damage if monster
        if self.subType == 'monster':
            self.damage = atrbRand.randint(0, 25)
            rChg += self.damage*10

        if self.subType == 'ore':
            rChg += atrbRand.randint(0, 100)
            gChg += atrbRand.randint(0, 100)
            bChg += atrbRand.randint(0, 100)

        # Convert to 3 character strings
        redChange   = '0' * (3 - len(str(rChg))) + str(rChg)
        greenChange = '0' * (3 - len(str(gChg))) + str(gChg)
        blueChange  = '0' * (3 - len(str(bChg))) + str(bChg)
        if DEBUGMODE:
            print(self.subType + '_' + redChange + '_' + greenChange + '_' + blueChange)

        # Set the name/path of the image for this square
        self.imageName = os.path.normpath(sys.path[0] + '/images/' + str(sqPxSize) + '/' + self.subType + '_' + redChange + '_' + greenChange + '_' + blueChange + '.gif')
        if DEBUGMODE:
            print('self.imageName:', self.imageName)

        if not os.path.isfile(self.imageName):  # If the image for this square doesn't exist yet, make it
            inImgPath = os.path.normpath(sys.path[0] + '/images/' + str(sqPxSize) + '/' + self.subType + '.gif') # Start with the image from the subtype
            img = Image.open(inImgPath).copy()  # Load the starting image
            img = img.convert('RGBA')  # Convert to RGBA - GIF uses one number to identify a color within the limited color palette. For some reason 'RGB' struggles to convert back, so we use 'RGBA'

            for y in range(img.height):
                for x in range(img.width):
                    currentPxLoc = (x, y)
                    px = img.getpixel(currentPxLoc)
                    r = px[0] + rChg
                    g = px[1] + gChg
                    b = px[2] + bChg
                    img.putpixel(currentPxLoc, (r, g, b))

            img.convert('P', palette=Image.ADAPTIVE)
            img.save(self.imageName)  # Save to the rightful place (name/path of the image for this square)



        # # # # # End of setting attributes # # # # #


class UserSquare:
    def __init__(self, sqPxSize):
        self.type = 'user'
        self.subType = 'user'
        self.imageName = os.path.normpath(sys.path[0] + '/images/' + str(sqPxSize) + '/' + self.subType + '.gif')

class PlayerSquare:
    def __init__(self, sqPxSize):
        self.type = 'player'
        self.subType = 'player'
        self.imageName = os.path.normpath(sys.path[0] + '/images/' + str(sqPxSize) + '/' + self.subType + '.gif')

