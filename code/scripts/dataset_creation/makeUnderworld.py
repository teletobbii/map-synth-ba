import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from statistics import mode
import os
import time

# creates a underworld themed map from every second data sample

def makeUnderworlds(src, des, cnt):

    bmap = cv.imread(src + str(cnt) + "_b.png", cv.IMREAD_COLOR)
    tmap = cv.imread(src + str(cnt) + "_t.png", cv.IMREAD_GRAYSCALE)
    hmap = cv.imread(src + str(cnt) + "_h.png", cv.IMREAD_GRAYSCALE)
    
    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([255, 255, 255])    #peak
    }

    overworldHeights = {
        1: np.array([255, 0, 0]),  #traversable
        2: np.array([0, 165, 255]),   #nonTraversable
    }


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

    underworld = np.zeros([128, 128, 3], dtype=np.uint8)
    heights = np.zeros([128, 128, 3], dtype=np.uint8)

    rows = bmap.shape[0]
    columns = bmap.shape[0]

    if (cnt % 2) == 0:

        for i in range(rows):
            for j in range(columns):
                if (bmap[i][j] == biomeColours[1]).all():
                    underworld[i][j] = underworldColors[1]
                elif (bmap[i][j] == biomeColours[2]).all():
                    underworld[i,j] = underworldColors[2]
                elif (bmap[i][j] == biomeColours[3]).all():
                    underworld[i,j] = underworldColors[3]
                elif (bmap[i][j] == biomeColours[4]).all():
                    underworld[i,j] = underworldColors[4]
                elif (bmap[i][j] == biomeColours[5]).all():
                    underworld[i,j] = underworldColors[5]
                elif (bmap[i][j] == biomeColours[6]).all():
                    underworld[i,j] = underworldColors[6]
                elif (bmap[i][j] == biomeColours[7]).all():
                    underworld[i,j] = underworldColors[7]
                
                if (tmap[i][j] == 255):
                    heights[i,j] = underworldHeights[1]
                else:
                    heights[i,j] = underworldHeights[2]

        cv.imwrite(des + str(cnt) + "_b.png", underworld)
        cv.imwrite(des + str(cnt) + "_t.png", heights)
    
    else:
        for i in range(rows):
            for j in range(columns):
                if (tmap[i][j] == 255):
                    heights[i,j] = overworldHeights[1]
                else:
                    heights[i,j] = overworldHeights[2]
        
        cv.imwrite(des + str(cnt) + "_t.png", heights)
        cv.imwrite(des + str(cnt) + "_b.png", bmap)


    cv.imwrite(des + str(cnt) + "_h.png", hmap)


def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(0, 4832):
        
        makeUnderworlds(src, des, i+1)

        print("*** done creating underworlds for every other " + str(i+1) + " ***")

def main():
    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\bmt_maps_secondbatch/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\bmt_maps_with_underworlds/"

    batch(folderName, destinationFolder)
    
if __name__ == "__main__":
    main()

