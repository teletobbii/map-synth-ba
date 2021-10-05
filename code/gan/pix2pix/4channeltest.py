from discriminator_model import test
import numpy as np
import config
import os
import cv2 as cv
from PIL import Image
from matplotlib import pyplot as plt
import torch



def make4channel():

    img_path = r"C:\Users\tobia\BA\dataset\readyDataFolders\t2bh_data\1.png"
    image = np.array(Image.open(img_path))
    input_image = image[:, :128, :]
    target_image1 = image[:, 128:256, :]
    target_image2 = image[:, 256:384, :]

    target_image2_gray = np.dot(target_image2[...,:3], [0.299, 0.587, 0.114])

    #target_image1 = target_image1[..., np.newaxis]  
    #mega = np.concatenate((target_image1, target_image2_gray), axis=3)

    mega = np.dstack((target_image1, target_image2_gray))

    # NACH NPDSTACK: mega[:,:,3:] ist die HEATMAP (?????)
    # und mega[:,:,:3] is die Biommap!

    #print(target_image1.shape)
    #print(target_image2_gray.shape)
    #print(mega.shape)
    #print(mega)
    #print(mega[:,:,3:])
    


    #plt.imshow(mega[:,:,:3], interpolation='nearest')
    #plt.show()
    #cv.imwrite(r"C:\Users\tobia\OneDrive\Desktop\test\mega2.png", mega[:,:,3:])

    test_zeros = np.zeros((128, 128))
    #print(test_zeros.shape)

    return mega


def learning_tensors(np_array):
    #x_np = torch.from_numpy(np_array)
    #print(x_np.shape)

    test = torch.rand([1, 4, 5, 5])
    print(test.shape)
    print(test[:,:3].shape)
    print(test[:,:3])
    print(test[:,3:].shape)
    print(test[:,3:])



def make3image():
    img1_path = r"C:\Users\tobia\BA\GAN\pix2pix_yt\data\4channel\1.png"
    img2_path = r"C:\Users\tobia\BA\GAN\pix2pix_yt\data\4channel\1_h.png"
    image = np.array(Image.open(img1_path))
    imageH = np.array(Image.open(img2_path))
    concatted = cv.hconcat([image, imageH])

    cv.imwrite(r"C:\Users\tobia\BA\GAN\pix2pix_yt\data\4channel\savedImage.png", concatted)

    print("done make 3 images")


def main():
    #make3image()
    nparr = make4channel()
    learning_tensors(nparr)



if __name__ == "__main__":
    main()
