import numpy as np
import rasterio
from rasterio.plot import show
from rasterio.windows import from_bounds
import patchify
from config import UNetTraining
config = UNetTraining.Configuration()

# 1. patch creation
opened_label_areas = [
    rasterio.open(config.filepath_label_nw),
    rasterio.open(config.filepath_label_se)]
# 1.1 label patches
patches_labels = []
for label_area in opened_label_areas:
    (w, s, e, n) = label_area.bounds
    label_area = label_area.read(1, 
        window = from_bounds(w, s, e, n, label_area.transform))

    cur_patches = patchify(label_area, 
        (config.patch_size[0], config.patch_size[1]), 
        step=config.patch_size[0]-config.overlap)
    reshaped_patches = np.reshape(cur_patches, 
        (cur_patches.shape[0]*cur_patches.shape[1], 
        cur_patches.shape[2], cur_patches.shape[3])) 
        # = (#patches, 256, 256)
    patches_labels.extend(reshaped_patches)
print("Mask/Label Patch Shape:", len(patches_labels))

