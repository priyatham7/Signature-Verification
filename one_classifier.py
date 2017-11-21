import math
import os
import glob
import ntpath
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier


#Path of Feature Template : change to location of DataSet (if needed)
genuine_path = "Feature_Template/GENUINE/oneuser/"
forgery_path = "Feature_Template/FORGERY/oneuser/"

max_no_of_users = 116 #total no of users

def classifier(genuinefilelist, forgeryfilelist):
	finalscore = 0
	counter = 116
	max_no_of_users = 116
	print("in classifier")
	while ( counter <= max_no_of_users ):
		print("hello1")
		if (counter<10):
			base1 = "00"
		elif (counter <100):
			base1 = "0"
		else:
			base1 = ""

		temp1 = str(counter) + ".sig"
		temp2 = str(counter) + ".sig"
		
		finalgenuinepath = genuine_path + temp1
		finalforgerypath = forgery_path + temp2

		if (temp1 in genuinefilelist and temp2 in forgeryfilelist):
			dfgenuine = pd.read_table(finalgenuinepath, sep=',',header=None)
			dfforgery = pd.read_table(finalforgerypath, sep=',',header=None)
			
			df_X = dfgenuine.append(dfforgery)
			df_Y = df_X[[300]]	#index 300, as 0-99:x-features; 100-199:y-features; 200-299:p-features; 300th bit for genuine or forgery user

			del df_X[300]	#Delete last bit
			
			df_Y = np.asarray(df_Y).squeeze()
			
			X_train, X_test, Y_train, Y_test = train_test_split(df_X, df_Y, test_size=0.3, random_state=1)
			
			#clf = MLPClassifier(solver='lbfgs', alpha=0.1, random_state=1,hidden_layer_sizes=(256, 128, 64)).fit(X_train, Y_train)
			clf = svm.SVC(kernel='poly', C=2.2).fit(X_train, Y_train)
			
			score = clf.score(X_test, Y_test)
			print("actual")
			print(Y_test)
			print("predicted")
			print(clf.predict(X_test))
			finalscore = finalscore + score	
			
			print "SCORE for user " + str(counter) + " : " + str(score)
			
			df_X = ""
			df_Y = ""
		counter = counter + 1

	length = len(genuinefilelist)
	print (finalscore/length)
	
#Function for testing all files
def testing():
	filenames = glob.glob(genuine_path + "*.sig")
	genuinefilelist = []
	for filename in filenames:
		filen = ntpath.basename(filename) #getting the base filename
		genuinefilelist.append(filen)
	#print genuinefilelist[0]

	filenames = glob.glob(forgery_path + "*.sig")
	forgeryfilelist = []
	for filename in filenames:
		filen = ntpath.basename(filename) #getting the base filename
		forgeryfilelist.append(filen)
	#print forgeryfilelist[0]

	classifier(genuinefilelist, forgeryfilelist)

testing()
