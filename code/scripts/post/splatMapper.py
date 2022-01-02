import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from statistics import mode
import random

def showMap(height_map):
    f = plt.figure()
    # matplotlib works with RGB while cv with BGR, so need to convert
    plt.imshow(cv.cvtColor(height_map, cv.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off')
    plt.show(block=True)

# create the two splatmaps from the generated and post processed biome maps

def colourFix():
    generated_biomes = cv.imread(r"C:\Users\tobia\OneDrive\Desktop\show\22_10\1_waterfix\post_more_data/" + "2_biomes_fixed.png", cv.IMREAD_COLOR)

    biomeColours = {
        1: np.array([255,52,35]),       #water
        2: np.array([153, 255, 156]),   #sand
        3: np.array([138, 176, 200]),   #forest
        4: np.array([0, 80, 120]),      #grass
        5: np.array([0, 94, 61]),       #steppe
        6: np.array([14, 233, 182]),    #mountain
        7: np.array([255, 255, 255])     #peak
    }

    mask1 = np.zeros([128, 128, 4], dtype=np.uint8)
    mask2 = np.zeros([128, 128, 4], dtype=np.uint8)


    rows = generated_biomes.shape[0]
    columns = generated_biomes.shape[0]
    for i in range(rows-1):
        for j in range(columns-1):
            if (generated_biomes[i][j] == biomeColours[1]).all():
                mask1[i][j] = (255, 0, 0, 0)
            elif (generated_biomes[i][j] == biomeColours[2]).all():
                mask1[i,j] = (0, 255, 0, 0)
            elif (generated_biomes[i][j] == biomeColours[3]).all():
                mask1[i,j] = (0, 0, 255, 0)
            elif (generated_biomes[i][j] == biomeColours[4]).all():
                mask1[i,j] = (0, 0, 0, 255)
            elif (generated_biomes[i][j] == biomeColours[5]).all():
                mask2[i,j] = (255, 0, 0, 0)
            elif (generated_biomes[i][j] == biomeColours[6]).all():
                mask2[i,j] = (0, 255, 0, 0)
            elif (generated_biomes[i][j] == biomeColours[7]).all():
                mask2[i,j] = (0, 0, 255, 0)

    img1 = Image.fromarray(mask1)
    img1.save(r"C:\Users\tobia\OneDrive\Desktop\show\22_10\1_waterfix\post_more_data/" + "mask1.png")
    img2 = Image.fromarray(mask2)
    img2.save(r"C:\Users\tobia\OneDrive\Desktop\show\22_10\1_waterfix\post_more_data/" + "mask2.png")

    cv.imwrite(r"C:\Users\tobia\OneDrive\Desktop\show\22_10\1_waterfix\post_more_data/" + "masked1.png", mask1)
    cv.imwrite(r"C:\Users\tobia\OneDrive\Desktop\show\22_10\1_waterfix\post_more_data/" + "masked2.png", mask2)

def main():

    colourFix()
    
if __name__ == "__main__":
    main()

