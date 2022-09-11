# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_CDDhitdata.py
Date: 2022-08-06
Authors: Virág Varga

Description:
	This program parses the full version of the *_hitdata.txt results file that 
		can be downloaded after a search of the NCBI Conserved Domain Database. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading modules & determining input & output files.
	2. Importing the dataframe into Pandas & reformatting contents.
	3. Filtering the database to include only desired columns.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This CDD results file parset is written specifically to suit the 
		full version of the hit data results file. 
	- The output file name is not user-defined; it is based on the input 
		file name. 

Usage
	./parse_CDDhitdata.py input_file
	OR
	python parse_CDDhitdata.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Loading modules & determining input & output files

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line argument
input_file = sys.argv[1]
#input_file = "OF_Mito3__OG0000060_hitdata.txt"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_CDDparsed.txt"


#Part 2: Importing the dataframe into Pandas & reformatting contents

#read in the input text file, assigning the first row as a header row
cdd_df = pd.read_csv(input_file, sep='\t', header=6, index_col=(False))
#the header is in row 8 (pythonic index 7)
#however, the file skips the blank line, so need to go one lower for the header line argument

#edit the contents of the first column to only include the species ID & protein name
#first, remove the first prefix
#ref: https://stackoverflow.com/questions/64463816/pandas-dataframe-split-and-get-last-element-of-list
cdd_df['Query'] = cdd_df['Query'].str.split(">").str[-1]
#then, remove the suffix
#ref: https://stackoverflow.com/questions/42349572/remove-first-x-number-of-characters-from-each-row-in-a-column-of-a-python-datafr
cdd_df['Query'] = cdd_df['Query'].str[:-2]
#for ease of use, rename column headers with spaces in them
cdd_df.columns = cdd_df.columns.str.replace(' ', '_')
#ref: https://www.geeksforgeeks.org/remove-spaces-from-column-names-in-pandas/


#Part 3: Filter the database to include only desired columns

#select the relevant columns and copy them to a new dataframe
filt_cdd_df = cdd_df[['Query', 'Short_name', 'Accession', 'Hit_type']].copy()

#group the results into 1 row per protein
filt_cdd_df = filt_cdd_df.groupby('Query')[['Short_name', 'Accession', 'Hit_type']].agg(list).reset_index()
#the above creates lists in the columns, so need to remove the brackets by converting to strings
filt_cdd_df['Short_name'] = filt_cdd_df['Short_name'].apply(lambda x: ';'.join(map(str, x)))
filt_cdd_df['Accession'] = filt_cdd_df['Accession'].apply(lambda x: ';'.join(map(str, x)))
filt_cdd_df['Hit_type'] = filt_cdd_df['Hit_type'].apply(lambda x: ';'.join(map(str, x)))


#Part 4: Write out the results to a file

#write out the results to a tab-separated text file
filt_cdd_df.to_csv(output_file, sep='\t', index=False)
