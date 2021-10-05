import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import time


def batch(src, des):

    path, dirs, files = next(os.walk(src))

    for i in range(int(len(files) / 3)):

        hmap = cv.imread(src + str(i+1) + "_h.png", cv.IMREAD_GRAYSCALE)
        bmap = cv.imread(src + str(i+1) + "_b.png", cv.IMREAD_COLOR)
        tmap = cv.imread(src + str(i+1) + "_t.png", cv.IMREAD_GRAYSCALE)
        #blurredBmaps = cv.imread(src + str(i+1) + "_bs.png", cv.IMREAD_COLOR)

        tmapc = cv.cvtColor(tmap,cv.COLOR_GRAY2BGR) # gotta convert gray to colour so they can be stacked together
        hmapc = cv.cvtColor(hmap,cv.COLOR_GRAY2BGR)

        
        combined = np.concatenate((tmapc, bmap), axis=1)
        combined2 = np.concatenate((combined, hmapc), axis=1)
        cv.imwrite(des + str(i+1) + ".png", combined)

        print("*** done combining map " + str(i+1) + " ***")


def main():
    print("***|| Starting traversifier ||***")
    start = time.time()

    folderName = "C:/Users/tobia/BA/map-synth-ba/dataset/new/notReady/bmt_maps/"
    destinationFolder = "C:/Users/tobia/BA/map-synth-ba/dataset/new/ready/t2bh_data/"

    batch(folderName, destinationFolder)

    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")

if __name__ == "__main__":
    main()
