#!/usr/bin/env python3
# InfiniRoamWorld.py

import InfiniRoamSquare
import random

__author__ = 'Peter Maar'
__version__ = '0.1.0'


class World:
    def __init__(self, sqPxSzArg):
        self.sqPxSz = sqPxSzArg
        self.worldRandom = random.Random()
        self.modifiedSquares = {}
        self.userPos = (0, 0)
        self.userSquare = InfiniRoamSquare.UserSquare(self.sqPxSz)
        self.userInventory = []
        self.userHealth = 100
        self.userFood = 100
        self.userAwake = True

    def modifyLocation(self, loc, newContents):
        self.modifiedSquares[loc] = newContents

    def getLocation(self, loc):
        if loc == self.userPos:
            return self.userSquare
        elif not self.userAwake:
            return self.userSquare
        elif loc in self.modifiedSquares:
            return self.modifiedSquares[loc]
        else:
            return InfiniRoamSquare.Square(loc, self.sqPxSz)

    def userInteract(self, loc, char):
        sq = self.getLocation(loc)
        st = sq.subType
        t = sq.type

        # Consume food, then health, then pass out
        if self.userFood > 0:
            self.userFood -= 1
        elif self.userHealth > 0:
            self.userHealth -= 4
        else:
            self.userAwake = False
            return 'You passed out!'

        # Healing
        if self.userHealth < 100 and self.userFood > 75:
            self.userHealth += 2
            self.userFood += 1


        if t == 'ground' or t == 'spreading':
            if st == 'dirt' and 'crop' in self.userInventory and char != char.lower():
                self.modifyLocation(loc, InfiniRoamSquare.Square(loc, self.sqPxSz, setSubType='crop'))
                self.userInventory.remove('crop')
            else:
                self.userPos = loc

        elif st == 'water':
            if 'boat' in self.userInventory:
                self.userPos = loc
            else:
                return "You need a boat to travel through water!"

        # Ice is slippery, cross ice and you will travel until you hit an object (but you don't interact with it)
        elif st == 'ice':
            if char.lower() == 'w':
                # Keep slipping if blocks are somewhere you can go
                while  self.getLocation((self.userPos[0], self.userPos[1] - 1)).type == 'ground' or self.getLocation((self.userPos[0], self.userPos[1] - 1)).type == 'spreading'\
                    or self.getLocation((self.userPos[0], self.userPos[1] - 1)).subType == 'ice'\
                    or (self.getLocation((self.userPos[0], self.userPos[1] - 1)).subType == 'water' and 'boat' in self.userInventory):
                        self.userPos = (self.userPos[0], self.userPos[1] - 1)
            elif char.lower() == 'a':
                # Keep slipping if blocks are somewhere you can go
                while  self.getLocation((self.userPos[0] - 1, self.userPos[1])).type == 'ground'\
                    or self.getLocation((self.userPos[0] - 1, self.userPos[1])).type == 'spreading'\
                    or self.getLocation((self.userPos[0] - 1, self.userPos[1])).subType == 'ice'\
                    or (self.getLocation((self.userPos[0] - 1, self.userPos[1])).subType == 'water' and 'boat' in self.userInventory):
                        self.userPos = (self.userPos[0] - 1, self.userPos[1])
            elif char.lower() == 's':
                # Keep slipping if blocks are somewhere you can go
                while  self.getLocation((self.userPos[0], self.userPos[1] + 1)).type == 'ground'\
                    or self.getLocation((self.userPos[0], self.userPos[1] + 1)).type == 'spreading'\
                    or self.getLocation((self.userPos[0], self.userPos[1] + 1)).subType == 'ice'\
                    or (self.getLocation((self.userPos[0], self.userPos[1] + 1)).subType == 'water' and 'boat' in self.userInventory):
                        self.userPos = (self.userPos[0], self.userPos[1] + 1)
            elif char.lower() == 'd':
                # Keep slipping if blocks are somewhere you can go
                while  self.getLocation((self.userPos[0] + 1, self.userPos[1])).type == 'ground'\
                    or self.getLocation((self.userPos[0] + 1, self.userPos[1])).type == 'spreading'\
                    or self.getLocation((self.userPos[0] + 1, self.userPos[1])).subType == 'ice'\
                    or (self.getLocation((self.userPos[0] + 1, self.userPos[1])).subType == 'water' and 'boat' in self.userInventory):
                        self.userPos = (self.userPos[0] + 1, self.userPos[1])



        elif st == 'tree':
            self.modifyLocation(loc, InfiniRoamSquare.Square(loc, self.sqPxSz, setSubType='dirt'))
            for i in range(sq.woodCount):
                self.userInventory.append('wood')

        elif st == 'crop':
            self.modifyLocation(loc, InfiniRoamSquare.Square(loc, self.sqPxSz, setSubType='dirt'))
            self.userInventory.append('crop')
            if self.userFood < 50:  # Only effective to a point - can't 'stockpile' food via crops, need 'food' squares to go above ~50
                self.userFood += 3

        elif t == 'food':
            self.userFood += sq.foodPoints
            self.modifyLocation(loc, InfiniRoamSquare.Square(loc, self.sqPxSz, setSubType='dirt'))

        return 'You are now at ' + str(self.userPos)


    def make(self, thingToMake):
        if thingToMake == 'boat':
            if 'boat' in self.userInventory:
                return "You don't need more than one boat!"
            elif self.userInventory.count('wood') >= 5:
                for i in range(5):
                    self.userInventory.remove('wood')
                self.userInventory.append('boat')
                return 'Made a boat from 5 wood.'
            else:
                return "You need 5 wood to make a boat. You only have: " + str(self.userInventory.count('wood')) + ' wood.'
        return "Didn't make anything."