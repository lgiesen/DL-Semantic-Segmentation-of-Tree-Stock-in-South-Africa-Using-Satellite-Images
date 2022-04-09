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

        self.input_img = nn.()

        layers.Input(input_shape[1:], name='Input')

        self.pp_in_layer = nn.()

        layers.GaussianNoise(gaussian_noise)(input_img)
        self.pp_in_layer = nn.()

        layers.BatchNormalization()(pp_in_layer)

        self.c1 = nn.()

        layers.Conv2D(1*layer_count, (3, 3),
                      activation='relu', padding='same')(input_img)
        self.c1 = nn.()

        layers.Conv2D(1*layer_count, (3, 3),
                      activation='relu', padding='same')(c1)
        self.n1 = nn.()

        layers.BatchNormalization()(c1)
        self.p1 = nn.()

        layers.MaxPooling2D((2, 2))(n1)

        self.c2 = nn.()

        layers.Conv2D(2*layer_count, (3, 3),
                      activation='relu', padding='same')(p1)
        self.c2 = nn.()

        layers.Conv2D(2*layer_count, (3, 3),
                      activation='relu', padding='same')(c2)
        self.n2 = nn.()

        layers.BatchNormalization()(c2)
        self.p2 = nn.()

        layers.MaxPooling2D((2, 2))(n2)

        self.c3 = nn.()

        layers.Conv2D(4*layer_count, (3, 3),
                      activation='relu', padding='same')(p2)
        self.c3 = nn.()

        layers.Conv2D(4*layer_count, (3, 3),
                      activation='relu', padding='same')(c3)
        self.n3 = nn.()

        layers.BatchNormalization()(c3)
        self.p3 = nn.()

        layers.MaxPooling2D((2, 2))(n3)

        self.c4 = nn.()

        layers.Conv2D(8*layer_count, (3, 3),
                      activation='relu', padding='same')(p3)
        self.c4 = nn.()

        layers.Conv2D(8*layer_count, (3, 3),
                      activation='relu', padding='same')(c4)
        self.n4 = nn.()

        layers.BatchNormalization()(c4)
        self.p4 = nn.()

        layers.MaxPooling2D(pool_size=(2, 2))(n4)

        self.c5 = nn.()

        layers.Conv2D(16*layer_count, (3, 3),
                      activation='relu', padding='same')(p4)
        self.c5 = nn.()

        layers.Conv2D(16*layer_count, (3, 3),
                      activation='relu', padding='same')(c5)

        self.u6 = nn.()

        layers.UpSampling2D((2, 2))(c5)
        self.n6 = nn.()

        layers.BatchNormalization()(u6)
        self.u6 = nn.()

        layers.concatenate([n6, n4])
        self.c6 = nn.()

        layers.Conv2D(8*layer_count, (3, 3),
                      activation='relu', padding='same')(u6)
        self.c6 = nn.()

        layers.Conv2D(8*layer_count, (3, 3),
                      activation='relu', padding='same')(c6)

        self.u7 = nn.()

        layers.UpSampling2D((2, 2))(c6)
        self.n7 = nn.()

        layers.BatchNormalization()(u7)
        self.u7 = nn.()

        layers.concatenate([n7, n3])
        self.c7 = nn.()

        layers.Conv2D(4*layer_count, (3, 3),
                      activation='relu', padding='same')(u7)
        self.c7 = nn.()

        layers.Conv2D(4*layer_count, (3, 3),
                      activation='relu', padding='same')(c7)

        self.u8 = nn.()

        layers.UpSampling2D((2, 2))(c7)
        self.n8 = nn.()

        layers.BatchNormalization()(u8)
        self.u8 = nn.()

        layers.concatenate([n8, n2])
        self.c8 = nn.()

        layers.Conv2D(2*layer_count, (3, 3),
                      activation='relu', padding='same')(u8)
        self.c8 = nn.()

        layers.Conv2D(2*layer_count, (3, 3),
                      activation='relu', padding='same')(c8)

        self.u9 = nn.()

        layers.UpSampling2D((2, 2))(c8)
        self.n9 = nn.()

        layers.BatchNormalization()(u9)
        self.u9 = nn.()

        layers.concatenate([n9, n1], axis=3)
        self.c9 = nn.()

        layers.Conv2D(1*layer_count, (3, 3),
                      activation='relu', padding='same')(u9)
        self.c9 = nn.()

        layers.Conv2D(1*layer_count, (3, 3),
                      activation='relu', padding='same')(c9)

        self.d = nn.()

        layers.Conv2D(len(input_label_channel), (1, 1),
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
