import cv2
import os
import numpy as np

def faceDetection(test_img):
	# Color image to gray image
	gray_img = cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)
	
	# Classifier we are going to use is a haar classifiers: basically trained to detect certain objects (faces)
	face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')			

	# Variable loading the haar classifier, then call function to return a rectangle to where a face is detected in that image
	# scaleFactor is defined by: say 1.32, decrease size image by 32%, images bigger in size will be detected by the haar classifier
	# minNeighbors = it should have atleast 5 neighbors for it to be considered true positive
	# faces returns the coordinate values of the face
	faces = face_haar_cascade.detectMultiScale(gray_img, scaleFactor=1.32,minNeighbors=3)
	
	return faces, gray_img		# will need the rectangles and gray_img
	
# Going through Directory and extracting the images
def labels_for_training_data(directory):
	faces=[]
	faceID=[]		# Corresponding labels 
	
	# os.walk() generate the filenames in a directory tree by walking the tree either top down or bottom up
	for path,subdirnames,filenames in os.walk(directory):
		for filename in filenames:
			# for each file, fetch it an .h path (header)
			if filename.startswith("."):
				print("Skipping system file")
				continue
			
			# If path is not a system file, we want to extract id, use os.path.basename. It will go to the openCV project directory 
			# How os.walk works is that it goes recursively into directories and into more sub directories and get all files
			id = os.path.basename(path)
			
			# gets the path of the image
			img_path = os.path.join(path,filename)
			
			print("img_path: ", img_path)
			print("id: ", id)
			
			test_img = cv2.imread(img_path)
			if test_img is None:
				print("Image not loaded properly")
				continue
			
			faces_rect,gray_img = faceDetection(test_img)
			
			# If more than one faces are recognized, skip
			if len(faces_rect) != 1:
				continue
			
			# This rectangle will be return by faces_rect of faces argument
			(x,y,w,h) = faces_rect[0]
			# Region of interest in the grey image, 
			# Cropping out from the grey image the part which is the face
			# We are going to feed only the part to our classifier
			roi_gray = gray_img[y:y+w,x:x+h]
			
			# Our classifier will only take labels of type int
			faces.append(roi_gray)	# Cropping out from the grey image the part which is the face
			faceID.append(int(id))
	return faces, faceID

# Function to train our classifier on these training images
def train_classifier(faces,faceID):
	# LBPH: Local Binary Pattern Histogram
	# Instead of looking at the entire image, instead we see 3x3 pixels values which we write down and take central pixel and compare with surrounding values
	# If central value is bigger than one sibling, we assign it as 0, else assign it as 1
	# This is represented in Binary, later converted into Decimal
	# Creates a Histogram of the image through many other steps
	face_recognizer = cv2.face.LBPHFaceRecognizer_create()
	
	# .train takes in a numpy array, convert our parameters in func to numpy array
	face_recognizer.train(faces, np.array(faceID))
	return face_recognizer
	
# Draw the bounding box around our face
# Take parameters: test_img, and the rectangle coordinates of the image
def draw_rect(test_img,face):
	(x,y,w,h) = face 
	cv2.rectangle(test_img, (x,y), (x+w, y+h), (255,0,0), thickness=5)


# To put a certain text on our image, whose name it is
# Parameters: take the image, text and x and y coordinates
def put_text(test_img,text,x,y):
	# Using putText func of cv2, and creates a text for our images
	cv2.putText(test_img,text,(x,y),cv2.FONT_HERSHEY_DUPLEX, 5,(255,0,0),6)
