from enum import Enum
import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal
from config import config
config = config.Configuration()

class Channel(Enum):
    GRAYSCALE = 0
    RED = 0
    GREEN = 1
    BLUE = 2

class TiffLoader:
    def __init__(self, path):
        self._dataset = gdal.Open(path, gdal.GA_ReadOnly)
        self._bands = [self._dataset.GetRasterBand(
            x) for x in range(1, self._dataset.RasterCount + 1)]

    def load_rgb(self, x, y, xs, ys):
        r = self.load(Channel.RED, x, y, xs, ys)
        g = self.load(Channel.GREEN, x, y, xs, ys)
        b = self.load(Channel.BLUE, x, y, xs, ys)
        return np.dstack((r, g, b))

    def load(self, channel: Channel, x, y, xs, ys):
        return self._bands[channel.value].ReadAsArray(
            x, y, win_xsize=xs, win_ysize=ys)

def gray_to_rgb(grayscale_img):
    assert len(grayscale_img.shape) == 2
    return np.stack((corrected_labels(grayscale_img),) * 3,
                    axis=-1).astype(np.uint8)

def corrected_labels(labels):
    labels = np.where(labels != 0, 255, 0)
    return labels

def show(data, label):
    plt.imshow(np.hstack((data, gray_to_rgb(label))))
    plt.show()