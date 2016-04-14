#!/usr/bin/python

import sys, os, time

from sklearn.svm import LinearSVC
from sklearn import decomposition

import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt
import warnings
import cv2


Rsol = 30




def vectorize_test(Y):
    ht, wd = np.shape(Y)
    if (ht > wd):
        y = Rsol
        x = int(round((Rsol*wd)/float(ht)))
    else:
        x = Rsol
        y = int(round((Rsol*ht)/float(wd)))

    # print Y
    # print np.shape(Y), x, y
    Y = cv2.resize(Y, (x,y))

    v = np.zeros((Rsol, Rsol), dtype=int)
    v[0:y,0:x] = Y

    v = np.reshape(v, Rsol*Rsol)
    v = map(int, v)
    return np.array(v)

def get_HoG(xs, size_cell=4, size_block=4, orientation=7):
    hog_xs = []
    for x in xs:
        fd = hog(x.reshape((Rsol, Rsol)),
                    orientations=orientation,
                    pixels_per_cell=(size_cell, size_cell),
                    cells_per_block=(size_block, size_block), visualise=False)
        hog_xs.append(fd)
    return hog_xs



def get_class(clf, im):
    lblMap = {0: 'Person', 1: 'Bicycle', 2: 'Motorcycle',3: 'Rickshaw',4: 'Autorickshaw',5: 'Car'}
    
    X_test = vectorize_test(im)
    X_test = [X_test]
    y_pred = clf.predict(get_HoG(X_test))
    return lblMap[y_pred[0]]




def get_clf():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)

        extnsn = "_grey_ftr.csv"

        train_dir = "CSVs/train_dir"

        X_train_o = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
        y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)

        X_train = get_HoG(X_train_o)

        clf = LinearSVC()
        clf.fit(X_train, y_train)
        return clf

