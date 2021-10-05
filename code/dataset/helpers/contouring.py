import numpy as np
import cv2 as cv
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import time

#https://cs.heightmap.skydark.pl/#

def showMap(height_map):
    f = plt.figure()
    # matplotlib works with RGB while cv with BGR, so need to convert
    plt.imshow(cv.cvtColor(height_map, cv.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off')
    plt.show(block=True)


def resizeMap(height_map, dimensions):
    resized = cv.resize(height_map, (dimensions, dimensions))
    return resized

def batch(src, des):

    path, dirs, files = next(os.walk(src))

    for i in range(len(files)):
        hmap = cv.imread(src + "fs (" + str(i+1) + ").png", cv.IMREAD_GRAYSCALE)
        resizedhMap = resizeMap(hmap, 128)
        cv.imwrite(des + str(i+1) + "_h.png", resizedhMap)
        contoured = createContouredMap(resizedhMap)
        cv.imwrite(des + str(i+1) + "_c.png", contoured)

        combined = np.concatenate((contoured, resizedhMap), axis=1)
        cv.imwrite(des + str(i+1) + ".png", combined)

        print("*** done contouring map " + str(i+1) + " ***")


# https://stackoverflow.com/questions/55827778/elevation-xyz-data-to-slope-gradient-map-using-python
# Slope gradients
def createContouredMap(height_map):
    # Using the Sobel filter to figure out the steepness of the gradients of the heightmap
    sobelMap = np.zeros((128,128))
    start = time.time()
    rows = height_map.shape[0]
    columns = height_map.shape[0]
    for i in range(rows-1):
        for j in range(columns-1):
            height = int(height_map[i][j])
            dx = int(height_map[i+1][j]) - height
            dy = int(height_map[i][j+1]) - height
            sobelMap[i][j] = np.sqrt(dx * dx + dy * dy)
    end = time.time()
    #print("time of loop:" + str(1000 * round((end - start), 5)) + "ms")

    sobelMap = cv.normalize(sobelMap, sobelMap, 0, 255, cv.NORM_MINMAX)

    # Displaying only steepness values above 115
    # 110 for original 
    #retval, thresholded = cv.threshold(sobelMap, 110, 255, cv.THRESH_BINARY)
    # 70 for generated
    retval, thresholded = cv.threshold(sobelMap, 75, 255, cv.THRESH_BINARY)
    
    # Filtering out areas of non-traversability that are smaller than 45 pixel to get rid of speckles
    thresholdedPatched = np.array(thresholded, dtype='int16')
    cv.filterSpeckles(thresholdedPatched, 0, 45, 255)[0]

    thresholdedPatched.astype(np.uint8)
    return thresholdedPatched

def single():

    folderName = r"C:/Users/tobia\OneDrive\Desktop\show\15_9\2.5/"
    
    hmap = cv.imread(folderName + "91_h.png", cv.IMREAD_GRAYSCALE)

    contoured = createContouredMap(hmap)

    # create kernel
    kernel = np.ones((5,5), np.uint8)
    thresholdedDilated = cv.dilate(contoured, kernel)

    thresholdedEroded = cv.erode(thresholdedDilated, kernel)


    cv.imwrite(folderName + "91_h_trav.png", thresholdedEroded)






def main():
    print("***|| Starting traversifier ||***")
    start = time.time()

    folderName = r"C:/Users/tobia/BA/map-synth-ba/dataset/b4/"
    destinationFolder = r"C:/Users/tobia/BA/map-synth-ba/dataset/after/"
    #batch(folderName, destinationFolder)
    
    single()

    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")
    print("***|| All done ||***")
if __name__ == "__main__":
    main()
