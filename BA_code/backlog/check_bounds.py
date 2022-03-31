# check if bounds are valid
def check_bounds(opened_raster, checked_c_w, checked_c_s, checked_c_e, checked_c_n, ):
    c_w, c_e = opened_raster.bounds[0], opened_raster.bounds[2]
    c_n, c_s = opened_raster.bounds[1], opened_raster.bounds[3]
    print("Bounds (west, south, east, north):", c_w, c_s, c_e, c_n)
    if checked_c_w < c_w: print("The coordinates are too far west ({}). Increase it between {} and {}".format(checked_c_w, c_w, c_e))
    if checked_c_e > c_e: print("The coordinates are too far east ({}). Decrease it between {} and {}".format(checked_c_e, c_w, c_e))
    if checked_c_n < c_n: print("The coordinates are too far north ({}). Decrease it between {} and {}".format(checked_c_n, c_s, c_n))
    if checked_c_s > c_s: print("The coordinates are too far south ({}). Increase it between {} and {}".format(checked_c_s, c_s, c_n))
