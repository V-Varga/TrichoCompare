# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: subfilter_ALE_GFam_CHOICE.py
Date: 2022.09.13
Author: Virág Varga

Description:
	This program parses data from the Gene Family-based reformatting of the ALE results 
		data produced by the parse_ALE_Nodes_GFam_Annot.py program in order the return 
		information on which type of DTL even occurred at which node of the species
		tree. It is intended for use on the original node IDs, not the R-reformatted
		ones. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Importing data into Pandas dataframe. 
	3. Extracting query OGs matching the search criteria
	4. Writing out results to a text file. 

Known bugs and limitations:
	- There is only limited quality-checking integrated into the code.
	- This program requires the input of an OG database produced by the 
		parse_ALE_Nodes_GFam_Annot.py program. 
	- The output file name is only partially user-defined.

Usage
	./subfilter_ALE_GFam_CHOICE.py input_db query_node DTL_search output_extension 
	OR
	python subfilter_ALE_GFam_CHOICE.py input_db query_node DTL_search output_extension 

	Where the query_node is the number assigned to the query node in the ALE analysis; and 
		the pre_query_node is the number assigned to the node ancestral to the query node 
		(previous node, up by 1). These are not always numerically linked!
	Where the DTL_search variable should be one of the following: "Losses" OR "Originations"
		OR "Copies" in order to signify the type of DTL event information to be returned to 
		the user. 

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
#input_db = "SP_Mito3__Events_Final_GFam.txt"

#query node
query_node = int(sys.argv[2])
#query_node = 44 #Trichomonas vaginalis node

#select type of DTL event to be searched
DTL_search = sys.argv[3]
#DTL_search = "Originations"
#define the acceptable values for the DTL event options
DTL_profile = ["Losses", "Originations", "Copies"]


#quick basic QC on DTL event category
if DTL_search not in DTL_profile: 
	#test to make sure an existing DTL event type was selected
	#return this message to the command line if an incorrect option was given
	print("Note that the acceptable DTL event options are: 'Losses' OR 'Originations' OR 'Copies'. Please try again.")
	#and exit the program
	sys.exit(1)
else: 
	#if the node and presence absence choices are acceptable
	#return the following message to the stdout & continue running the program
	print("Testing for DTL event "+ DTL_search + " at node " + str(query_node) + ".")


#output file
output_extension = sys.argv[4]
#output_extension = "Tvag"
#determine file name suffix/extension for query
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_db = out_full + "_" + output_extension + ".txt"


#Part 2: Import data into Pandas dataframes

#read in the input dollo parsimony data file, assigning the first row as a header row
input_df = pd.read_csv(input_db, sep = '\t', header=0)
#the file is a tab-delimited text file, so the separator needs to be specified
#the header can be found in the first row (pythonic index 0)


#Part 3: Extracting query OGs matching the search criteria

#create an empty list that will contain OG IDs that match the query
good_OG_list = []

#next, iterate over the database & convert protein loss to OG loss
for index, row in input_df.iterrows():
	#iterate through the dataframe row by row
		if row['Node'] == str(query_node): 
			#identify rows where info on the query_node is contained
			event_presence = row[DTL_search]
			#save the contents of the queried DTL event number to variable event_presence
			if int(event_presence) > 0:
				#identify events that exist at that node
				#and append the OG ID from that node to the list of good OGs
				good_OG_list.append(row['Gene_Family'])


#Part 4: Write out results to a text file

with open(output_db, 'w') as outfile: 
	#open the outfile for writing
	#and write a quick contextual introduction to the contents of the file.
	outfile.write("At node " + str(query_node) + ", the following OGs met the search criteria." + "\n")
	outfile.write("The DTL query category was: " + DTL_search + "\n")
	#for ease of perusal, include the number of OGs matching the query criteria
	outfile.write("A total of " + str(len(good_OG_list)) + " OGs met the search criteria. They are included below:" + "\n")
	for good_OG in good_OG_list: 
		#iterate over the list of OGs matching the search criteria
		#and write them out to the results file
		outfile.write(good_OG + "\n")
