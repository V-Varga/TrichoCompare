# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: calc_seq_length.py
Date: 2022-03-15
Author: Virág Varga

Description:
	This program parses a FASTA file and outputs a dataframe in the format:
		Query\tSequence_Length

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules & assigning command line argument.
	2. Parsing FASTA file to create dictionary of sequence lengths.
	3. Converting dictionary to Pandas dataframe & writing out results to a
		tab-separated text file.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is pre-determined (not user-defined), based on
		the name of the input FASTA file.

Usage
	./calc_seq_length.py input_fasta
	OR
	python calc_seq_length.py input_fasta

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import modules, set up command-line arguments

#import necessary modules
import sys #allows execution of script from command line
import pandas as pd #allows manipulation of dataframes in Python


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "Test_Files/EP00771_Trimastix_marina_edit.fasta"
output_file = ".".join(input_fasta.split('.')[:-1]) + '__SeqLength.txt'


#Part 2: Parse FASTA file to create dictionary of sequence lengths

#create empty dictionary to save sequence length data to
seq_length_dict = {}

with open(input_fasta, "r") as infile:
	#open the input FASTA file for reading
	for line in infile:
		#iterate through the file line by line
		line = line.strip()
		#remove the endline character ("\n") from the line
		if line.startswith(">"):
			#identify the header lines
			header = line[1:]
			#save the FASTA header without the ">" character at the beginning
			sequence = next(infile).strip()
			#move to the next line in the file (sequence line), and save that to variable
			#remove endline character ("\n") here, too
			seq_length = len(sequence)
			#calculate and save the sequence length to a variable
			#save the header (protein query ID) and sequence length to the sequence length dictionary
			seq_length_dict[header] = seq_length


#Part 3: Convert dictionary to Pandas dataframe & write out

#convert dictionary to Pandas dataframe
seq_length_df = pd.DataFrame.from_dict(seq_length_dict, orient='index', columns=['Seq_Length'])

#write out results to tab-separated text file
seq_length_df.to_csv(output_file, sep='\t', index=True, header=False)
#need `index=True` because the dictionary to dataframe conversion makes the queries into an index column
#use `header=False` to prevent column headers from printing, so species files can be concatenated easily
