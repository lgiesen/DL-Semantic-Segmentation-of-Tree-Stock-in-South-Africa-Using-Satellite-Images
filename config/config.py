import os


# Configuration of the parameters for the 2-UNetTraining.ipynb notebook
class Configuration:
    def __init__(self):
        # 1. Paths
        from sys import platform

        if platform in ["linux", "linux2"]:
            self.base_dir = "/home/jovyan/work/"
            self.path_data = f"{self.base_dir}saved_data/south_africa_tree_stock/"

            self.model_path = f"{self.path_data}saved_models/"

            self.path_labeled_data = f"{self.path_data}1_labeled_data/tif/"
            self.path_satellite = f"{self.base_dir}satellite_data/"
            self.filepath_satellite = f"{self.path_satellite}2629BD_2018.tif"
            self.filepath_satellite_nw = self.path_data + "2_satellite/satellite-nw.tif"

            self.filepath_label_nw = self.path_labeled_data + "labels-22-02-23-nw.tif"
            self.filepath_label_se = self.path_labeled_data + "labels-22-02-23-se.tif"
        elif platform == "darwin":
            self.base_dir = "/Users/leori/Desktop/BA/"
            self.path_data = f"{self.base_dir}1_Data/"

            self.model_path = f"{self.base_dir}4_Project/saved_models/"

            self.filepath_satellite_exported = self.path_data + \
                "2_satellite/2629BD_2018_exported.tif"
            self.filepath_satellite = self.path_data + "2_satellite/2629BD_2018.tif"
            self.path_satellite = f"{self.path_data}2_satellite/"
            self.filepath_satellite_nw = self.path_satellite + "satellite-nw.tif"

            self.path_labeled_data = f"{self.path_data}1_labeled_data/tif/"
            self.path_labeled_data_qgis = self.path_labeled_data + \
                "labeled_areas/labeled_areas_extracted_with_QGIS/"
            self.filepath_label_nw = self.path_labeled_data_qgis + "labels-22-02-23-nw.tif"
            self.filepath_label_se = self.path_labeled_data_qgis + "labels-22-02-23-se.tif"
        elif platform == "win32":
            print("Something went wrong")

        self.path_patches = f"{self.path_data}3_patches/"
        self.path_pred = f"{self.path_data}4_pred/"
        # self.path_labeled_data_areas = f"{self.path_labeled_data}labeled_areas/"
        self.path_patches_labels = f"{self.path_patches}satellite_patches.npy"
        self.path_patches_satellite = f"{self.path_patches}label_patches.npy"

        self.filepath_model = f"{self.model_path}20220404_1826_AdaDelta_weightmap_tversky_256.h5"
        self.pred_imgs = ["2629BD_2018.tif"]

        self.filepath_label = f"{self.path_labeled_data}labels-22-02-23-compressed.tif"
        self.filepath_labels_bounding_boxes = self.path_labeled_data + \
            "label_polygons/labels-area-all/labels_bounding_box.shp"

        # 2. data preparation
        self.size = 256
        self.overlap = 32
        # Height * Width * (Input + Output) channels # (256,256,4)
        self.patch_size = (self.size, self.size, 4)

        # 3. training
        self.test_ratio = 0.2
        self.val_ratio = 0.2
        # Shape of the input data, height*width*channel; Here: RGB
        self.input_shape = (self.size, self.size, 3)

        self.BATCH_SIZE = 32
        self.VAL_BATCH_SIZE = 8
        self.VAL_BATCH_SIZE = 8
        self.NB_EPOCHS = 100
        self.MAX_TRAIN_STEPS = 50
