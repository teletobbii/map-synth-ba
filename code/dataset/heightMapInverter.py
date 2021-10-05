import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import time

def invertMap(src, des, cnt):

    hmap = cv.imread(src + str(cnt) + "_h.png", cv.IMREAD_GRAYSCALE)

    # inverting the height map to make brighter = taller
    height_map = cv.bitwise_not(hmap)

    cv.imwrite(des + str(cnt) + "_h.png", height_map)


def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(int(len(files) / 2)):
        
        invertMap(src, des, i+1)

        print("*** done contouring map " + str(i+1) + " ***")


def main():
    print("***|| Starting Inverter ||***")
    
    start = time.time()

    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\bh_128p/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\inverted_h_128p/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")
    print("***|| All done ||***")

if __name__ == "__main__":
    main()