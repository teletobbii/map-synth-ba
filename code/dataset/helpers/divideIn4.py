#https://oleksandrg.medium.com/how-to-divide-the-image-into-4-parts-using-opencv-c0afb5cab10c

import cv2
import os
import time

def divideIn4(imgPath, cnt, type, des):
    
    # load image
    img = cv2.imread(imgPath)

    ##########################################
    # At first vertical devide image         #
    ##########################################
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    left1 = img[:, :width_cutoff]
    right1 = img[:, width_cutoff:]
    # finish vertical devide image

    ##########################################
    # At first Horizontal devide left1 image #
    ##########################################
    #rotate image LEFT1 to 90 CLOCKWISE
    img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    l1 = img[:, :width_cutoff]
    l2 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(des + str(cnt*4 - 3) + "_" + str(type) + ".png", l1)
    #rotate image to 90 COUNTERCLOCKWISE
    l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(des + str(cnt*4 - 2) + "_" + str(type) + ".png", l2)
    ##########################################
    # At first Horizontal devide right1 image#
    ##########################################
    #rotate image RIGHT1 to 90 CLOCKWISE
    img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    r1 = img[:, :width_cutoff]
    r2 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    r1 = cv2.rotate(r1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(des + str(cnt*4 - 1) + "_" + str(type) + ".png", r1)
    #rotate image to 90 COUNTERCLOCKWISE
    r2 = cv2.rotate(r2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    cv2.imwrite(des + str(cnt*4) + "_" + str(type) + ".png", r2)

def batch(src, des):

    path, dirs, files = next(os.walk(src))

    for i in range(len(files)):
        divideIn4(src + str(i+1) + "_b.png", i+1, "b", des)
        divideIn4(src + str(i+1) + "_h.png", i+1, "h", des)

        print("*** done contouring map " + str(i+1) + " ***")




def main():
    print("***|| Starting divider ||***")
    start = time.time()

    folderName = r"C:/Users/tobia/BA/dataset/fullsize/bh_256p/"
    destinationFolder = r"C:/Users/tobia/BA/dataset/fullsize/bh_128p/"
    batch(folderName, destinationFolder)
    
    end = time.time()
    print("Done cutting the maps after " + str(1000 * round((end - start), 5)) + "ms")
    print("***|| All done ||***")


if __name__ == "__main__":
    main()
   
