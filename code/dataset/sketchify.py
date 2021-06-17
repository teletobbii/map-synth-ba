import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from glob import glob, has_magic
from PIL import Image

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
def contouring(height_map):
    print("*** Starting contouring ***")   
    print(height_map.shape)

    print(height_map[:,:].size)

    #fig,ax=plt.subplots(1,1)
    #cp = ax.contour(X, Y, Z)
    #plt.show()

    # Using the Sobel filter to figure out the steepness of the gradients of the heightmap
    sobelMap = np.zeros((128,128))
    import time
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
    retval, thresholded = cv.threshold(sobelMap, 115, 255, cv.THRESH_BINARY)
    thresholded.astype(np.uint8)
    
    print("*** Done contouring ***")
    return thresholded



# Creating the traversability map
# Creates a final map matrix with the height, biome and traverse data stored in it
def createTraversibilityMap(height_map, biome_map):
    print("*** Starting creation of traversibility-map ***")

    # Creating the steepness from the heightmap to add to the non traversable biomes
    gradientImage = contouring(height_map)
    #img = Image.fromarray(np.uint8(gradientImage), 'L')
    #img.show()

    biomeColours = {
        1: np.array([254,52,31]),       #water
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
    
    import time
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
    #print("time of loop:" + str(1000 * round((end - start), 5)) + "ms")

    # Filtering out areas of non-traversability that are smaller than 20 pixels
    traversabilityMap = np.array(map[:,:,2], dtype='int16')
    cv.filterSpeckles(traversabilityMap, 0, 35, 255)[0]
    img = Image.fromarray(np.uint8(traversabilityMap), 'L')
    img.show()

    print("*** Done with traversibility-map ***")


def main():
    print("***|| Starting sketchifier ||***")
    
    import time
    start = time.time()
    #reading the two different maps
    hmap = cv.imread(r"C:\Users\tobia\OneDrive\Desktop\BA\data\presketch\1_h.png", cv.IMREAD_GRAYSCALE)
    bmap = cv.imread(r"C:\Users\tobia\OneDrive\Desktop\BA\data\presketch\1_b.png", cv.IMREAD_COLOR)
    readDataTime = time.time()
    print("finished reading the map after " + str(1000 * round((readDataTime - start), 5)) + "ms")

    # inverting the height map to make brighter = taller
    hmap = cv.bitwise_not(hmap)

    #showMaps(hmap,bmap)

    createTraversibilityMap(hmap, bmap)
    
    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")
    print("***|| All done ||***")

if __name__ == "__main__":
    main()
