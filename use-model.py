import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
'''
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
tf.config.experimental.set_visible_devices(devices=gpus[0], device_type='GPU')
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)
'''

import numpy as np
import time
import os
import random
import lut_tools

from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.callbacks import ModelCheckpoint

print(tf.__version__)
if(tf.test.is_gpu_available() and tf.test.is_built_with_cuda()): print("TF using GPU")


def load_image(image_path):
    img = tf.keras.preprocessing.image.img_to_array( # not scaled to 0.0-1.0, do in model
        tf.keras.preprocessing.image.load_img(image_path, target_size=(240, 160), interpolation="bicubic")
    )
    print("img shape:", img.shape)
    return img.reshape(1, img.shape[0], img.shape[1], 3)

def predict_lut(model, imgdata):
    return model.predict(imgdata)

def load_model(modelpath):
    return tf.keras.models.load_model(modelpath)

def run(imgpath, cubepath, modelpath):
    model = load_model(modelpath)
    lut = predict_lut(model, load_image(imgpath))
    lut = lut.reshape(512, 3)
    lut_buffer = lut_tools.create_file(lut, 8)
    lut_tools.save_to_file(lut_buffer, cubepath)
    return True

if __name__ == '__main__':
    image_test = './jernej-graj-Mcb9AaM7BD4-unsplash.jpg'
    output_cube_path = "testimage3.cube"

    run(image_test, output_cube_path, "./trained/models/large2-model-1622504119_model-64-0.085.model")
    