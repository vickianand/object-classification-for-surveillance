#!/usr/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys



directory = sys.argv[1]
directory = directory.rstrip('/')
print directory
Rsol = int(sys.argv[2])


lblMap = {'Person' : 0, 'Bicycle' : 1, 'Motorcycle' : 2, 'Rickshaw' : 3, 'Autorickshaw' : 4, 'Car' : 5}
labels = lblMap.keys()


data_vector = []
clr_data_vector = []
bnw_data_vector = []
label_vector = []

for label in labels :
	path = os.path.join(directory, label)
	if not os.path.exists(path):
		print path , " does not exist"
		continue
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
		# cv2.waitKey(0)

		# plt.imshow(v, cmap='Greys_r')
		# plt.title(str2label(pkl[i]['label']))
		# plt.show()

		v = np.reshape(v, Rsol*Rsol)
		v1 = np.reshape(v1, Rsol*Rsol*3)
		v = map(int, v)
		v1 = map(int, v1)
		# print np.shape(v), np.shape(v1)
		# sys.exit()

		data_vector.append(v)
		clr_data_vector.append(v1)
		label_vector.append( int(lblMap[label]) )
		# label_vector += {label_vectorMap[label]}

		# Z = np.reshape(data_vector[0], (Rsol,Rsol))
		# plt.imshow(Z, cmap='Greys_r')
		# plt.title(label_vector[0])
		# plt.show()
# print label_vector

print x, y, len(v), len(v1), len(label_vector)

np.savetxt( 'CSVs/' + directory + str(Rsol) + "_grey_ftr.csv", data_vector, delimiter=",", fmt='%d')
np.savetxt( 'CSVs/' + directory + str(Rsol) + "_clr_ftr.csv", clr_data_vector, delimiter=",", fmt='%d')
np.savetxt( 'CSVs/' + directory + str(Rsol) + "_lbl.csv", label_vector, delimiter=",", fmt='%d')
