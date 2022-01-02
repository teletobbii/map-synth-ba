import numpy as np
import os
import cv2 as cv
import time

# changes Peak biome colour to white which helps with distinguishing it from water

def fixPeaks(src, des, cnt):

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([118, 104, 98])     #peak
    }

    bmap = cv.imread(src + str(cnt) + "_b.png", cv.IMREAD_COLOR)
    
    rows = bmap.shape[0]
    columns = bmap.shape[0]
    maxHeight = 0
    for i in range(rows-1):
        for j in range(columns-1):
            if (bmap[i][j] == biomeColours[7]).all():
                bmap[i][j] = [255, 255, 255]

    cv.imwrite(des + str(cnt) + "_b.png", bmap)



def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(0, 4832):
        
        fixPeaks(src, des, i+1)

        print("*** done fixing color of peaks in biomes " + str(i+1) + " ***")

def main():
    print("***|| Starting Fixer ||***")
    
    start = time.time()

    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\bh_maps_with_corrected_water_hmap/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\bh_maps_with_changed_peak_white/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("***|| All done ||***")

if __name__ == "__main__":
    main()