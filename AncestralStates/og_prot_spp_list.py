# -*- coding: utf-8 -*-
#!/bin/python
"""

Title:og_prot_spp_list.py
Date: 2022-05-09
Author: Virág Varga

Description:
	This program filters any version of the large Metamonad database that includes
		query IDs, species category designation, and OG ID information from the
		oerthologous clustering program of interest.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Importing modules and assigning command-line arguments.
	2. Importing input data into Pandas dataframe.
	3. Filtering the metamonad database to only include relevant OG ID, Query
		protein ID and species ID desigantions, before writing out results to
		a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but instead based on the input
		OG ID column name.

Usage
	./og_prot_spp_list.py input_db og_col
	OR
	python og_prot_spp_list.py input_db og_col

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import modules and assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line argument; load input and output files
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__filt_scores-startAA-pfam__HEAD200.txt"
og_col = sys.argv[2]
#og_col = "SonicParanoid_OG"
output_db = og_col + '__Prot_Spp.txt'


#Part 2: Import data into Pandas dataframes

#import Metamonad database into a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)
# sys:1: DtypeWarning: Columns (6,7,27,31) have mixed types.Specify dtype option on import or set low_memory=False.


#Part 3: Extract relevant data & write out results

filt_input_df = input_df[[og_col, 'Query', 'Species_Id']].copy()
#copy the relevant columns to a new dataframe

og_df = filt_input_df[filt_input_df[og_col] != "-"].copy()
#remove protein queries without an OG ID from the datafram
og_df.sort_values(by = og_col, inplace=True)
#order the rows by OG ID to make the dataframe look nicer


#write out the resulting dataframe
og_df.to_csv(output_db, sep='\t', index=False)
