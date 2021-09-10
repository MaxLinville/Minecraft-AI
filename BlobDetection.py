import cv2
import numpy as np
import mss
import cv2
import time

def findLeaves():
	with mss.mss() as sct:
		blob_area = {"top": 0, "left": 0, "width": 3840, "height": 2160}
		output = "sct-{top}x{left}_{width}x{height}.png".format(**blob_area)
		blob_image = np.array(sct.grab(blob_area))
		hsv = cv2.cvtColor(blob_image, cv2.COLOR_BGR2HSV)

	# Setup SimpleBlobDetector parameters.
	params = cv2.SimpleBlobDetector_Params()
	params.filterByArea = True
	params.minArea = 1000
	params.filterByCircularity = False
	params.minCircularity = 0
	params.filterByConvexity = False
	params.minConvexity = 0.87
	params.filterByInertia = False
	params.minInertiaRatio = 0.01

	# Create a detector with the parameters
	# OLD: detector = cv2.SimpleBlobDetector(params)
	detector = cv2.SimpleBlobDetector_create(params)

	#im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	lower_red = np.array([0, 0, 0])
	upper_red = np.array([10, 10, 10])
	mask = cv2.inRange(hsv, lower_red, upper_red)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

	cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	min_area = 1000
	max_area = 1000000
	image_number = 0

	boundingBox = []
	for c in cnts:
	    area = cv2.contourArea(c)
	    if area > min_area and area < max_area:
	        x,y,w,h = cv2.boundingRect(c)
	        boundingBox.append([x,y,w,h])
	        #cv2.rectangle(blob_image, (x, y), (x + w, y + h), (36,255,12), 2)
	        image_number += 1

	boundingBox.sort()
	# Detect blobs.
	#keypoints = detector.detect(final_mask)

	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures
	# the size of the circle corresponds to the size of blob
	#leaves = cv2.drawKeypoints(final_mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	'''scale_percent = 40 # percent of original size
	width = int(blob_image.shape[1] * scale_percent / 100)
	height = int(blob_image.shape[0] * scale_percent / 100)
	dim = (width, height)

	newimage = cv2.resize(blob_image, dim)
	# Show blobs
	cv2.imshow("Keypoints", newimage)
	cv2.waitKey(25)'''
	#return bounding box locations as a dictionary with x-y corner as key, width height as value
	return(boundingBox)

def findTree():
	#use the bounding box found by findLeaves() expand  downward and create a separate mask for the brown pixel values ranges, this would isolate 
	#logs from dirt and since it is connected to leaves it must be a tree trunk, filtering by inertia may come in use to find the long trunk, but not all
	#trunks are long, now figure out how to actually do this
	with mss.mss() as sct:
		blob_area = {"top": 0, "left": 0, "width": 3840, "height": 2160}
		blob_image = np.array(sct.grab(blob_area))
		hsv = cv2.cvtColor(blob_image, cv2.COLOR_BGR2HSV)

	leafClumps = findLeaves()
	for i in range(len(leafClumps)):
		leafClumps[i][3] = leafClumps[i][3] + 200
		print(leafClumps[i])
		cv2.rectangle(blob_image, (leafClumps[i][0], leafClumps[i][1]), (leafClumps[i][0] + leafClumps[i][2], leafClumps[i][1] + leafClumps[i][3]), (36,255,12), 2)

	params = cv2.SimpleBlobDetector_Params()
	params.filterByArea = False
	params.minArea = 1000
	params.filterByCircularity = False
	params.minCircularity = 0
	params.filterByConvexity = False
	params.minConvexity = 0.87
	params.filterByInertia = False
	params.minInertiaRatio = 0.01

	# Create a detector with the parameters
	detector = cv2.SimpleBlobDetector_create(params)

	#im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	lower_red = np.array([15, 127, 40])
	upper_red = np.array([20, 145, 80])
	mask = cv2.inRange(hsv, lower_red, upper_red)

	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	close = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

	cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if len(cnts) == 2 else cnts[1]

	min_area = 1000
	max_area = 1000000
	image_number = 0


	scale_percent = 40 # percent of original size
	width = int(blob_image.shape[1] * scale_percent / 100)
	height = int(blob_image.shape[0] * scale_percent / 100)
	dim = (width, height)

	newimage = cv2.resize(mask, dim)
	# Show blobs
	cv2.imshow("Keypoints", newimage)
	cv2.waitKey(25)
	logBoxes = leafClumps
	return(logBoxes)

def main():
	findTree()

while True:
	main()
