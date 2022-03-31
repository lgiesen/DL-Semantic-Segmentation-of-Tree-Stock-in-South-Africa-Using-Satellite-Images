import geopandas as gpd
import json
import rasterio
from rasterio.windows import from_bounds
from rasterio.plot import show
from osgeo import gdal
from config import UNetTraining
config = UNetTraining.Configuration()
labels_bb = gpd.read_file(config.filepath_labels_bounding_boxes)
# get polygon coordinates 
g = json.loads(labels_bb.to_json())
coords = [
    g['features'][polygon]['geometry']['coordinates'][0]
    for polygon in range(len(g))]
# visualize labels
src_label = rasterio.open(config.filepath_label)
label_file = gdal.Open(config.filepath_label)
labels = coord_labels_bb = filepath_labeled_areas = []
for polygon in range(len(g)):
    west, south = coords[polygon][0][0], coords[polygon][0][1]
    east, north = coords[polygon][2][0], coords[polygon][2][1]
    coord_labels_bb.append((west, south, east, north))
    # labels
    print(polygon, ":", coord_labels_bb[polygon])
    labels.append(src_label.read(1, window = 
        from_bounds(west, south, east, north, src_label.transform)))
    show(labels[polygon])
    # satellite
    filepath_labeled_area = (f'{config.path_labeled_data_areas}\
        labeled_areas_extracted_by_code/label-area-{str(polygon)}.tif')
    filepath_labeled_areas.append(filepath_labeled_area)
    cropped_window = (west,north,east,south)
    print(filepath_labeled_area, cropped_window)
    gdal.Translate(filepath_labeled_area, label_file, 
        projWin = cropped_window)
