import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import time

# making the heights of the water uniform in the training height-maps

def fixWater(src, des, cnt):

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([255, 255, 255])     #peak
    }

    hmap = cv.imread(src + str(cnt) + "_h.png", cv.IMREAD_GRAYSCALE)
    bmap = cv.imread(src + str(cnt) + "_b.png", cv.IMREAD_COLOR)
    
    rows = hmap.shape[0]
    columns = hmap.shape[0]
    maxHeight = 0
    for i in range(rows-1):
        for j in range(columns-1):
            if (bmap[i][j] == biomeColours[1]).all():
                maxHeight = max(maxHeight, hmap[i][j])
    
    if (maxHeight == 50): 
        maxHeight = 49
    print(maxHeight)

    for i in range(rows-1):
        for j in range(columns-1):
            if (bmap[i][j] == biomeColours[1]).all():
                hmap[i][j] = maxHeight

    cv.imwrite(des + str(cnt) + "_h.png", hmap)



def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(0, 4832):
        
        fixWater(src, des, i+1)

        print("*** done fixing water in heightMap " + str(i+1) + " ***")

def main():
    print("***|| Starting Water Fixer ||***")
    
    start = time.time()

    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\inverted_h_128p/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\bh_maps_with_corrected_water_hmap/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("***|| All done ||***")

if __name__ == "__main__":
    main()