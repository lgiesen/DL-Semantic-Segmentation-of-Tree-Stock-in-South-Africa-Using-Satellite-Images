class Configuration:
    def __init__(self):
        from sys import platform
        if platform in ['linux', 'linux2']:
            self.path_data = '/home/jovyan/work/' + \
                'saved_data/south_africa_tree_stock/'
            self.model_path = f'{self.path_data}saved_models/'
            self.filepath_satellite = '/home/jovyan/work' + \
                '/satellite_data/2629BD_2018.tif'
        # if local device is MacOS:
        elif platform == 'darwin':
            self.path_data = '/path/to/1_Data/'
            self.model_path = '/path/to/saved_models/'
            self.filepath_satellite = self.path_data + \
                '2_satellite/2629BD_2018_exported.tif'
        elif platform == 'win32':
            print('Something went wrong')

# load config in different file like this
# from config import ConfigFileName
# config = ConfigFileName.Configuration()
