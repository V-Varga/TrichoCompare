#!/bin/python
"""

Title: decodeHeaders.py
Date: 28.07.2021
Author: Virág Varga

Description:
	This program decodes the random alphanumeric headers assigned by the
		assignFASTAheaders.py program with the original FASTA headers, using the
		reference file created by the other program as a guide. It is intended
		for use on the *_OGall*.csv species & strain databases.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	re
	pandas

Procedure:
	1. Loading required modules & assigning command line arguments.
	2. Using Pandas to load the contents of the reference file into a dictionary.
	3. Parsing the input database file in order to match the random headers to the
		original headers via the reference file.
	4. Writing out the new database file with the original FASTA headers.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The user needs to check that the correct reference file is assigned.

Usage
	./decodeHeaders.py input_db ref_doc
	OR
	python decodeHeaders.py input_db ref_doc

This script was written for Python 3.8.10, in Spyder 5.0.5.

"""

#import necessary modules
import sys #allows execution of script from command line
import re #enables regex pattern matching
import pandas as pd #allow manipulation of data files


#load input and output files
input_db = sys.argv[1]
#input_db = "BM_anaeromoeba_DB_OFall.csv"
ref_doc = sys.argv[2]
#ref_doc = "encoding_summary_ref.txt"
#output_db name is based on the input_fasta name
output_db = ".".join(input_db.split('.')[:-1]) + '__decode.csv'


#create and populate dictionary using the reference file
with open(ref_doc, "r") as inref:
	REF = pd.read_csv(inref, sep="\t", header=None)
	REF = REF.set_index(0)
	ref_dict = REF.T.to_dict('list')
	#note that this manner of conversion makes the dictionary value a list

#reading in the input database into a Pandas dataframe
species_df = pd.read_csv(input_db, header=0)
#set the first column (containing the protein query ids) as an index
species_df.set_index('Query')


#replace the spaces (' ') in the FASTA headers with underscores ('_')
for key, value in ref_dict.items():
	#iterate through the ref_dict dictionary
	if ' ' in value[0]:
		#identify values which contain spaces (' ')
		value[0] = re.sub(' ', '_', value[0])
		#replace spaces in the values with underscores ('_')


#iterate through the species_df dataframe
#where the protein query id matches a key in the ref_dict dictionary, fill in the empty cell (value)
#in the final column with the corresponding dictionary value (ie. original FASTA header)
for id_num, prot_id in enumerate(species_df['Query']):
	#iterate over the contents of the first column of the species_df dataframe (header/column name  = 'Query')
	#prot_id contains the value in the cell; id_num contains the index of that value
	for ref_key in ref_dict:
		#iterate through the og_dict dictionary using its keys
		if prot_id == ref_key:
			#if the protein id in the species_df dataframe matches the key in the og_dict dictionary
			#extract the associated value from dictionary og_dict (ie. orthologous group assignment)
			#and place it in the appropriately indexed cell
			species_df.iat[id_num, 0] = ref_dict[ref_key][0]
			#indexing the ref_dict value (FASTA header) makes the contents print as a string instead of a list


#write out the results to a new .csv file
species_df.to_csv(output_db, index=False)
