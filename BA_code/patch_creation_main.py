def main():
    data_loader = TiffLoader(config.filepath_satellite_nw)
    label_loader = TiffLoader(config.filepath_label_nw)
    size = config.size # step size
    x_size, y_size = data_loader.size
    x_offset, y_offset = 0, 0
    satellite_patches, label_patches = [], []

    while y_offset + size < y_size:
        while x_offset + size < x_size:
            data = data_loader.load_rgb(
                x_offset, y_offset, size, size)
            label = corrected_labels(label_loader.load(
                Channel.GRAYSCALE, x_offset, y_offset, size, size))
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
            x_offset += size - config.overlap
            
        x_offset = 0
        y_offset += size - config.overlap

    np.save(config.path_patches_satellite, satellite_patches)
    np.save(config.path_patches_labels, label_patches)

if __name__ == '__main__':
    main()
