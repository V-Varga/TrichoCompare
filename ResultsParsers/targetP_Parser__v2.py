#!/bin/python
"""
Title: targetP_Parser__v2.py
Date: 2022-03-01
Authors: Virág Varga

Description:
	This program parses the TargetP summary search results and creates an output
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
	2. Importing data into a Pandas dataframe.
	3. Filtering the Pandas dataframe to exclude queries with no predicted target.
	4. Creating a new dataframe with the desired data columns, and writing out
		the results to a tab-separated text file.

Known bugs and limitations:
	- This TargetP results parser is made specifically to suit the formatting
		of the TargetP search output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version:
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop.

Usage
	./targetP_Parser__v2.py input_file
	OR
	python targetP_Parser__v2.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows manipulation of dataframes
import numpy as np #allows numerical manipulations, empty dataframe columns

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit_summary.targetp2"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_TargetP.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_TargetP.txt"


#Part 2: Import the data into a Pandas dataframe

#read in the input tsv file, assigning the first row as a header row
target_df = pd.read_csv(input_file, sep='\t', header=1)
#remove the # and space from the name of the first column, and rename it to 'Query'
#this is done to match other files
target_df.rename(columns={'# ID': 'Query'}, inplace=True)
#set the column containing the query IDs as the index
target_df.set_index('Query')


#Part 3: Filter the Pandas dataframe

#remove query sequences without predictions
filt_target_df = target_df[target_df.Prediction != "noTP"].copy()
#create an empty column at the end filled with NaN
filt_target_df['Probability'] = np.nan


#Part 4: Create output with prediction probabilities

#copy signal peptide probabilities to 'Probability' column
filt_target_df.loc[filt_target_df['Prediction']=='SP', 'Probability'] = filt_target_df['SP']
#copy mitochondrial transit peptide probabilities to 'Probability' column
filt_target_df.loc[filt_target_df['Prediction']=='mTP', 'Probability'] = filt_target_df['mTP']
#create a new dataframe containing only the desired columns
pred_target_df = filt_target_df[['Query', 'Prediction', 'Probability']].copy()
#write out the results to a tab-separated file
pred_target_df.to_csv(output_file, sep='\t', index=False)
