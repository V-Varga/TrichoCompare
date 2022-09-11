#!/bin/python
"""
Title: deepLoc_Parser__v2.py
Date: 2022-03-02
Authors: Virág Varga

Description:
	This program parses the DeepLoc search results and creates an output
		text file containing selected categories of information	for each query sequence.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas
	numpy

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Importing the data into a Pandas dataframe. 
	3. Writing out a version of the dataframe containing only the query IDs, the 
		predicted localization, and the probability of said localization. 

Known bugs and limitations:
	- This DeepLoc results parser is made specifically to suit the formatting
		of the DeepLoc search output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version: 
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop. 
	More significant alterations were made to the bulk of the program - efficency of 
		use was improved by the use of pandas. In addition, more columns were extracted
		for the more significant breadth of the Thesis project vs. the preliminary
		exploratory project. 

Usage
	./deepLoc_Parser__v2.py input_file
	OR
	python deepLoc_Parser__v2.py input_file

This script was written for Python 3.8.10, in Spyder 5.0.5.

"""


#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows manipulation of dataframes
import numpy as np #allows numerical manipulations, empty dataframe columns

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_DL.txt"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_DeepLocP.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_DeepLocP.txt"


#Part 2: Import the data into a Pandas dataframe

#read in the input text file, assigning the first row as a header row
#this means using Pythonic index 0
deeploc_df = pd.read_csv(input_file, sep='\t', header=0)
#rename the first column to 'Query' to match the other files
deeploc_df.rename(columns={'ID': 'Query'}, inplace=True)
#set the column containing the query IDs as the index
#deeploc_df.set_index('Query')

#create a list of columns
pred_list = list(deeploc_df)
#filter the list down to only the prediction category headers
pred_list = pred_list[2:]


#Part 3: Create output with prediction probabilities

#create an empty column at the end filled with NaN
deeploc_df['Probability'] = np.nan

for pred in pred_list:
	#iterate over the list of possible prediction locations
	deeploc_df.loc[deeploc_df['Location']==pred, 'Probability'] = deeploc_df[pred]
	#when the predicted location of the protein query matches a protein location in the list
	#copy the prediction probability for that location from the appropriate column
	#into the Probability column at the end

#create a new dataframe containing only the desired columns
final_deeploc_df = deeploc_df[['Query', 'Location', 'Probability']].copy()
#write out the results to a tab-separated file
final_deeploc_df.to_csv(output_file, sep='\t', index=False)
