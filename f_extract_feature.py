import math
import os
import glob
import ntpath

#Path of DataSet : change to location of DataSet (if needed)
#SOURCE_PATH = "InterpolatedDataSet/GENUINE/SESSION1/*.sig"
#SOURCE_PATH = "InterpolatedDataSet/GENUINE/SESSION2/*.sig"
SOURCE_PATH = "InterpolatedDataSet/FORGERY/*.sig"
#SOURCE_PATH = "InterpolatedDataSet/VALIDATION/VALIDATION_GENUINE/*.sig"
#SOURCE_PATH = "InterpolatedDataSet/VALIDATION/VALIDATION_FORGERY/*.sig"


#Path of the folder where you want to save feature of DataSet : change to destination folder
#DESTINATION_PATH  = "FeatureSet/GENUINE/SESSION1"
#DESTINATION_PATH  = "FeatureSet/GENUINE/SESSION2"
DESTINATION_PATH  = "FeatureSet/FORGERY"
#DESTINATION_PATH  = "FeatureSet/VALIDATION/VALIDATION_GENUINE"
#DESTINATION_PATH  = "FeatureSet/VALIDATION/VALIDATION_FORGERY"


#Kth order feature
kth_order = 5

#os.makedirs to make directories recursively
if not os.path.exists(DESTINATION_PATH):
	os.makedirs(DESTINATION_PATH);    

def findk(a, b):
	return int(b) - int(a)
	
#Function to calculate kth order features
def calculate(input_file, output_file):
	f = open(input_file, "r")	#Open input file
	data = []
	
	#Read input line by line
	for line in f:
		data.append(line)
	length = len(data)
	f.close()	#Close input file

	#Open output file (it is same input file)
	out = open( output_file, "w")
	
	out.write("Feature Set\n")
	out.write("xk	yk\n")

	for i in range(2, length-2):    #Skip first two lines; First two lines are header
		linei  = data[i].split(" ")
		linei1 = data[i+1].split(" ")
		xk     =  findk(linei[0], linei1[0])
		yk     =  findk(linei[1], linei1[1])
		pk     =  findk(float(linei[3]), float(linei1[3]))

		#We have reduced no of feature are training data was not that big
		'''rk = math.sqrt( xk**2 + yk**2);
		thetak = 0.0
		if( xk != 0 ):
			thetak = math.degrees( math.atan(yk/(xk*1.0)) )
		else:
			thetak = 90.0

		temp = str(xk) + " " + str(yk) +  " " + str(rk) + " " + str(thetak) + " " + str(pk) + " \n"
		'''
		temp = str(xk) + " " + str(yk) + " 0 " + str(pk) + "\n"
		out.write(temp)
				
	out.close() 		#close output file


#Function to extract kth order feature
def extract_features(k):
	filenames = glob.glob(SOURCE_PATH)

	left = len(filenames)	#Total no of files

	#Recurse through all files in SOURCE_PATH
	for filename in filenames:
		target_file = ntpath.basename(filename)			#getting the base filename
		path = DESTINATION_PATH + "/" + target_file     #creating path for the file

		if(left > 1):
			print str(left) + " files are left. Extracting Features from " + target_file
		else:
			print str(left) + " file is left. Extracting Features from " + target_file
		
		#print filename
		calculate(filename, path)
		for i in range(k-1):
			calculate(path, path) #Reading from same file(path) and writing to same file(path); first reading then writing
		left = left - 1

extract_features( kth_order )  #kth order features
