# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og_db_plusSpeciesRep__v2.py
Date: 2022-04-04
Author: Virág Varga

Description:
	This program parses the parsed results of orthologous clustering software
		(OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) and creates an output
		file in the format:
			OG_ID\tSpecies_Percent\tSpecies_Represented\tPhylum_Percent\tPhyla_Represented

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
	4. Creating dictionaries of species categories and phyla represented in each OG.
	5. Creating new dataframes from the dictionaries.
	6. Merging the species and phylum dataframes and writing out results to a tab-separated 
		text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined - it is based on the input file name
	- The input file used for the program must be an un-pivoted results file of either
		Broccoli, OrthoFinder, SonicParanoid, or ProteinOrtho, following the structure
		used by the parsers used previously in this workflow.
	- The program cannot accept multiple input parsed OG files simultaneously.

Version:
	This is version 2.0 of this program. This version has the added functionality of
		adding a second column with the list of phyla represented in a given OG.

Usage:
	./og_db_plusSpeciesRep__v2.py input_db ref_db
	OR
	python og_db_plusSpeciesRep__v2.py input_db ref_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files


#designate input file name as variable
infile = sys.argv[1]
#infile = "OF_OGs_parsed.txt"
#designate reference file name as variable
ref_db = sys.argv[2]
#ref_db = "Prots_Species_Phyla_DB.txt"

#define the output file based on the input file name
base = os.path.basename(infile)
out_full = os.path.splitext(base)[0]
output_db = out_full + "__OG-Species-PhylaPercent.txt"


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


#Part 4: Create dictionaries of species categories and phyla represented in each OG

#get number of species represented
total_species = ref_df.Species_Category.unique()
#save list of species categories to a variable
total_species_num = len(total_species)
#count the number of elements of the species category list
#for the original Thesis project workflow, this should be 26

#create empty dictionary for species information
species_OG_dict = {}
#create empty dictionary for species percentage information
species_OG_percent_dict = {}


#get number of phyla represented
total_phyla = ref_df.Phylum.unique()
#save list of phyla to a variable
total_phyla_num = len(total_phyla)
#count the number of elements of the phylum list
#for the original Thesis project workflow, this should be 5

#create empty dictionary for phylum information
phylum_OG_dict = {}
#create empty dictionary for phylum percentage information
phylum_OG_percent_dict = {}


#now populate the empty dictionaries above
for key in ortho_dict.keys():
	#iterate over the dictionary via its keys
	species_list = []
	#create empty list that will be populated with species information
	phylum_list = []
	#create empty list that will be populated with phylum information
	og_prot_list = ortho_dict[key]
	#save list of protein query IDs associated with the given OG
	for prot in og_prot_list:
		#iterate over the list of protein query IDs
		#first deal with the species representation
		prot_species = ref_df.loc[ref_df['Query'] == prot, 'Species_Category'].iloc[0]
		#with .loc, find the location where the protein query ID is found in the 'Query' column
		#then extract the contents of that cell, as well as the cell in the same row that is in the 'Species_Category' column
		#use slicing and .iloc to extract the contents of the 'Species_Category' column
		#and save the species category to variable prot_species
		#append the species category to the species_list
		species_list.append(prot_species)
		#and now deal with the phylum representation
		prot_phylum = ref_df.loc[ref_df['Query'] == prot, 'Phylum'].iloc[0]
		#with .loc, find the location where the protein query ID is found in the 'Query' column
		#then extract the contents of that cell, as well as the cell in the same row that is in the 'Phylum' column
		#use slicing and .iloc to extract the contents of the 'Phylum' column
		#and save the species category to variable prot_phylum
		#append the species category to the phylum_list
		phylum_list.append(prot_phylum)
	#first deal with the species category data
	species_set = set(species_list)
	#turn the species_list into a set to eliminate duplicates
	#and save the species_set as the value in the OG to species dictionary
	species_OG_dict[key] = species_set
	#now populate the dictionary of species percentages
	species_percent = round(len(species_set)/total_species_num, 3)
	#get the percent of species represented as a decimal to 3 decimal places
	#and save it to the species percentage dictionary
	species_OG_percent_dict[key] = species_percent
	#and next deal with the phylum data
	phylum_set = set(phylum_list)
	#turn the phylum_list into a set to eliminate duplicates
	#and save the phylum_set as the value in the OG to phlya dictionary
	phylum_OG_dict[key] = phylum_set
	#now populate the dictionary of phylum percentages
	phylum_percent = round(len(phylum_set)/total_phyla_num, 3)
	#get the percent of phyla represented as a decimal to 3 decimal places
	#and save it to the phylum percentage dictionary
	phylum_OG_percent_dict[key] = phylum_percent


#Part 5: Create new dataframes

#create new dataframe with OGs and species percentages
species_percent_df = pd.DataFrame.from_dict(species_OG_percent_dict, orient='index', columns=['Species_Percent'])
#note that this method of conversion puts the dictionary keys in the index

#create new column for list of species represented in the OG
species_percent_df['Species_Represented'] = "-"

#now add in the lists of species represented per OG
for og_key in species_OG_dict.keys():
	#iterate over the dictionary of species included in OGs via its keys
	#and add in the list of species at the appropriate locations
	species_percent_df.at[og_key, 'Species_Represented'] = list(species_OG_dict[og_key])

#turn the lists in the cells into comma-separated strings
species_percent_df['Species_Represented'] = species_percent_df['Species_Represented'].apply(lambda x: ', '.join(map(str, x)))

#pull the OG ID column out of the index
species_percent_df.reset_index(inplace=True)
#and rename the first column of the dataframe according to the program
species_percent_df.rename(columns={'index': og_col}, inplace=True)


#create new dataframe with OGs and phylum percentages
phylum_percent_df = pd.DataFrame.from_dict(phylum_OG_percent_dict, orient='index', columns=['Phylum_Percent'])
#note that this method of conversion puts the dictionary keys in the index

#create new column for list of phyla represented in the OG
phylum_percent_df['Phyla_Represented'] = "-"

#now add in the lists of species represented per OG
for og_key in phylum_OG_dict.keys():
	#iterate over the dictionary of phyla included in OGs via its keys
	#and add in the list of phyla at the appropriate locations
	phylum_percent_df.at[og_key, 'Phyla_Represented'] = list(phylum_OG_dict[og_key])

#turn the lists in the cells into comma-separated strings
phylum_percent_df['Phyla_Represented'] = phylum_percent_df['Phyla_Represented'].apply(lambda x: ', '.join(map(str, x)))

#pull the OG ID column out of the index
phylum_percent_df.reset_index(inplace=True)
#and rename the first column of the dataframe according to the program
phylum_percent_df.rename(columns={'index': og_col}, inplace=True)


#Part 6: Merge dataframes and write out resulting dataframe to file

#merge dataframes on the OG column
total_percent_df = species_percent_df.merge(phylum_percent_df, how='outer')
#since the species_percent_df is given the merge command, the data from it will be on the left,
#while the data from phylum_percent_df will be on the right
#the `how='outer'` argument ensures that all queries are kept, even the ones without overlap
#it isn't particularly important here, though, since the dataframes are the same length

#Writing out the results to a tab-separated text file
total_percent_df.to_csv(output_db, sep='\t', index=False)
