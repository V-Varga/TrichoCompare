# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og_prot_list.py
Date: 2022.05.14
Author: Virág Varga

Description:
	This program filters (a version of) the Metamonad database in order to extract
		the encoded protein query IDs and species IDs associated with a provided list
		of query OG IDs. For each input query OG ID, the program will output a
		results file in the format: Query\tSpecies_Id\t[OG_Program_OG_ID]

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; assigning command line arguments.
	2. Importing data into Pandas dataframe and creating OG ID to list of query protein
		IDs dictionary.
	3. Extracting information on proteins in query OGs, and writing out results to
		a tab-separated text file per OG.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file names are not user-defined.

Usage
	./og_prot_list.py input_db og_program og_ids [search_identifier]
	OR
	python og_prot_list.py input_db og_program og_ids [search_identifier]

	Where the input_db is a (possibly filtered) version of the Metamonad database
		including Query IDs, Species IDs, and OG IDs of orthologous clustering
		program whose OGs are being queried.
	Where og_program is the column name of the orthologous clustering program whose
		OG IDs are being queried.
	Where og_ids must be a query OG ID list in on of the following formats:
		- Singular OG ID provided on the command line
		- Comma-separated list of OG IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of OG IDs in format: ID1\nID2 etc.
	Where search_identifier should be a string describing the particular type of 
		data being filtered for (ex.: 'mito3'), that will be included in the output file
		name. 

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__filt_scores-startAA-pfam__HEAD200.txt"

og_program = sys.argv[2]
#og_program = "SonicParanoid_OG"
if og_program == "SonicParanoid_OG": 
	#if the program whose OGs are being queried is SonicParanoid
	#save a shortened version of the name to a variable
	#for use in the output file name
	og_program_short = "SP"
elif og_program == "OrthoFinder_OG": 
	#if the program whose OGs are being queried is OrthoFinder
	#save a shortened version of the name to a variable
	#for use in the output file name
	og_program_short = "OF"
else: 
	#if none of SP or OF are selected
	print("Incorrect orthologous clustering program selected. Please try again!")

og_ids = sys.argv[3]
#og_ids = "OG_25,OG_39"
#og_ids = "MetamonadCtrl_mito_3_SP_OGs_Tv_nonTvP.txt"
#import the query list
if os.path.isfile(og_ids):
	#if the input selection of OGs is a file
	with open(og_ids, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of protein query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
		#eliminate duplicates
		query_list = list(set(query_list))
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = og_ids.split(",")
	#eliminate duplicates
	query_list = list(set(query_list))


#Part 2: Import data into Pandas dataframe & create OG dictionary

#read in the Metamonad database to a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0)
#extract the relevant portions of the dataframe to a new dataframe
og_df = input_df[['Query', 'Species_Id', og_program]].copy()
#then remove those rows that are not associated with any OG
og_df = og_df.loc[og_df[og_program] != '-']


#create a dictionary in the format: og_dict[og_id] = list_of_proteins
#this will allow easier analysis
grouped_og_df = og_df.groupby(og_program)['Query'].apply(list).reset_index(name="OG_members")
#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
#the new column of lists is named 'OG_members'
og_dict = grouped_og_df.set_index(og_program).to_dict()['OG_members']
#the new dataframe is converted into a dictionary,
#where the OG IDs are the keys, and the lists of protein members of the OGs are the values


#Part 3: Extracting query OGs & writing out results

#create empty dictionary for query OG information
filt_og_dict = {}

for og_key in og_dict.keys():
	#iterate over the keys of the OG dictionary
	if og_key in query_list:
		#identify OG IDs that are in the list of queries
		#and populate those entries over into the new filtered dictionary
		filt_og_dict[og_key] = og_dict[og_key]


for filt_key in filt_og_dict.keys():
	#iterate over the query OG IDs in the filtered dictionary
	if len(sys.argv) == 5: 
		#if the user provides an identifier for the file
		search_identifier = sys.argv[4]
		#add the search_identifier to the output file name
		output_db = og_program_short + "_" + search_identifier + "__" + filt_key + ".txt"
	else: 
		#otherwise simply use the OG program and the OG ID in the output file name
		output_db = og_program_short + "__" + filt_key + ".txt"
	#create the output file for that OG
	prot_list = filt_og_dict[filt_key]
	#extract the query proteins associated with the OG into a list
	temp_df = og_df[og_df['Query'].isin(prot_list)].copy()
	#use `.isin()` to iterate over entire list of query protein IDs
	#use `.copy()` to ensure the dataframe is separate from the og_df
	#and now write out results to a tab-separated text file
	temp_df.to_csv(output_db, sep = '\t', index=False)
