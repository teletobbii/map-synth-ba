import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image
import time


# Just to display the height and biome map after reading it
def showMaps(height_map, biome_map):
    f = plt.figure()
    f.add_subplot(1,2, 1)
    # need to flip heightmap for some reason
    flipped_height_map = cv.flip(height_map, 1)
    # matplotlib works with RGB while cv with BGR, so need to convert
    plt.imshow(cv.cvtColor(height_map, cv.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off')
    f.add_subplot(1,2, 2)
    plt.imshow(cv.cvtColor(biome_map, cv.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show(block=True)


# https://stackoverflow.com/questions/55827778/elevation-xyz-data-to-slope-gradient-map-using-python
# Slope gradients
def createContouredMap(height_map):
    #print("*** Starting contouring ***")   

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

    # Displaying only steepness values above 110
    retval, thresholded = cv.threshold(sobelMap, 110, 255, cv.THRESH_BINARY)
    
    # Filtering out areas of non-traversability that are smaller than 50 pixel to get rid of speckles
    thresholdedPatched = np.array(thresholded, dtype='int16')
    cv.filterSpeckles(thresholdedPatched, 0, 45, 255)[0]

    thresholdedPatched.astype(np.uint8)

    kernel = np.ones((5,5), np.uint8)
    thresholdedDilated = cv.dilate(thresholdedPatched, kernel)

    thresholdedEroded = cv.erode(thresholdedDilated, kernel)


    #print("*** Done contouring ***")
    return thresholdedEroded

# Creating the traversability map
# Creates a final map matrix with the height, biome and traverse data stored in it
def createTraversibilityMap(src, des, cnt):
    #print("*** Starting creation of traversibility-map ***")

    #reading the two different maps
    hmap = cv.imread(src + str(cnt) + "_h.png", cv.IMREAD_GRAYSCALE)
    biome_map = cv.imread(src + str(cnt) + "_b.png", cv.IMREAD_COLOR)
    readDataTime = time.time()

    # inverting the height map to make brighter = taller
    height_map = cv.bitwise_not(hmap)

    # Creating the steepness from the heightmap to add to the non traversable biomes
    gradientImage = createContouredMap(height_map)

    img = Image.fromarray(np.uint8(gradientImage), 'L')
    #img.show()

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([118, 104, 98])     #peak
    }

    # Matrix that stores the biome and height value for each point
    map = np.zeros((128,128,3))
    # Get just the biome -> (map[:,:,0]) or just the biome map -> (map[:,:,1]) or just the traverse map -> (map[:,:,2]) 
    
    start = time.time()
    rows = biome_map.shape[0]
    columns = biome_map.shape[0]
    for i in range(rows):
        for j in range(columns):
            # Copying the height data
            map[i][j][0] = height_map[i][j]
            # Copying the biome / traverse data
            if((biome_map[i][j] == biomeColours[1]).all()):
                map[i][j][1] = 1
                map[i][j][2] = 255
            elif((biome_map[i][j] == biomeColours[2]).all()):
                map[i][j][1] = 2
            elif((biome_map[i][j] == biomeColours[3]).all()):
                map[i][j][1] = 3
            elif((biome_map[i][j] == biomeColours[4]).all()):
                map[i][j][1] = 4
            elif((biome_map[i][j] == biomeColours[5]).all()):
                map[i][j][1] = 5
            elif((biome_map[i][j] == biomeColours[6]).all()):
                map[i][j][1] = 6
                map[i][j][2] = 255
            else: 
                map[i][j][1] = 7
                map[i][j][2] = 255
            map[i][j][2] = map[i][j][2] + gradientImage[i][j]
    end = time.time()

    traversabilityMap = np.array(map[:,:,2], dtype='int16')
    
    #img = Image.fromarray(np.uint8(traversabilityMap), 'L')
    #traversabilityMap.show()
    
    cv.imwrite(des + str(cnt) + "_t.png", traversabilityMap)

    #print("*** Done with traversibility-map ***")


def batch(src, des):
    path, dirs, files = next(os.walk(src))

    for i in range(int(len(files) / 2)):
        
        createTraversibilityMap(src, des, i+1)

        print("*** done contouring map " + str(i+1) + " ***")

def main():
    print("***|| Starting sketchifier ||***")
    start = time.time()

    folderName = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\inverted_h_128p/"
    destinationFolder = r"C:\Users\tobia\BA\map-synth-ba\dataset\new\notReady\rawFullsize\test/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")
    print("***|| All done ||***")

if __name__ == "__main__":
    main()
