# from get_frames import get_frames
import cv2

import cv2.cv as cv
import sys
import os

import json
def get_frames(fname, frame_count):
	print fname
	frames = [[] for _ in range(frame_count)]
	with open(fname) as json_data:
		data = json.load(json_data)
		for _,item in data.iteritems():
			for fno,inst in item["boxes"].iteritems():
				inst['label'] = item['label']
				frames[int(fno)].append(inst)
	return frames


video=sys.argv[1]
vf_name = video.split('.')[0]
cap = cv2.VideoCapture(video)
fcount = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
print fcount
frames = get_frames('label_data/' +vf_name+'.json', int(fcount))

#print len(frames[0])
#print frames[1][0]
#print frames[0][0][u'occluded']

path = os.getcwd()

object_id=0
cap = cv2.VideoCapture(video)
fno = 0 
cv2.namedWindow("image",flags=cv2.WINDOW_NORMAL)

while(cap.isOpened()):
	ret, image = cap.read()
	if not ret:
		break
	else:
		try:
			for obj in frames[fno]:
				if obj[u'occluded'] == 0 and obj[u'outside'] == 0:
					crop_img = image[obj[u'ytl']:obj[u'ybr'], obj[u'xtl']:obj[u'xbr']]
					
					direct = path + '/' + obj['label']
					if not os.path.exists(direct):
						os.makedirs(direct)				
					cv2.imwrite(direct+'/'+str(fno)+'_'+str(object_id)+'_'+video+'.jpg', crop_img)
					
					direct = path + '/' + vf_name + '/' + obj['label']
					if not os.path.exists(direct):
						os.makedirs(direct)				
					cv2.imwrite(direct+'/'+str(fno)+'_'+str(object_id)+'_'+video+'.jpg', crop_img)
				
				object_id = object_id+1
			fno=fno+1
		except:
			fno+=1
			continue;
