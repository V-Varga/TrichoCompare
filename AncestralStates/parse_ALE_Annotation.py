# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_ALE_Annotation.py
Date: 2022.06.25
Author: Virág Varga
With gratitude to: Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil)

Description:
	This program iterates over a data file derived from ALE relating to the events
		occurring at any given node per gene family. It is intended to be used on 
		the larger data file consolidating this information between all gene families, 
		in order to extract a portion of the dataframe containing queried node or 
		OG IDs. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas
	datetime.datetime

Procedure:
	1. Loading required modules; assigning command-line arguments.
	2. Importing the contents of the DTL events data table into a Pandas dataframe. 
	3. Querying the reference dataframe for the desired data & writing out
		results to a tab-separated text file. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but is instead based on the input
		file name.  

Citation: 
	This program is a based off of the ALE parsing programs used in the ALE-pipeline 
		program written by Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil), 
		which can be found here: https://github.com/maxemil/ALE-pipeline

Usage:
	./parse_ALE_Annotation.py input_db query_type query_ids [ouptut_name]
	OR
	python parse_ALE_Annotation.py input_db query_type query_ids [output_name]
	
	Where the query_type can be either: "OG" OR "Node"
	Where the list of query_ids can be given in the following formats:
		- Singular OG ID provided on the command line
		- Comma-separated list of OG IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of OG IDs in format: ID1\nID2 etc.

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files
from datetime import datetime #access data from system regarding date & time


#designate input file name as variable
input_db = sys.argv[1]


#determine the type of query input being used
query_type = sys.argv[2]
if query_type == "OG":
	#if the input query type is an OG ID
	#designate the query column as the encoded dta column
	query_col = "Gene_Family"
	print("Query type: OG ID")
elif query_type == "Node":
	#if the input query type is a Node ID
	#designate the query column as the unencoded dta column
	query_col = "Node"
	print("Query type: Node ID")
else:
	#if the user does not determine the input query type as OG or Node ID
	#display this error message
	print("Please select query type: OG OR Node")
	#and exit the program
	sys.exit(1)

#save the list of query IDs to search for to a list
query_ids = sys.argv[3]
if os.path.isfile(query_ids):
	#if the input selection of OGs is a file
	with open(query_ids, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = query_ids.split(",")

#define the output file
#determine output file name based on input file name
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#determine basename of input file
#and use that basename to determine the output file name
if len(sys.argv) == 4:
	#if no output file name is provided by the user
	#determine date & time of query
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y--%H%M%S")
	#and create the resulting outfile name
	output_db = out_full + "__QUERY_" + time_now + ".txt"
elif len(sys.argv) == 5:
	#if the user provides an output file name extension
	#then identify the extension given
	output_usr_ext = sys.argv[4]
	#and add that to the end of the basename
	output_db = out_full + "__" + output_usr_ext + ".txt"
else:
	#if the wrong number of command line arguments are used
	#display this error message
	print("The command-line input format is incorrect. It should be: \n \
	   python query_prot_ids.py input_db query_type query_ids [output_name]")
	#and exit the program
	sys.exit(1)


#Part 2: Import events data into Pandas dataframe

events_df = pd.read_csv(input_db, sep = '\t', header=0)
#the file is a tab-delimited text file, so the separator needs to be specified


#Part 3: Query the reference dataframe for the desired data & write out

#search the appropriate column to extract the rows of the dataframe where the query IDs are found
filt_events_df = events_df[events_df[query_col].isin(query_list)].copy()


filt_events_df.to_csv(output_db, sep = '\t', index=False)
#results will be written out to a tab-separated text file
