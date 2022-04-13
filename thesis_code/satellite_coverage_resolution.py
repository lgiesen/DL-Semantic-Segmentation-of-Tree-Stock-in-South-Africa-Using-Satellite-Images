from os import listdir
from os.path import isfile, join
import rasterio

path_satellite = "/home/jovyan/work/satellite_data/"
all_tif = [f for f in listdir(path_satellite)
           if isfile(join(path_satellite, f)) and f.endswith('.tif')]
# furthest west, furthest east = min_x, max_x
# furthest north, furthest south = max_y, min_y
# initialize with first window
filepath = join(path_satellite, all_tif[0])
src_img = rasterio.open(filepath)
(min_x, min_y, max_x, max_y) = src_img.bounds
west_img = south_img = east_img = north_img = all_tif[0]
xRes, yRes = src_img.res
min_res, max_res = xRes, xRes
# update coordinate extend, if cur extend exceeds the window
for file in all_tif:
    filepath = join(path_satellite, file)
    src_img = rasterio.open(filepath)
    # bounds
    (west, south, east, north) = src_img.bounds
    if west < min_x:    min_x = west;    west_img = file
    if east > max_x:    max_x = east;    east_img = file
    if south < min_y:   min_y = south;   south_img = file
    if north > max_y:   max_y = north;   north_img = file
    # resolution
    xRes, yRes = src_img.res
    if min_res > xRes:  min_res = xRes;  min_res_img = file
    elif max_res < xRes:max_res = xRes;  max_res_img = file

satellite_coverage = (min_x, min_y, max_x, max_y)

def get_res(filename):
    src_img = rasterio.open(path_satellite + filename)
    return src_img.res

print("Satellite Coverage:", satellite_coverage)
print("Edge Files:", west_img, south_img, east_img, north_img)
print(f"Resolution Range: {min_res_img}: {get_res(min_res_img)}")
print(f"{max_res_img}: {get_res(max_res_img)}")
