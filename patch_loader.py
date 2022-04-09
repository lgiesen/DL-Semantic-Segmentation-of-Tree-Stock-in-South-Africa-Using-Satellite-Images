import numpy as np
from sklearn.model_selection import train_test_split

from config import config

config = config.Configuration()


class Patch_Loader:
    def __init__(self):


def main():
    patches_labels = np.load(config.path_patches_labels)
    patches_satellite = np.load(config.path_patches_satellite)

    # scale the color values
    patches_satellite_train, patches_labels_train = [
        patch/255 for patch in patches_satellite], [patch/255 for patch in patches_labels]

    X_train_, X_test, y_train_, y_test = train_test_split(
        patches_satellite_train, patches_labels_train, test_size=config.test_ratio, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_, y_train_, test_size=config.val_ratio, random_state=42)

    X_train, y_train = np.array(X_train), np.array(y_train)
    X_val, y_val = np.array(X_val), np.array(y_val)
    X_test, y_test = np.array(X_test), np.array(y_test)


if __name__ == '__main__':
    main()
