#!/usr/bin/python

import os, warnings
import matplotlib.pyplot as plt

extnsn = "_grey_"
Rsol = 50

xlabel = "max_depth(1000 is for None)"
figdir = 'DT_figs'


ylabel = "mean accuracy"
rang = 	rang = [10, 20, 50, 100, 200, 400, 1000]


ans = [	
	0.497884344147
,	0.527503526093
,	0.503526093089
, 	0.521861777151
, 	0.504936530324
, 	0.524682651622
,	0.514809590973]


plt.plot(rang, ans, linewidth=2.0)
plt.xlabel(xlabel)
plt.ylabel(ylabel)
if not os.path.exists(figdir):
    os.mkdir(figdir)
# plt.title("KNN, "+extnsn+", resolution="+str(Rsol))
plt.axis([0,400, 0.45, 0.55])
plt.savefig(figdir+"/" +xlabel +".png")

plt.close()
