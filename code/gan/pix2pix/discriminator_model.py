import torch
import torch.nn as nn

class CNNBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=2):
        super(CNNBlock, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(
                in_channels, out_channels, 4, stride, 1, bias=False, padding_mode="reflect"
            ),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.2),
        )

    def forward(self, x):
        return self.conv(x)


class Discriminator(nn.Module):
    # 3 channels bc rgb -> will be changed to 2 because were gonna have height and biome as our channels ?
    # or 1 because we only have the black and white traverse map as input
    #
    # the features are what were going to use for the CNN block
    # the initial bblock will be a nn.sequential, no batch block here but just a conv2d
    def __init__(self, in_channels=4, features=[32, 64, 128, 256]):
        super().__init__()
        self.initial = nn.Sequential(
            nn.Conv2d(
                # in channels times 2 because we send in x and y
                in_channels * 2,
                features[0],
                kernel_size=4,
                stride=2,
                padding=1,
                padding_mode="reflect",
            ),
            nn.LeakyReLU(0.2),
        )

        layers = []
        in_channels = features[0]
        for feature in features[1:]:
            layers.append(
                CNNBlock(in_channels, feature, stride=1 if feature == features[-1] else 2),
            )
            in_channels = feature

        layers.append(
            nn.Conv2d(
                in_channels, 1, kernel_size=4, stride=1, padding=1, padding_mode="reflect"
            ),
        )

        self.model = nn.Sequential(*layers)

    # for forward we'll get self and a x and y as input, y either fake or real
    def forward(self, x, y):
        x = torch.cat([x, y], dim=1)
        x = self.initial(x)
        x = self.model(x)
        return x


def test():
    x = torch.randn((1, 3, 128, 128))
    y = torch.randn((1, 4, 128, 128))
    #model = Discriminator(in_channels=4)
    #preds = model(x, y)
    #print(preds.shape)

if __name__ == "__main__":
    test()