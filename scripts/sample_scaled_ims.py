#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

path = "sample_images/"

Rsol = 50


lblMap = {'Person' : 0, 'Bicycle' : 1, 'Motorcycle' : 2, 'Rickshaw' : 3, 'Autorickshaw' : 4, 'Car' : 5}

for file_name in os.listdir(path):
	Y = cv2.imread(os.path.join(path, file_name), 0)
	Y1 = cv2.imread(os.path.join(path, file_name))
	ht, wd = np.shape(Y)
	if (ht > wd):
		y = Rsol
		x = int(round((Rsol*wd)/float(ht)))
	else:
		x = Rsol
		y = int(round((Rsol*ht)/float(wd)))

	Y = cv2.resize(Y, (x,y))
	Y1 = cv2.resize(Y1, (x,y))
	# print np.shape(Y), np.shape(Y1)		

	v = np.zeros((Rsol, Rsol), dtype=int)
	v[0:y,0:x] = Y
	v1 = np.zeros((Rsol, Rsol, 3), dtype=int)
	v1[0:y,0:x,0:3] = Y1

	# cv2.imshow('image',v)
	# cv2.waitKey()

	# plt.imshow(v, cmap='Greys_r')
	# plt.title(str2label(pkl[i]['label']))
	# plt.show()

	v = np.reshape(v, Rsol*Rsol)
	v1 = np.reshape(v1, Rsol*Rsol*3)
	v = map(int, v)
	v1 = map(int, v1)
	# print np.shape(v), np.shape(v1)
	# sys.exit()

	# data_vector.append(v)
	# clr_data_vector.append(v1)
	# label_vector.append( int(lblMap[label]) )
	# label_vector += {label_vectorMap[label]}

	Z = np.reshape(v, (Rsol,Rsol))
	plt.imshow(Z, cmap='Greys_r')
	# plt.title(label_vector[0])
	plt.show()
	plt.savefig('sample_grey_images/'+file_name+'_grey.png')
