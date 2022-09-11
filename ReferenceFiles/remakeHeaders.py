#!/bin/python
"""

Title: remakeHeaders.py
Date: 2022-02-08
Author: Virág Varga

Description:
	This program replaces the original FASTA headers with the random alphanumeric
		headers assigned by the assignFASTAheaders.py program, using the
		reference file created by the other program as a guide.
	This program was created as a result of the accidental deletion of a number of
		the encoded FASTA files, in order to recreate them.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	re
	pandas

Procedure:
	1. Loading required modules & assigning command line arguments.
	2. Using Pandas to load the contents of the reference file into a dictionary.
	3. Parsing the input FASTA file in order to match the random headers to the
		original headers via the reference file.
	4. Writing out the new FASTA file with the original FASTA headers.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The user needs to check that the correct reference file is assigned.

Usage
	./remakeHeaders.py input_fasta ref_doc
	OR
	python remakeHeaders.py input_fasta ref_doc

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#import necessary modules
import sys #allows execution of script from command line
import re #enables regex pattern matching
import pandas as pd #allow manipulation of data files


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "Test_Files/EP00771_Trimastix_marina.fasta"
#the user choses the specific file, in case it isn't the original FASTA being used for the reversal
ref_doc = sys.argv[2]
#ref_doc = "Test_Files/EP00771_Trimastix_marina_ref.txt"
#output_fasta name is based on the input_fasta name
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_edit.fasta'


#create and populate dictionary using the reference file
with open(ref_doc, "r") as inref:
	REF = pd.read_csv(inref, sep="\t", header=None)
	REF = REF.set_index(0)
	ref_dict = REF.T.to_dict('list')
	#note that this manner of conversion makes the dictionary value a list


#write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input and output fasta files
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines
			header = line.strip()
			#remove the ">" character at the start of the line
			#this enables easier manipulation of the FASTA header
			header = re.sub(">", "", header)
			#iterate through the reference dictionary keys
			for k in ref_dict.keys():
				#save the original header to a variable
				og_header = ref_dict[k]
				#the original header will be in list form, so need to convert to string
				og_header = ' '.join([str(item) for item in og_header])
				if header == og_header:
					#match the original headers in the FASTA & reference files
					#now print the new header to the outfile
					outfile.write(">" + k + "\n")
		else:
			#sequence lines are copied to the outfile without changes
			outfile.write(line)
