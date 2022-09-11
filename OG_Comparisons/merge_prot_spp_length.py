# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: merge_prot_spp_length.py
Date: 2022-03-12
Author: Virág Varga

Description:
	This program merges the protein query IDs to species categories & phyla dataframe
		with the protein query IDs to sequence lengths dataframe, and writes out the
		resulting dataframe to a tab-separated text file.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Assigning command-line arguments, import modules.
	2. Importing input data into Pandas dataframes.
	3. Merging species and sequence length dataframes.
	4. Writing out the dataframe to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.

Usage
	./merge_prot_spp_length.py species_db seqlength_db output_db
	OR
	python merge_prot_spp_length.py species_db seqlength_db output_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Assign command-line arguments, import modules

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line arguments; load input and output files
species_db = sys.argv[1]
#species_db = "Prots_Species_Phyla_DB.txt"
seqlength_db = sys.argv[2]
#seqlength_db = "prot_lengths_ref.txt"
output_db = sys.argv[3]
#output_db = "Prots_Species_Phyla_SeqLength_DB.txt"


#Part 2: Import data into Pandas dataframes

#import query to species categories dataframe into Pandas
species_df = pd.read_csv(species_db, sep = "\t", header=0)

#set names of columns for imported sequence length dataframe
colnames=['Query', 'Sequence_Length']
#import sequence length database into a Pandas dataframe
seq_length_df = pd.read_csv(seqlength_db, sep = '\t', names=colnames, header=None)


#Part 3: Merge dataframes

merged_df = species_df.merge(seq_length_df, how='outer')
#since the species_df is given the merge command, the data from it will be on the left,
#while the data from seq_length_df will be on the right
#the `how='outer'` argument ensures that all queries are kept, even the ones without overlap
#it isn't particularly important here, though, since the dataframes are the same length


#Part 4: Write out resulting dataframe to a tab-separated text file

#write out the resulting dataframe
merged_df.to_csv(output_db, sep='\t', index=False)
