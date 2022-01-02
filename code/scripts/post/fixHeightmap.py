import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from statistics import median, mode


def showMap(height_map):
    f = plt.figure()
    # matplotlib works with RGB while cv with BGR, so need to convert
    plt.imshow(cv.cvtColor(height_map, cv.COLOR_BGR2RGB), cmap='gray')
    plt.axis('off')
    #plt.show(block=True)


def heightFix():

    generated_heights = cv.imread(r"C:\Users\tobia\BA\DISC\combination/" + "1_h_gen.png", cv.IMREAD_GRAYSCALE)

    bilat = cv.bilateralFilter(generated_heights,3,50,50)
    gauss = cv.GaussianBlur(generated_heights, (5,5),0)

    showMap(bilat)

    #cv.imwrite(r"C:\Users\tobia\BA\map-synth-ba\ba\pic\fixbiomes/" + "heights_overworld_fixed.png", bilat)
    cv.imwrite(r"C:\Users\tobia\BA\DISC\combination/" + "1_h_fixed.png", gauss)


def main():

    heightFix()
    
if __name__ == "__main__":
    main()


