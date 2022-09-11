#!/bin/python
"""

Title: orthoFinder_Parser.py
Date: 2022-02-11
Author: Virág Varga

Description:
	This program pivots the Orthogroups.tsv file's data, creating an output file that
		contains query proteins in individual columns and the OG associated with them
		in a cell in the same row.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas
	itertools

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the Orthogroups.tsv file into a
		dataframe.
	3. Condensing the contents of all species columns into 1 large column, then
		separating out the protein ids into unique cells (instead of comma-separated
		strings in each cell), and then flipping the column order so that the query
		protein IDs are in the first column.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of the OrthoFinder results file, Orthogroups.tsv;
		or a file with identical formatting.

Version:
	This script can be considered a "Version 2" of the pivot_OGs.py script, with minor
		changes made due to a better understanding of the sorts of output files needed.

Usage
	./orthoFinder_Parser.py input_db output_db
	OR
	python orthoFinder_Parser.py input_db output_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
from  itertools import product


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "Orthogroups.tsv"
output_db = sys.argv[2]
#output_db = "OF_OGs_parsed.txt"


#import input database into a Pandas dataframe
ortho_df = pd.read_csv(input_db, sep = '\t', header = 0)
#rename the first column header for ease of manipulation
ortho_df.rename(columns={'Orthogroup': 'OrthoFinder_OG'}, inplace=True)


#first, condense the contents of the species columns,
#since the species information is unnecessary (already in large database)
ortho_df = ortho_df.melt(id_vars="OrthoFinder_OG", var_name="Species", value_name="Query")
#melting the database like this creates 3 columns


#pull apart the parts of the database that are comma-separated
#ie. flatten the database: each protein gets its own cell
#ref: https://stackoverflow.com/questions/50789834/parse-a-dataframe-column-by-comma-and-pivot-python
df1 = ortho_df.applymap(lambda x: x.split(', ') if isinstance (x, str) else [x])
#split apart the comma-separated lists of protein ids in each cell
df2 = pd.DataFrame([j for i in df1.values for j in product(*i)], columns=ortho_df.columns)
#give each protein ID its own cell, while still associated with the species ID and OG


#flip the column order, putting the proteins in the first column
df3 = df2.iloc[:, ::-1]

#remove rows where ""Query"" column contains a nan as the null indicator
final_df = df3[df3['Query'].notna()]


#now write out the results to a tab-separated text file
final_df.to_csv(output_db, sep='\t', index=False)
