import math
import os
import glob
import ntpath
import pandas as pd
import numpy as np

#Path of DataSet : change to location of DataSet (if needed)
SOURCE_PATH  = "Feature_Vector_Bin/GENUINE/SESSION1";
#SOURCE_PATH  = "Feature_Vector_Bin/GENUINE/SESSION2";
#SOURCE_PATH  = "Feature_Vector_Bin/FORGERY";
#SOURCE_PATH  = "Feature_Vector_Bin/VALIDATION/VALIDATION_GENUINE";
#SOURCE_PATH  = "Feature_Vector_Bin/VALIDATION/VALIDATION_FORGERY";

#Path of the folder where you want to save feature vector for DataSet : change to destination folder
DESTINATION_PATH  = "Feature_Template/GENUINE/SESSION1";
#DESTINATION_PATH  = "Feature_Template/GENUINE/SESSION2";
#DESTINATION_PATH  = "Feature_Template/FORGERY";
#DESTINATION_PATH  = "Feature_Template/VALIDATION/VALIDATION_GENUINE";
#DESTINATION_PATH  = "Feature_Template/VALIDATION/VALIDATION_FORGERY";

#os.makedirs to make directories recursively
if not os.path.exists(DESTINATION_PATH):
	os.makedirs(DESTINATION_PATH);    

max_no_of_users = 116			#Maximum no of user in dataset in 115
max_no_of_files_per_user = 10   #Maximum no of file per user in dataset is 10

#Calculate feature vector for all files in list
def makeFeatureVector(filelist):
	base = "_1_"	#For SESSION on base _1_; For SESSION2 _2_;  for FORGERY _f_
	base1 = ""
	person = 1
	stringperson = str(person)
	instance = 1	#It represet will file no is current explored
	footer = ".sig" #Extesion for datasets (Feature Vector file)
	
	#While feature vectors of all user are not made
	while( person <= max_no_of_users ):
		outstring = []
		if (person<10):
			base1 = "00"
		elif (person <100):
			base1 = "0"
		else:
			base1 = ""
			
		#Create base file name
		final = base1 + str(person) + base + str(instance) + footer
		finalfilestring = SOURCE_PATH + "/" + final
		
		if (final in filelist):	#If file is present for current person
			if (instance == 1):
				finalfile = np.array([])
				df = pd.read_csv(finalfilestring,sep=',', header = None, nrows = 1)
				tempfile = np.asarray(df).squeeze() 
				finalfile = np.hstack((finalfile,tempfile))
				df = ""
				tempfile = ""
				
				final = base1 + str(person) + base + str(instance) + footer
				finalfilestring = SOURCE_PATH + "/" + final
				instance = instance + 1
			if ( instance < 11 and instance != 1 ):
				df = pd.read_csv(finalfilestring,sep=',', header = None, nrows = 1)
				tempfile = np.asarray(df).squeeze() 
				finalfile = np.vstack((finalfile,tempfile))
				df = ""
				tempfile = ""
				#print "Making Feature Template for person " + str(person)
				instance = instance + 1

		else:
			if (instance == 11):	#If all files (total 10 files per users) are explored - make feature template
				print "Making Feature Template for person " + str(person)
				df_1 = pd.DataFrame(finalfile)
				temp2 = str(DESTINATION_PATH + "/" + str(person) + ".sig")	#Destination for feature template
				df_1.to_csv(temp2, index=False, header=None) 
			person = person + 1	#Go for next person
			instance = 1	#Start exploring from first file

#Function to make list for all files and calling makeFeatureVector for those files
def makeFileList():
	filenames = glob.glob(SOURCE_PATH + "/*.sig")
	filelist = []
	for filename in filenames:
		filelist.append( ntpath.basename(filename) )
	makeFeatureVector(filelist)

makeFileList()  
