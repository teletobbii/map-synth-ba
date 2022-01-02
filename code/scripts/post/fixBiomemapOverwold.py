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
    generated_biomes = cv.imread(r"C:\Users\tobia\BA\DISC\combination/" + "1_b_gen.png", cv.IMREAD_COLOR)

    bilat = cv.bilateralFilter(generated_biomes,15,70,70)

    fixed = np.zeros((128,128,3), np.uint8)

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([255, 255, 255])     #peak
    }

    hsv=cv.cvtColor(bilat,cv.COLOR_BGR2HSV)

    # (1. divide by 2, others normalise to 255)
    # water in hsv = 235, 86%, 100% -> 117, 219, 255
    water_lo=np.array([85,75,75])
    water_hi=np.array([140,245,255])
 
    # sand in hsv = 118, 40%, 100% -> 58, 102, 255
    sand_lo=np.array([45,75,180])
    sand_hi=np.array([80,125,255])

    mountains_lo=np.array([0,180,180])
    mountains_hi=np.array([90,255,255])

    # grass in hsv = 40, 100%, 47% -> 20, 255, 125
    grass_lo=np.array([10,120,100])
    grass_hi=np.array([30,255,155])

    # forest in hsv = 34, 35%, 78% -> 17, 90, 191
    forest_lo=np.array([0,30,170])
    forest_hi=np.array([30,125,230])

    # steppe in hsv = 81, 100%, 37% -> 40, 255, 95
    steppe_lo=np.array([30,200,75])
    steppe_hi=np.array([50,255,130])

    # peak in hsv = 222, 17%, 46% -> 111, 43, 118
    # peakwhite in hsv = 0, 0%, 100% -> 0, 00, 255
    peak_lo=np.array([0, 0, 200])
    peak_hi=np.array([70, 70, 255])

    # Mask image to only select browns
    water=cv.inRange(hsv,water_lo,water_hi)
    sand=cv.inRange(hsv,sand_lo,sand_hi)
    mountains=cv.inRange(hsv,mountains_lo,mountains_hi)
    grass=cv.inRange(hsv,grass_lo,grass_hi)
    forest=cv.inRange(hsv,forest_lo,forest_hi)
    steppe=cv.inRange(hsv,steppe_lo,steppe_hi)
    peak=cv.inRange(hsv,peak_lo,peak_hi)

    rows = fixed.shape[0]
    columns = fixed.shape[0]
    for i in range(rows):
        for j in range(columns):
            if (water[i][j] == 255):
                fixed[i][j] = biomeColours[1]
            elif (sand[i][j] == 255):
                fixed[i][j] = biomeColours[2]
            elif (forest[i][j] == 255):
                fixed[i][j] = biomeColours[3]
            elif (grass[i][j] == 255):
                fixed[i][j] = biomeColours[4]
            elif (steppe[i][j] == 255):
                fixed[i][j] = biomeColours[5]
            elif (mountains[i][j] == 255):
                fixed[i][j] = biomeColours[6]
            elif (peak[i][j] == 255):
                fixed[i][j] = biomeColours[7]

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
                        if ((arr[k] == biomeColours[1]).all()):
                            countArray[k] = 1
                        elif ((arr[k] == biomeColours[2]).all()):
                            countArray[k] = 2
                        elif ((arr[k] == biomeColours[3]).all()):
                            countArray[k] = 3
                        elif ((arr[k] == biomeColours[4]).all()):
                            countArray[k] = 4
                        elif ((arr[k] == biomeColours[5]).all()):
                            countArray[k] = 5
                        elif ((arr[k] == biomeColours[6]).all()):
                            countArray[k] = 6
                        elif ((arr[k] == biomeColours[7]).all()):
                            countArray[k] = 7
                    if not (np.count_nonzero(countArray == 0) == 8):
                        toFill = mode(countArray[np.nonzero(countArray)])
                        fixed[i][j] = biomeColours[toFill]
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

    cv.imwrite(r"C:\Users\tobia\BA\DISC\combination/" + "1_b_fixed.png", fixed)


def main():

    colourFix()
    
if __name__ == "__main__":
    main()


