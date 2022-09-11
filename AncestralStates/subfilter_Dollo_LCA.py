# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: subfilter_Dollo_LCA.py
Date: 2022.05.31
Author: Virág Varga

Description:
	This program uses data from the Count program to filter the input file used for
		Count down to the OGs which are ancestral to a node realtive to the previous
		node on the evolutionary tree. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas import the contents of the Count annotated input data file and
		Count Dollo parsimony data output file.
	3. Filtering out the OGs unique to the query node, before writing out the
		results to a tab-delimited text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of an OG database prepped as input into Count,
		along with an output file from Count containing Dollo Parsimony data.
	- The output file name is only partially user-defined.

Version:
	This script can be considered a Version 2.0 of the subfilterDollo_Parab.py script
		prepared for the preliminary project. It allows for the filtration of the
		Dollo results table produced by Count by any given node.

Usage
	./subfilter_Dollo_LCA.py input_db ref_db query_node pre_query_node output_extension
	OR
	python subfilter_Dollo_LCA.py input_db ref_db query_node _pre_query_node output_extension

	Where the query_node is the number assigned to the query node in the Dollo parsimony
		analysis; and the pre_query_node is the number assigned to the node one up from
		(prior to) the query node. These are not always numerically linked!

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
#input files
input_db = sys.argv[1]
#input_db = "MetamonadCtrl_sec_3_SP__CountPivot__Dollo.txt"
ref_db = sys.argv[2]
#ref_db = "MetamonadCtrl_sec_3_SP__CountPivot.txt"

#query node
query_node = sys.argv[3]
#query_node = 12 #Parabasalia/Anaeramoebidae split
pre_query_node = sys.argv[4]
#pre_query_node = 13

#output file
output_extension = sys.argv[5]
#output_extension = "ParaAna12"
#determine file name suffix/extension for query
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_db = out_full + "_" + output_extension + ".txt"


#Part 2: Import data into Pandas dataframes

#read in the input dollo parsimony data file, assigning the first row as a header row
input_df = pd.read_csv(input_db, skiprows=0, sep = '\t', header=1)
#the file is a tab-delimited text file, so the separator needs to be specified
#`skiprows=1` allows the first line of the file (which does not contain data or headers) to be skipped
#the header line has to be moved down 1 line as well, as a result
input_df.rename(columns={'# Family':'Orthogroup'}, inplace=True)
#rename first column header for ease of use

ref_df = pd.read_csv(ref_db, sep = '\t', header = 0)
#import the reference dataframe with the first row as a header row


#Part 3: Extracting query OGs & writing out results

#convert the node numbers into strings to use as column header names
query_header = str(query_node)
pre_query_header = str(pre_query_node)

#extract rows from the input database where the OG is present
dollo_df_1 = input_df[input_df[query_header] == 1]
#dollo_df_1 contains all OGs present at the query node
dollo_df_2 = dollo_df_1[dollo_df_1[pre_query_header] == 1]
#by selecting OGs present at at the pre_query_node,
#we filter down to the ancestral OGs still preserved at the query_node


#extract desired OGs with PFam data from the reference database
filt_OG_list = dollo_df_2['Orthogroup'].tolist()
#convert OG IDs column into a list

ref_og_col = ref_df.columns[0]
#extract the name of the OG column from the reference dataframe
filt_ref_df = ref_df[ref_df[ref_og_col].isin(filt_OG_list)]
#filter the reference database to only those OGs unique to parabasalids


#reformatting for ease of use
col = filt_ref_df['pfamEN_hits_Counts']
#saving the pfamEN_hits_Counts column to a new variable
filt_ref_df.pop('pfamEN_hits_Counts')
#removing the pfamEN_hits_Counts column from the original dataframe
filt_ref_df.insert(filt_ref_df.columns.get_loc(ref_og_col) + 1, col.name, col, allow_duplicates=False)
#putting the pfamEN_hits_Counts column back into the dataframe, but at a different location


#write out results to a tab-separated text file
filt_ref_df.to_csv(output_db, sep = '\t', index=False)
