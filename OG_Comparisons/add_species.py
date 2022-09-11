# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: add_species.py
Date: 2022-03-02
Author: Virág Varga

Description:
	This program adds the species name (extracted from the file name) to the
		second column of a file containing nothing but a list of protein query IDs.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the input file into a
		dataframe.
	3. Adding the species identifier to the dataframe as a new column, and writing
		out the result to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-determined.

Usage
	./add_species.py input_file
	OR
	python add_species.py input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part1: Assign command-line arguments, import modules

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line arguments; load input and output files
input_file = sys.argv[1]
#input_file = "EP00771_Trimastix_marina_edit_prots.txt"
#define the output file based on the input file name
base = os.path.basename(input_file)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_species.txt"


#Part 2: Import into Pandas and add new species designation column

#import input database into a Pandas dataframe
prot_df = pd.read_csv(input_file, header = None)

#extract species designation
species = out_full.replace('_edit_prots', '')
#create new column filled with species designation
prot_df[len(prot_df.columns)] = species

#write out the resulting dataframe
prot_df.to_csv(output_file, sep='\t', index=False, header=False)
