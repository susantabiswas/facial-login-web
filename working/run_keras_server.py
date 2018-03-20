# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages
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
from webcam_utility import *
np.set_printoptions(threshold=np.nan)
from PIL import Image
import flask
import io
import cv2

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None
user_db = None

def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    # triplet formula components
    pos_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[1])) )
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[2])) )
    basic_loss = pos_dist - neg_dist + alpha
    
    loss = tf.maximum(basic_loss, 0.0)
   
    return loss


def load_FRmodel():
	# load the pre-trained Keras model (here we are using a model
	# pre-trained on ImageNet and provided by Keras, but you can
	# substitute in your own networks just as easily)
	global model
	model = load_model('models/model_orig.h5', custom_objects={'triplet_loss': triplet_loss})
	#model.summary()

def ini_user_database():
	global user_db
	# check for existing database
	if os.path.exists('database/user_dict.pickle'):
		with open('database/user_dict.pickle', 'rb') as handle:
			user_db = pickle.load(handle)
	else:
		# make a new one
		# we use a dict for keeping track of mapping of each person with his/her face encoding
		user_db = {}
	#print(len(user_db))
	return user_db


def find_face(encoding, database, model, threshold=0.6):
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



@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		if flask.request.files.get("image"):
			# read the image in PIL format
			image = flask.request.files["image"].read()
			image = np.array(Image.open(io.BytesIO(image)))
			#cv2.imwrite('saved_image/new.jpg', np.array(image))
			
			
			# classify the input image and then initialize the list
			# of predictions to return to the client
			resize_img('saved_image/dog.jpg')
			encoding = img_to_encoding('saved_image/dog.jpg', model)
			min_dist, identity = find_face(encoding, user_db, model, threshold=0.7)
			
			data["min_dist"] = str(min_dist)
			data['identity'] = identity
			print(image.shape)

			# indicate that the request was a success
			data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_FRmodel()
	ini_user_database()
	app.run()
