# from get_frames import get_frames
import cv2

import cv2.cv as cv
import sys
import os
import time

start_time = time.time()

# for cutting the some fraction of frames during entry and exit of objects
edge_cut_factor = 5

# factor for filtering repetition
cut_factor_slow = 16
cut_factor_medium = 8
cut_factor_fast = 4

repetition_cut_factor = {
u'Person' : cut_factor_slow, 
u'Car' : cut_factor_fast,
u'Bicycle' : cut_factor_medium,
u'Motorcycle' : cut_factor_fast,
u'Autorickshaw' : cut_factor_fast,
u'Rickshaw' : cut_factor_medium,
u'Number-plate' : cut_factor_fast
}

import json
def get_frames(fname, frame_count):

	frames = [[] for _ in range(frame_count)]
	with open(fname) as json_data:
		data = json.load(json_data)
		
		obj_list = data.keys()
		obj_frames = {}
		for obj_id in obj_list:
			obj_frames[obj_id] = {}
		
		for obj_id, item in data.iteritems():
			for fno, inst in item["boxes"].iteritems():
				inst['label'] = item['label']
				if inst['outside'] == 1  or inst['occluded'] == 1:
					continue
				obj_frames[obj_id][int(fno)] = inst



		for obj_id in obj_list:
			
			# filtering frames for each of the objects in loop
			frames_list = obj_frames[obj_id].keys()
			n = len(frames_list)
			#filter the edges (from entry and exit)
			frames_list = frames_list[(n/edge_cut_factor) : n-(n/edge_cut_factor)]
			
			#filter for repetition 
			i = 0
			for fno in frames_list:
				inst = obj_frames[obj_id][fno]
				if i%repetition_cut_factor[inst['label']] == 0:
					# Append only the filtered frames
					frames[fno].append(inst)
				i += 1
	
	return frames



def reject(ht, wd, lbl):
	# if lbl == 'Bicycle' && (ht < 75 || wd)
	return False


video=sys.argv[1]
vf_name = video.split('.')[0]
cap = cv2.VideoCapture(video)
fcount = cap.get(cv.CV_CAP_PROP_FRAME_COUNT)
fcount = int(fcount)
print "number of frames = ", fcount

print "Parsing JSON data ...",
frames = get_frames('label_data/' +vf_name+'.json', int(fcount))
print "\rParsing JSON Completed"

#print len(frames[0])
#print frames[1][0]
#print frames[0][0][u'occluded']

path = os.getcwd()
path = path + '/filtered_images'

object_id=0
cap = cv2.VideoCapture(video)
fno = 0 
cv2.namedWindow("image",flags=cv2.WINDOW_NORMAL)


i = 0
print "Extracting and saving cropped object images ..."
while(cap.isOpened()):
	ret, image = cap.read()
	if not ret:
		break
	else:
		try:
			for obj in frames[fno]:
				
				# if obj[u'occluded'] == 0 and obj[u'outside'] == 0:
				
				# if reject(obj[u'ytl'] - obj[u'ybr'], obj[u'xtl'] - obj[u'xbr'], obj['label']):
				# 	continue

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
	i += 1
	if(i%10):
		print "\r", float(i*100)/fcount , " Complete",

print "\r", float(i*100)/fcount , " Complete",
print "\n~~~~~~~~~ total time taken = %s seconds ~~~~~~~~~\n" %(time.time() - start_time)
