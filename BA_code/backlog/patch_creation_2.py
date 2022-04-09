# 1.2 satellite patches
satellite_img = rasterio.open(config.filepath_satellite)
patches_satellite = []
for index, label_area in enumerate(label_area):
    # get coordinates
    (w, s, e, n) = label_area[index].bounds    
    satellite_area = satellite_img.read(None, 
        window = from_bounds(w, s, e, n, satellite_img.transform))
    filename = label_area[0].name\
        .replace(config.path_labeled_data_areas,"")[6:-4] 
    # -4 to cut off the .tif file extension and 6 to cut off label

    cur_patches = patchify(satellite_area, 
        config.input_shape[::-1], 
        step=config.patch_size[0]-config.overlap)[0]
    reshaped_patches = np.reshape(cur_patches, 
        (cur_patches.shape[0]*cur_patches.shape[1], 
        cur_patches.shape[2], cur_patches.shape[3], cur_patches.shape[3]))
        # = (#patches, 3, 256, 256)
    patches_satellite.extend(reshaped_patches)
print("Satellite Patch Shape:", len(patches_satellite))

# 2. manual loop over image
src_label = rasterio.open(config.filepath_label)
def compare_satellite_label():
    left, top = satellite_img.bounds[0], satellite_img.bounds[3] 
    # right and bottom analog in bounds
    patch_size = config.patch_size[0]
    xRes, yRes = satellite_img.res 
    # or: src.meta['transform'][0], -src.meta['transform'][4]    
    x_cutout_max  = int(satellite_img.width / patch_size)
    y_cutout_max = int(satellite_img.height / patch_size)
    for y_cutout in range(y_cutout_max):
        for x_cutout in range(x_cutout_max):
            right  = left + patch_size * xRes 
            bottom = top  - patch_size * yRes

            print("X: {}, Y: {}".format(x_cutout, y_cutout))
            print("({}, {}, {}, {})".format(left, top, right, bottom)) #Cutout Window: 
            print("Size of cutout window in px: {} x {}".format(
                round((right - left) / xRes), round((top - bottom) / yRes)))
            cutout_satellite = satellite_img.read(1, 
                window = from_bounds(left, bottom, right, top, satellite_img.transform))
            cutout_label = src_label.read(1, 
                window = from_bounds(left, bottom, right, top, src_label.transform))
            
            show(cutout_satellite)
            show(cutout_label)
            
            # adjust cutout window for next iteration (with 32 px overlap to cover trees on the edge)
            # adjust cutout window on the x-axis => move cutout window to the right - the overlap
            left = right - config.overlap * xRes # use right as a base and move left by the overlap  
            right  = left + patch_size * xRes # move patch_size to the right from left # += patch_size * xRes
        # reset the x-axis
        left = satellite_img.bounds[0]
        right  = left + patch_size * xRes
        # adjust cutout window on the y-axis => move cutout window to the bottom
        top = bottom - config.overlap * yRes
        bottom = top - patch_size * yRes
