import io

import tensorflow as tf
import os
import matplotlib.pyplot as plt
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import PIL
from tensorflow.keras.layers import Input, Dense, Conv2D, SeparableConv2D, MaxPool2D, Dropout, Flatten, BatchNormalization
from tensorflow.keras.models import Sequential


class PneumoniaModel:

    def __init__(self):
        self.model = Sequential([
            Input(shape=(150, 150, 3)),
            # 1
            Conv2D(filters=16, kernel_size=(3, 3), activation='relu', padding='same'),
            Conv2D(filters=16, kernel_size=(3, 3), activation='relu', padding='same'),
            MaxPool2D(pool_size=(2, 2)),
            # 2
            Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same'),
            Conv2D(filters=32, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPool2D(pool_size=(2, 2)),
            # 3
            Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
            Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPool2D(pool_size=(2, 2)),
            # 4
            SeparableConv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            SeparableConv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPool2D(pool_size=(2, 2)),
            Dropout(0.25),
            # 5
            SeparableConv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            SeparableConv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPool2D(pool_size=(2, 2)),
            Dropout(0.25),
            # 6
            SeparableConv2D(filters=256, kernel_size=(3, 3), activation='relu', padding='same'),
            SeparableConv2D(filters=256, kernel_size=(3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPool2D(pool_size=(2, 2)),
            Dropout(0.25),
            # 7
            Flatten(),
            Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=1e-5, l2=1e-4)),
            Dropout(0.5),
            Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=1e-5, l2=1e-4)),
            Dropout(0.4),
            Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.L1L2(l1=1e-5, l2=1e-4)),
            Dropout(0.3),
            Dense(1, activation='sigmoid')
        ])

        path = os.path.join(os.path.expanduser("~"), "Desktop") + '\medsys\\'
        file = 'my_model_weights.h5'

        self.model.load_weights(path + file)


    def predict(self, img):
        with io.BytesIO() as output:
            img.save(output, format='JPEG')
            contents = output.getvalue()

        image = Image.open(io.BytesIO(contents)).resize((150, 150), resample=Image.BICUBIC).convert('RGB')
        x = tf.keras.utils.img_to_array(image)
        x /= 255
        x = np.expand_dims(x, axis=0)
        prediction = self.model.predict(x)
        return prediction.take(0)

#path = os.path.join(os.path.expanduser("~"), "Desktop") + '\infected.jpeg'
#image = PIL.Image.open(path)

