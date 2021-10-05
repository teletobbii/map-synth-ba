from contouring import showMap
import cv2 as cv
import os
import time
import numpy as np

def batch(src, des):

    # create kernel
    kernel = np.ones((3,2), np.uint8)

    path, dirs, files = next(os.walk(src))

    for i in range(int(len(files) / 3)):

        bmap = cv.imread(src + str(i+1) + "_b.png", cv.IMREAD_COLOR)
        

        # apply morphology open to smooth the outline https://stackoverflow.com/questions/60016168/how-to-implement-a-photoshop-like-effect-oilpaint-effect-in-opencv
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (6,6))
        morph = cv.morphologyEx(bmap, cv.MORPH_OPEN, kernel)

        # brighten dark regions (not really necessary here)
        #result = cv.normalize(morph,None, 0,255,cv.NORM_MINMAX)

        bmapSketched = cv.blur(morph,(4,4)) 

        cv.imwrite(des + str(i+1) + "_bs.png", bmapSketched)


def main():
    print("***|| Starting traversifier ||***")
    start = time.time()

    folderName = "C:/Users/tobia/BA/dataset/notReady/bmt_maps/"
    destinationFolder = "C:/Users/tobia/BA/dataset/notReady/singles/sketched_b_maps/"

    batch(folderName, destinationFolder)

    end = time.time()
    print("***|| All done ||***")

if __name__ == "__main__":
    main()
