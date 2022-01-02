import cv2 as cv
import time

# draw sketch in online app Photopea
# export from photopea -> will be 8 bitdepth
# need 24 bit
# this will convert to 24 which then can be used for training / predicting

def fixBitDepth():

    maps = cv.imread(r"C:\Users\tobia\BA\map-synth-ba\code\gan\pix2pix\data\val/" + "testmix2.png", cv.IMREAD_COLOR)
    
    rows = maps.shape[0]
    columns = maps.shape[1]
    print(columns)
    maxHeight = 0
    for i in range(rows-1):
        for j in range(columns-1):
            if (j > 128):
                maps[i][j] = [255, 255, 255]

    cv.imwrite(r"C:\Users\tobia\BA\map-synth-ba\code\gan\pix2pix\data\val/" + "2.png", maps)

def main():
    print("***|| Starting Test File Maker ||***")
    
    start = time.time()
    fixBitDepth()
    
    end = time.time()
    print("***|| All done ||***")

if __name__ == "__main__":
    main()