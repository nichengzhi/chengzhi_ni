import numpy as np
import cv2
import os
train_path = "C:\\train"
test_path = "C:\\test1"
train_images = [os.path.join(train_path,i) for i in os.listdir(train_path)]
test_images = [os.path.join(test_path,i) for i in os.listdir(test_path)]





def image_process(image_list):
    images_array = np.ndarray((len(image_list),width,length,3),dtype=np.uint8)
    for i in range(len(image_list)):
        img = cv2.imread(image_list[i], cv2.IMREAD_COLOR)
        img =cv2.resize(img, (width, length), interpolation=cv2.INTER_CUBIC)
        images_array[i] = img
    return images_array









if __name__ == '__main__':
    width = 128
    length = 128#256 will make memory error
    train = image_process(train_images)
    test = image_process(test_images)

    print(train.shape)
    print(test.shape)
    np.save('train.npy', train)
    np.save('test.npy', test)