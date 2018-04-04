# Python code for Keras Server

# Usage
# Starting the server:
# python keras_server.py
# 'http://localhost:5000/predict'
#  Client request can be given by:
#	python simple_request.py

# import the necessary packages

import keras 
from keras import *
from keras.models import load_model
import numpy as np
import tensorflow as tf
import os
from collections import defaultdict
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///login_db.db', echo=True)

import pickle
import cv2
import os.path
from utility import img_to_encoding, resize_img
from PIL import Image
import flask
from flask import request, url_for, Response
from flask import flash, redirect, render_template, request, session, abort
import requests
import io

# initialize the Flask application and other variables
app = flask.Flask(__name__)
app.secret_key = os.urandom(1)

model = None
user_db = None
IMAGE_SAVE_PATH = './images'


# for detecting the face boundary
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

# custom loss function for model
def triplet_loss(y_true, y_pred, alpha = 0.2):
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    # triplet formula components
    pos_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[1])) )
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(y_pred[0], y_pred[2])) )
    basic_loss = pos_dist - neg_dist + alpha
    
    loss = tf.maximum(basic_loss, 0.0)
   
    return loss

# for checking whether a face is there in image or not
# returns true if a face is found and also saves a cropped bounded face picture 
# otherwise returns false
def face_present(image_path):
    img = cv2.imread(image_path, -1)
    save_loc = 'saved_image/new.jpg'
    face_present = False
    
    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # required region for the face
        roi_color = img[y-90:y+h+70, x-50:x+w+50]
        
        # crop to 96 X 96, required by the model
        roi_color = cv2.resize(roi_color, (96, 96))
        # save the detected face
        cv2.imwrite(save_loc, roi_color)
        # make face present as true
        face_present = True

        # Just for visualization purpose
        # draw a rectangle bounding the face and save it
        roi = img[y-90:y+h+70, x-50:x+w+50]
        cv2.rectangle(img, (x-10, y-70),
                    (x+w+20, y+h+40), (15, 175, 61), 4)
        cv2.imwrite('static/saved_images/bounded.jpg', img)
    return face_present


# for loading the facenet trained model 
def load_FRmodel():
    global model
    model = load_model('models/model.h5', custom_objects={'triplet_loss': triplet_loss})
    model.summary()


# load the saved user database
def ini_user_database():
    global user_db
    # check for existing database
    if os.path.exists('database/user_dict.pickle'):
        with open('database/user_dict.pickle', 'rb') as handle:
            user_db = pickle.load(handle)
    else:
        # make a new one
        # we use a dict for keeping track of mapping of each person with his/her face encoding
        user_db = defaultdict(dict)
    return user_db



# for checking if the given input face is of a registered user or not
def face_recognition(encoding, database, model, threshold=0.6):
    min_dist = 99999
    # keeps track of user authentication status
    authenticate = False
    # loop over all the recorded encodings in database
    for email in database.keys():
        # find the similarity between the input encodings and claimed person's encodings using L2 norm
        dist = np.linalg.norm(np.subtract(database[email]['encoding'], encoding))
        # check if minimum distance or not
        if dist < min_dist:
            min_dist = dist
            identity = email

    if min_dist > threshold:
        print("User not in the database.")
        identity = 'Unknown Person'
        authenticate = False
    else:
        print("Hi! " + str(identity) + ", L2 distance: " + str(min_dist))
        authenticate = True

    return min_dist, identity, authenticate



# for adding user face
def add_face():
    data = {"face_present": False}
    encoding = None
    # CHECK FOR FACE IN THE IMAGE
    valid_face = False
    valid_face = face_present('saved_image/new.jpg')
    # add user only if there is a face inside the picture
    if valid_face:
        # create image encoding 
        encoding = img_to_encoding('saved_image/new.jpg', model)
        # save the output for sending as json
        data['face_present'] = True
    else:
        # save the output for sending as json
        data['face_present'] = False
        print('No subject detected !')
    
    return data, encoding


#dashboard page
@app.route('/dashboard')
def dashboard():
    return flask.render_template('dashboard.html')


# index page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return flask.render_template("index.html")
    else:
        return dashboard()


# login page
@app.route('/login')
def login():
    return flask.render_template("login.html")


