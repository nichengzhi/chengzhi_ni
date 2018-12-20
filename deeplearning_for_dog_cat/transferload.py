import h5py, math
import numpy as np
import tensorflow as tf
from keras.layers import Dense, Dropout, Activation, Flatten, Input
from sklearn.utils import shuffle
from keras.models import Sequential,Model
import pandas as pd
import os
import matplotlib.pyplot as plt

file_path = './transfer_learning_data/'
filenames = [ "vector_InceptionV3.h5", "vector_Xception.h5"]
filenames = [file_path + filename for filename in filenames]
x_train = []
x_test = []
for filename in filenames:
    with h5py.File(filename, 'r') as h:
        x_train.append(np.array(h['train']))
        x_test.append(np.array(h['test']))
        y_train = (np.array(h['train_label']))

x_train = np.concatenate(x_train, axis=1)
x_test = np.concatenate(x_test, axis=1)
y_train = y_train.reshape(len(y_train), -1)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
np.random.seed(222)
#model = Sequential()

#model.add(Dense(1, activation = 'sigmoid', input_shape = (x_train.shape[1],)))
#model.add(Dropout(0.5))
#model.add(Dense(1, activation='sigmoid'))
input_tensor = Input(x_train.shape[1:])
x = Dropout(0.5)(input_tensor)
x = Dense(1, activation='sigmoid')(x)
model = Model(input_tensor, x)

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=128, epochs=10, validation_split=0.2)
predict1 = model.predict(x_test, verbose=0)

testid = range(1,12501)
sub = pd.DataFrame({'id':testid,'label':predict1[:, 0]})
sub.to_csv("new_sub_transfer.csv",index = False)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()