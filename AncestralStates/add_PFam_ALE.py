# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: add_PFam_ALE.py
Date: 2022.07.05
Author: Virág Varga

Description:
	This program adds PFam annotation information based on OG IDs to a concatenated
		ALE results table reporting OG information per gene family and per node.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Importing the data into Pandas dataframes.
	3. Reformatting the input dataframe to match the PFam dataframe's data formatting.
	4. Adding the PFam annotation information into the input dataframe, and 
		restructuring the column order.
	5. Writing out the results to a tab-delimited text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
    - The output file name is not user-defined, but is instead based on the input
        file name. 
	- This program requires the input of a file in the format [OG_ID]\tQuery\tSpecies_Id
		(created by either the og_prot_spp_list.py or filter_OG_profile.py scripts) and a
		file in the format [OG_ID]\t[PFam_Data] (created by the og2PFam_pivot__v2.py script).

Version:
	This program is modified from the create_counts_table.py script. The original was 
		written to create the data table that could be used as input for the Count 
		program, while this script adds annotations to the concatenated parsed 
		results of the ALE pipeline. 

Usage
	./add_PFam_ALE.py input_db input_pfams
	OR
	python add_PFam_ALE.py input_db input_pfams

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allow execution of code from the command line
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "SP_Mito3__Events_Final.txt"
input_pfams = sys.argv[2]
#input_pfams = "OG_Lists/OGs2PFams_SonicParanoid_OG_Counts.txt"

#determine output file name based on input file name
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_db = out_full + "_PFam.txt"


#Part 2: Import the data into Pandas dataframes

input_df = pd.read_csv(input_db, sep = '\t', header=0)
#read in the filtered OG_ID\tQuery\tSpecies_Id dataframe

pfam_df = pd.read_csv(input_pfams, sep = '\t', header=0)
#creating a dataframe for the OG_ID\tPFam
og_col = pfam_df.columns[0]
#extract the name of the OG ID columns


#Part 3: Reformat input dataframe to match PFam dataframe data formatting

input_df[og_col] = input_df['Gene_Family'] 
#duplicate the OG column of the input dataframe
#name the new column to match the PFam dataframe

input_df[og_col] = input_df[og_col].str.split('__').str.get(-1)
#split elements of the column based on the placement of the double underscore ("__")
#ref: https://stackoverflow.com/questions/63934605/pandas-dataframe-column-remove-string-before-the-first-specific-character


#Part 4: Adding the PFam information into the dataframe

annot_df = input_df.merge(pfam_df, on=og_col, how='left').fillna('-')
#want to do left merge, because the PFam reference dataframe has information on all OGs
#but we only need the information for the filtered OGs in the pivot table
#this adds the annotation column to the rightmost end, which is where it needs to be

annot_df.drop([og_col], axis=1, inplace=True)
#drop the now-unnecessary original OG name column

pfam_col = annot_df.columns[-1]
#extract the name of the PFam annotation column
#using a variable here enables both count-based and non-count-based PFam annotation
annot_df = annot_df[['Gene_Family', pfam_col, 'Node', 'Duplications', 'Transfers', 
					 'Losses', 'Originations', 'Copies']]
#rearrange the column order to pull PFam information into the second column


#Part 5: Writing out the results

annot_df.to_csv(output_db, sep='\t', index=False)
#write out results to a tab-delimited text file
