import rasterio
from rasterio.plot import show
from rasterio.windows import from_bounds, Window
from config import UNetTraining
config = UNetTraining.Configuration()
img = rasterio.open(config.filepath_label_compressed)
# 1. inspect image
# get bounding box coordinates, resolution and size of image
img_info = (img.bounds, img.res, img.width, img.height)
print(img_info)
# 2. windowed reading
start_x = start_y = steps_x = steps_y = 512
img_cutout_steps = img.read(None, 
    window=Window(start_x,start_y,steps_x,steps_y))
show(img_cutout_steps)
west, south = 29.74801671786931, -26.24955085491147
east, north = 29.74923159879657, -26.248335973984698
img_cutout_coord = img.read(None, 
    window=from_bounds(west, south, east, north, img.transform))
show(img_cutout_coord)
