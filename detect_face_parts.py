# import the necessary packages
from imutils import face_utils
from collections import OrderedDict

import numpy as np
import argparse
import imutils
import dlib
import cv2

import boto3

def Deid_Img(input_image):
	FACIAL_LANDMARKS_68_IDXS = OrderedDict([
		("mouth", (48, 68)),
		#("inner_mouth", (60, 68)),
		("right_eyebrow", (17, 22)),
		("left_eyebrow", (22, 27)),
		("right_eye", (36, 42)),
		("left_eye", (42, 48)),
		("nose", (27, 36)),
		#("jaw", (0, 17))
	])

	FACIAL_LANDMARKS_IDXS = FACIAL_LANDMARKS_68_IDXS

	def My_Visualize_Facial_Landmarks(image, shape, colors=None, alpha=0.75):
		# create two copies of the input image -- one for the
		# overlay and one for the final output image
		overlay = image.copy()
		output = image.copy()

		# if the colors list is None, initialize it with a unique
		# color for each facial landmark region
		if colors is None:
			colors = [(0, 0, 0), (0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),]

		# startX, startY = shape[17]
		# endX, endY = shape[12]

		# face = output[startY:endY, startX:endX]
		# blur = cv2.GaussianBlur(face,(99,99), 30)
		# output[startY:endY, startX:endX] = blur

		pts = shape[0:68]

		hull = cv2.convexHull(pts)
		cv2.drawContours(overlay, [hull], -1, colors, -1)
		cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

		# return the output image
		return output

	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")

	# load the input image, resize it, and convert it to grayscale
	image = cv2.imread(input_image)
	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale image
	rects = detector(gray, 1)

	if len(rects) > 1:
		print('Upload Fail')
		print('There are many people in the picture')
		# cv2.imshow("Image", image)
		# cv2.waitKey(0)

		return False

	else:
	# loop over the face detections
		for (i, rect) in enumerate(rects):
			# determine the facial landmarks for the face region, then
			# convert the landmark (x, y)-coordinates to a NumPy array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

			# visualize all facial landmarks with a transparent overlay
			(x, y, w, h) = face_utils.rect_to_bb(rect)
			color = cv2.mean(image[x:x+w][y:y+h])

			# print(color)
			output = My_Visualize_Facial_Landmarks(image, shape, color, alpha=1.0)
			# cv2.imshow("Image", output)
			# cv2.waitKey(0)

		cv2.imwrite('{}'.format(input_image), output)
		
		# Save died image file in S3
		BUCKET_NAME = "mybide"
		AWS_ACCESS_KEY = "AKIAYLOHHE3A4V4D5I6F"
		AWS_SECRET_KEY = "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"

		s3 = boto3.client('s3',
				aws_access_key_id = AWS_ACCESS_KEY,
				aws_secret_access_key = AWS_SECRET_KEY
			)

		filename = input_image 
		bucket_name = BUCKET_NAME
		key = input_image 

		s3.upload_file(filename, bucket_name, key)

		return True