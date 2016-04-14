#!/usr/bin/python

import sys, os, time

from sklearn.neighbors import KNeighborsClassifier
from sklearn import decomposition

import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt

extnsn = "_grey_ftr.csv"
Rsol = 30

# train_dir = "CSVs/" + sys.argv[1].rstrip('/'z)
# test_dir = "CSVs/" + sys.argv[2].rstrip('/')

train_dir = "CSVs/train_dir"
test_dir = "CSVs/test_dir"

X_train, y_train = [], []
X_test, y_test = [], []

X_train_o = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
X_test_o =  genfromtxt(test_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)

print np.shape(X_test_o), ", ",np.shape(X_train_o)

def get_HoG(xs, size_cell=4, size_block=4, orientation=7):
    hog_xs = []
    for x in xs:
        fd = hog(x.reshape((Rsol, Rsol)),
                    orientations=orientation,
                    pixels_per_cell=(size_cell, size_cell),
                    cells_per_block=(size_block, size_block), visualise=False)
        hog_xs.append(fd)
    return hog_xs


X_train, X_test = X_train_o, X_test_o
# X_train, X_test = get_HoG(X_train_o), get_HoG(X_test_o)


# def get_PCA(Xs, n_components):
#     pca = decomposition.PCA(n_components=n_components)
#     print "PCA: n_features = ", len(Xs[0]),
#     # pca.fit(Xs)
#     Xs1 = pca.fit_transform(Xs)
#     print "PCA: n_components = ", len(Xs1[0]),
#     return Xs1


import warnings
import matplotlib.pyplot as plt


if __name__ == "__main__":
    start_time = time.time()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        