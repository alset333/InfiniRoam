#!/usr/bin/env python3
import os
import sys
import shutil
import InfiniRoamSquare

DEBUGMODE = False

startSize = int(input("Start size:\n"))
endSize = int(input("End size:\n"))
for squarePixelSize in range(startSize, endSize + 1):
    # Scale the images
    try:
        if not os.path.isdir(os.path.normpath(sys.path[0] + '/images/' + str(squarePixelSize))):
            orig = os.path.normpath(sys.path[0] + '/images/originals')
            newDest = os.path.normpath(sys.path[0] + '/images/' + str(squarePixelSize))
            shutil.copytree(orig, newDest)

            for imageName in InfiniRoamSquare.SQUARE_SUBTYPES:
                if DEBUGMODE:
                    print('sips -z ' + str(squarePixelSize) + ' ' + str(squarePixelSize) + ' "' + os.path.normpath(sys.path[0] + '/images/' + str(squarePixelSize) + '/' + imageName + '.gif') + '"')
                    os.system('sips -z ' + str(squarePixelSize) + ' ' + str(squarePixelSize) + ' "' + os.path.normpath(sys.path[0] + '/images/' + str(squarePixelSize) + '/' + imageName + '.gif') + '"')
                else:
                    os.system('sips -z ' + str(squarePixelSize) + ' ' + str(squarePixelSize) + ' "' + os.path.normpath(sys.path[0] + '/images/' + str(squarePixelSize) + '/' + imageName + '.gif') + '" > /dev/null 2>&1')
    except:
        print("Error attempting to scale images. Hopefully they're already there.")
