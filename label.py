#!/usr/bin/python

import cv2
import sys
import os

refPt = []
label = False
block = False
forgroundlabel = False

def clickListener(event, x, y, flags, callback):
	global refPt, label, block

	#start left-click press
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		block = False
		label = False

	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP and forgroundlabel:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
		label = True

		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

def saveFrame(currFrame, image):
	# global image
	global folder
	global fno
	i = 0
	height, width = image.shape[:2]
	print height, width
	for vehicle in currFrame:
		for area in currFrame[vehicle]:
			y = [area['rect'][0][1], area['rect'][1][1]]
			x = [area['rect'][0][0], area['rect'][1][0]]
			y.sort()
			x.sort()
			print x, y
			crop_img = image[max(0,y[0]):min(height,y[1]), max(0,x[0]):min(width,x[1])]
			if area['type'] == 1:
				cv2.imwrite(folder+'/'+vehicle+'/'+str(fno) + '_' + str(i) + '.jpg', crop_img)
			else:
				cv2.imwrite(folder+'/b'+vehicle+'/'+str(fno) + '_' + str(i) + '.jpg', crop_img)
			i = i+1

#"car" : c
# "motorcycle" : m
# "auto" : a
# "bicycle" : b
# "pedestrian" : p
# "rickshaw" : r

##blocked 	- x

def frameListener():
	global image
	block = False
	clone = image.copy()

	currFrame = {
		"car" : [],
		"motorcycle" : [],
		"auto" : [],
		"bicycle" : [],
		"pedestrian" : [],
		"rickshaw" : []
	}
	while True:
		#wait for keypress to label image
		key = cv2.waitKey(0) & 0xFF
		
		# if the 'r' key is pressed, reset labelling
		if key == ord("z"):
			cv2.imshow("image", clone)
			image = clone.copy()
			cv2.imshow("image", clone)
			currFrame = {
				"car" : [],
				"motorcycle" : [],
				"auto" : [],
				"bicycle" : [],
				"pedestrian" : [],
				"rickshaw" : []
			}

		#go to next frame
		elif key == ord("e"):
			print currFrame
			break

		#label is partially blocked
		elif key == ord("x") and label:
			block = True

		#label is pedestrian
		elif key == ord("p") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked pedestrian")
				print refPt
				lobject["type"] = 0
			else:
				print("pedestrian")
				print refPt
			currFrame["pedestrian"].append(lobject)
			block = False

		#label is car
		elif key == ord("c") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked car")
				print refPt
				lobject["type"] = 0
			else:
				print("car")
				print refPt
			currFrame["car"].append(lobject)
			block = False

		#label is motor-cycle
		elif key == ord("m") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked motorcycle")
				print refPt
				lobject["type"] = 0
			else:
				print("motorcycle")
				print refPt
			currFrame["motorcycle"].append(lobject)
			block = False

		#label is auto
		elif key == ord("a") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked auto")
				print refPt
				lobject["type"] = 0
			else:
				print("auto")
				print refPt
			currFrame["auto"].append(lobject)
			block = False

		#label is bicycle
		elif key == ord("b") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked cycle")
				print refPt
				lobject["type"] = 0
			else:
				print("bicycle")
				print refPt
			currFrame["bicycle"].append(lobject)
			block = False

		#label is rickshaw
		elif key == ord("r") and label:
			lobject = {
				"rect" : refPt,
				"type" : 1
			}
			if block:
				print("Blocked rickshaw")
				print refPt
				lobject["type"] = 0
			else:
				print("rickshaw")
				print refPt
			currFrame["rickshaw"].append(lobject)
			block = False

	saveFrame(currFrame, clone)






if len(sys.argv) != 2 :
	print('Provide a file name to process as an input argument.')
	print('like.. python label.py example.mp4')
	sys.exit(0)
else:
	inputfile = sys.argv[1]

directory = '../dataset'
if not os.path.exists(directory):
	os.makedirs(directory)

folder = directory+'/'+inputfile
if not os.path.exists(folder):
	os.makedirs(folder)

vfolders = ['car', 'bcar',  'auto', 'bauto', 'bicycle', 'bbicycle', 'pedestrian','bpedestrian', 'motorcycle', 'bmotorcycle', 'rickshaw', 'brickshaw'  ]
for f in vfolders:
	if not os.path.exists(folder+'/'+f):
		os.makedirs(folder+'/'+f)

cap = cv2.VideoCapture(inputfile)
fno = 1 
cv2.namedWindow("image",flags=cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", clickListener)

while(cap.isOpened()):
	refPt = []
	ret, image = cap.read()
	if not ret:
		break
	else:
		if fno % 10 == 1 :
			cv2.imshow("image", image)
			key = cv2.waitKey(0) & 0xFF

			if key == ord("f"):
				print("Foreground Frame")
				forgroundlabel = True
				currFrame = frameListener()
				forgroundlabel = False
			elif key == ord("b"):
				print("Background Frame")
			elif key == ord("q"):
				break
	fno += 1

cap.release()
cv2.destroyAllWindows()
