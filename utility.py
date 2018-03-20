import numpy as np
import os
import cv2

def img_to_encoding(image_path, model):
    img1 = cv2.imread(image_path, -1)
    img = img1[...,::-1]
    img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
    x_train = np.array([img])
    embedding = model.predict_on_batch(x_train)
    return embedding

# loads and resizes an image
def resize_img(image_path):
    img = cv2.imread(image_path, 1)
    img = cv2.resize(img, (96, 96))
    cv2.imwrite(image_path, img)
