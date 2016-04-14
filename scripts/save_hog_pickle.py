#!/usr/bin/python

import sys, os, time

# from sklearn.neighbors import KNeighborsClassifier
from sklearn import decomposition

import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt
import pickle


train_dir = "CSVs/train_dir"
test_dir = "CSVs/test_dir"

Rsol = 50
extnsn = "_grey_ftr.csv"


def get_HoG(xs, size_cell=4, size_block=4, orientation=7):
	hog_xs = []
	for x in xs:
		fd = hog(x.reshape((Rsol, Rsol)),
		            orientations=orientation,
		            pixels_per_cell=(size_cell, size_cell),
		            cells_per_block=(size_block, size_block), visualise=False)
		hog_xs.append(fd)
	return hog_xs


if __name__ == "__main__" :
	if not os.path.exists('HOG'+str(Rsol)+extnsn+'.pickle'):
		X_train_o = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
		y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
		X_test_o =  genfromtxt(test_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
		y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
		
		X_train, X_test = get_HoG(X_train_o), get_HoG(X_test_o)

		with open('HOG'+str(Rsol)+extnsn+'.pickle', 'w+') as f:
			pickle.dump([X_train, y_train, X_test, y_test], f)

	if not os.path.exists('plain'+str(Rsol)+extnsn+'.pickle'):
		X_train = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
		y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
		X_test =  genfromtxt(test_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
		y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
		

		with open('plain'+str(Rsol)+extnsn+'.pickle', 'w+') as f:
			pickle.dump([X_train, y_train, X_test, y_test], f)
	