import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from statistics import mode
import random


def showMap(height_map):
    f = plt.figure()
    # matplotlib works with RGB while cv with BGR, so need to convert
    plt.imshow(cv.cvtColor(height_map, cv.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off')
    plt.show(block=True)

# assigns the actual biome colours to the generated biome-maps by applying colour ranges

def colourFix():
    generated_biomes = cv.imread(r"C:\Users\tobia\BA\DISC\combination/" + "2_b_gen.png", cv.IMREAD_COLOR)

    bilat = cv.bilateralFilter(generated_biomes,15,70,70)

    fixed = np.zeros((128,128,3), np.uint8)
    
    underworldColors = {
        1: np.array([0, 0, 255]),       #lava
        2: np.array([0, 0, 35]),   #obsidian
        3: np.array([90, 145, 90]),   #swamp
        4: np.array([30, 160, 210]),      #desert
        5: np.array([90, 80, 130]),       #wasteland
        6: np.array([128, 128, 128]),    #rocks
        7: np.array([210, 170, 135])    #ice
    }

    underworldHeights = {
        1: np.array([0, 255, 0]),  #traversable
        2: np.array([0, 0, 255]),   #nonTraversable
    }


    hsv=cv.cvtColor(bilat,cv.COLOR_BGR2HSV)

    # (1. divide by 2, others normalise to 255)
    # lava in hsv = 0, 100%, 100% 
    lava_lo=np.array([0,200,200])
    lava_hi=np.array([19,255,255])
 
    # obsidian in hsv = 0, 100%, 10% -> 0, 255, 25
    obsidian_lo=np.array([0,200,5])
    obsidian_hi=np.array([30,255,40])

    # swamp in hsv = 125, 40%, 60% -> 170, 100, 150
    swamp_lo=np.array([50,70,120])
    swamp_hi=np.array([100,135,180])

    # desert in hsv = 45, 90%, 80% -> , 220, 200
    desert_lo=np.array([0,180,170])
    desert_hi=np.array([60,255,205])

    # wasteland in hsv = 250, 38%, 50% -> 125, 100, 125
    wasteland_lo=np.array([50,80,100])
    wasteland_hi=np.array([200,145,170])

    # rocks in hsv = 0, 0%, 50% -> 0, 0, 125
    rocks_lo=np.array([0,0,90])
    rocks_hi=np.array([40,40,150])

    # ice in hsv = 212, 36%, 83% -> 106, 88, 207
    ice_lo=np.array([60, 50, 180])
    ice_hi=np.array([140, 100, 245])

    # Mask image to only select browns
    lava=cv.inRange(hsv,lava_lo,lava_hi)
    obsidian=cv.inRange(hsv,obsidian_lo,obsidian_hi)
    swamp=cv.inRange(hsv,swamp_lo,swamp_hi)
    desert=cv.inRange(hsv,desert_lo,desert_hi)
    wasteland=cv.inRange(hsv,wasteland_lo,wasteland_hi)
    rocks=cv.inRange(hsv,rocks_lo,rocks_hi)
    peak=cv.inRange(hsv,ice_lo,ice_hi)

    rows = fixed.shape[0]
    columns = fixed.shape[0]
    for i in range(rows):
        for j in range(columns):
            if (lava[i][j] == 255):
                fixed[i][j] = underworldColors[1]
            elif (obsidian[i][j] == 255):
                fixed[i][j] = underworldColors[2]
            elif (swamp[i][j] == 255):
                fixed[i][j] = underworldColors[3]
            elif (desert[i][j] == 255):
                fixed[i][j] = underworldColors[4]
            elif (wasteland[i][j] == 255):
                fixed[i][j] = underworldColors[5]
            elif (rocks[i][j] == 255):
                fixed[i][j] = underworldColors[6]
            elif (peak[i][j] == 255):
                fixed[i][j] = underworldColors[7]


    thereAreStillBlackSpots = True
    while thereAreStillBlackSpots == True:
        copyfix = fixed
        thereAreStillBlackSpots = False
        for i in np.random.permutation(126):
            i += 1
            for j in np.random.permutation(126):
                j += 1
                if (fixed[i][j] == 0).all():
                    toFill = 0
                    arr = np.zeros((8,3))
                    arr[0] = copyfix[i-1][j-1]
                    arr[1] = copyfix[i-1][j]
                    arr[2] = copyfix[i-1][j+1]
                    arr[3] = copyfix[i][j-1]
                    arr[4] = copyfix[i][j+1]
                    arr[5] = copyfix[i+1][j-1]
                    arr[6] = copyfix[i+1][j]
                    arr[7] = copyfix[i+1][j+1]

                    countArray = np.zeros(8, dtype='int16')
                    for k in range(len(arr)):
                        if ((arr[k] == underworldColors[1]).all()):
                            countArray[k] = 1
                        elif ((arr[k] == underworldColors[2]).all()):
                            countArray[k] = 2
                        elif ((arr[k] == underworldColors[3]).all()):
                            countArray[k] = 3
                        elif ((arr[k] == underworldColors[4]).all()):
                            countArray[k] = 4
                        elif ((arr[k] == underworldColors[5]).all()):
                            countArray[k] = 5
                        elif ((arr[k] == underworldColors[6]).all()):
                            countArray[k] = 6
                        elif ((arr[k] == underworldColors[7]).all()):
                            countArray[k] = 7
                    if not (np.count_nonzero(countArray == 0) == 8):
                        toFill = mode(countArray[np.nonzero(countArray)])
                        fixed[i][j] = underworldColors[toFill]
                    else:
                        thereAreStillBlackSpots = True

    # borders
    for i in range(0, rows):
        if (fixed[0][i] == 0).all(): # top
            fixed[0][i] = fixed[1][i]
        if (fixed[rows-1][i] == 0).all(): # bottom
            fixed[rows-1][i] = fixed[rows-2][i]
        if (fixed[i][0] == 0).all(): # left
            fixed[i][0] = fixed[i][1] 
        if (fixed[i][rows-1] == 0).all(): # right
            fixed[i][rows-1] = fixed[i][rows-2]

    # corners
    for i in range (0, 4):
        if (fixed[0][0] == 0).all():
            fixed[0][0] = fixed[1][1]
        if (fixed[rows-1][rows-1] == 0).all():
            fixed[rows-1][rows-1] = fixed[rows-2][rows-2]
        if (fixed[rows-1][0] == 0).all():
            fixed[rows-1][0] = fixed[rows-2][1]
        if (fixed[0][rows-1] == 0).all():
            fixed[0][rows-1] = fixed[1][rows-2]

    cv.imwrite(r"C:\Users\tobia\BA\DISC\combination/" + "2_b_fixed.png", fixed)


def main():

    colourFix()
    
if __name__ == "__main__":
    main()


