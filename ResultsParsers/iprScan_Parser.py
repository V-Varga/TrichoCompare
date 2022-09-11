#!/bin/python
"""
Title: iprScan_Parser.py
Date: 2022-03-04
Authors: Virág Varga

Description:
	This program parses the .tsv results file produced by the InterProScan program
		when it has been run with the command line options of
			`--goterms --iprlookup --pathways`
		and creates an output tab-separated text file containing selected categories
		of information for each query sequence.

List of functions:
	drop_nan_groupby
		(Based on: https://stackoverflow.com/questions/47376077/how-to-drop-nan-elements-in-a-groupby-on-a-pandas-dataframe)

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Assigning command line arguments and output file name, loading modules,
		defining function used in script.
	2. Importing the dataframe into Pandas.
	3. Filtering the database to include only desired columns, and removing rows
		containing unique queries.
	4. Grouping the contents of the table based on the protein query IDs, then
		performing necessary edits to clean up the formatting of cell contents
		in the dataframe.
	5. Adding the unique query rows back in, and writing out the results to a
		tab-separated text file.

Known bugs and limitations:
	- This InterProScan results parser is made specifically to suit the formatting
		of the InterProScan tsv-format output files, for runs with the command-line
		options of:
			`--goterms --iprlookup --pathways`
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Usage
	./iprScan_Parser.py input_file
	OR
	python iprScan_Parser.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import pandas as pd #allows the easy manipulation of dataframes in Python

#function to drop null values during grouping
#based on: https://stackoverflow.com/questions/47376077/how-to-drop-nan-elements-in-a-groupby-on-a-pandas-dataframe
def drop_nan_groupby(x):
	#drop the null (nan) values from the input
    y = x.dropna()
	#if the cells are empty return "-", otherwise return y
    return ["-"] if y.empty else y

#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit_StandardAA.fasta.tsv"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
#remove the ".fasta" at the end of the file name - this gives a list
out_list = out_full.split(".")[:-1]
#concatenate the list back into a string
outname = '.'.join(out_list)
output_file = outname + "_IPRScan.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_edit_StandardAA.fasta.txt"


#Part 2: Importing the dataframe into Pandas

#from the documentation, can find the column meanings
#ref: https://interproscan-docs.readthedocs.io/en/latest/OutputFormats.html
#replacing 'Protein accession' with 'Query' to match other files
ipr_columns = ['Query', 'Sequence_MD5_digest', 'Sequence_length', 'Analysis-Pfam-PRINTS-Gene3D',
			   'Signature_accession', 'Signature_description', 'Start_location', 'Stop_location',
			   'Score', 'Status_of_match', 'Run_date', 'InterPro_annotations-accession',
			   'InterPro_annotations-description', 'GO_annotations', 'Pathways_annotations']

#read in the input text file, assigning the first row as a header row
iprScan_df = pd.read_csv(input_file, sep='\t', names=ipr_columns, index_col=(False))
#there is no header, which means column "names" will be numeric indices
#instead of the usual `header=None`, set the column names immediately
#this helped prevent a pandas error I was having where pandas was expecting 13 columns instead of 15
#the error in question: 
# pandas.errors.ParserError: Error tokenizing data. C error: Expected 13 fields in line 2, saw 15
#ref: https://stackoverflow.com/questions/18039057/python-pandas-error-tokenizing-data/54098017#54098017


#Part 3: Filter the database to include only desired columns

#select the relevant columns and copy them to a new dataframe
filt_iprScan_df = iprScan_df[['Query', 'Signature_accession', 'Signature_description', 'Score',
							  'InterPro_annotations-accession', 'InterPro_annotations-description',
							  'GO_annotations', 'Pathways_annotations']].copy()

#protein queries that occur only once in the dataframe don't do well with the .agg(list)
#so extract them into a small dataframe now, prior to grouping
#and add them back in at the end
non_duplicate_df = filt_iprScan_df.drop_duplicates(subset='Query', keep=False).copy()
#set the 'Query' column as index to match the grouped database that will be built after this
non_duplicate_df.set_index('Query', inplace=True)

#then drop those unique IDs from the primary filtered database
filt_iprScan_df = filt_iprScan_df[filt_iprScan_df.duplicated(subset=['Query'], keep=False)]


#Part 4: Group the contents of the table based on the protein query IDs, then perform necessary edits

#group the results into 1 row per protein
filt_iprScan_df = filt_iprScan_df.groupby('Query', dropna=True)[['Signature_accession', 'Signature_description',
																 'Score', 'InterPro_annotations-accession',
																 'InterPro_annotations-description', 'GO_annotations',
																 'Pathways_annotations']].agg(drop_nan_groupby).agg(list)
#the drop_nan_groupby function drops nan cells and inserts "-" characters into empty cells
#the .agg(list) groups the contents of the columns into lists on the basis of the query ID
#groupby automatically sets the Query columns as a new index

#convert lists currently in columns into strings
for column in filt_iprScan_df:
	#iterate through the dataframe row by row
	#join all lists into comma- and space-separated strings
	filt_iprScan_df[column] = filt_iprScan_df[column].apply(lambda x: ', '.join(map(str, x)))

#this process leaves a lot of extraneous, useless characters, so now need to remove those
for column in filt_iprScan_df:
	#iterate through the dataframe row by row
	#in the following rows, replace unnecessary characters, including blanks in the form of "-" characters
	filt_iprScan_df[column] = filt_iprScan_df[column].str.replace(" -,", "")
	filt_iprScan_df[column] = filt_iprScan_df[column].str.replace(", -", "")
	filt_iprScan_df[column] = filt_iprScan_df[column].str.replace("\|", ", ", regex=True)
	# FutureWarning: The default value of regex will change from True to False in a future version.
	# In addition, single character regular expressions will *not* be treated as literal strings when regex=True.
	# filt_iprScan_df[column] = filt_iprScan_df[column].str.replace("|", ", ")
	#use backslash "\" to break out of special character, and allow regex=True to deal with the error above
	filt_iprScan_df[column] = filt_iprScan_df[column].str.replace("-, ", "")


#Part 5: Recombine the dataframes and write out results file

#concatenating the two dataframes
filt_iprScan_df = pd.concat([filt_iprScan_df, non_duplicate_df], axis=0)
#use `axis=0` to concatenate based on index - this adds one dataframe below the other

#write out the results to a tab-separated text file
filt_iprScan_df.to_csv(output_file, sep='\t', index=True)
#since the query IDs are now in the index, need to write out the index, too
