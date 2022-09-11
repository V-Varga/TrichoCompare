# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_OG_profile.py
Date: 2022-05-09
Author: Virág Varga

Description:
	This program filters a dataframe containing OG and species ID information for
		each query protein ID down, in order to only include proteins belonging to
		OGs from a query OG ID list provided by the user.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Importing modules and assigning command-line arguments.
	2. Importing input data into Pandas dataframe.
	3. Filtering the dataframe to only include the rows associated with protein
		query IDs that are in the list of query OG IDs, before writing out results
		to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- All input and output file names are user-defined.

Usage
	./filter_OG_profile.py input_db og_ids output_db
	OR
	python filter_OG_profile.py input_db og_ids output_db

	Where input_db must be a file in the format:
		OG_ID\tQuery\tSpecies_Id (as produced by og_prot_spp_list.py)
	Where og_ids must be a query OG ID list in on of the following formats:
		- Singular OG ID provided on the command line
		- Comma-separated list of OG IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of OG IDs in format: ID1\nID2 etc.

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import modules and assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "SonicParanoid_OG__Prot_Spp.txt"

og_ids = sys.argv[2]
#og_ids = "OG_1,OG_10,OG_100"
#og_ids = "MetamonadCtrl_mito_3_SP_OGs_Tv_nonTvP.txt"
#import the query list
if os.path.isfile(og_ids):
	#if the input selection of OGs is a file
	with open(og_ids, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
		#eliminate duplicates
		query_list = list(set(query_list))
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = og_ids.split(",")
	#eliminate duplicates
	query_list = list(set(query_list))


output_db = sys.argv[3]
#output_db = "MetamonadCtrl_mito_3_SP_OGProtSpp.txt"


#Part 2: Import data into Pandas dataframes

#import Metamonad database into a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0)
og_col = input_df.columns[0]
#extract the name of the OG ID columns


#Part 3: Extract relevant data & write out results

filt_input_df = input_df[input_df[og_col].isin(query_list)].copy()
#filter the large OG dataframe to only include proteins from the query OGs


#write out the resulting dataframe
filt_input_df.to_csv(output_db, sep='\t', index=False)
