import os
# Configuration of the parameters for the 2-UNetTraining.ipynb notebook
class Configuration:
    def __init__(self):
        from sys import platform

        if platform in ['linux', 'linux2']:
            self.path_data = '/home/jovyan/work/saved_data/south_africa_tree_stock/' # os.getcwd()
            self.model_path = self.path_data + 'saved_models/'
            # Due to the export from QGIS, the satellite data is stored in "2_satellite/"
            self.filepath_satellite = '/home/jovyan/work/satellite_data/2629BD_2018.tif'
            # self.filepath_satellite = self.path_data + '2_satellite/2629BD_2018_exported.tif'
        elif platform == 'darwin':
            self.path_data = '/Users/leori/Desktop/BA/1_Data/'
            self.model_path = '/Users/leori/Desktop/BA/4_Project/saved_models/'
            # self.filepath_satellite = self.path_data + '2_satellite/2629BD_2018_exported.tif'
            self.filepath_satellite_server = self.path_data + '2_satellite/2629BD_2018.tif'
            self.path_labeled_data = self.path_data + '1_labeled_data/tif/'
            self.path_satellite = self.path_data + '2_satellite/'
        elif platform == 'win32':
            print('Something went wrong')

        self.filepath_label_compressed = self.path_labeled_data + 'labels-22-02-23-compressed.tif'

        

        self.path_labeled_data_areas = self.path_labeled_data + 'labeled_areas/'
        self.path_patches = self.path_data + '3_patches/'
        self.path_patches_masks = self.path_patches + 'masks/'
        self.path_patches_satellite = self.path_patches + 'satellite/'

        self.filepath_label = self.path_labeled_data + 'labels-22-02-23.tif'
        self.filepath_label_nw = self.path_labeled_data + 'labels-22-02-23-nw.tif'
        self.filepath_label_se = self.path_labeled_data + 'labels-22-02-23-se.tif'
        self.filepath_labels_bounding_boxes = self.path_labeled_data + 'label_polygons/labels_bounding_box.shp'
        
        # Patch generation; from the training areas (extracted in the last notebook), we generate fixed size patches.
        # random: a random training area is selected and a patch in extracted from a random location inside that training area. Uses a lazy stratergy i.e. batch of patches are extracted on demand.
        # sequential: training areas are selected in the given order and patches extracted from these areas sequential with a given step size. All the possible patches are returned in one call.
        # self.patch_generation_strategy = 'random' # 'random' or 'sequential'
        self.patch_size = (256,256,4) # Height * Width * (Input + Output) channels # (256,256,4)
        self.overlap = 32
        # # When stratergy == sequential, then you need the step_size as well
        # step_size = (128,128)
        
        # The training areas are divided into training, validation and testing set. Note that training area can have different sizes, so it doesn't guarantee that the final generated patches (when using sequential stratergy) will be in the same ratio. 
        self.test_ratio = 0.2 
        self.val_ratio = 0.2
        
        # Probability with which the generated patches should be normalized 0 -> don't normalize, 1 -> normalize all
        self.normalize = 0.4 

        
        # The split of training areas into training, validation and testing set, is cached in patch_dir.
        # self.patch_dir = './patches{}'.format(self.patch_size[0])
        # self.frames_json = os.path.join(self.patch_dir,'frames_list.json')


        # Shape of the input data, height*width*channel; Here channels are NVDI and Pan
        self.input_shape = (256,256,3) # TODO: Num of Channels - colors/grayscale => 1 # (256,256,2)
        self.input_image_channel = [0,1,2]
        self.input_label_channel = [3]
        self.input_weight_channel = [4]

        # CNN model related variables used in the notebook
        self.BATCH_SIZE = 16
        self.NB_EPOCHS = 100

        # number of validation images to use
        self.VALID_IMG_COUNT = 200
        # maximum number of steps_per_epoch in training
        self.MAX_TRAIN_STEPS = 1000

