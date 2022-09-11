#!/bin/python
"""
Title: yLoc_Parser__v2.py
Date: 2022-03-01
Authors: Virág Varga

Description:
	This program parses the YLoc+* Animals search results and creates an output
		text file containing selected categories of information	for each query sequence.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	re

Procedure:
	1. Assigning command line arguments and output file name; loading modules.
	2. Preparing necessary elements for character removal using regex.
	3. Parsing through the file to extract desired information.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- This YLoc results parser is made specifically to suit the formatting
		of the YLoc+* Animals search output files. It has not been tested on the
		results files of other YLoc models.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.

Version:
	This is version 2.0 of this program. Slight alterations were made to the naming
		convention used, in order to keep the entire basename (minus the file extension),
		to eliminate issues related to files from the same species being overwritten
		when the program was used in a loop.

Usage
	./yLoc_Parser__v2.py input_file
	OR
	python yLoc_Parser__v2.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#Part 1: Setup

#import necessary modules
import sys #allow assignment of files from the command line
import os #allow access to computer files
import re #enables regex pattern matching


#assign command line argument
input_file = sys.argv[1]
#input_file = "ParserTestData/EP00771_Trimastix_marina_edit_YL.txt"
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_YLparsed.txt"
#output_file = "ParserTestData/EP00771_Trimastix_marina_edit_YL_YLparsed.txt"


#Part 2: Prepare necessary elements for character removal using regex

#create list of characters to remove with regex
characters_to_remove = "() =%"
#use string concatenation of add the [] characters so that the pattern isn't read in order,
#but instead all of these characters are individually removed
pattern = "[" + characters_to_remove + "]"


#Part 3: Parse through the file to extract desired information
#Part 4: Write out the results to the output file

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
	#open the input YLoc result file for reading
	#open the output file for writing
	outfile.write("Query" + "\t" + "Prediction" + "\t" + "Probability" + "\n")
	#the header line is prepared and written out to the output file
	for line in infile:
		#read through the file line by line
		line = line.strip()
		#remove the '\n' endline character from the line
		seq_list = [None] * 2
		#empty list seq_list will hold the alignment data associated with each query-target match
		#with each iteration of the loop, this list is overwritten
		if line.startswith('=== Prediction for sequence:'):
			#identify lines that start with "=== Prediction for sequence:"
			#this is the first line with information on the next query
			query_id_line = line.split('\t')
			#the line with the query id is 'split' - separated into a list based on the locations of spaces
			query_id = query_id_line[1]
			#save the second element of the list, which contains the actual query id
			query_id = re.sub(pattern, "", query_id)
			#remove the unnecessary characters and save the query id to variable query_id
			next_line = next(infile).strip()
			#save the next line, where the query protein prediction will be, without endline character
			query_results = next_line.split('\t')
			#the line with the query id is 'split' - separated into a list based on the locations of tabs
			query_results = query_results[1]
			#the item with index 1 in the query_results list is the query sequence prediction
			#so we save only that
			query_results = query_results.split("(")
			#split the results-containing string into the result and its probability
			query_results[1] = re.sub(pattern, "", query_results[1])
			#remove the unnecessary characters from the probability field
			query_results[1] = float(query_results[1])/100
			#turn the probability percentage into a float
			outfile.write('{}\t{}\t{}\n'.format(query_id, query_results[0], query_results[1]))
			#write out the results to the output file
