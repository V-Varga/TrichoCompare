#!/bin/python
"""
Title: mitoFates_Parser__v2.py
Date: 2022-03-01
Authors: Virág Varga

Description:
	This program parses the MitoFates summary search results and creates an output
		text file containing selected categories of information	for each query sequence.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Importing the data into a Pandas dataframe.
	3. Filtering the dataframe to only include the desired columns of rows with
		proteins predicted to be targeted to the mitochonrion.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This MitoFates results parser is made specifically to suit the formatting
		of the MitoFates search output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version:
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop.

Usage
	./mitoFates_Parser__v2.py input_file
	OR
	python MitoFates_Parser__v2.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows the easy manipulation of dataframes in Python

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit_StandardAA_nonM_MFresults.txt"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_MFparsed.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_edit_StandardAA_nonM_MFresults_MFparsed.txt"


#Part 2: Importing the dataframe into Pandas

#read in the input text file, assigning the first row as a header row
mito_df = pd.read_csv(input_file, sep='\t', header=0, index_col=(False))
#replace spaces (' ') in column headers with underscores ('_')
mito_df.columns = mito_df.columns.str.replace(' ', '_')
#rename the first column header to 'Query' in order to match other files
mito_df.rename(columns={'Sequence_ID': 'Query'}, inplace=True)


#Part 3: Filter the database to include only desired rows and columns, reformatted

#filter out the results without a mitochondrial presequence
filt_mito_df = mito_df[mito_df.Prediction != "No mitochondrial presequence"].copy()
#remove all but first 3 columns
filt_mito_df  = filt_mito_df.iloc[: , :3]
#reorder columns
filt_mito_df = filt_mito_df[['Query', 'Prediction', 'Probability_of_presequence']]


#Part 4: Write out the results to a tab-separated file

#write out the results to a tab-separated text file
filt_mito_df.to_csv(output_file, sep='\t', index=False)
