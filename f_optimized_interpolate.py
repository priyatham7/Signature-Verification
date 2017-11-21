import os
import glob
import ntpath
import pandas as pd

#Path of DataSet : change to location of DataSet
#SOURCE_PATH = "VisualSubCorpus/GENUINE/SESSION1/*.sig";
#SOURCE_PATH = "VisualSubCorpus/GENUINE/SESSION2/*.sig";
SOURCE_PATH = "VisualSubCorpus/FORGERY/*.sig"
#SOURCE_PATH = "VisualSubCorpus/VALIDATION/VALIDATION_FORGERY/*.sig"


#Path of the folder where you want to save interpolated DataSet : change to destination folder
#DESTINATION_PATH = "InterpolatedDataSet/GENUINE/SESSION1"
#DESTINATION_PATH = "InterpolatedDataSet/GENUINE/SESSION2"
DESTINATION_PATH = "InterpolatedDataSet/FORGERY"
#DESTINATION_PATH = "InterpolatedDataSet/VALIDATION/VALIDATION_FORGERY"

#os.makedirs to make directories recursively
if not os.path.exists(DESTINATION_PATH):
	os.makedirs(DESTINATION_PATH);     

SampleInterval = 10     		#Interval between two consecutive data entries

#Calculate |a-b|
def distance(a, b):
	return abs(a-b)

#Main interpolate function
def interpolate(k0, k1, sample, out):   #  k0------------------------k1
	x0 = int(k0[0])		#x coordinate
	y0 = int(k0[1])		#y coordinate
	t0 = int(k0[2])		#time coordinate
	p0 = int(float(k0[3]))		#pressure coordinate

	x1 = int(k1[0])		#x coordinate
	y1 = int(k1[1])		#y coordinate
	t1 = int(k1[2])		#time coordinate
	p1 = int(float(k1[3]))		#pressure coordinate

	if( x0 > x1):
		x0, x1 = x1, x0
	if( y0 > y1):
		y0, y1 = y1, y0
	if( t0 > t1):
		t0, t1 = t1, t0
	if( p0 > p1):
		p0, p1 = p1, p0
	
	if( t0 == t1 ):
		x = int( (x0 + x1)/2.0 + 0.5 )
		y = int( (y0 + y1)/2.0 + 0.5 )
		p = int( (p0 + p1)/2.0 + 0.5 )
	else:
		#Interpolate point; We have used linear interpolation. All coordinates are integer (pixels are integer)
		x = int( x0 + ( (x1-x0)*(sample-t0)*1.0 ) / ((t1-t0)*1.0) + 0.5 ) #added 0.5 to roundoff
		y = int( y0 + ( (y1-y0)*(sample-t0)*1.0 ) / ((t1-t0)*1.0) + 0.5 )
		p = int( p0 + ( (p1-p0)*(sample-t0)*1.0 ) / ((t1-t0)*1.0) + 0.5 )

	#Make a temporary string to write in file
	temp = str(x) + " " + str(y) + " " + str(sample) + " " + str(p) + '\n'
	out.write(temp)

def calculateData( data, sample, out):
	d1 = data[0].split(" ")  #d1[0]->x,  d1[1]->y  , d1[2]->time, d1[3]->pressure
	d2 = data[1].split(" ")
	d3 = data[2].split(" ")
	d4 = data[3].split(" ")

	#Check if sample lie b/w d1-d2 or d2-d3 or d3-d4
	minDistance, minValue = 0, 0

	mid = int(d1[2]) + (int(d2[2])- int(d1[2]) )/2.0  #mid of first interval
	minDistance = distance(mid, sample)
	minValue = 1
	
	mid = int(d2[2]) + ( int(d3[2]) - int(d2[2]) )/2.0  #mid of second interval
	if( distance(mid, sample) <= minDistance ):
		minDistance = distance(mid, sample)
		minValue = 2									#2nd interval is choosen

	mid = int(d3[2]) + ( int(d4[2]) - int(d3[2]) )/2.0  #mid of third interval
	if( distance(mid, sample) <= minDistance ):
		minDistance = distance(mid, sample)
		minValue = 3									#3rd interval is choosen
	
	#it does not matter wheather you do left, right or interpolate :-)
	if( minValue == 1 ):							#if first invterval is selected
		interpolate(d1, d2, sample, out)
	elif( minValue == 2 ):							#if second invterval is selected
		interpolate(d2, d3, sample, out)
	elif( minValue == 3 ):							#if third invterval is selected
		interpolate(d3, d4, sample, out)

#Function to resample/interpolate the DataSet
def resampleData():
	#Open file from given SOURCE_PATH
	filenames = glob.glob(SOURCE_PATH)
	left =  len(filenames)
	for filename in filenames:
		data = []
		testCase = []

		f = open(filename,"r")
		target_file = ntpath.basename(filename)   #To get basename of file
		path = DESTINATION_PATH + "/" + target_file      #Location where we want to save the file
		out = open( path, "w")				#Open file for writing

		out.write("Interpolated DataSet\n")
		out.write("x	y	t   p\n")
		
		if(left > 1):
			print str(left) + " files are left. Interpolating " + target_file
		else:
			print str(left) + " file is left. Interpolating " + target_file

		left = left - 1

		count = 0							#Count is used to just skip first two lines in DataSet
		index = 0							#First two lines are headers
		for line in f:
			if ( count < 2):				#Skip first two lines in input file
				count += 1
				continue
			if ( index == 0 ):				#Write first line as it is in output file
				out.write(line)
			index += 1
			data.append(line)				#Add reset lines to a list for further calculations

		testCase = data[1:5]				#Pick first 4 data entries from list
		sample = SampleInterval	+ 0			#Interval between two consecutive data entries
		length =  len(data) - 2
		index = 0

		while( index < length ):
			line1 = data[index].split(" ")        #Split the data based on seperator (blank space)
			line2 = data[index+1].split(" ")

			if( int(line1[2]) <= sample <= int(line2[2]) ):  #If sample lie b/w two data entries
				#testCase = data[index-1:index+3]
				testCase[0] = data[index-1]
				testCase[1] = data[index]
				testCase[2] = data[index+1]
				testCase[3] = data[index+2]
				#print testCase
				calculateData(testCase, sample, out)
				sample = sample + SampleInterval
			elif sample < int(line1[2]):
				sample = sample + SampleInterval
			else:
				index = index + 1;

		#Addition of last two data entries
		calculateData(testCase, sample, out)
		calculateData(testCase, sample+SampleInterval, out)

		f.close() 			#close input file
		out.close() 		#close output file

resampleData()
