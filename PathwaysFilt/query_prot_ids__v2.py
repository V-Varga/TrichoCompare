# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: query_prot_ids__v2.py
Date: 2022-04-27
Author: Virág Varga

Description:
	This program parses the protein ID encoding reference file in order to extract queried
		portions of the dataframe (ie. encoded and unencoded value pairs).
		It can accommodate the name variation of the Trichomonas vaginalis proteins.

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	argparse
	sys
	pandas
	os
	datetime.datetime
	numpy
	itertools.chain

Procedure:
	Begin by parsing arguments. Then:
		1. Importing necessary modules, assigning command-line arguments.
		2. Importing data into Pandas dataframe.
		3. Querying the reference dataframe for the desired data & writing out
			results to a tab-separated text file.

Known bugs and limitations:
	- There is only limited quality-checking integrated into the code, relating to
		command-line inputs.
	- The default name of the output file is based on query time.
	- The reference file must be in the format: encoded_prot_ID\toriginal_prot_ID

Version:
	This is Version 2.0 of this program, which takes into account the fact that a
		number of the protein IDs used for Trichomonas vaginalis have had their official
		names changed. To accomadate this, an input file containing the protein ID
		aliases can be provided as input.

Usage:
	./query_prot_ids__v2.py [-h] [-tvag TVAG_FILE] [-out OUT_NAME] [-v] REF_DB QUERY_TYPE QUERY_IDS
	OR
	python query_prot_ids__v2.py [-h] [-tvag TVAG_FILE] [-out OUT_NAME] [-v] REF_DB QUERY_TYPE QUERY_IDS

	Where the QUERY_TYPE can be either: "encoded" OR "unencoded"
	Where the list of QUERY_IDS can be given in the following formats:
		- Singular protein ID provided on the command line
		- Comma-separated list of protein IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of protein IDs in format: ID1\nID2 etc.
	Where the TVAG_FILE provided must be the T. vaginalis protein name aliasses file obtained
		from TrichDB.

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#################################   ARGPARSE   #######################################
import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program parses the protein ID encoding reference file in order to extract queried \n \
									portions of the dataframe (ie. encoded and unencoded value pairs). \n \
									It can accomadate the name variation of the Trichomonas vaginalis proteins.')
#The most general description of what this program can do is defined here


#adding the arguments that the program can use
parser.add_argument(
	dest='ref_db',
	metavar='REF_DB',
	type=argparse.FileType('r'),
	help = 'The reference file should have encoded protein names in the first column \
		and original protein names in the second column.'
	)
	#this portion of code specifies that the program requires a reference file, and it should be opened for reading ('r')
parser.add_argument(
	dest='query_type',
	metavar='QUERY_TYPE',
	choices=['encoded', 'unencoded'],
	help = 'The query type must be specified as either: "encoded" OR "unencoded".'
	)
	#this portion of code specifies the options for the query type: encoded OR unencoded
parser.add_argument(
	dest='query_ids',
	metavar='QUERY_IDS',
	help = 'Here specify the query protein IDs in one of the following formats: \n \
		single protein ID OR comma-separated list of protein IDs (ex. `ID_1,ID_2,ID_3`) \n \
			OR file with protein IDs separated by newlines \n \
			When using unencoded query IDs, a key portion of the protein name is sufficient - \n \
				The entirety of the protein header does not need to be used.'
	)
	#this portion of code specifies that a query protein ID (or list of them) is required,
	#as well as the formats that can be used

parser.add_argument(
	'-tvag', '--Tvag_ref',
	dest='tvag_ref',
	metavar='TVAG_FILE',
	help = "The T. vaginalis protein name aliases file from TrichDB should be used as input.",
	type=argparse.FileType('r')
	)
	#the '-tvag' flag allows for the accomadation of the alternative names used for T. vaginalis proteins
parser.add_argument(
	'-out', '--outname',
	metavar='OUT_NAME',
	dest='out_name',
	help = 'This argument allows the user to define an output file name.'
	)

parser.add_argument(
	'-v', '--version',
	action='version',
	version='%(prog)s 2.0'
	)
	#This portion of the code specifies the version of the program; currently 2.0
	#The user can call this flag ('-v') without specifying input and output files


args = parser.parse_args()
#this command allows the program to execute the arguments in the flags specified above


#################################   Parse Arguments   ######################################


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files
from datetime import datetime #access data from system regarding date & time
import numpy as np #allows manipulation of arrays in Python
from itertools import chain #treats consecutive sequences as single sequence


#designate input file name as variable
input_db = args.ref_db.name
#input_db = "encoding_summary_ref.txt"


