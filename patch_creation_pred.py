from enum import Enum

import numpy as np
from matplotlib import pyplot as plt
from osgeo import gdal

from config import config

config = config.Configuration()


class Channel(Enum):
    RED = 0
    GREEN = 1
    BLUE = 2


class TiffLoader:
    def __init__(self, path):
        self._dataset = gdal.Open(path, gdal.GA_ReadOnly)
        self._bands = [self._dataset.GetRasterBand(
            x) for x in range(1, self._dataset.RasterCount + 1)]

    @property
    def size(self) -> (int, int):
        return self._dataset.RasterXSize, self._dataset.RasterYSize

    def print_details(self):
        print(
            f"Driver: {self._dataset.GetDriver().ShortName}/{self._dataset.GetDriver().LongName}")
        print(
            f"Size is {self._dataset.RasterXSize} x {self._dataset.RasterYSize} x {self._dataset.RasterCount}")
        print(f"Projection is {self._dataset.GetProjection()}")
        geo_transform = self._dataset.GetGeoTransform()
        if geo_transform:
            print(f"Origin = ({geo_transform[0]}, {geo_transform[3]})")
            print(f"Pixel Size = ({geo_transform[1]}, {geo_transform[5]})")

    def load_rgb(self, x, y, xs, ys):
        r = self.load(Channel.RED, x, y, xs, ys)
        g = self.load(Channel.GREEN, x, y, xs, ys)
        b = self.load(Channel.BLUE, x, y, xs, ys)

        return np.dstack((r, g, b))

    def load(self, channel: Channel, x, y, xs, ys):
        return self._bands[channel.value].ReadAsArray(x, y, win_xsize=xs, win_ysize=ys)


def scale_data(data):
    return [patch/255 for patch in data]


def main():
    # for filename in config.pred_imgs:
    filename = config.pred_imgs[0]
    data_loader = TiffLoader(config.path_satellite + filename)
    step_size = config.size

    x_size, y_size = data_loader.size

    x_offset = 0
    y_offset = 0
    satellite_patches = []
    while y_offset + step_size <= y_size: #min(y_size, 7500):
        while x_offset + step_size <= x_size: #min(x_size, 7500):
            data = data_loader.load_rgb(
                x_offset, y_offset, step_size, step_size)
            # plt.imshow(data)
            # plt.show()

            satellite_patches.append(np.divide(data, 255))

            x_offset += step_size - config.overlap
        x_offset = 0
        y_offset += step_size - config.overlap

    np.save(
        f"{config.path_patches}pred_patches_{filename[:-4]}.npy", satellite_patches)


if __name__ == '__main__':
    main()
