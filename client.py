# cLient code for keras server

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
KERAS_REST_API_URL = "http://localhost:5000/predict"
# image path
IMAGE_PATH = "saved_image/profile.jpg"

# load the input image and construct the payload for the request
# this will be sent using json
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# submit the request
server_response = requests.post(KERAS_REST_API_URL, files=payload).json()

# ensure the request was sucessful
if server_response["success"]:
	# loop over the predictions and display them
	print('Working.....')
	print('Face_present: ' + str(server_response['face_present']))
	print('Identity: ' + server_response['identity'])
	print('Minimum distance: ' + server_response['min_dist'])
# otherwise, the request failed
else:
	print("Request failed")
