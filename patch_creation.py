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


def gray_to_rgb(grayscale_img):
    assert len(grayscale_img.shape) == 2
    return np.stack((corrected_labels(grayscale_img),) * 3, axis=-1).astype(np.uint8)


def corrected_labels(labels):
    """
    Make all values of the array which are not 0, 1. Either label or no label.
    This has to be performed, because the exported labels have color values, which have to be normalized.
    Somehow, some color values have been above 255, which might have happened due to a faulty export from QGIS.
    patches_labels_training = [patch==1.0 if patch != 0.0 else 0.0 for patch in patches_labels]
    """
    labels = np.where(labels != 0, 255, 0)
    return labels


def show(data, label):
    plt.imshow(np.hstack((data, gray_to_rgb(label))))
    plt.show()


def main():
    data_loader = TiffLoader(config.filepath_satellite_nw)
    label_loader = TiffLoader(config.filepath_label_nw)
    step_size = config.size

    x_size, y_size = data_loader.size

    x_offset = 0
    y_offset = 0
    satellite_patches, label_patches = [], []
    while y_offset + step_size < y_size:
        while x_offset + step_size < x_size:
            data = data_loader.load_rgb(
                x_offset, y_offset, step_size, step_size)
            label = corrected_labels(label_loader.load(
                Channel.GRAYSCALE, x_offset, y_offset, step_size, step_size))

            satellite_patches.append(data)
            label_patches.append(label)

            # horizontal augmentation
            satellite_patches.append(np.fliplr(data))
            label_patches.append(np.fliplr(label))

            # vertical augmentation
            satellite_patches.append(data[::-1])
            label_patches.append(label[::-1])

            # horizontal & vertical augmentation
            satellite_patches.append(np.fliplr(data[::-1]))
            label_patches.append(np.fliplr(label[::-1]))

            x_offset += step_size - config.overlap
        x_offset = 0
        y_offset += step_size - config.overlap

    np.save(config.path_patches_satellite, satellite_patches)
    np.save(config.path_patches_labels, label_patches)


if __name__ == '__main__':
    main()
