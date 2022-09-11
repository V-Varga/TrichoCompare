# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: extract_prot_db.py
Date: 2022.04.16
Author: Virág Varga

Description:
	This program filters the species database generated by prot_DB_plus_OGs.py
		(Metamonada_pred_OG_DB.txt) - or a filtered version of the same, with the same
		key columns - in order to extract only those rows that contain protein queries
		used as input. Alternately, searching for a match in a difference column 
		can be specified. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas
	os.path

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the input database.
	3. Filtering the dataframe based on list of protein IDs & writing out the results to a
		tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a flat database created by prot_DB_plus_OGs.py
		(named Metamonada_pred_OG_DB.txt in the original workflow), or a filtered verison
		of the same.
	- Both the input and output files are user-defined.

Usage
	./extract_prot_db.py input_db input_prots output_db [search_col]
	OR
	python extract_prot_db.py input_db input_prots output_db [search_col]

	Where the list of query_ids can be given in the following formats:
		- Singular protein ID provided on the command line
		- Comma-separated list of protein IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of protein IDs in format: ID1\nID2 etc.
	Where the search_col variable specifies the column of the database to be
		searched. Default is "Query".

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
import os.path #helps return path information for files


#assign command line arguments; load input and output files
#assign the Metamonad database as input_db
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__HEAD.txt"


#save the selection of proteins to filter for
input_prots = sys.argv[2]
#input_prots = "encodingSummary_Tvag_ctrl_encoded.txt"

if os.path.isfile(input_prots):
	#if the input selection of proteins is a file
	with open(input_prots, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein IDs) to a list
		prot_list = [line.rstrip('\n') for line in infile]
else:
	#if the input protein ID list is a string instead of a text file
	#save the protein IDs to a list based on comma placement in the input string
	prot_list = input_prots.split(",")

#assign output file name
output_db = sys.argv[3]


#determine the column to search for matches in 
if len(sys.argv) == 4:
	#if alternative to the Query column is not provided by the user
	search_col = "Query"
elif len(sys.argv) == 5:
	#if the user provides an alternative search column
	search_col = sys.argv[4]
else:
	#if the wrong number of command line arguments are used
	#display this error message
	print("The command-line input format is incorrect. It should be: \n \
	   python extract_prot_db.py input_db input_prots [search_col]")
	#and exit the program
	sys.exit(1)


#Part 2: Create Pandas dataframe from input data

#read in the input OG database file, assigning the first row as a header row
ortho_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)
# sys:1: DtypeWarning: Columns (6,7,27,31) have mixed types.Specify dtype option on import or set low_memory=False.


#Part 3: Filter dataframe based on list of protein IDs & write out

#filter the dataframe
filt_ortho_df = ortho_df[ortho_df[search_col].isin(prot_list)].copy()
#only search the values in the specified column for matches
#check to see whether the rows contain the values found in the prot_list
#copy the rows that match these conditions to a new dataframe


#write out the filtered dataframe to a tab-separated text file
filt_ortho_df.to_csv(output_db, sep = '\t', index=False)
