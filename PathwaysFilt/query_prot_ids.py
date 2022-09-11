# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: query_prot_ids.py
Date: 2022-04-11
Author: Virág Varga

Description:
	This program parses the protein ID encoding reference file in order to extract queried
		portions of the dataframe (ie. encoded and unencoded value pairs).

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	sys
	pandas
	os
	datetime.datetime

Procedure:
	1. Importing necessary modules, assigning command-line arguments.
	2. Importing data into Pandas dataframe.
	3. Querying the reference dataframe for the desired data & writing out
		results to a tab-separated text file.

Known bugs and limitations:
	- There is only limited quality-checking integrated into the code, relating to
		command-line inputs.
	- The default name of the output file is based on query time.
	- The input file must be in the format: encoded_prot_ID\toriginal_prot_ID

Usage:
	./query_prot_ids.py input_db query_type query_ids [ouptut_name]
	OR
	python query_prot_ids.py input_db query_type query_ids [output_name]

	Where the query_type can be either: "encoded" OR "unencoded"
	Where the list of query_ids can be given in the following formats:
		- Singular protein ID provided on the command line
		- Comma-separated list of protein IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of protein IDs in format: ID1\nID2 etc.

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
#input_db = "encoding_summary_ref.txt"


#determine the type of query input being used
query_type = sys.argv[2]
#query_type = "unencoded"
if query_type == "encoded":
	#if the input query type is an encoded protein ID
	#designate the query column as the encoded dta column
	query_col = "Encoded"
	print("Query type: encoded")
elif query_type == "unencoded":
	#if the input query type is an unencoded protein ID
	#designate the query column as the unencoded dta column
	query_col = "Unencoded"
	print("Query type: unencoded")
else:
	#if the user does not determine the input query type as encoded or unencoded
	#display this error message
	print("Please select query type: encoded OR unencoded")
	#and exit the program
	sys.exit(1)

#save the list of query IDs to search for to a list
query_ids = sys.argv[3]
#query_ids = "TVAG_343440,TVAG_343470"
#query_ids = "Control_data/Reference_prot_ids_Tvag_mito_filt.txt"
#query_ids = "Control_data/Reference_prot_ids_Tvag_sec_filt.txt"

if os.path.isfile(query_ids):
	#if the input selection of OGs is a file
	with open(query_ids, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
		#eliminate duplicates
		query_list = list(set(query_list))
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = query_ids.split(",")
	#eliminate duplicates
	query_list = list(set(query_list))

#define the output file
if len(sys.argv) == 4:
	#if no output file name is provided by the user
	base = os.path.basename(input_db)
	out_full = os.path.splitext(base)[0]
	#first extract base file name
	#then determine date & time of query
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y--%H%M%S")
	#and create the resulting outfile name
	output_db = out_full + "__QUERY_" + time_now + ".txt"
elif len(sys.argv) == 5:
	#if the user provides an output file name
	output_db = sys.argv[4]
else:
	#if the wrong number of command line arguments are used
	#display this error message
	print("The command-line input format is incorrect. It should be: \n \
	   python query_prot_ids.py input_db query_type query_ids [output_name]")
	#and exit the program
	sys.exit(1)


#Part 2: Import data into Pandas dataframes

#create list of column names to use for dataframe upon import into Pandas
column_names=["Encoded", "Unencoded"]

#import input file into pandas dataframe
ref_df = pd.read_csv(input_db, sep = '\t', header = None, names = column_names)
#use `header = None, names = column_names`
#because the reference file has no header line
#and the column names need to be manually determined based on the list created


#Part 3: Query the reference dataframe for the desired data & write out

#search the appropriate column for all to extract the rows of the dataframe where the IDs are found
#filt_ref_df = ref_df[ref_df[query_col].isin(query_list)].copy()
filt_ref_df = ref_df[ref_df[query_col].str.contains('|'.join(query_list))].copy()
#need to use the str.contains() method 
#because the names of the proteins are sometimes part of a longer name


filt_ref_df.to_csv(output_db, sep = '\t', index=False)
#results will be written out to a tab-separated text file
