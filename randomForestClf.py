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

train_dir = "CSVs/" + sys.argv[1]
test_dir = "CSVs/" + sys.argv[2]


Rsol = 200


def get_HoG(xs, size_cell, size_block, orientation):
    hog_xs = []
    for x in xs:
        fd = hog(x.reshape((Rsol, Rsol)),
                    orientations=orientation,
                    pixels_per_cell=(size_cell, size_cell),
                    cells_per_block=(size_block, size_block), visualise=False)
        hog_xs.append(fd)
    return hog_xs



def get_balanced_sets(labels, n):
    m = len(labels)
    if n == m:
        return np.arange(n)

    q = n/10
    r = n - q*10
    nums = [q for i in range(10)]
    for i in range(10):
        if i < r: nums[i] += 1
    idxs = []

    for i in range(m):
        if nums[labels[i]] > 0:
            nums[labels[i]] -= 1
            idxs.append(i)
    return idxs

X_train, y_train = [], []
X_test, y_test = [], []

def build_data_sets(n_train=10000, n_test=1000, size_cell=4, size_block=3, orientation=3):
    global X_train, y_train, X_test, y_test
    
    X_train = genfromtxt(train_dir +  str(Rsol) +"_ftr.csv", delimiter=',', dtype=int)
    y_train = genfromtxt(train_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)
    X_test =  genfromtxt(test_dir +  str(Rsol) +"_ftr.csv", delimiter=',', dtype=int)
    y_test =  genfromtxt(test_dir +  str(Rsol) +"_lbl.csv", delimiter=',', dtype=int)




    # mnist = datasets.fetch_mldata('MNIST original')
    # features = np.array(mnist.data, 'int16')
    # labels = np.array(mnist.target, 'int')

    # train_idx = get_balanced_sets(labels[:60000], n_train)
    # test_idx = get_balanced_sets(labels[60000:], n_test)
    # for i in range(n_test):
    #     test_idx[i] += 60000

    # X_train, y_train = features[train_idx], labels[train_idx]
    # X_test, y_test = features[test_idx], labels[test_idx]



    X_train = get_HoG(X_train, size_cell, size_block, orientation)
    X_test = get_HoG(X_test, size_cell, size_block, orientation)



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
        
        nTrain, nTest = 10000, 1000
        build_data_sets()
        
        print "size of training-set, test-set = ", nTrain, ", ", nTest
        print "HoG Params: orientations = ", 3, ", pixels_per_cell = ", 4, ", cells_per_block = ", 3
        print "following are the results on varying the number of estimators :\n-----------------------------------"
        rang = range(100,111, 50)
        ans = []
        for i in rang:
            ans.append(get_rf_results(num_estimators=i))
        plt.plot(rang, ans, linewidth=2.0)
        plt.xlabel("number of trees")
        plt.ylabel("mean accuracy")
        plt.savefig("RF_figs/num_estimators.png")
        plt.close()

    print "\n~~~~~~~~~~~~~~~~~~ total time taken = %s seconds ~~~~~~~~~~~~~~~~~~\n" %(time.time() - start_time)
