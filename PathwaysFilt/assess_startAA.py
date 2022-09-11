# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: assess_startAA.py
Date: 2022.04.28
Author: Virág Varga

Description:
	This program determines the first amino acid of each protein sequence in a protein
		FASTA file, and produces an output file in the format:
			Query\tStartAA
		Where the options for "StartAA" are: Met OR Leu OR ELSE

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	re
	pandas

Procedure:
	1. Loading required modules & assigning command line argument.
    2. Iterating over the file to collect the data on the first amino acid for each
		FASTA sequence, which is saved to a dictionary.
	3. Converting the dictionary to a Pandas dataframe, and writing out the results
		to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not defined by the user, but based instead on the
		input file name.

Usage
	./assess_startAA.py input_fasta
	OR
	python assess_startAA.py input_fasta

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules & command line argument

#import necessary modules
import sys #allows execution of script from command line
import re #enables regex pattern matching
import pandas as pd #allows manipulation of dataframes


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "EP00771_Trimastix_marina_edit_50.fasta"
output_db = ".".join(input_fasta.split('.')[:-1]) + '_startAA.txt'


#Part 2: Iterate over the file to collect the data

#create an empty dictionary to hold the association data
startAA_dict = {}

with open(input_fasta, "r") as infile:
	#open the input file for reading
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines
			header = line.strip()
			#save the contents of the line, without the endline character, to a variable
			header = re.sub(">", "", header)
			#remove the ">" character at the front of the string
			#now we have the actual protein ID saved to a variable
			#so skip on to the next line
			sequence = next(infile)
			#and now determine the first amino acid in each sequence
			if sequence.startswith("M"):
				#if Methionine is the first amino acid in the protein sequence
				#add the protein ID and to the dictionary associated with Methionine
				startAA_dict[header] = "Met"
			elif sequence.startswith("L"):
				#if Leucine is the first amino acid in the protein sequence
				#add the protein ID and to the dictionary associated with Leucine
				startAA_dict[header] = "Leu"
			else:
				#if neither Methionine not Leucine is the first amino acid in the protein sequence
				#add the protein ID and to the dictionary without an amino acid association
				startAA_dict[header] = "ELSE"


#Part 3: Convert the dictionary to a Pandas dataframe and write out

#convert the dictionary to a dataframe using the keys as the row indexes
startAA_df = pd.DataFrame.from_dict(startAA_dict, orient='index')
#then pull the query ID information out of the index
startAA_df.reset_index(inplace=True)
#and rename the columns
startAA_df.rename(columns={"index": "Query", 0: "StartAA"}, inplace=True)


#write out results to tab-separated text file
startAA_df.to_csv(output_db, sep='\t', index=False)
