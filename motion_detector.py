import argparse
import datetime
import imutils
import time
import cv2
import pickle

from classify_foreground import *

start_time = time.time()

Rsol = 30

if os.path.exists('SVC'+str(Rsol)+'.pickle'):
    with open('SVC'+str(Rsol)+'.pickle') as f:
        clf = pickle.load(f)
else:
    clf = get_clf()
    with open('SVC'+str(Rsol)+'.pickle') as f:
        pickle.dump(clf, f)


print "model learnt in %s seconds" %(time.time()-start_time)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(args["video"])
 
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the Object/NoObject
	# text
	(grabbed, frame) = camera.read()
	text = "NoObject"
 
	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break
 
	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=700)
	gray_orig = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray_orig, (21, 21), 0)
 
	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
# compute the absolute difference between the current frame and first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	#print frameDelta
	firstFrame=gray
	thresh = cv2.threshold(frameDelta, 1, 255, cv2.THRESH_BINARY)[1]
	#print thresh
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	#print len(cnts)
 	color=0
	# loop over the contours
	for c in cnts:
		#color=color+255/len(cnts)
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue
 
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)




		crop_img = gray_orig[y:y+h,x:x+w]
		# print np.shape(gray_orig), y, h, x, w, np.shape(crop_img)
		cv2.imshow("cropped_image", crop_img)

		class_text = get_class(clf, crop_img)







		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = class_text

		cv2.putText(frame, text, (x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


	# # draw the text and timestamp on the frame
	# #color=color+255/cnts
	# cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
	# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	# cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
	# 	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)


 
	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
