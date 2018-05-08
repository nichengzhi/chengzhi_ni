from keras.models import Sequential
from keras.layers import Input, Dropout, Flatten, Dense, Activation
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, GlobalAveragePooling2D,LeakyReLU
from keras.optimizers import RMSprop, SGD, Adam
from keras.callbacks import ModelCheckpoint, Callback, EarlyStopping

from keras.layers.normalization import BatchNormalization
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

train_path = "C:\\train"
train_y = [1 if 'dog' in i else 0 for i in os.listdir(train_path)]

X_train = np.load('C:\\Users\\TEMP\\Desktop\\dogvscat\\train.npy')
X_test = np.load('C:\\Users\\TEMP\\Desktop\\dogvscat\\test.npy')
X_train = X_train / 255
X_test = X_test / 255

def dogcatmodel():

    model1 = Sequential()
    model1.add(Conv2D(32, (3, 3), input_shape=(128,128,3),kernel_initializer='he_normal',padding = 'same'))
    model1.add(Activation('relu'))
    #BatchNormalization(axis=-1)
    model1.add(MaxPooling2D(pool_size=(2, 2)))

    model1.add(Conv2D(64, (3, 3),kernel_initializer='he_normal',padding = 'same'))
    model1.add(Activation('relu'))
    model1.add(MaxPooling2D(pool_size=(2, 2)))
    #BatchNormalization(axis=-1)
    model1.add(Conv2D(128, (3, 3),kernel_initializer='he_normal',padding = 'same'))
    model1.add(Activation('relu'))

    model1.add(MaxPooling2D(pool_size=(2, 2)))
    #BatchNormalization(axis=-1)
    model1.add(Conv2D(256, (3, 3),kernel_initializer='he_normal',padding = 'same'))
    model1.add(Activation('relu'))

    model1.add(MaxPooling2D(pool_size=(2, 2)))
    model1.add(Flatten())
    model1.add(Dropout(0.4))

    model1.add(Dense(256, activation='relu'))
    model1.add(Dropout(0.3))

    model1.add(Dense(1))
    model1.add(Activation('sigmoid'))
    #RMSprop(lr=1e-4),
    #Adam(lr=0.0012, beta_1=0.9, beta_2=0.9, epsilon=1e-08, amsgrad=True)
    #SGD(lr=1e-3, decay=1e-6, momentum=0.9, nesterov=True)
    model1.compile(loss='binary_crossentropy', optimizer=RMSprop(lr=1e-4), metrics=['accuracy'])

    return model1
def main():
    model1 = dogcatmodel()
    #callbacks = [EarlyStopping(monitor='val_loss', patience=2, verbose=0),]
    #, callbacks=callbacks
    history = model1.fit(X_train, train_y, epochs=20,shuffle=True,
                         batch_size = 500, validation_split = 0.1)

    predict1 = model1.predict(X_test, verbose=0)

    testid = range(1,12501)
    sub = pd.DataFrame({'id':testid,'label':predict1[:, 0]})
    sub.to_csv("new_sub_early_stop.csv",index = False)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
if __name__ == '__main__':
    main()