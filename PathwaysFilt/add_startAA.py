# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: add_startAA.py
Date: 2022-04-28
Author: Virág Varga

Description:
	This program merges the dataframe containing information on the first amino acid
		in each protein sequence into the larger Metamonad database.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Importing modules and assigning command-line arguments.
	2. Importing input data into Pandas dataframes.
	3. Merging the Metamonad and start codon dataframes and writing out the resulting
		dataframe to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but instead based on the input
		file name.

Usage
	./add_startAA.py input_db startAA_db
	OR
	python add_startAA.py input_db startAA_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import modules and assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line argument; load input and output files
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__200prots.txt"
startAA_db = sys.argv[2]
#startAA_db = "EP00771_Trimastix_marina_edit_50_startAA.txt"
output_db = ".".join(input_db.split('.')[:-1]) + '_startAA.txt'


#Part 2: Import data into Pandas dataframes

#import Metamonad database into a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)
# sys:1: DtypeWarning: Columns (6,7,27,31) have mixed types.Specify dtype option on import or set low_memory=False.

#import start codon database into Pandas
startAA_df = pd.read_csv(startAA_db, sep = '\t', header=0)


#Part 3: Merge dataframes and write out

merged_df = input_df.merge(startAA_df, how='outer', on='Query')
#since the input_df is given the merge command, the data from it will be on the left,
#while the data from startAA_df will be on the right
#the `how='outer'` argument ensures that all queries are kept, even the ones without overlap
#it isn't particularly important here, though, since the dataframes are the same length


#write out the resulting dataframe
merged_df.to_csv(output_db, sep='\t', index=False)
