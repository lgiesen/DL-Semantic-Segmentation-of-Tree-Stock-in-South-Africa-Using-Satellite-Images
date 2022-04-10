def load_cutout(satellite, label):
    # file =  rasterio.open(complete_filepath)
    filepath_satellite, filepath_label = path_satellite + satellite, path_labels + label
    # check if filepath exists
    if not os.path.isfile(filepath_satellite):
        print(
            f"{colors.FAIL}1 Failure: File(s) do(es) not exist: {filepath_satellite}{colors.ENDC}")
        return
    elif not os.path.isfile(filepath_label):
        print(
            f"{colors.FAIL}1 Failure: File(s) do(es) not exist: {filepath_label}{colors.ENDC}")
        return

    src_label = rasterio.open(filepath_label)
    src_satellite = rasterio.open(filepath_satellite)

    left, top = src_satellite.bounds[0], src_satellite.bounds[3]
    patch_size = config.patch_size[0]
    overlap = config.overlap  # similar to previous project: 0.12 * 256 = 30.72
    # or: src.meta['transform'][0], -src.meta['transform'][4]
    xRes, yRes = src_satellite.res
    x_cutout_max, y_cutout_max = int(
        src_satellite.width / patch_size), int(src_satellite.height / patch_size)
    # print("max cutout:", x_cutout_max, y_cutout_max)

    # tmp testing
    x_cutout_max = 3
    y_cutout_max = 3
    # skip first row, because no data there
    # left, top, right, bottom = 29.748021463931796, -26.24839922837354, 29.74923634485858, -26.249614109300325
    # left, top = 29.761112169, -26.262076578039085

    for y_cutout in range(y_cutout_max):
        for x_cutout in range(x_cutout_max):

            right = left + patch_size * xRes
            bottom = top - patch_size * yRes

            print("X: {}, Y: {}".format(x_cutout, y_cutout))
            print("Cutout Window: ({}, {}, {}, {})".format(
                left, top, right, bottom))
            # print("Size of cutout window in px: {} x {}".format(round((right - left) / xRes), round((top - bottom) / yRes)))

            cutout_satellite = src_satellite.read(None, window=from_bounds(
                left, bottom, right, top, src_satellite.transform))
            cutout_label = src_label.read(1, window=from_bounds(
                left, bottom, right, top, src_label.transform))

            show(cutout_satellite)
            show(cutout_label)

            print("Shapes:", cutout_satellite.shape, cutout_label.shape)
            satellite_cutouts.append(cutout_satellite)
            label_cutouts.append(cutout_label)

            # adjust cutout window for next iteration (with 32 px overlap to cover trees on the edge)
            # adjust cutout window on the x-axis => move cutout window to the right - the overlap
            left = right - overlap * xRes  # use right as a base and move left by the overlap
            # move patch_size to the right from left # += patch_size * xRes
            right = left + patch_size * xRes
        # reset the x-axis
        left = src_satellite.bounds[0]
        right = left + patch_size * xRes
        # adjust cutout window on the y-axis => move cutout window to the bottom
        top = bottom - overlap * yRes
        bottom = top - patch_size * yRes  # -= patch_size * yRes

    src_satellite.close()
    src_label.close()
