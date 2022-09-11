# -*- coding: utf-8 -*-
#!/bin/python
"""
Title: eggNOG_dn_PFam_Parser_bad.py
Date: 2022-04-15
Authors: Virág Varga

Description:
	This program parses the de novo PFam search results produced by the eggNOG program
		and creates an output text file containing selected categories of information
		for each query sequence.
	This version of the EggNOG PFam parser is specifically intended for the "bad" output
		files, wherein the contents of the query and PFam hit have been reversed.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Importing the dataframe into Pandas.
	3. Filter the database to include only desired columns, correctly formatted.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This eggNOG PFam results parser is made specifically to suit the formatting
		of the eggNOG PFam de novo search output files.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version:
	This script is a modified version of the eggNOG_dn_PFam_Parser__v2.py program,
		which is intended to be run on .pfam files with incorrect column contents
		(swapped content of query and PFam hit columns).

Usage
	./eggNOG_dn_PFam_Parser_bad.py input_file
	OR
	python eggNOG_dn_PFam_Parser_bad.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows the easy manipulation of dataframes in Python

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/BS_newprots_may21.anaeromoeba_edit.emap.emapper.pfam"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_PFam.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_edit.emap.emapper_PFam.txt"


#Part 2: Importing the dataframe into Pandas

#read in the input text file, assigning the first row as a header row
pfam_df = pd.read_csv(input_file, sep='\t', header=4, index_col=(False), skipfooter=3, engine='python')
#the header is in row 5 (pythonic index 4)
#the `skipfooter=3` argument is included because the last 3 rows are informational/summary lines
#the `engine='python'` is needed because otherwise `skipfooter` raises an error
#rename the first column header to 'Query' in order to match other files
pfam_df.rename(columns={'# query_name': 'hit', 'hit': 'Query'}, inplace=True)


#Part 3: Filter the database to include only desired columns

#select the relevant columns and copy them to a new dataframe
filt_pfam_df = pfam_df[['Query', 'hit', 'evalue', 'sum_score']].copy()

#group the results into 1 row per protein
filt_pfam_df = filt_pfam_df.groupby('Query')[['hit', 'evalue', 'sum_score']].agg(list).reset_index()
#the above creates lists in the columns, so need to remove the brackets by converting to strings
filt_pfam_df['hit'] = filt_pfam_df['hit'].apply(lambda x: ', '.join(map(str, x)))
filt_pfam_df['evalue'] = filt_pfam_df['evalue'].apply(lambda x: ', '.join(map(str, x)))
filt_pfam_df['sum_score'] = filt_pfam_df['sum_score'].apply(lambda x: ', '.join(map(str, x)))


#Part 4: Write out the results to a file

#write out the results to a tab-separated text file
filt_pfam_df.to_csv(output_file, sep='\t', index=False)
