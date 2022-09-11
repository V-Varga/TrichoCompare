# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: create_counts_table.py
Date: 2022.05.09
Author: Virág Varga

Description:
	This program creates a pivot table of counts of proteins present in an OG
		per species, as well as the PFam annotations associated with those OGs, on
		the basis of a file in the format [OG_ID]\tQuery\tSpecies_Id (created by either
		the og_prot_spp_list.py or filter_OG_profile.py scripts) and a file in the
		format [OG_ID]\t[PFam_Data] (created by the og2PFam_pivot__v2.py script).

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Importing the data into Pandas dataframes.
	3. Pivot the data table so that eeach row contains one OG ID, with information
		on the number of proteins present in that OG in each species in columns with
		the species IDs as the headers.
	4. Adding the PFam annotation information onto the end of the dataframe.
	5. Writing out the results to a tab-delimited text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a file in the format [OG_ID]\tQuery\tSpecies_Id
		(created by either the og_prot_spp_list.py or filter_OG_profile.py scripts) and a
		file in the format [OG_ID]\t[PFam_Data] (created by the og2PFam_pivot__v2.py script).

Version:
	This program can be considered a Version 2.0 of the pivotCounts.py script, with some
		aspects of the annotateCounts.py script included. This script integrates integrates
		the functionality of those earlier scripts, and accomadates the greater diversity
		of input data being used.

Usage
	./create_counts_table.py input_db input_pfams output_db
	OR
	python create_counts_table.py input_db input_pfams output_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allow execution of code from the command line
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "MetamonadCtrl_mito_3_SP_OGProtSpp.txt"
input_pfams = sys.argv[2]
#input_pfams = "OGs2PFams_SonicParanoid_OG_Counts.txt"
output_db = sys.argv[3]
#output_db = "MetamonadCtrl_mito_3_SP__CountPivot.txt"


#Part 2: Import the data into Pandas dataframes

input_df = pd.read_csv(input_db, sep = '\t', header=0)
#read in the filtered OG_ID\tQuery\tSpecies_Id dataframe
og_col = input_df.columns[0]
#extract the name of the OG ID columns

pfam_df = pd.read_csv(input_pfams, sep = '\t', header=0)
#creating a dataframe for the OG_ID\tPFam


#Part 3: Creating the pivot table of OG, protein & species ID data

#create the pivot table
count_df = pd.pivot_table(data=input_df, index=og_col, values= 'Query', columns='Species_Id',
						  aggfunc='count', fill_value=0)
#the Orthogroup data is used as the index, the data in the Query column is used to fill the table
#and the Species_Id categories are used as headers
#`aggfunc='count'` fills the columns with counts of unique appearances (vs. the actual protein IDs themselves)
#`fill_value=0` fills empty cells with 0 (zero) instead of NaN (don't have to do it manually later)
count_df.reset_index(inplace=True)
#reset the headers to move the OG IDs out of the index


#Part 4: Adding the PFam information into the dataframe

annot_df = count_df.merge(pfam_df, on=og_col, how='left')
#want to do left merge, because the PFam reference dataframe has information on all OGs
#but we only need the information for the filtered OGs in the pivot table
#this adds the annotation column to the rightmost end, which is where it needs to be


#Part 5: Writing out the results

annot_df.to_csv(output_db, sep='\t', index=False)
#the Count program needs the input data table to be in tab-delimited formatting
