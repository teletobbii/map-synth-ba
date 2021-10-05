import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import time

# https://stackoverflow.com/questions/55827778/elevation-xyz-data-to-slope-gradient-map-using-python
def createContouredMap(height_map):
    # Using the Sobel filter to figure out the steepness of the gradients of the heightmap
    sobelMap = np.zeros((128,128))
    rows = height_map.shape[0]
    columns = height_map.shape[0]
    for i in range(rows-1):
        for j in range(columns-1):
            height = int(height_map[i][j])
            dx = int(height_map[i+1][j]) - height
            dy = int(height_map[i][j+1]) - height
            sobelMap[i][j] = np.sqrt(dx * dx + dy * dy)
    end = time.time()

    sobelMap = cv.normalize(sobelMap, sobelMap, 0, 255, cv.NORM_MINMAX)

    # Displaying only steepness values above 110
    retval, thresholded = cv.threshold(sobelMap, 110, 255, cv.THRESH_BINARY)
    
    # Filtering out areas of non-traversability that are smaller than 50 pixel to get rid of speckles
    thresholdedPatched = np.array(thresholded, dtype='int16')
    cv.filterSpeckles(thresholdedPatched, 0, 45, 255)[0]

    thresholdedPatched.astype(np.uint8)

    kernel = np.ones((5,5), np.uint8)
    thresholdedDilated = cv.dilate(thresholdedPatched, kernel)
    thresholdedEroded = cv.erode(thresholdedDilated, kernel)

    return thresholdedEroded


def createTraversibilityMap(src, des, cnt):
    height_map = cv.imread(src + str(cnt) + "_h.png", cv.IMREAD_GRAYSCALE)
    biome_map = cv.imread(src + str(cnt) + "_b.png", cv.IMREAD_COLOR)

    gradientImage = createContouredMap(height_map)

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([118, 104, 98])     #peak
    }

    map = np.zeros((128,128))
    
    # Filling the map with white for where it is either inpassible terrain or too steep
    rows = biome_map.shape[0]
    columns = biome_map.shape[0]
    for i in range(rows):
        for j in range(columns):
            if ((biome_map[i][j] == biomeColours[1]).all()) or ((biome_map[i][j] == biomeColours[6]).all()) or ((biome_map[i][j] == biomeColours[7]).all()):
                map[i][j] = 255
            map[i][j] = map[i][j] + gradientImage[i][j]

    traversabilityMap = np.array(map[:,:], dtype='int16')
    
    cv.imwrite(des + str(cnt) + "_t.png", traversabilityMap)


def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(int(len(files) / 2)):    
        createTraversibilityMap(src, des, i+1)


def main():
    print("***|| Starting sketchifier ||***")
    start = time.time()

    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\inverted_h_128p/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\test/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")

if __name__ == "__main__":
    main()