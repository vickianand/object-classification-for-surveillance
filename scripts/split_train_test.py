#!/usr/bin/python

import os, sys, shutil

source_dir = "proper_images_collection/"
target_dirs = ['train_dir', 'test_dir', 'vald_dir']

for d in target_dirs:
	if not os.path.exists(d):
		os.mkdir(d)

print "distributing images from ", source_dir

l = os.listdir(source_dir)
for d in target_dirs:
	for sd in l:
		path = os.path.join(d, sd)
		if not os.path.exists(path):
			os.mkdir(path)
# ==============================================

summry = ""
for sd in l:
	path1 = os.path.join(source_dir, sd)
	iml = os.listdir(path1)
	n = len(iml)
	summry = summry+"number of "+sd+" = "+str(n)
	# q = n/6
	# r = n%6
	trainl, testl, valdl = [], [], []
	
	for i in range(n):
		if(i%6 == 0): testl.append(iml[i])
		elif(i%6 == 1): valdl.append(iml[i])
		else: trainl.append(iml[i])

	# path2 = os.path.join('train_dir', sd)
	# for im in trainl:
	# 	spath = os.path.join(path1, im) 
	# 	dpath = os.path.join(path2, im)
	# 	if not os.path.exists(dpath):
	# 		shutil.copy(spath, dpath)

	path2 = os.path.join('test_dir', sd)
	for im in testl:
		spath = os.path.join(path1, im) 
		dpath = os.path.join(path2, im)
		if not os.path.exists(dpath):
			shutil.copy(spath, dpath)

	path2 = os.path.join('vald_dir', sd)
	for im in valdl:
		spath = os.path.join(path1, im) 
		dpath = os.path.join(path2, im)
		if not os.path.exists(dpath):
			shutil.copy(spath, dpath)

	

with open('split_summary.txt', 'w+') as f:
	f.write(summry)
