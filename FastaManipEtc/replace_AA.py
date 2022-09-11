#!/bin/python
"""

Title: replace_AA.py
Date: 21.12.2021
Author: Virág Varga

Description:
	This program replaces a selected non-standard amino acid in a protein FASTA
		with a chosen replacement.
	It is intended for use in instances of uncertain amino acids (ex.: "B", "Z",
		or "J"). In these instances, the user can replace the uncertain amino acid
		with their choice of replacement. If no replacement is given, the uncertain
		amino acid is simply removed.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required modules & assigning command line argument.
	2. Parsing the input FASTA file in order to replace selected non-standard
		amino acid in the sequences with chosen replacement.
	3. Writing out the new FASTA file with standardized amino acids.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is pre-determined (not user-defined), based on
		the name of the input FASTA file.

Usage
	./replace_AA.py input_fasta nonStandard_aa replacement_aa
	OR
	python replace_AA.py input_fasta nonStandard_aa replacement_aa

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#import necessary modules
import sys #allows execution of script from command line


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "non_standard_test.seq.fasta"
nonStandard_aa = sys.argv[2]
if len(sys.argv) == 4:
	replacement_aa = sys.argv[3]
else:
	replacement_aa = ""
#nonStandard_aa = "B"
#replacement_aa = "D"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_replaceAA_' + replacement_aa + '.fasta'


#write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input and output files
	for line in infile:
		#iterate through the input file line by line
		if not line.startswith(">"):
			#identify the sequence lines
			sequence = line.strip()
			#remove the "\n" endline character from the end of the sequence lines
			sequence = sequence.replace(nonStandard_aa, replacement_aa)
			#replace non-standard characters
			#now print the standardized amino acid sequence to the outfile
			outfile.write(sequence + "\n")
		else:
			#sequence lines are copied to the outfile without changes
			outfile.write(line)
