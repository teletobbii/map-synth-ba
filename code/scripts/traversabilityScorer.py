import numpy as np
import os
import cv2 as cv
import matplotlib.pyplot as plt
import time

# evaluate the Traversability score of the ground truth map as well as the actual traversability-map that has
# been created from the generated samples 

def createTraversibilityMap(src, cnt):
    generated_trav = cv.imread(src + str(cnt) + "_t.png", cv.IMREAD_COLOR)
    original_trav = cv.imread(src + str(cnt) + "_input.png", cv.IMREAD_COLOR)

    rows = generated_trav.shape[0]
    columns = generated_trav.shape[0]

    maxscore = rows*columns
    matched = 0.0
    traversable = 0.0
    nonTraversable = 0.0
    maxTraversable = 0
    maxNonTraversable = 0
    for i in range(rows):
        for j in range(columns):
            if ((original_trav[i][j] == np.array([0, 165, 255])).all()):
                maxTraversable = maxTraversable + 1
            else:
                maxNonTraversable = maxNonTraversable + 1
            if ((generated_trav[i][j] == np.array([0, 165, 255])).all() and (original_trav[i][j] == np.array([0, 165, 255])).all()):
                traversable = traversable + 1
            elif ((generated_trav[i][j] == np.array([255, 0, 0])).all() and (original_trav[i][j] == np.array([255, 0, 0])).all()):
                nonTraversable = nonTraversable + 1    
                
            if ((generated_trav[i][j] == original_trav[i][j]).all()):
                matched = matched + 1

    print(matched)
    score =  matched / maxscore

    orangescore =  traversable / maxTraversable
    bluescore =  nonTraversable / maxNonTraversable

    avg = (orangescore + bluescore*2) / 3

    print("Map " + str(cnt) + " has a total score of: " + str(score))
    print("Map " + str(cnt) + " has a orange score of: " + str(orangescore))
    print("Map " + str(cnt) + " has a orange score of: " + str(bluescore))
    print("Map " + str(cnt) + " has an average score of: " + str(avg))


def batch(src):
    path, dirs, files = next(os.walk(src))

    for i in range(0, 7):    
        createTraversibilityMap(src, i+1)


def main():
    print("***|| Starting sketchifier ||***")
    start = time.time()

    folderName = r"C:\Users\tobia\BA\DISC\useability\traversed/"
    batch(folderName)
    
    end = time.time()
    print("Done creating the maps after " + str(1000 * round((end - start), 5)) + "ms")

if __name__ == "__main__":
    main()