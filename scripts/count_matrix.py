#!/usr/bin/python

import os, sys, shutil
import numpy as np

source_dir = "proper_images_collection/"
# target_dirs = ['train_dir1', 'test_dir1', 'vald_dir1']

# for d in target_dirs:
# 	if not os.path.exists(d):
# 		os.mkdir(d)

print "distribution of images from ", source_dir

matrx = np.zeros((6,6), dtype=int)
lblMap = {'Person' : 0, 'Bicycle' : 1, 'Motorcycle' : 2, 'Rickshaw' : 3, 'Autorickshaw' : 4, 'Car' : 5}
vidMap = {'datasam':0, 'input_video_sample1':1, 'input_video_sample2':2, 'input_video_sample3':3, 'videosample5':4}
lblRev ={}
vidRev ={}
for k in lblMap.keys():
	lblRev[lblMap[k]] = k
for k in vidMap.keys():
	vidRev[vidMap[k]] = k

l = os.listdir(source_dir)

for sd in l:

	path1 = os.path.join(source_dir, sd)
	iml = os.listdir(path1)
	for im in iml:
		fl = 1
		for k in vidMap.keys():
			if k in im:
				matrx[vidMap[k]][lblMap[sd]] += 1
				fl = 0
		if fl: matrx[5][lblMap[sd]] += 1

print "'Person''Bicycle''Motorcycle''Rickshaw''Autorickshaw' 'Car'"
print matrx

# for d in target_dirs:
# 	for sd in l:
# 		path = os.path.join(d, sd)
# 		if not os.path.exists(path):
# 			os.mkdir(path)
# ==============================================
