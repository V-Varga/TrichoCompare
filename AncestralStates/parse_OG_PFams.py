# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_OG_PFams.py
Date: 2022.05.18
Author: Virág Varga

Description:
	This program iterates over a file produced by the create_counts_table.py program
		to create one or multiple of the following:
			- A filtered version of the file without OGs lacking PFam domain hits
			- A indexing database in the format: [OG_ID]\tAssocPFams
			- A text file containing the unique PFam IDs in the input database in
				the format: PFam1\nPFam2\nPFam3 etc.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; assigning command line arguments.
	2. Importing data into Pandas dataframe.
	3.1: Creating database version without OGs lacking PFam annotations.
	3.2: Creating database of OG IDs and associated PFam IDs.
	3.3: Creating list of unique PFam IDs.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file names are based on the input file name.

Usage
	./parse_OG_PFams.py input_db filt_option
	OR
	python parse_OG_PFams.py input_db filt_option

	Where the input_db file contains OG IDs and associated PFams in a column
		named "pfamEN_hits_Counts".
	Where filt_option allows the user to specify the type(s) of filtration to be
		performed:
			- "list": to output a file containing a unique list of PFams in the
				format: PFam1\nPFam2\nPFam3 etc.
			- "index": to output an indexing file in the format:
				[OG_ID]\tAssocPFams
			- "remove": To output a copy of the input database without the OGs
				that lack PFam domain hits.
		Multiple options can be selected by placing them in a comma-separated list
		on the command line (ex.: `python parse_OG_PFams.py input_db list,index`).

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "MetamonadCtrl_sec_3_SP__CountPivot.txt"

filt_option = sys.argv[2]
#filt_option = "test"
#save the contents of the comma-separated string to a list variable
filt_list = filt_option.split(",")


#output file name should be based on input file name
base = os.path.basename(input_db)
#assign the basename of output file
out_base = os.path.splitext(base)[0]


#Part 2: Import data into Pandas dataframe

#read in the Metamonad database to a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0)
#then extract the name of the OG program
og_program = input_df.columns[0]


#Part 3.1: Create database version without OGs lacking PFam annotations

#remove the rows from the dataframe containing OGs without PFam domain hits
filt_df = input_df.dropna().copy()
#`.dropna()` removes rows containing NaNs
#since this only occurs for OGs where there is no PFam entry, this works for our data


if "remove" in filt_list:
	#if the option to output a database without OGs lacking PFam domain hits has been selected
	print("remove option selected")

	#determine output file name
	output_db = out_base + "_allPFam.txt"
	#and write out results to a tab-separated text file
	filt_df.to_csv(output_db, sep = '\t', index=False)


#Part 3.2: Create database of OG IDs and associated PFam IDs

if "index" in filt_list:
	#if the option to output an indexing database in the format: [OG_ID]\tAssocPFams
	#has been selected
	print("index option selected")

	#create a dictionary in the format: pfam_prep_dict[OG_ID] = list_of_PFams
	pfam_prep_dict = filt_df.set_index(og_program).to_dict()['pfamEN_hits_Counts']
	#create an empty dictionary to populate with the actual PFam ID lists
	pfam_dict = {}

	for key in pfam_prep_dict.keys():
		#iterate over the dictionary via its keys (the OG IDs)
		temp_pfam_list = []
		#create an empty list to hold the PFam domain IDs for each OG
		pfam_split_list = pfam_prep_dict[key].split(",")
		#split the PFam domain IDs into a list based on comma placement
		for m in pfam_split_list:
			#iterate over the list of PFam domains with frequency data
			pfam_id = m.split(":")[0]
			#identify the PFam domain ID
			#and add it to the list of PFam IDs
			temp_pfam_list.append(pfam_id)
		#populate the new dictionary with the OG & PFam ID data
		pfam_dict[key] = temp_pfam_list

	#create a new dataframe from the dictionary
	#ref: https://stackoverflow.com/questions/50751184/pandas-dataframe-from-dictionary-of-list-values
	og_pfam_df = pd.DataFrame([(key, var) for (key, L) in pfam_dict.items() for var in L],
							  columns=[og_program, 'AssocPFams'])

	#determine output file name
	output_index = out_base + "_PFamIndex.txt"
	#and write out results to a tab-separated text file
	og_pfam_df.to_csv(output_index, sep = '\t', index=False)


#Part 3.3: Create list of unique PFam IDs

if "list" in filt_list:
	#if the option to output a list of unique PFam IDs has been given
	print("list option selected")

	#send PFams to a list
	full_pfam_list = filt_df.pfamEN_hits_Counts.tolist()

	#create new empty list for PFam domains
	pfam_list = []

	for i in full_pfam_list:
		#iterate over the list of PFam domains associated with number of occurances
		pfam_split_list = i.split(",")
		#split the small list via the comma placement
		for j in pfam_split_list:
			#iterate over the list of PFam domains with frequency data
			pfam_id = j.split(":")[0]
			#identify the PFam domain ID
			#and add it to the list of PFam IDs
			pfam_list.append(pfam_id)

	#remove duplicates from the list
	pfam_setlist = list(set(pfam_list))

	#determine the output file name
	output_pfams = out_base + "_PFamList.txt"
	#and write out results to a file
	with open(output_pfams, "w") as outfile:
		#open the output file for writing
		for k in pfam_setlist:
			#iterate over the list of unique PFam domain IDs
			#and write each PFam domain ID to a new line in the file
			outfile.write(k + "\n")


else:
	#if the user has not provided an appropriate program run option
	#display the following help message
	print("Input arguments are incorrect. Consider the following usage instructions:" + "\n" +
	"python parse_OG_PFams.py input_db filt_option" + "\n" +
	"Where the input_db file contains OG IDs and associated PFams in a column named 'pfamEN_hits_Counts'" + "\n" +
	"Where filt_option allows the user to specify the type(s) of filtration to be performed:" + "\n" +
		"- 'list': to output a file containing a unique list of PFams in the format: PFam1\nPFam2\nPFam3 etc." + "\n" +
		"- 'index': to output an indexing file in the format: [OG_ID]\tAssocPFams" + "\n" +
		"- 'remove': To output a copy of the input database without the OGsthat lack PFam domain hits." + "\n" +
	"Multiple options can be selected by placing them in a comma-separated list on the command line" + "\n" +
	"(ex.: python parse_OG_PFams.py input_db list,index).")
