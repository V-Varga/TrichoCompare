# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: remove_duplicatesBR__ALL.py
Date: 2022-03-21
Author: Virág Varga

Description:
	This program deals with the duplicates in the parsed Broccoli OG data in 1 or 2 ways:
		1. (Mandatory) Outputs a file containing only those protein query IDs that
			were not grouped into more than 1 OG.
		2. (Optional) Outputs an additional results file in the format:
			Query\tBr_Grouped_OGs\tBr_Single_OGs

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules & assigning command line arguments.
	2. Importing data into Pandas dataframe.
	3. Creating dataframe without duplicates and writing it out to a tab-separated
		text file.
	4. (Optional): Creating output dataframe with both grouped and dropped OG ID info,
		and writing it out to a tab-separated text file.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the mandatory output file is pre-determined (not user-defined), based on
		the name of the input FASTA file.

Usage
	./remove_duplicatesBR__ALL.py broccoli_db [drop_group_db]
	OR
	python remove_duplicatesBR__ALL.py broccoli_db [drop_group_db]

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import modules, set up command-line arguments

#import necessary modules
import sys #allows execution of script from command line
import pandas as pd #allows manipulation of dataframes in Python


#load input and output files
broccoli_db = sys.argv[1]
#broccoli_db = "Broccoli_OGs_parsed.txt"

#his outfile will be produced with both teh standard and optional runs
#prot_ref_db = "Prots_Species_Phyla_SeqLength_DB.txt"
output_db = ".".join(broccoli_db.split('.')[:-1]) + '_nonDuplicate.txt'


#Part 2: Import data into appropriate data into Pandas dataframe

#import Broccoli database into Pandas dataframe
broccoli_df = pd.read_csv(broccoli_db, sep = "\t", header=0)


#Part 3: Create dataframe without duplicates and write out

#drop all queries IDs that have duplicates
non_duplicate_df = broccoli_df.drop_duplicates(subset=['Query'], keep=False)

#write out the resulting dataframe in tab-separated format
non_duplicate_df.to_csv(output_db, sep='\t', index=False)


#Part 4 (Optional): Create output dataframe with both grouped and dropped OG ID info

if len(sys.argv) == 3:
	#if the program is run with the option to create a databbase with dropped AND clustered OG IDs
	drop_group_db = sys.argv[2]
	#drop_group_db = "Broccoli_OGs_parsed__Group-Drop.txt"
	#assign the last argument as the output file name

	#create dataframe of only duplicated query IDs
	duplicate_df = broccoli_df[broccoli_df.duplicated(subset=['Query'], keep=False)]
	#create dataframe grouping the OG IDs based on the query IDs
	grouped_duplicate_df = duplicate_df.groupby('Query')['Broccoli_OG'].apply(list).reset_index(name="Broccoli_OG")
	#the OGs in the 'Broccoli_OG' column are grouped into lists according to the protein they are associated with
	#the new column of lists is named 'Broccoli_OG'
	#now sort out the formatting of those lists of queries
	grouped_duplicate_df['Broccoli_OG'] = grouped_duplicate_df['Broccoli_OG'].apply(lambda x: ', '.join(map(str, x)))

	#now combine the grouped dataframe with the non-duplicate dataframe
	grouped_df = pd.concat([non_duplicate_df, grouped_duplicate_df], axis=0)
	#rename second column
	grouped_df.rename(columns={'Broccoli_OG':'Br_Grouped_OGs'}, inplace=True)

	#create merged dataframe with both the dropped and and grouped data in the columns
	#first, reset the indices of the dataframes to be merged
	grouped_df.set_index('Query')
	non_duplicate_df.set_index('Query')
	#now perform the actual merge
	merged_df = grouped_df.merge(non_duplicate_df, how='outer')
	#rename third column
	merged_df.rename(columns={'Broccoli_OG':'Br_Single_OGs'}, inplace=True)
	#and fill NaN values with "-"
	merged_df.fillna('-', inplace=True)

	#now write out the results to a tab-separated text file
	merged_df.to_csv(drop_group_db, sep='\t', index=False)