#determine the type of query input being used
query_type = args.query_type
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
query_ids = args.query_ids
#query_ids = "TVAG_343440,TVAG_343470"
#query_ids = "Control_data/Reference_prot_ids_Tvag_mito_filt.txt"
#query_ids = "Control_data/Tvag_ctrl_deMiguel2010_secretome_IDs.txt"

if os.path.isfile(query_ids):
	#if the input selection of OGs is a file
	with open(query_ids, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
		#eliminate duplicates
		query_list = list(set(query_list))
		#also remove spaces in list elements, if they exist
		query_list = [x.strip(' ') for x in query_list]
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = query_ids.split(",")
	#eliminate duplicates
	query_list = list(set(query_list))


#define the output file
if args.out_name:
	#if the user provides an output file name
	#use that file name as the output file name
	output_db = args.out_name
else:
	#if no output file name is provided by the user
	base = os.path.basename(input_db)
	out_full = os.path.splitext(base)[0]
	#first extract base file name
	#then determine date & time of query
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y--%H%M%S")
	#and create the resulting outfile name
	output_db = out_full + "__QUERY_" + time_now + ".txt"


#Part 2: Import data into Pandas dataframes

#create list of column names to use for dataframe upon import into Pandas
column_names=["Encoded", "Unencoded"]

#import input file into pandas dataframe
ref_df = pd.read_csv(input_db, sep = '\t', header = None, names = column_names)
#use `header = None, names = column_names`
#because the reference file has no header line
#and the column names need to be manually determined based on the list created


#Part 3: Query the reference dataframe for the desired data & write out

if args.tvag_ref:
	#if the user provides the T. vaginalis protein aliases file

	#save the file name to a variable
	tvag_file = args.tvag_ref.name
	#tvag_file = "Control_data/TrichDB-57_TvaginalisG3_GeneAliases.txt"
	#and read the file into a new Pandas dataframe
	#ref: https://stackoverflow.com/questions/27020216/import-csv-with-different-number-of-columns-per-row-using-pandas
	#Loop the data lines
	with open(tvag_file, 'r') as temp_f:
		#open the file for reading
		#and get the numbber of columns in each line
		col_count = [ len(l.split("\t")) for l in temp_f.readlines() ]
	#Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
	column_names2 = [i for i in range(0, max(col_count))]
	#Read in the tab-separated text file
	tvag_alias_df = pd.read_csv(tvag_file, sep="\t", header=None, names=column_names2)


	#identify the alternative names that exist for those proteins
	#ref: https://stackoverflow.com/questions/26640129/search-for-string-in-all-pandas-dataframe-columns-and-filter
	mask = np.column_stack([tvag_alias_df[col].str.contains('|'.join(query_list), na=False) for col in tvag_alias_df])
	#can use `np.column_stack` to stack 1-D arrays as columns into a 2-D array
	#To check every column, use `for col in df` to iterate through the column names,
	#and then call `str.contains()` on each column, using `na=False` t prevet the NaN values from causing an error
	#this will yield an arrary where each row has a list of True/False based on whether there is a match
	filt_alias_df = tvag_alias_df.loc[mask.any(axis=1)]
	#use `.loc` to select portions of the database that evaluated as True


	#extract the portions of the reference dataframe containing those protein IDs
	filt_alias_list = filt_alias_df.values.tolist()
	#combine all values in the dataframe into a list
	#this list will contain nested lists (1 per each row), so need to un-nest them
	filt_alias_list = list(chain.from_iterable(filt_alias_list))
	#use chain to un-nest the list
	clean_alias_list = [x for x in filt_alias_list if str(x) != 'nan']
	#remove nan values from the list
	alias_setlist = list(set(clean_alias_list))
	#if there are duplicates, remove them

	#search the appropriate column for all to extract the rows of the dataframe where the IDs are found
	filt_ref_df = ref_df[ref_df[query_col].str.contains('|'.join(alias_setlist))].copy()
	#need to use the str.contains() method
	#because the names of the proteins are sometimes part of a longer name


	filt_ref_df.to_csv(output_db, sep = '\t', index=False)
	#results will be written out to a tab-separated text file

else:
	#in a case where the T. vaginalis reference file isn't being used

	#search the appropriate column for all to extract the rows of the dataframe where the IDs are found
	filt_ref_df = ref_df[ref_df[query_col].str.contains('|'.join(query_list))].copy()
	#need to use the str.contains() method
	#because the names of the proteins are sometimes part of a longer name


	filt_ref_df.to_csv(output_db, sep = '\t', index=False)
	#results will be written out to a tab-separated text file
