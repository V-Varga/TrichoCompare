#!/bin/python
"""
Title: eggNOG_dn_Parser__v2.py
Date: 2022-03-01
Authors: Virág Varga

Description:
	This program parses the .annotations results file produced by the eggNOG program
		when doing de novo PFam searches and creates an output text file containing
		selected categories of information for each query sequence.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Creating a dictionary containing the pertinent results of the eggNOG
		annotations file.
	3. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This eggNOG results parser is made specifically to suit the formatting
		of the eggNOG annotations output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version: 
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop. 

Usage
	./eggNOG_Parser__v2.py input_file
	OR
	python eggNOG_Parser__v2.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows the easy manipulation of dataframes in Python

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit.emap.emapper.annotations"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_eggNOG.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_edit.emap.emapper_eggNOG.txt"


#Part 2: Importing the dataframe into Pandas

#read in the input text file, assigning the first row as a header row
eggNOG_df = pd.read_csv(input_file, sep='\t', header=4, index_col=(False), skipfooter=3, engine='python')
#the header is in row 5 (pythonic index 4)
#the `skipfooter=3` argument is included because the last 3 rows are informational/summary lines
#the `engine='python'` is needed because otherwise `skipfooter` raises an error
#rename the first column header to 'Query' in order to match other files
eggNOG_df.rename(columns={'#query': 'Query'}, inplace=True)


#Part 3: Filter the database to include only desired columns, then write out results file

#select the relevant columns and copy them to a new dataframe
filt_eggNOG_df = eggNOG_df[['Query', 'seed_ortholog', 'evalue', 'score', 'eggNOG_OGs', 'Preferred_name', 'GOs', 'KEGG_ko', 'KEGG_Pathway', 'KEGG_Reaction', 'PFAMs']].copy()
#write out the results to a tab-separated text file
filt_eggNOG_df.to_csv(output_file, sep='\t', index=False)
