import math
import os
import glob
import ntpath
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt


#Path of Feature Template : change to location of DataSet (if needed)
genuine_path = "Feature_Template/GENUINE/SESSION1/"
forgery_path = "Feature_Template/FORGERY/"

max_no_of_users = 116 #total no of users

def classifier(genuinefilelist, forgeryfilelist):
	finalscore = 0
	counter = 1
	max_no_of_users = 116
	finalscore = 0
	finalfirst1 = 0
	finalfirst2 = 0
	finalsecond1 = 0
	finalsecond2 = 0
	finalcm = np.matrix('0 0; 0 0')


	while ( counter <= max_no_of_users ):
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
			#clf = svm.SVC(kernel='poly', C=2.2).fit(X_train, Y_train)
			clf = RandomForestClassifier(n_estimators=500 ,verbose = 1).fit(X_train, Y_train)
			
			score = clf.score(X_test, Y_test)
			print("Actual Value : "),
			print(Y_test)
			print("Predicted Value : "),
			print(clf.predict(X_test))
			finalscore = finalscore + score	
			preds = clf.predict(X_test)
			#print ("Correct Results")
			#print (Y_test)
			#print ("Predicted Results")
			#print (preds)
			#finalscore = finalscore + score	
			print("For File " + temp1 + " " +str(score) )

			df_X = ""
			df_Y = ""
			cm = confusion_matrix(Y_test, preds)
			finalcm = finalcm + cm

			first1 = cm.item(0)
			first2 = cm.item(1)
			second1 = cm.item(2)
			second2 = cm.item(3)
			print "Confusion Matrix : "
			print (cm)
			finalfirst1 = finalfirst1 + first1
			finalfirst2 = finalfirst2 + first2
			finalsecond1 = finalsecond1 + second1
			finalsecond2 = finalsecond2 + second2

			print "SCORE for user " + str(counter) + " : " + str(score)
			
			df_X = ""
			df_Y = ""
		counter = counter + 1

	length = len(genuinefilelist)
	print "Accuracy for Random Forest classifier : ",
	print (finalscore/length)*100
	print (finalfirst1)
	print (finalfirst2)
	print (finalsecond1)
	print (finalsecond2)
	print (finalcm)
	#finalcm = np.matrix('276 48; 69 297')
	plt.matshow(finalcm)
	plt.title('Confusion matrix')
	plt.colorbar()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
	plt.show()

	
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
