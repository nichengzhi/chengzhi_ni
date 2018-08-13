import h5py, math
from keras.layers import Input, Lambda
from keras.applications import inception_v3, resnet50, xception
import numpy as np
import os
IMAGE_SIZE = 128
X_train = np.load('C:\\Users\\TEMP\\Desktop\\dogvscat\\train.npy')
X_test = np.load('C:\\Users\\TEMP\\Desktop\\dogvscat\\test.npy')
train_path = "C:\\train"
train_y = [1 if 'dog' in i else 0 for i in os.listdir(train_path)]

def write_feature_vector(MODEL, pre_process):
    inputs = Input((IMAGE_SIZE, IMAGE_SIZE, 3))
    if pre_process:
        inputs = Lambda(pre_process)(inputs)

    model = MODEL(input_tensor=inputs, weights='imagenet', include_top=False, pooling='avg')
    train_vector = model.predict(X_train)
    test_vector = model.predict(X_test)

    with h5py.File("./transfer_learning_data/vector_{}.h5".format(MODEL.__name__)) as h:
        h.create_dataset("train", data=train_vector)
        h.create_dataset("test", data=test_vector)
        h.create_dataset("train_label", data=train_y)
    print(MODEL.__name__ + " ok.")

write_feature_vector(inception_v3.InceptionV3, pre_process=inception_v3.preprocess_input)

write_feature_vector(xception.Xception, pre_process=xception.preprocess_input)
