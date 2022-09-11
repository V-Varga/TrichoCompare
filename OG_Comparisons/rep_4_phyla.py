# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: rep_4_phyla.py
Date: 2022-03-21
Author: Virág Varga

Description:
	This program performs filters the parsed results of orthologous clustering software
		(OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) in order to identify OGs
		that are present in either the 4 main phyla, or the 4 main phyla and more basal
		species.
		An optional argument allows the isolation of OGs that are found in all 4 phyla
			and the basal species (Barthelona).

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	sys
	pandas
	os

Procedure:
	1. Importing necessary modules, assigning command-line arguments.
	2. Importing data into Pandas dataframes.
	3. Setting up data types (dataframe for ref file, dictionary for infile) that will be used.
	4. Creating dictionary of phyla represented in each OG.
	5. Identifying OGs that include representatives of all 4 phyla.
	6. Copying threshold-meeting OG information into a new dataframe & writing out.
	7. (Optional) Writing out only those OGs that include the 4 main phyla and Barthelona
		This step can be called with the use of the string "other" as the 4th command-line argument.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file(s) is/are not user-defined.
	- The input file used for the program must be an un-pivoted results file of either
		Broccoli, OrthoFinder, SonicParanoid, or ProteinOrtho, following the structure
		used by the parsers used previously in this workflow.
	- The program cannot accept multiple input parsed OG files simultaneously.
	- In order to activate the optional argument to output OGs including the 4 main phyla
		and Barthelona, the user must provide the string "other" as the 4th command-line argument.

Usage:
	./rep_4_phyla.py input_db ref_db ["other"]
	OR
	python rep_4_phyla.py input_db ref_db ["other"]

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files


#designate input file name as variable
infile = sys.argv[1]
#designate reference file name as variable
ref_db = sys.argv[2]

#define the output file based on the input file name
base = os.path.basename(infile)
out_full = os.path.splitext(base)[0]
output_file = out_full + "_min4Phyla.txt"


#Part 2: Import data into Pandas dataframes

#import input file into pandas dataframe
ortho_df = pd.read_csv(infile, sep = '\t', header = 0)

#remove 3rd column from Pandas dataframe if necessary
#needed for original parsed results of OrthoFinder, ProteinOrtho & SonicParanoid
col_num = len(ortho_df.columns)
#count number of columns
if col_num == 3:
	#select dataframes with 3 columns
	#remove middle column with species information
	ortho_df.drop(ortho_df.columns[1], axis=1, inplace=True)


#import reference file into Pandas dataframe
ref_df = pd.read_csv(ref_db, sep = '\t', header = 0)


#Part 3: Set up data types (dataframe for ref file, dictionary for infile) that will be used

#identify OG column name (for use later)
og_col = ortho_df.columns[1]

#create a dictionary in the format: og_dict[og_id] = list_of_proteins
#this will allow easier analysis
grouped_ortho_df = ortho_df.groupby(og_col)['Query'].apply(list).reset_index(name="OG_members")
#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
#the new column of lists is named 'OG_members'
ortho_dict = grouped_ortho_df.set_index(og_col).to_dict()['OG_members']
#the new dataframe is converted into a dictionary,
#where the OG IDs are the keys, and the lists of protein members of the OGs are the values


#Part 4: Create dictionary of phyla represented in each OG

#create empty dictionary for phyla information
phyla_OG_dict = {}

for key in ortho_dict.keys():
	#iterate over the dictionary via its keys
	phyla_list = []
	#create empty list that will be populated with phyla information
	og_prot_list = ortho_dict[key]
	#save list of protein query IDs associated with the given OG
	for prot in og_prot_list:
		#iterate over the list of protein query IDs
		prot_phyla = ref_df.loc[ref_df['Query'] == prot, 'Phylum'].iloc[0]
		#with .loc, find the location where the protein query ID is found in the 'Query' column
		#then extract the contents of that cell, as well as the cell in the same row that is in the 'Phylum' column
		#use slicing and .iloc to extract the contents of the 'Phylum' column
		#and save the phyla category to variable prot_species
		#append the phyla category to the species_list
		phyla_list.append(prot_phyla)
	phyla_set = set(phyla_list)
	#turn the phyla_list into a set to eliminate duplicates
	#and save the phyla_set as the value in the OG to species dictionary
	phyla_OG_dict[key] = phyla_set


#Part 5: Identify OGs that include representatives of all 4 phyla

#create list of 4 main phyla
main_phyla_list = ['Anaeramoebidae', 'Parabasalia', 'Fornicata', 'Preaxostyla']
#create list of 5 existing phyla
full_phyla_list = ref_df.Phylum.unique()


#create new dictionary for data that meets the threshold
threshold_og_list = []

for key in phyla_OG_dict.keys():
	#iterate over the dictionary via its keys
	if (phyla_OG_dict[key] == set(main_phyla_list)) or (phyla_OG_dict[key] == set(full_phyla_list)):
		#identify the OGs that include members of at least 4 phyla
		#and save the OG to the list of threshold_og_list
		threshold_og_list.append(key)


#Part 6: Copy threshold-meeting OG information into a new dataframe & write out

#create new dataframe with good OGs
threshold_df = ortho_df[ortho_df[og_col].isin(threshold_og_list)].copy()
#use `.isin()` to iterate over entire list of OGs
#use `.copy()` to ensure the dataframe is seperate from the ortho_df

#Writing out the results to a tab-separated text file
threshold_df.to_csv(output_file, sep='\t', index=False)


#Part 7 (Optional): Write out only those OGs that include the 4 main phyla and Barthelona

if len(sys.argv) == 4:
	#identify cases where the final, optional argument was used
	if sys.argv[3] == "other":
		#check to ensure that the item in this position isn't a random accident
		output_file_v2 = out_full + "_5Phyla.txt"

		#create new dictionary for data that meets the threshold
		threshold_v2_og_list = []

		for key in phyla_OG_dict.keys():
			#iterate over the dictionary via its keys
			if phyla_OG_dict[key] == set(full_phyla_list):
				#identify the OGs that include members of all 5 phyla
				#and save the OG to the list of threshold_og_list
				threshold_v2_og_list.append(key)

		#create new dataframe with good OGs
		threshold_v2_df = ortho_df[ortho_df[og_col].isin(threshold_v2_og_list)].copy()
		#use `.isin()` to iterate over entire list of OGs
		#use `.copy()` to ensure the dataframe is seperate from the ortho_df

		#Writing out the results to a tab-separated text file
		threshold_v2_df.to_csv(output_file_v2, sep='\t', index=False)
