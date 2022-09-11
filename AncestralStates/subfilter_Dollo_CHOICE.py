# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: subfilter_Dollo_CHOICE.py
Date: 2022.05.31
Author: Virág Varga

Description:
	This program uses data from the Count program to filter the input file used for
		Count down to the OGs which are ancestral to a node relative to the previous
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
	- There is only limited quality-checking integrated into the code.
	- This program requires the input of an OG database prepped as input into Count,
		along with an output file from Count containing Dollo Parsimony data.
	- The output file name is only partially user-defined.

Version:
	This script can be considered a Version 3.0 of the subfilterDollo_Parab.py script
		prepared for the preliminary project. It allows for the filtration of the
		Dollo results table produced by Count by any given node, and allows for more 
		choices related to the ssearch for ancestral vs. derived OGs on the tree. 

Usage
	./subfilter_Dollo_CHOICE.py input_db ref_db query_node pre_query_node query_presence pre_query_presence 
		output_extension
	OR
	python subfilter_Dollo_CHOICE.py input_db ref_db query_node pre_query_node query_presence pre_query_presence 
		output_extension

	Where the query_node is the number assigned to the query node in the Dollo parsimony
		analysis; and the pre_query_node is the number assigned to the node one up from
		(prior to) the query node. These are not always numerically linked!
	Where the query_presence and pre_query_presence arguments can be either 0 (to represent absence of
		of an OG at the given node)	or 1 (to represent presence of an OG at the given node).

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
query_node = int(sys.argv[3])
#query_node = 12 #Parabasalia/Anaeramoebidae split
pre_query_node = int(sys.argv[4])
#pre_query_node = 13

#node presence
query_presence = int(sys.argv[5])
pre_query_presence = int(sys.argv[6])
#define the acceptable values for the presence/absence options
presence_absence_profile = [0, 1]

#quick basic QC on input values
if query_presence not in presence_absence_profile: 
	#if the options given are not applicable options (ie. 0 or 1)
	#return this message to the command line 
	print("Note that presence of an OG at a node is represented by 1, while absence represented by 0. Please try again.")
	#and exit the program
	sys.exit(1)
elif pre_query_node > 31 or query_node > 31: 
	#test for node numbers on the tree, to make sure the values are acceptable
	#return this message to the command line 
	print("Please note that this program was designed for the Thesis_Trich project, where the largest node number was 31. \
	   The node number you have selected is too high. Please either correct your command use or modify this program file.")
	#and exit the program
	sys.exit(1)
else: 
	#if the node and presence absence choices are acceptable
	#return the following message to the stdout & continue running the program
	print("Testing for value of "+ str(query_presence) + " at node " + str(query_node) + " and value of " + \
	   str(pre_query_presence) + " at node " + str(pre_query_node) + ".")


#output file
output_extension = sys.argv[7]
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
dollo_df_1 = input_df[input_df[query_header] == query_presence]
#dollo_df_1 contains all OGs with the given presence/absence profile at the query node
dollo_df_2 = dollo_df_1[dollo_df_1[pre_query_header] == pre_query_presence]
#dollo_df2 filters dollo_df1 to only the OGs 
#that match the given pre_query_node presence/absence profile


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
