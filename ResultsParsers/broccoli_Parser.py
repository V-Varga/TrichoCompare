#!/bin/python
"""

Title: broccoli_Parser.py
Date: 2022-02-11
Author: Virág Varga

Description:
	This program pivots the orthologous_groups.txt file, creating an output file that
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
	2. Using Pandas to import the contents of the orthologou_groups.txt file into a
		dataframe.
	3. Reorganizing the dataframe so that each protein query is in its own row.
	4. Writing out the results to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of the Broccoli results file, orthologous_groups.txt;
		or a file with identical formatting.

Usage
	./broccoli_Parser.py input_db output_db
	OR
	python broccoli_Parser.py input_db output_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
from  itertools import product


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "orthologous_groups.txt"
output_db = sys.argv[2]
#output_db = "Broccoli_OGs_parsed.txt"


#import input database into a Pandas dataframe
ortho_df = pd.read_csv(input_db, sep = '\t', header = 0)
#rename the first column header for ease of manipulation in Python
ortho_df.rename(columns={'#OG_name': 'Broccoli_OG', 'protein_names': 'Query'}, inplace=True)


#pull apart the parts of the database that are space-separated
#ie. flatten the database: each protein gets its own cell
#ref: https://stackoverflow.com/questions/50789834/parse-a-dataframe-column-by-comma-and-pivot-python
df1 = ortho_df.applymap(lambda x: x.split(' ') if isinstance (x, str) else [x])
#split apart the comma-separated lists of protein ids in each cell
df2 = pd.DataFrame([j for i in df1.values for j in product(*i)], columns=ortho_df.columns)
#give each protein ID its own cell, while still associated with the species ID and OG


#flip the column order, putting the proteins in the first column
final_df = df2.iloc[:, ::-1]


#now write out the results to a tab-separated text file
final_df.to_csv(output_db, sep='\t', index=False)
