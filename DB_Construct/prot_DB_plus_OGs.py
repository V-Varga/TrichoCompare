# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: prot_DB_plus_OGs.py
Date: 2022-03-19
Author: Virág Varga

Description:
	This program conbines the data from the large predicted protein function database with
		the parsed results files of the  broccoli_Parser.py, proteinOrtho_Parser.py, 
		orthoFinder_Parser.py and sonicParanoid_Parser.py scripts. 
		The data in these parsed files is concatenated into one large, flat database.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas
	functools.reduce

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas import the contents of the Broccoli, ProteinOrtho, OrthoFinder and
		SonicParanoid parsed results files.
	3. Cpncatenating the databases and filling NaN values with "-".
	4. Writing out the results to a tab-delimited text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of the parsed files created thorugh the use of
		broccoli_Parser.py, proteinOrtho_Parser.py, orthoFinder_Parser.py and sonicParanoid_Parser.py
		parser programs.
	- All input and output files are user-defined: This means the user must ensure that
		the correct file names have been assigned to the program.

Usage
	./prot_DB_plus_OGs.py Prot_DB Broccoli_Parsed ProteinOrtho_Parsed OrthoFinder_Parsed SonicParanoid_Parsed Output_DB
	OR
	python prot_DB_plus_OGs.py Prot_DB Broccoli_Parsed ProteinOrtho_Parsed OrthoFinder_Parsed SonicParanoid_Parsed Output_DB

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
from functools import reduce #allow same function to be applied iteratively


#assign command line arguments: input & output files
#input parsed OG files
Prot_DB = sys.argv[1]
Broccoli_Parsed = sys.argv[2]
ProteinOrtho_Parsed = sys.argv[3]
OrthoFinder_Parsed = sys.argv[4]
SonicParanoid_Parsed = sys.argv[5]
#output final database
Output_DB = sys.argv[6]


#Part 2: Importing parsed data file contents into Pandas dataframes

#Large protein functional annotation database
with open(Prot_DB, "r") as prot_infile:
	#open the protein functional prediction data file
	prot_df = pd.read_csv(prot_infile, sep='\t', header = 0, low_memory=False)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	prot_df = prot_df.set_index('Query')
	#set the first column (containing query sequence names) as an index

#Broccoli results
with open(Broccoli_Parsed, "r") as broccoli_infile:
	#open the parsed Broccoli data file
	broccoli_df = pd.read_csv(broccoli_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	broccoli_df = broccoli_df.set_index('Query')
	#set the first column (containing query sequence names) as an index

#ProteinOrtho results
with open(ProteinOrtho_Parsed, "r") as proteinortho_infile:
	#open the parsed ProteinOrtho data file
	proteinortho_df = pd.read_csv(proteinortho_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	proteinortho_df.drop(proteinortho_df.columns[1], axis=1, inplace=True)
	#drop the species column of the dataframe
	proteinortho_df = proteinortho_df.set_index('Query')
	#set the first column (containing query sequence names) as an index

#OrthoFinder results
with open(OrthoFinder_Parsed, "r") as orthofinder_infile:
	#open the parsed OrthoFinder data file
	orthofinder_df = pd.read_csv(orthofinder_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	orthofinder_df.drop(orthofinder_df.columns[1], axis=1, inplace=True)
	#drop the species column of the dataframe
	orthofinder_df = orthofinder_df.set_index('Query')
	#set the first column (containing query sequence names) as an index

#SonicParanoid results
with open(SonicParanoid_Parsed, "r") as sonicparanoid_infile:
	#open the parsed SonicParanoid data file
	sonicparanoid_df = pd.read_csv(sonicparanoid_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	sonicparanoid_df.drop(sonicparanoid_df.columns[1], axis=1, inplace=True)
	#drop the species column of the dataframe
	sonicparanoid_df = sonicparanoid_df.set_index('Query')
	#set the first column (containing query sequence names) as an index


#Part 3: Merge the dataframes and write out

#ref: https://stackoverflow.com/questions/44327999/python-pandas-merge-multiple-dataframes
#save the dataframes to be merged into a list
data_frames = [prot_df, broccoli_df, proteinortho_df, orthofinder_df, sonicparanoid_df]
#merge the dataframes iteratively using reduce
merged_df = reduce(lambda  left,right: pd.merge(left,right,on=['Query'], how='outer'), data_frames).fillna('-')


#merged_df = pd.concat([prot_df, broccoli_df, proteinortho_df, orthofinder_df, sonicparanoid_df], axis=1).reset_index(inplace=True, drop=True)
#concatenate the dataframes along the x axis, horizontally
#merged_df.fillna('-', inplace=True)
#fill empty cells with string "-"


#write out results to tab-delimited text file
merged_df.to_csv(Output_DB, sep='\t', index=True)
#since the Query columns got shifted into indexes, need to use `index=True`
