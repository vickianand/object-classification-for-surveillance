#!/usr/bin/python

import sys, os, time
# from mnist import MNIST

# from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt

extnsn = "_grey_ftr.csv"
Rsol = 30

print "LinearSVC results for ", extnsn, " with feature and resolution = ", Rsol

train_dir = "CSVs/" + sys.argv[1].rstrip('/')
test_dir = "CSVs/" + sys.argv[2].rstrip('/')


def get_HoG(xs, size_cell, size_block, orientation):
    hog_xs = []
    for x in xs:
        fd = hog(x.reshape((Rsol, Rsol)),
                    orientations=orientation,
                    pixels_per_cell=(size_cell, size_cell),
                    cells_per_block=(size_block, size_block), visualise=False)
        hog_xs.append(fd)
    return hog_xs

X_train, y_train = [], []
X_test, y_test = [], []


def build_data_sets(size_cell=3, size_block=3, orientation=7):
    global X_train, y_train, X_test, y_test
    
    X_train = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
    y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
    X_test =  genfromtxt(test_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
    y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)


    X_train = get_HoG(X_train, size_cell, size_block, orientation)
    X_test = get_HoG(X_test, size_cell, size_block, orientation)



def get_svc_results(num_estimators=10):
    
    global X_train, y_train, X_test, y_test

    # clf = RandomForestClassifier(n_estimators=num_estimators, n_jobs=2)
    clf = LinearSVC()

    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    mean_accuracy = clf.score(X_test, y_test)
    
    print "Mean accuracy: \t", mean_accuracy
    # print "confusion matrix: \n", metrics.confusion_matrix(y_test, y_pred), "\n"

    return mean_accuracy


import warnings
import matplotlib.pyplot as plt


if __name__ == "__main__":
    start_time = time.time()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        

        # rang = range(3, 12)
        # ans = []
        # for i in rang:

        #     build_data_sets(orientation=i)
        #     nTrain, nTest = len(y_train), len(y_test)
            
        #     print "size of training-set, test-set = ", nTrain, ", ", nTest
        #     print "HoG Params: orientations = ", i, ", pixels_per_cell = ", 4, ", cells_per_block = ", 3
        #     print "Dimension of feature vectors = ", len(X_train[0])        
        #     ans.append(get_svc_results(num_estimators=i))
        #     print "------------------------------------------------------"
        # print ans

        # Best accuracy came out for orientations = 7
        rang = range(1, 10)
        ans = []
        for i in rang:

            build_data_sets(size_cell=i)
            nTrain, nTest = len(y_train), len(y_test)
            
            print "size of training-set, test-set = ", nTrain, ", ", nTest
            print "HoG Params: orientations = ", 7, ", pixels_per_cell = ", i, ", cells_per_block = ", 3
            print "Dimension of feature vectors = ", len(X_train[0])        
            ans.append(get_svc_results())
            print "------------------------------------------------------"
        print ans

        param = "HoG_Cell-Size"

        plt.plot(rang, ans, linewidth=2.0)
        plt.xlabel(param)
        plt.ylabel("mean accuracy")
        figdir = 'SVC_figs'
        if not os.path.exists(figdir):
            os.mkdir(figdir)
        plt.savefig(figdir+"/" +param +".png")
        plt.close()

    print "\n~~~~~~~~~~~~~~~~~~ total time taken = %s seconds ~~~~~~~~~~~~~~~~~~\n" %(time.time() - start_time)

