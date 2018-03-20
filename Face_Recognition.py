# coding: utf-8

# # <u>Face Recognition System
# This is based on Siamsese network.
# The advantage of **Siamese Network** is that it allows a way to do this sort of verification task with very little user data, as it is quite unreasonable to train using thousands of images for each user. Here we will be using **FaceNet Model**.
# FaceNet learns a neural network that encodes a face image into a vector of 128 numbers. So by comparing two such vectors, we can then determine if two pictures are of the same person.

from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
K.set_image_data_format('channels_first')

from keras.models import load_model
import pickle
import cv2
import os.path
import os
import numpy as np
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf
from utility import *
from inception_blocks_v2 import *
from webcam_utility import *
np.set_printoptions(threshold=np.nan)


# ## Model
# The model makes an encoding vector consisting of 128 numbers for the input image. Two encodings are compared and if the two encodings are similar then we say that the two images are of the same person otherwise they are different. 
# The model uses **Triplet loss function**. The aim is to minimize this function.

# triplet loss function
#  y_pred - list containing three objects:
#         anchor(None, 128) -- encodings for the anchor images
#         positive(None, 128) -- encodings for the positive images
#         negative(None, 128) -- encodings for the negative images
def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    
    # triplet formula components
    pos_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[1])) )
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[2])) )
    basic_loss = pos_dist - neg_dist + alpha
    
    loss = tf.maximum(basic_loss, 0.0)
   
    return loss


# ### Loading the Model
# The model outputs a vector of 128 numbers which represent encoding for the given input image. We will be using this encoding vector for comparing two images.
# #### Input
# - This network takes as input 96x96 RGB image as its input. Specifically, inputs a tensor of shape $(m, n_C, n_H, n_W)$ , where $n_C$ = channel.
# 
# #### Output
# - A matrix of shape **(m, 128)** where the 128 numbers are the encoding values for $ith$ image.
# load the model
def create_model():
    FRmodel = faceRecoModel(input_shape=(3, 96, 96))
    FRmodel.compile(optimizer = 'adam', loss = triplet_loss, metrics = ['accuracy'])
    return FRmodel

# ### Loading the trained weights
# We will be using a pretrained model since it requires a lot of time and data for training such a model.
def load_model_weights(FRmodel):
    # load saved weights
    #load_weights_from_FaceNet(FRmodel)
    FRmodel = load_model('models/mod1.h5')
    #FRmodel.load_weights('models/weights.h5')
    return FRmodel

# We will create a database of registered. For this we will use a simple dictionary and map each registered user with his/her face encoding.
# initialize the user database
def ini_user_database():
    # check for existing database
    if os.path.exists('database/user_dict.pickle'):
        with open('database/user_dict.pickle', 'rb') as handle:
            user_db = pickle.load(handle)
    else:
        # make a new one
        # we use a dict for keeping track of mapping of each person with his/her face encoding
        user_db = {}

    return user_db


# adds a new user face to the database using his/her image stored on disk using the image path
def add_user_img_path(user_db, FRmodel, name, img_path):
    if name not in user_db:
        user_db[name] = img_to_encoding(img_path, FRmodel)
        # save the database
        with open('database/user_dict.pickle', 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('User ' + name + ' added successfully')
    else:
        print('The name is already registered! Try a different name.........')
    

# adds a new user using image taken from webcam
def add_user_webcam(user_db, FRmodel, name):
    # we can use the webcam to capture the user image then get it recognized
    face_found = detect_face(user_db, FRmodel)

    if face_found:
        resize_img("saved_image/1.jpg")
        if name not in user_db:
            add_user_img_path(user_db, FRmodel, name, "saved_image/1.jpg")
        else:
            print('The name is already registered! Try a different name.........')
    else:
        print('There was no face found in the visible frame. Try again...........')


# deletes a registered user from database
def delete_user(user_db, name):
    popped = user_db.pop(name, None)

    if popped is not None:
        print('User ' + name + ' deleted successfully')
        # save the database
        with open('database/user_dict.pickle', 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
    elif popped == None:
        print('No such user !!')


# ### Putting everything together
# For making this face recognition system we are going to take the input image, find its encoding and then 
# see if there is any similar encoding in the database or not. We define a threshold value to decide whether the two images are similar 
# or not based on the similarity of their encodings.
def find_face(image_path, database, model, threshold=0.6):
    # find the face encodings for the input image
    encoding = img_to_encoding(image_path, model)

    min_dist = 99999
    # loop over all the recorded encodings in database
    for name in database:
        # find the similarity between the input encodings and claimed person's encodings using L2 norm
        dist = np.linalg.norm(np.subtract(database[name], encoding))
        # check if minimum distance or not
        if dist < min_dist:
            min_dist = dist
            identity = name

    if min_dist > threshold:
        print("User not in the database.")
        identity = 'Unknown Person'
    else:
        print("Hi! " + str(identity) + ", L2 distance: " + str(min_dist))

    return min_dist, identity

# for doing face recognition 
def do_face_recognition(user_db, FRmodel, threshold=0.7, save_loc="saved_image/1.jpg"):
    # we can use the webcam to capture the user image then get it recognized
    face_found = detect_face(user_db, FRmodel)

    if face_found:
        resize_img("saved_image/1.jpg")
        find_face("saved_image/1.jpg", user_db, FRmodel, threshold)
    else:
        print('There was no face found in the visible frame. Try again...........')


FRmodel = create_model()
print('\n\nModel created...')
FRmodel = load_model_weights(FRmodel)
print('Model weights loaded...')

user_db = ini_user_database()
print('User database loaded')
