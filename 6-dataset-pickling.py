import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tqdm.std import tqdm
from tqdm import tqdm

import numpy as np
import time
import os
import random
import gc

import lut_tools

DATASET_BASEPATH = "./dataset-scaled"

#   Create train data
# get paths and zip
def load_files_from_folder(folderpath, filetype):
    all_files = []
    for root, dirs, files in os.walk(folderpath):
        for file in files:
            if file.endswith(filetype):
                file_path = os.path.join(root, file)
                all_files.append( (file_path, file) )
    return all_files

luts = load_files_from_folder(DATASET_BASEPATH, ".cube")
luts_db = {}
for l in luts:
    path, filename = l
    luts_db[filename] = path

images = load_files_from_folder(DATASET_BASEPATH, ".jpg")

train_paths = []
for img in images:
    path, filename = img
    try:
        lut_path = luts_db['lut-'+filename.split('.')[0]+'.cube']
        train_paths.append((path, lut_path))
    except Exception as e:
        print('didnt find lut', e)
print(len(train_paths))

def create_training_data(train_paths):
    trainX = []
    trainY = []
    bad_shapes = 0
    random.shuffle(train_paths) # Shuffle training set
    for paths in tqdm(train_paths, leave=False):
        img_path, lut_path = paths
        img = tf.keras.preprocessing.image.img_to_array( # not scaled to 0.0-1.0, do in model
            tf.keras.preprocessing.image.load_img(img_path)
        )

        lut = np.array(lut_tools.text_to_lut(
            lut_tools.load_lut(lut_path)[0]
        ))
        
        if lut.shape == (512,3):
            trainX.append(img)
            trainY.append(lut)
        else:
            bad_shapes += 1

    #print(bad_shapes, "bad shaped luts")

    # Create validation data
    VALIDATION_SPLIT_PERCENTAGE = 0.08
    valid_split = int(len(trainX)*VALIDATION_SPLIT_PERCENTAGE)

    # Create numpy arrays
    validX = np.array(trainX[:valid_split])
    validY = np.array(trainY[:valid_split])

    trainX = np.array(trainX[valid_split:])
    trainY = np.array(trainY[valid_split:])

    trainX = trainX.reshape(trainX.shape[0], 240, 160, 3)
    validX = validX.reshape(validX.shape[0], 240, 160, 3)
    trainY = trainY.reshape(trainY.shape[0], trainY.shape[1] * trainY.shape[2])
    validY = validY.reshape(validY.shape[0], validY.shape[1] * validY.shape[2])
    gc.collect()

    return (trainX, trainY, validX, validY)


BATCH_SIZE = 7_500
CACHED_DATASET_FOLDER = "./dataset_training_cache/"


tqdm_total = len(train_paths)
pbar = tqdm(total=tqdm_total)
counter = 0
while len(train_paths) > 0:
    counter += 1

    batch = train_paths[-BATCH_SIZE:]
    train_paths = train_paths[:-BATCH_SIZE]

    arrays = create_training_data(batch)

    path = CACHED_DATASET_FOLDER+"dataset-"+str(BATCH_SIZE)+"--"+str(counter)
    np.savez(path, *arrays)

    pbar.update(len(train_paths))