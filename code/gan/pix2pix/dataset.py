import numpy as np
import config
import os
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision.utils import save_image


class MapDataset(Dataset):
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.list_files = os.listdir(self.root_dir)

    def __len__(self):
        return len(self.list_files)

    def __getitem__(self, index):
        img_file = self.list_files[index]
        img_path = os.path.join(self.root_dir, img_file)
        image = np.array(Image.open(img_path))
        input_imageRaw = image[:, :128, :]
        #target_image = image[:, 128:, :]

        zero_image = np.zeros((128, 128), dtype=np.uint8)
        input_image = np.dstack((input_imageRaw, zero_image))

        # modify data handler to deal with 4 channels (rgb + height) 
        target_imageB = image[:, 128:256, :]
        target_imageH = image[:, 256:384, :]

        # convert to 1 dimension (dot product) because read as 3d image 
        target_imageH_gray = np.dot(target_imageH[...,:3], [0.299, 0.587, 0.114])

        # add the two images together - now is 4d with rgb + height
        target_image = np.dstack((target_imageB, target_imageH_gray))

        augmentations = config.both_transform(image=input_image, image0=target_image)
        input_image = augmentations["image"]
        target_image = augmentations["image0"]

        input_image = config.transform_only_input(image=input_image)["image"]
        target_image = config.transform_only_mask(image=target_image)["image"]

        return input_image, target_image


if __name__ == "__main__":
    dataset = MapDataset("data/train/")
    loader = DataLoader(dataset, batch_size=5)
    for x, y in loader:
        print(x.shape)
        print(y.shape)
        save_image(x, "x.png")
        save_image(y, "y.png")
        import sys

        sys.exit()