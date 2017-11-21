import math
import os
import glob
import ntpath

#Path of DataSet : change to location of DataSet (if needed)
#SOURCE_PATH  = "FeatureSet/GENUINE/SESSION1/*.sig";
#SOURCE_PATH  = "FeatureSet/GENUINE/Testing/forgery/*.sig";
#SOURCE_PATH  = "FeatureSet/GENUINE/SESSION2/*.sig";
SOURCE_PATH  = "FeatureSet/FORGERY/*.sig";
#SOURCE_PATH  = "FeatureSet/VALIDATION/VALIDATION_GENUINE/*.sig";
#SOURCE_PATH  = "FeatureSet/VALIDATION/VALIDATION_FORGERY/*.sig";

#Path of the folder where you want to save feature vector for DataSet : change to destination folder
#DESTINATION_PATH  = "Feature_Vector/GENUINE/SESSION1"
#DESTINATION_PATH  = "Feature_Vector/GENUINE/Testing/forgery"
#DESTINATION_PATH  = "Feature_Vector/GENUINE/SESSION2"
DESTINATION_PATH  = "Feature_Vector/FORGERY"
#DESTINATION_PATH  = "Feature_Vector/VALIDATION/VALIDATION_GENUINE"
#DESTINATION_PATH  = "Feature_Vector/VALIDATION/VALIDATION_FORGERY"

#lastbit = 0 #This will be appended at the end of the file and indicate wheather the file is genuine or forgery

#os.makedirs to make directories recursively
if not os.path.exists(DESTINATION_PATH):
	os.makedirs(DESTINATION_PATH)    

no_of_bins = 100   #Fixed for now

#Function which will make a feature vector from extracted features
def makeFeatureVector(input_file, output_file):
	f = open(input_file,"r")
	
	x_data = []		#Temporary list to store data from input file
	y_data = []
	p_data = []
	
	count = 0

	for line in f:
		if( count < 2 ):	#Skip first two lines
			count += 1
			continue
		temp_data = line.split(" ");
		x_data.append( int(temp_data[0]) )
		y_data.append( int(temp_data[1]) )
		p_data.append( int(temp_data[3]) )

	f.close() 

	minX = min(x_data)	#Minimum value of x coordinate
	maxX = max(x_data)	#Maximum value of x coordinate

	minY = min(y_data)	#Minimum value of y coordinate
	maxY = max(y_data)	#Maximum value of y coordinate

	minP = min(p_data)	#Minimum value of pressure
	maxP = max(p_data)	#Maximum value of pressure
	
	#Total no of bins required
	bin_x_size = math.ceil( (maxX - minX)/( no_of_bins*1.0) )
	bin_y_size = math.ceil( (maxY - minY)/( no_of_bins*1.0) )
	bin_p_size = math.ceil( (maxP - minP)/( no_of_bins*1.0) )

	#List to store frequencies of the feature vectors
	x_bin = [0]*( no_of_bins )
	y_bin = [0]*( no_of_bins )
	p_bin = [0]*( no_of_bins )

	out = open( output_file, "w")
	
	for i in range(0, len(x_data)):
		count = 1
		while( int(x_data[i]) > minX + count*bin_x_size): #finding right position in bin for x feature element
			count += 1
		x_bin[ count-1 ] += 1
		
	for i in range(0, len(y_data)):
		count = 1
		while( int(y_data[i]) > minY + count*bin_y_size): #finding right position in bin for x feature element
			count += 1
		y_bin[ count - 1 ] += 1

	for i in range(0, len(p_data)):
		count = 1
		while( int(p_data[i]) > minP + count*bin_p_size): #finding right position in bin for x feature element
			count += 1
		p_bin[ count - 1 ] += 1
		
	for i in range(0, no_of_bins):  #writing x feature element to feature file
		temp = str(x_bin[i])
		out.write(temp + "\n")

	for i in range(0, no_of_bins):	#writing y feature element to feature file
		temp = str(y_bin[i])
		out.write(temp + "\n")

	for i in range(0, no_of_bins): #writing p feature element to feature file
		temp = str(p_bin[i])
		out.write(temp + "\n")
	
	out.close() 					 #close output file

#Function to make feature vector for each file
def feature_vector():
	filenames = glob.glob(SOURCE_PATH)
	left = len(filenames)
	for filename in filenames:
		target_file = ntpath.basename(filename) #getting the base filename
		path = DESTINATION_PATH + "/" + target_file    #creating path for the file
		
		if(left > 1):
			print str(left) + " files are left. Making Features Vector of " + target_file
		else:
			print str(left) + " file is left. Making Features Vector of " + target_file

		makeFeatureVector(filename, path)

		left = left - 1

feature_vector()  
