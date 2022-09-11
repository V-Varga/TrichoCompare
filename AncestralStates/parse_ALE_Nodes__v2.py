# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_ALE_Nodes__v2.py
Date: 2022.06.25
Author: Virág Varga
With gratitude to: Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil)

Description:
	This program iterates over a file containing data on the types of events taking place
		at each node per OG, and consolidates it into a summary data table showing the 
		total number of each type of event occurring at each node. 
	The data to be used as input should be dreived from the results of the ALE program, 
		after the initial parsing of the data with the parse_ALE_Events.py script and subsequent
		consolidation, or a filtered version of the same (via the parse_ALE_Annotations.py
		program in this workflow). 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; assigning command-line arguments.
	2. Importing the contents of the DTL events data table into a Pandas dataframe.
		Optionally, create a indexing dictionary to enable conversion of nodes in 
			the dataframe to those used in R. 
	3. Consolidating the DTL events dataframe so that each row summarizes the number 
		of each event type occurring per node. 
		Optionally, use an input indexing file to convert the node numbers to those
			used in R. 
	4. Writing out the results to a tab-separated text file. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but is instead based on the input
		file name.  

Citation: 
	This program is a based off of the ALE parsing programs used in the ALE-pipeline 
		program written by Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil), 
		which can be found here: https://github.com/maxemil/ALE-pipeline

Version: 
	This is Version 2.0 of this program. It can optionally output a version of the 
		summary annotation table where the node numbers have been adjusted to match 
		those generated internally when the species tree is read into R, if an 
		indexing file is provided in the format:  R_Nodes\tOriginal_Nodes

Usage
	./parse_ALE_Nodes__v2.py input_events [R_indexing_file]
	OR
	python parse_ALE_Nodes__v2.py input_events [R_indexing_file]

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_events = sys.argv[1]
#input_events = "SP_Mito3__Events_final.txt"

#determine output file name based on input file name
base = os.path.basename(input_events)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_db = out_full + "_Nodes.txt"

if len(sys.argv) == 3: 
	#if the optional indexig file for node number conversion
	#to match the numbering system internal to R
	#is provided, then identify the indexng file
	R_indexing_file = sys.argv[2]
	#R_indexing_file = "ALE_2R_Indexing.txt"
	#and define a new output file
	output_db_R = out_full + "_Nodes_R.txt"


#Part 2: Import the contents of the DTL events data table into a Pandas dataframe
events_df = pd.read_csv(input_events, sep = '\t', header=0)
#the file is a tab-delimited text file, so the separator needs to be specified


if 'output_db_R' in vars(): 
	#check to see whether the option R-formatted node file has been requested
	#if so, create a an empty dictionary to store the node indexing information
	#ref: https://stackoverflow.com/questions/53961659/python-how-to-convert-txt-file-two-columns-to-dictionary-elements
	indexing_dict = {}
	with open(R_indexing_file, "r") as infile: 
		#open the indexing file for reading
		next(infile)
		#and skip the first line of the file  since it's a header line
		for line in infile: 
			#read through the indexing file line by line
			value, key = line.strip().split() 
			#split each line into two elements based on the tab placement
			#and remove the newline character at the end of the line
			#then save the node values to the indexing dictionary
			indexing_dict[key] = (value) 


#Part 3: Consolidate table so that each row summarizes the number of each event type per node

#drop the first column, containing the gene family IDs
events_df = events_df.iloc[: , 1:]

#group the rows based on the node IDs in the Node column
node_summary_df = events_df.groupby(['Node']).sum()
#and round the values to whole numbers for easier visualization
node_summary_df = node_summary_df.round(decimals=0)

#pull the nodes column out of the index
node_summary_df.reset_index(inplace=True)


if 'output_db_R' in vars(): 
	#check to see whether the option R-formatted node file has been requested
	#then use the dictionary to replace the ALE-derived node IDs 
	#with the R-generated node IDs
	#ref: https://sparkbyexamples.com/pandas/pandas-remap-values-in-column-with-a-dictionary-dict/#:~:text=Using%20Pandas%20DataFrame.-,replace(),regular%20expressions%20for%20regex%20substitutions.
	node_summary_df_R = node_summary_df.replace({"Node": indexing_dict})
	#and write out the results to a tab-separated text file
	node_summary_df_R.to_csv(output_db_R, sep = '\t', index=False)


#Part 4: Write out results to a tab-separated text file
node_summary_df.to_csv(output_db, sep = '\t', index=False)
