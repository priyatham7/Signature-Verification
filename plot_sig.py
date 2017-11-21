import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline


#Path of DataSet : change to location of DataSet
paths  = "VisualSubCorpus/GENUINE/SESSION1/001_1_1.sig";
#paths  = "InterpolatedDataSet/GENUINE/SESSION1/001_1_1.sig"
#paths = "VisualSubCorpus/FORGERY/001_f_1.sig"

#Path of the folder where you want to save interpolated DataSet : change to destination folder
folername = "InterpolatedDataSet/GENUINE/SESSION1"
#folername = "InterpolatedDataSet/FORGERY"


#Function to resample the DataSet
def plotdata():
	#Open file from given paths
	#print paths
	x = []
	y = []

	f = open(paths, "r")

	count = 0
	for line in f:
		if (count < 2):
			count += 1
			continue
		data = line.split(" ")
		x.append(int(data[0]))
		y.append(int(data[1]))

	#Need to see smooth line; not working properly
	#length = len(x)
	#x = np.array(x)
	#y = np.array(y)

	#xnew = np.linspace(x.min(), x.max(), length)
	#p_smooth = spline(x, y, xnew)
	
	plt.scatter(x, y)
	plt.show()

plotdata()