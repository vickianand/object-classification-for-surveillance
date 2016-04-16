#!/usr/bin/python

import sys, os, time

from sklearn import decomposition

import numpy as np
from sklearn import datasets
from skimage.feature import hog
from sklearn.utils import shuffle
from sklearn import metrics
import sys
from numpy import genfromtxt
import pickle

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import matplotlib.pyplot as plt


extnsn = "_grey_ftr.csv"
# extnsn = "_clr_ftr.csv"
Rsol = 30


f = open('HOG'+str(Rsol)+extnsn+'.pickle')
X_train_hog, y_train, X_test_hog, y_test = pickle.load(f)
f.close()


f = open('plain'+str(Rsol)+extnsn+'.pickle')
X_train, y_train, X_test, y_test = pickle.load(f)
f.close()




def dt_results():
	print "--------------DecisionTreeClassifier-----------------"
	rang = [None, 10, 20, 50, 100, 200, 400]
	
	print "--------------With HOG-----------------"
	ans = []
	print "maxDepth	Accuracy"
	for i in rang:
		clf = DecisionTreeClassifier(max_depth=i)
		clf.fit(X_train_hog, y_train)
		mean_accuracy = clf.score(X_test_hog, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans
	
	print "\n--------------Without HOG-----------------"
	ans = []
	print "maxDepth	Accuracy"
	for i in rang:
		clf = DecisionTreeClassifier(max_depth=i)
		clf.fit(X_train, y_train)
		mean_accuracy = clf.score(X_test, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans


def RF_results():
	print "--------------RandomForestClassifier-----------------"
	rang = [None, 10, 20, 50, 100, 200, 400]
	
	print "--------------With HOG-----------------"
	ans = []
	print "n_estimators	Accuracy"
	for i in rang:
		clf = RandomForestClassifier(n_estimators=i)
		clf.fit(X_train_hog, y_train)
		mean_accuracy = clf.score(X_test_hog, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans
	
	print "\n--------------Without HOG-----------------"
	ans = []
	print "n_estimators	Accuracy"
	for i in rang:
		clf = RandomForestClassifier(n_estimators=i)
		clf.fit(X_train, y_train)
		mean_accuracy = clf.score(X_test, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans

def AB_results(): # AdaBoostClassifier
	print "--------------AdaBoostClassifier-----------------"
	rang = [60, 80]
	
	# print "--------------With HOG-----------------"
	# ans = []
	# print "n_estimators	Accuracy"
	# for i in rang:
	# 	clf = AdaBoostClassifier(n_estimators=i)
	# 	clf.fit(X_train_hog, y_train)
	# 	mean_accuracy = clf.score(X_test_hog, y_test)
	# 	print i, "	", mean_accuracy
	# 	ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	# print ans

	# plt.plot(rang, ans, linewidth=2.0)
	# plt.xlabel("n_estimators")
	# plt.ylabel("mean_accuracy")
	# plt.savefig("temp_hog.png")

	
	print "\n--------------Without HOG-----------------"
	ans = []
	print "n_estimators	Accuracy"
	for i in rang:
		clf = AdaBoostClassifier(n_estimators=i)
		clf.fit(X_train, y_train)
		mean_accuracy = clf.score(X_test, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans
	plt.plot(rang, ans, linewidth=2.0)
	plt.xlabel("n_estimators")
	plt.ylabel("mean_accuracy")
	plt.savefig("temp_plain.png")


def SVC_results():
	print "--------------LinearSVC-----------------"
	rang = [1]
	
	print "--------------With HOG-----------------"
	ans = []
	print "n_estimators	Accuracy"
	for i in rang:
		clf = LinearSVC()
		clf.fit(X_train_hog, y_train)
		y_pred = clf.predict(X_test_hog)
		print "confusion matrix: \n", metrics.confusion_matrix(y_test, y_pred), "\n"
		mean_accuracy = clf.score(X_test_hog, y_test)
		print i, "	", mean_accuracy
		ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	print ans


	# plt.plot(rang, ans, linewidth=2.0)
	# plt.xlabel("n_estimators")
	# plt.ylabel("mean_accuracy")
	# plt.savefig("temp_hog.png")

	
	# print "\n--------------Without HOG-----------------"
	# ans = []
	# print "n_estimators	Accuracy"
	# for i in rang:
	# 	clf = LinearSVC()
	# 	clf.fit(X_train, y_train)
	# 	mean_accuracy = clf.score(X_test, y_test)
	# 	print i, "	", mean_accuracy
	# 	ans.append('('+str(i)+", "+str(mean_accuracy)+')')
	# print ans

	# plt.plot(rang, ans, linewidth=2.0)
	# plt.xlabel("n_estimators")
	# plt.ylabel("mean_accuracy")
	# plt.savefig("temp_plain.png")



# dt_results()
# RF_results()
# AB_results()

SVC_results()