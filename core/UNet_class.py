import torch.nn as nn
import torch.nn.functional as F
from config import config
from tensorflow.keras import layers, models, regularizers

config = config.Configuration()


class UNetModel(nn.Module):

    def __init__(self, input_shape, input_label_channel, layer_count=64, regularizers=regularizers.l2(0.0001), gaussian_noise=0.1, weight_file=None):
        # , num_inputs, num_hidden, num_outputs):
        """ Method to declare the UNet model.

        Args:
            input_shape: tuple(int, int, int, int)
                Shape of the input in the format (batch, height, width, channels).
            input_label_channel: list([int])
                list of index of label channels, used for calculating the number of channels in model output.
            layer_count: (int, optional)
                Count of kernels in first layer. Number of kernels in other layers grows with a fixed factor.
            regularizers: keras.regularizers
                regularizers to use in each layer.
            weight_file: str
                path to the weight file.
        """
        super().__init__()
        input_img = layers.Input(input_shape[1:], name='Input')
#        pp_in_layer = layers.GaussianNoise(gaussian_noise)(input_img)
#        pp_in_layer = layers.BatchNormalization()(pp_in_layer)

        c1 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(input_img)
        c1 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(c1)
        n1 = layers.BatchNormalization()(c1)
        p1 = layers.MaxPooling2D((2, 2))(n1)

        c2 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(p1)
        c2 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(c2)
        n2 = layers.BatchNormalization()(c2)
        p2 = layers.MaxPooling2D((2, 2))(n2)

        c3 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(p2)
        c3 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(c3)
        n3 = layers.BatchNormalization()(c3)
        p3 = layers.MaxPooling2D((2, 2))(n3)

        c4 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(p3)
        c4 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(c4)
        n4 = layers.BatchNormalization()(c4)
        p4 = layers.MaxPooling2D(pool_size=(2, 2))(n4)

        c5 = layers.Conv2D(16*layer_count, (3, 3),
                           activation='relu', padding='same')(p4)
        c5 = layers.Conv2D(16*layer_count, (3, 3),
                           activation='relu', padding='same')(c5)

        u6 = layers.UpSampling2D((2, 2))(c5)
        n6 = layers.BatchNormalization()(u6)
        u6 = layers.concatenate([n6, n4])
        c6 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(u6)
        c6 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(c6)

        u7 = layers.UpSampling2D((2, 2))(c6)
        n7 = layers.BatchNormalization()(u7)
        u7 = layers.concatenate([n7, n3])
        c7 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(u7)
        c7 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(c7)

        u8 = layers.UpSampling2D((2, 2))(c7)
        n8 = layers.BatchNormalization()(u8)
        u8 = layers.concatenate([n8, n2])
        c8 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(u8)
        c8 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(c8)

        u9 = layers.UpSampling2D((2, 2))(c8)
        n9 = layers.BatchNormalization()(u9)
        u9 = layers.concatenate([n9, n1], axis=3)
        c9 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(u9)
        c9 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(c9)

        d = layers.Conv2D(len(input_label_channel), (1, 1),
                          activation='sigmoid', kernel_regularizer=regularizers)(c9)

        seg_model = models.Model(inputs=[input_img], outputs=[d])
        if weight_file:
            seg_model.load_weights(weight_file)
        seg_model.summary()

    def forward(self, input_img, layer_count=64, input_label_channel=None):
        if input_label_channel is None:
            input_label_channel = [config.input_shape[2]]
        # Perform the calculation of the model to determine the prediction
        # input_img = layers.Input(input_shape[1:], name='Input')
        #        pp_in_layer = layers.GaussianNoise(gaussian_noise)(input_img)
        #        pp_in_layer = layers.BatchNormalization()(pp_in_layer)

        c1 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(input_img)
        c1 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(c1)
        n1 = layers.BatchNormalization()(c1)
        p1 = layers.MaxPooling2D((2, 2))(n1)

        c2 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(p1)
        c2 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(c2)
        n2 = layers.BatchNormalization()(c2)
        p2 = layers.MaxPooling2D((2, 2))(n2)

        c3 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(p2)
        c3 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(c3)
        n3 = layers.BatchNormalization()(c3)
        p3 = layers.MaxPooling2D((2, 2))(n3)

        c4 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(p3)
        c4 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(c4)
        n4 = layers.BatchNormalization()(c4)
        p4 = layers.MaxPooling2D(pool_size=(2, 2))(n4)

        c5 = layers.Conv2D(16*layer_count, (3, 3),
                           activation='relu', padding='same')(p4)
        c5 = layers.Conv2D(16*layer_count, (3, 3),
                           activation='relu', padding='same')(c5)

        u6 = layers.UpSampling2D((2, 2))(c5)
        n6 = layers.BatchNormalization()(u6)
        u6 = layers.concatenate([n6, n4])
        c6 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(u6)
        c6 = layers.Conv2D(8*layer_count, (3, 3),
                           activation='relu', padding='same')(c6)

        u7 = layers.UpSampling2D((2, 2))(c6)
        n7 = layers.BatchNormalization()(u7)
        u7 = layers.concatenate([n7, n3])
        c7 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(u7)
        c7 = layers.Conv2D(4*layer_count, (3, 3),
                           activation='relu', padding='same')(c7)

        u8 = layers.UpSampling2D((2, 2))(c7)
        n8 = layers.BatchNormalization()(u8)
        u8 = layers.concatenate([n8, n2])
        c8 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(u8)
        c8 = layers.Conv2D(2*layer_count, (3, 3),
                           activation='relu', padding='same')(c8)

        u9 = layers.UpSampling2D((2, 2))(c8)
        n9 = layers.BatchNormalization()(u9)
        u9 = layers.concatenate([n9, n1], axis=3)
        c9 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(u9)
        c9 = layers.Conv2D(1*layer_count, (3, 3),
                           activation='relu', padding='same')(c9)

        d = layers.Conv2D(len(input_label_channel), (1, 1),
                          activation='sigmoid', kernel_regularizer=regularizers)(c9)

        self.d = layers.Conv2D(len(input_label_channel), (1, 1),
                               activation='sigmoid', kernel_regularizer=regularizers)(c9)
        return x
