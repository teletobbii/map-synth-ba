from PIL import Image
import os

path = r"C:\Users\tobia\BA\GAN\pix2pix_yt\data\test/"
pathToSave = r"C:\Users\tobia\BA\GAN\pix2pix_yt\data\test/"

resize_ratio = 4.6875  # where 0.5 is half size, 2 is double size

def resize_aspect_fit():
    dirs = os.listdir(path)
    n = 1
    for item in dirs:
        if item == '.jpg':
            continue
        if os.path.isfile(path+item):
            image = Image.open(path+item)
            file_path, extension = os.path.splitext(path+item)

            new_image_height = int(image.size[0] / (1/resize_ratio))
            new_image_length = int(image.size[1] / (1/resize_ratio))

            image = image.resize((new_image_height, new_image_length), Image.ANTIALIAS)
            image.save(pathToSave + str(n) + extension, 'JPEG', quality=90)
        n = n + 1


resize_aspect_fit()