from os import listdir
from os.path import isfile, join
import rasterio
path_satellite = "/home/jovyan/work/satellite_data/"
all_tif = [f for f in listdir(path_satellite) if isfile(join(path_satellite, f)) and f.endswith('.tif')]
# print(len(all_tif)) # => 342

# furthest west, furthest east = min_x, max_x
# furthest north, furthest south = max_y, min_y

# initialize with first window
filepath = join(path_satellite, all_tif[0])
src_img = rasterio.open(filepath)
satellite_coverage = (min_x, min_y, max_x, max_y) = src_img.bounds
west_img = south_img = east_img = north_img = all_tif[0]

for file in all_tif:
    # get current extend and update coordinate extend, if it exceeds the window
    filepath = join(path_satellite, file)
    src_img = rasterio.open(filepath)
    (west, south, east, north) = src_img.bounds
    # print(filepath, (west, south, east, north))
    if west < min_x: min_x = west; west_img = file
    if east > max_x: max_x = east; east_img = file
    if south < min_y: min_y = south; south_img = file
    if north > max_y: max_y = north; north_img = file

satellite_coverage = (min_x, min_y, max_x, max_y)
print("Satellite Coverage:", satellite_coverage)
print("Edge Files:", west_img, south_img, east_img, north_img)
# Satellite Coverage: (19.995774381181494, -27.00336829746086, 32.901645860560464, -25.996668734922206)
# Edge Files: 2620CC_2013.tif 2623DD_2013.tif 2632DD_2016.tif 2620AA_2013.tif
