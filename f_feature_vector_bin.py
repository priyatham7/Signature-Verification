import math
import os
import glob
import ntpath
import pandas as pd
import numpy as np

#Path of DataSet : change to location of DataSet (if needed)
#SOURCE_PATH  = "Feature_Vector/GENUINE/SESSION1/";
#SOURCE_PATH  = "Feature_Vector/GENUINE/SESSION2/";
SOURCE_PATH  = "Feature_Vector/FORGERY/";
#SOURCE_PATH  = "Feature_Vector/VALIDATION/VALIDATION_GENUINE/*.sig";
#SOURCE_PATH  = "Feature_Vector/VALIDATION/VALIDATION_FORGERY/*.sig";

#Path of the folder where you want to save feature vector for DataSet : change to destination folder
#DESTINATION_PATH  = "Feature_Vector_Bin/GENUINE/SESSION1";
#DESTINATION_PATH  = "Feature_Vector_Bin/GENUINE/SESSION2";
DESTINATION_PATH  = "Feature_Vector_Bin/FORGERY";
#DESTINATION_PATH  = "Feature_Vector_Bin/VALIDATION/VALIDATION_GENUINE";
#DESTINATION_PATH  = "Feature_Vector_Bin/VALIDATION/VALIDATION_FORGERY";

#os.makedirs to make directories recursively
if not os.path.exists(DESTINATION_PATH):
	os.makedirs(DESTINATION_PATH);    

last_bit = 0	#1 for genuine user;  0 for forgery users

def makeFileList():
	filenames = glob.glob(SOURCE_PATH + "*.sig")
	for filename in filenames:
		print filename
		df = pd.read_table(filename, sep='\n',header=None)
		x = np.asarray(df[[0]]).squeeze()
		
		finalx = np.append(x, last_bit)	#For genuine files
		
		df_x = pd.DataFrame(finalx)

		target_file = ntpath.basename(filename) #getting the base filename
		df_x.transpose().to_csv(DESTINATION_PATH+"/"+target_file, index=False, header=None)

makeFileList()  
