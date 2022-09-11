#!/bin/python
"""

Title: remove_nonStandardAA.py
Date: 17.12.2021
Author: Virág Varga

Description:
	This program removes non-standard amino acids from protein FASTA files.
		X and * characters are removed entirely from FASTA sequences, while
		selenocysteine (recorded as U) is replaced with simple cysteine (C).

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required modules & assigning command line argument.
	2. Parsing the input FASTA file in order to replace non-standard amino acids
		in the sequences. X and * characters are removed entirely from FASTA
		sequences, while selenocysteine (recorded as U) is replaced with simple
		cysteine (C).
	3. Writing out the new FASTA file with only standard amino acids.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is pre-determined (not user-defined), based on
		the name of the input FASTA file.

Usage
	./remove_nonStandardAA.py input_fasta
	OR
	python remove_nonStandardAA.py input_fasta

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#import necessary modules
import sys #allows execution of script from command line


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "non_standard_test.seq.fasta"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_StandardAA.fasta'


#write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input and output files
	for line in infile:
		#iterate through the input file line by line
		if not line.startswith(">"):
			#identify the sequence lines
			sequence = line.strip()
			#remove the "\n" endline character from the end of the sequence lines
			sequence = sequence.upper()
			#make sure all characters are uppercase
			#this should already be the case, but just in case an X is lowercase
			standard_seq = sequence.replace("U", "C")
			#replace the selenocysteines (U) with cysteines (C)
			standard_seq = standard_seq.replace("*", "")
			#remove non-standard * characters
			standard_seq = standard_seq.replace("X", "")
			#remove non-standard X characters
			#now print the standardized amino acid sequence to the outfile
			outfile.write(standard_seq + "\n")
		else:
			#sequence lines are copied to the outfile without changes
			outfile.write(line)