# for verifying user
@app.route('/authenticate_user', methods=["POST"])
def authenticate_user():
    POST_USERNAME = str(request.form['exampleInputEmail1'])
    POST_PASSWORD = str(request.form['exampleInputPassword1'])
    #making a session
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    # if the user is logged in
    if result:
        session['logged_in'] = True
        return dashboard()
    else:
        flash('wrong password!')
    return login()


#logout page
@app.route("/logout", methods=['POST'])
def logout():
    # logging out the user
    session['logged_in'] = False
    return index()


# Sign up page display
@app.route('/sign_up')
def sign_up():
    return flask.render_template("sign_up.html")


# to add user through the sign up from
@app.route('/signup_user', methods=["POST"])
def signup_user():
    #declaring the engine
    engine = create_engine('sqlite:///login_db.db', echo=True)
    
    # whether user registration was successful or not
    user_status = {'registration': False, 'face_present': False, 'duplicate':False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        print('Inside post')
        # getting the email and password from the user
        POST_USERNAME = str(request.form['email'])
        POST_PASSWORD = str(request.form['pass'])
        NAME = str(request.form['name'])

        if POST_USERNAME not in user_db.keys():
            # add new user's face
            if flask.request.files.get("image"):
                print('Inside Image')
                # read the image in PIL format
                image = flask.request.files["image"].read()
                image = np.array(Image.open(io.BytesIO(image)))
                print('Image saved success')
                # save the image on server side
                cv2.imwrite('saved_image/new.jpg',
                            cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                # check if any face is present or not in the picture
                data, encoding = add_face()
                # set face detected as True
                user_status['face_present'] = data['face_present']
            # if no image was sent
            else:
                user_status['face_present'] = False

            # only create a new session if complete user details is present
            if data['face_present']:
                # create a new session
                Session = sessionmaker(bind=engine)
                s = Session()
                # add data to user_db dict
                user_db[POST_USERNAME]['encoding'] = encoding
                user_db[POST_USERNAME]['name'] = NAME

                # save the user_db dict
                with open('database/user_dict.pickle', 'wb') as handle:
                    pickle.dump(user_db, handle,protocol=pickle.HIGHEST_PROTOCOL)
                print('User ' + POST_USERNAME + ' added successfully')

                # adding the user to data base
                user = User(POST_USERNAME, POST_PASSWORD)
                s.add(user)
                s.commit()

                # set registration status as True
                user_status['registration'] = True
                #logging in the user
                session['logged_in'] = True
                #return dashboard()
        else:
            user_status['duplicate'] = True
    
    #return sign_up()
    return flask.jsonify(user_status)
   


# predict function 
@app.route("/predict", methods=["POST"])
def predict():
    # this will contain the 
    data = {"success": False}
    # for keeping track of authentication status
    data['authenticate'] = False
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = np.array(Image.open(io.BytesIO(image)))
            
            # save the image on server side
            cv2.imwrite('saved_image/new.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            
            # CHECK FOR FACE IN THE IMAGE
            valid_face = False
            valid_face = face_present('saved_image/new.jpg')

            # do facial recognition only when there is a face inside the frame
            if valid_face:
                # find image encoding and see if the image is of a registered user or not
                encoding = img_to_encoding('saved_image/new.jpg', model)
                min_dist, identity, authenticate = face_recognition(
                                                    encoding, user_db, model, threshold=0.9)
                
                # save the output for sending as json
                data["min_dist"] = str(min_dist)
                data['email'] = identity
                if identity != 'Unknown Person':
                    data['name'] = user_db[identity]['name']
                else:
                    data['name'] = 'Unknown Person'
                data['face_present'] = True
                data['authenticate'] = authenticate

            else:
                # save the output for sending as json
                data["min_dist"] = 'NaN'
                data['identity'] = 'NaN'
                data['name'] = 'NaN'
                data['face_present'] = False
                data['authenticate'] = False
                print('No subject detected !')
            
            # indicate that the request was a success
            data["success"] = True

        # create a new session
        Session = sessionmaker(bind=engine)
        s = Session()
        # check if the user is logged in
        if data['authenticate']:
            session['logged_in'] = True
        else:
            flash('Unknown Person!')

    # return the data dictionary as a JSON response
    return flask.jsonify(data)



# first load the model and then start the server
if __name__ == "__main__":
    

    print("** Starting Flask server.........Please wait until the server starts ")
    print('Loading the Neural Network......\n')
    load_FRmodel()
    print('Model loaded..............')
    ini_user_database()
    print('Database loaded...........')
    app.run(host='0.0.0.0', port=5000)
