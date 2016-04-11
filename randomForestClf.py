#!/usr/bin/python

import sys, os, time
# from mnist import MNIST
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt

# extnsn = "_grey_ftr.csv"
extnsn = "_clr_ftr.csv"
Rsol = 30


print "RandomForestClassifier results for ", extnsn, " with feature and resolution = ", Rsol

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

def build_data_sets(size_cell=4, size_block=3, orientation=3):
    global X_train, y_train, X_test, y_test
    
    X_train = genfromtxt(train_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
    y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
    X_test =  genfromtxt(test_dir +  str(Rsol) + extnsn, delimiter=',', dtype=int)
    y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)

    X_train = get_HoG(X_train, size_cell, size_block, orientation)
    X_test = get_HoG(X_test, size_cell, size_block, orientation)

    # print len(X_train[0])
    # sys.exit()


def get_rf_results(num_estimators=10):
    
    global X_train, y_train, X_test, y_test

    clf = RandomForestClassifier(n_estimators=num_estimators, n_jobs=2)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    mean_accuracy = clf.score(X_test, y_test)
    print "Number of trees in forest = ", num_estimators
    
    print "Mean accuracy: \t", mean_accuracy
    print "confusion matrix: \n", metrics.confusion_matrix(y_test, y_pred), "\n"

    return mean_accuracy


import warnings
import matplotlib.pyplot as plt


if __name__ == "__main__":
    start_time = time.time()
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",category=DeprecationWarning)
        
        build_data_sets()
        nTrain, nTest = len(X_train), len(X_test)
        
        print "size of training-set, test-set = ", nTrain, ", ", nTest
        print "HoG Params: orientations = ", 3, ", pixels_per_cell = ", 4, ", cells_per_block = ", 3
        print "following are the results on varying the number of estimators :\n-----------------------------------"
        rang = range(25, 126, 25)
        ans = []
        for i in rang:
            ans.append(get_rf_results(num_estimators=i))
        plt.plot(rang, ans, linewidth=2.0)
        plt.xlabel("number of trees")
        plt.ylabel("mean accuracy")
        plt.title("RandomForestClassifier, "+extnsn+", resolution="+str(Rsol))
        plt.savefig("RF_figs/num_estimators_"+str(Rsol) + extnsn+".png")
        plt.close()

    print "\n~~~~~~~~~~~~~~~~~~ total time taken = %s seconds ~~~~~~~~~~~~~~~~~~\n" %(time.time() - start_time)
