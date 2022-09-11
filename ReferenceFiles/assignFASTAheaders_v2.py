#!/bin/python
"""

Title: assignFASTAheaders_v2.py
Date: 28.11.2021
Author: Virág Varga

Description:
	This program replaces FASTA headers in a FASTA file with a 16-character random
		alphanumeric code. A reference file is also printed that links the
		random code to the original FASTA header. A larger reference file is used
		as input and then appended to in order to ensure that no alphanumeric header
		is repeated.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	re
	random
	string
	pandas

Procedure:
	1. Loading required modules & assigning command line argument.
    2. Contents of the large reference database are loaded into a Pandas dataframe,
		and existing alphanumeric headers are extracted to ensure no repitition.
	3. Parsing the input FASTA file in order to extract headers and generate
		random alphanumeric codes to replace them.
	4. Writing out the new FASTA file with the alphanumeric code headers,
		accompanied by the reference file.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.

Version: 2.0
	The previous version of this script (assignFASTAheaders.py) did not include any
		mechanism for ensuring that the alphanumeric headers were not repeated.

Usage
	./assignFASTAheaders.py input_fasta ref_file
	OR
	python assignFASTAheaders.py input_fasta ref_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#import necessary modules
import sys #allows execution of script from command line
import re #enables regex pattern matching
import random #enables random number & variable generation
import string #imports a collection of string constants
import pandas as pd #allows manipulation of dataframes


#load input and output files
input_fasta = sys.argv[1]
ref_db_file = sys.argv[2]
#ref_db_file = "Extract__encoding_summary_ref.txt"
#input_fasta = "Extract__Carpediemonas_membranifera.PRJNA719540.fasta"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_edit.fasta'
ref_doc = ".".join(input_fasta.split('.')[:-1]) + '_ref.txt'


#write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile, open(ref_doc, "w") as outref, open(ref_db_file, "r+") as ref_db:
	#open the input and output files
	#start by importing the large reference database into a Pandas dataframe
	ref_df = pd.read_csv(ref_db, sep="\t", header=None)
	encoding_list = ref_df[0].tolist()
	#open the input and output files
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines
			header = line
			#remove the ">" character at the start of the line
			#this enables easier manipulation of the FASTA header
			header = re.sub(">", "", header)
			while True:
				#generate a random 16-character alphanumeric string to replace the original header
				assigned_header = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
				if len(encoding_list) > 0:
					#check if the reference database-derived encoding list exists
					#if it does, check that the same alphanumeric code hasn't already been used somewhere
					if assigned_header not in encoding_list:
						break
			#now print the new header to the outfile
			outfile.write(">" + assigned_header + "\n")
			#and print the assigned reference to the outref file
			outref.write(assigned_header + "\t" + header)
			#add the header to the large reference dataframe
			ref_db.write(assigned_header + "\t" + header)
		else:
			#sequence lines are copied to the outfile without changes
			outfile.write(line)
