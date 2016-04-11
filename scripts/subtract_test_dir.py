#!/usr/bin/python

import os, sys, shutil

train = "train_dir"
test = "test_dir"
count = 0
for sd in os.listdir(train):
		ptrain = os.path.join(train, sd)
		ptest = os.path.join(test, sd)
		l2 = os.listdir(ptest)
		for i in l2:
			im = os.path.join(ptrain, i)
			try:
				os.remove(im)
				count += 1
			except:
				continue
print count, " images removed"