#!/bin/python
"""
Title: signalP_Parser__v2.py
Date: 2022-03-01
Authors: Virág Varga

Description:
	This program parses the SignalP summary search results and creates an output
		text file containing selected categories of information	for each query sequence.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Creating a dictionary containing the pertinent results of the SignalP
		search file.
	3. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This SignalP results parser is made specifically to suit the formatting
		of the SignalP search output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version:
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop.
	More significant alterations were made to the bulk of the program - efficency of
		use was improved by the use of pandas.

Usage
	./signalP_Parser__v2.py input_file
	OR
	python signalP_Parser__v2.py input_file

This script was written for Python 3.8.10, in Spyder 5.0.5.

"""


#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows manipulation of dataframes

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit_summary.signalp5"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_SignalP.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_SignalP.txt"


#Part 2: Import the data into a Pandas dataframe

#read in the input text file, assigning the second row as a header row
#this means using Pythonic index 1
signal_df = pd.read_csv(input_file, sep='\t', header=1)
#remove the # and space from the name of the first column, and rename it to 'Query'
#this is done to match other files
signal_df.rename(columns={'# ID': 'Query', 'SP(Sec/SPI)': 'SP_Probability'}, inplace=True)
#set the column containing the query IDs as the index
signal_df.set_index('Query')


#Part 3: Filter the Pandas dataframe

#remove query sequences without predictions
filt_signal_df = signal_df[signal_df.Prediction != "OTHER"].copy()


#Part 4: Create output with prediction probabilities

#create a new dataframe containing only the desired columns
pred_signal_df = filt_signal_df[['Query', 'Prediction', 'SP_Probability']].copy()
#write out the results to a tab-separated file
pred_signal_df.to_csv(output_file, sep='\t', index=False)
