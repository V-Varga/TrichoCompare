#!/bin/python
"""

Title: check_OG_duplicates.py
Date: 2022-03-02
Author: Virág Varga

Description:
	This program checks a file to see whether elements of the first column
		(Pythonic index 0; must be named "Query") are repeated.
	It was written to determine whether orthologous clustering programs were
		clustering proteins into more than one orthologous group.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas
	itertools

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the ortholog_groups.tsv file into a
		dataframe.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a file with query IDs in the first column.

Usage
	./check_OG_duplicates.py input_db
	OR
	python check_OG_duplicates.py input_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part1: Assign command-line arguments, import modules

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "Broccoli_OGs_parsed.txt"
#input_db = "OF_OGs_parsed.txt"
#input_db = "SP_OGs_parsed.txt"
#input_db = "PO_OGs_parsed.txt"
#input_db = "encoding_summary_ref.txt"

#used the above to queck the query ids themselves weren't replicated


#Part 2: Check for duplicates & report results

#import input database into a Pandas dataframe
ortho_df = pd.read_csv(input_db, sep = '\t', header = 0)

#send query colummn to list
query_list = ortho_df.iloc[:, 0].to_list()


#check if list members are entirely unique
if(len(set(query_list)) == len(query_list)):
	print(input_db + "___ results DO NOT have duplicates among the queries!")
else:
	print(input_db + " results HAVE duplicates among the queries!")
	copy_ortho_df = ortho_df.iloc[:, [0, -1]].copy()
	#the script works up until here
	#I'm able to make a dataframe with the line above that includes only the OG numbers & query IDs
	duplicate_df = pd.concat(g for _, g in copy_ortho_df.groupby("Query") if len(g) > 1)
	base = os.path.basename(input_db)
	out_full = os.path.splitext(base)[0]
	output_file = out_full + "_DUPLICATES.txt"
	duplicate_df.to_csv(output_file, sep='\t', index=False)
