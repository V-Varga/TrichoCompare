#!/bin/python
"""

Title: remove_nonM.py
Date: 17.12.2021
Author: Virág Varga

Description:
	This program removes sequences from a protein FASTA file if the sequence does
		not start with Methionine (M).

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required modules & assigning command line argument.
	2. Parsing the input FASTA file in order to remove sequences that do not start
		with Methionine (M).
	3. Writing out the new FASTA file with only standard amino acids.


Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is pre-determined (not user-defined), based on
		the name of the input FASTA file.

Usage
	./remove_nonM.py input_fasta
	OR
	python remove_nonM.py input_fasta

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#import necessary modules
import sys #allows execution of script from command line


#load input and output files
input_fasta = sys.argv[1]
#input_fasta = "non_standard_test.seq_StandardAA.Bad_M.fasta"
output_fasta = ".".join(input_fasta.split('.')[:-1]) + '_nonM.fasta'


#write the program
with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
	#open the input and output files
	for line in infile:
		#iterate through the input file line by line
		if line.startswith(">"):
			#identify the header lines
			header = line.strip()
			#remove the "\n" endline character from the end of the header lines
		if line.startswith("M"):
			#identify sequence lines that start with "M"
			sequence = line.strip()
			#remove the "\n" endline character from the end of the sequence lines
			#now print the standardized amino acid sequence to the outfile
			outfile.write(header + "\n" + sequence + "\n")
