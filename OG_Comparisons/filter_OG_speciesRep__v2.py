# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_OG_speciesRep__v2.py
Date: 2022-03-22
Author: Virág Varga

Description:
	This program performs filters the parsed results of orthologous clustering software
		(OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) in order to exclude paralogs
		(ie. "orthologs" where all member proteins come from the same species or assemblage).

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	argparse
	pandas
	os

Procedure:
	1. Assignment of command-line arguments with argparse.
	2. Importing modules and parsing arguments. Running code specific to individual
		arguments for import into a Pandas dataframe.
	3. Main program code:
		- Setting up outfile, importing data into Pandas & variables
		- Setting up data types (dataframe for ref file, dictionary for infile) that will be used
		- Creating dictionary of species represented in each OG
		- Identifying OGs that meet the species percentage representation threshold
	4. Writing out dataframe of minimum species membership threshold-matching OGs to a
		tab-separated text file.
	5. Writing out summary text file. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.
	- The input file used for the program must be an un-pivoted results file of either
		Broccoli, OrthoFinder, SonicParanoid, or ProteinOrtho, following the structure
		used by the parsers used previously in this workflow.
	- The program cannot accept multiple input parsed OG files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Version: 
	This is version 2.0 of this script. There is now a summary text file produced at the end listing
		the number of OGs that have the threshold minimum percent species represented, as well as 
		the OG IDs of these OGs. 

Usage:
	./filter_OG_speciesRep__v2.py [-h] [--threshold_minimum THRESHOLD_MINIMUM] [-br] [-of] [-po] [-sp] [-v] INPUT_FILE REFERENCE_FILE
	OR
	python filter_OG_speciesRep__v2.py [-h] [--threshold_minimum THRESHOLD_MINIMUM] [-br] [-of] [-po] [-sp] [-v] INPUT_FILE REFERENCE_FILE

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""

#################################   ARGPARSE   #######################################

import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program filters the parsed results of orthologous \
								 clustering software (OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) \
								 based on whether a threshold percentage of species are represented \
								 (default = 85%).')
#The most general description of what this program can do is defined here


#adding the arguments that the program can use
parser.add_argument(
	'-br', '--Broccoli',
	action='store_true',
	help = 'This argument will parse the results of the Broccoli program.'
	)
	#the '-br' flag will import the input file in the manner appropriate for the parsed Broccoli results
parser.add_argument(
	'-of', '--OrthoFinder',
	action='store_true',
	help = 'This argument will parse the results of the OrthoFinder program.'
	)
	#the '-br' flag will import the input file in the manner appropriate for the parsed OrthoFinder results
parser.add_argument(
	'-po', '--ProteinOrtho',
	action='store_true',
	help = 'This argument will parse the results of the ProteinOrtho program.'
	)
	#the '-br' flag will import the input file in the manner appropriate for the parsed ProteinOrtho results
parser.add_argument(
	'-sp', '--SonicParanoid',
	action='store_true',
	help = 'This argument will parse the results of the SonicParanoid program.'
	)
	#the '-sp' flag will import the input file in the manner appropriate for the parsed SonicParanoid results
parser.add_argument(
	"--threshold_minimum",
	type=int,
	default=85,
	help = "Integer value of minimum percent of species that should be represented in OGs. (Default = 85)"
	)
	#the `type=int` argument allows argparse to accept the input as an integer
	#the `default=3` gives a default minimum membership filtration value
	#ref: https://stackoverflow.com/questions/44011031/how-to-pass-a-string-as-an-argument-in-python-without-namespace
	#ref: https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
parser.add_argument(
	#'-i', '--input',
	#the above line of code is left in as further clarification of this argument
	dest='input_file',
	metavar='INPUT_FILE',
	help = "The input file should be parsed orthologous clustering results.",
	type=argparse.FileType('r')
	)
	#this portion of code specifies that the program requires an input file, and it should be opened for reading ('r')
parser.add_argument(
	#'-r', '--ref',
	#the above line of code is left in as further clarification of this argument
	dest='ref_file',
	metavar='REFERENCE_FILE',
	help = "The reference file should be in the format: Query\tSpecies_ID\tSpecies_Category\tPhylum.",
	type=argparse.FileType('r')
	)
	#this portion of code specifies that the program requires a reference file, and it should be opened for reading ('r')
parser.add_argument(
	'-v', '--version',
	action='version',
	version='%(prog)s 1.0'
	)
	#This portion of the code specifies the version of the program; currently 1.0
	#The user can call this flag ('-v') without specifying input and output files


args = parser.parse_args()
#this command allows the program to execute the arguments in the flags specified above


#################################   Parse Arguments   ######################################


#import necessary modules
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files


#designate input file name as variable
infile = args.input_file.name
#designate reference file name as variable
ref_db = args.ref_file.name
#designate mimium OG membership threshold value as variable
threshold_value = args.threshold_minimum


#parse arguments
if args.Broccoli:
	#if -br argument is called
	print("Broccoli results recieved")
	#save the input program ID for use in the output file
	prog_id = "Broccoli"

if args.OrthoFinder:
	#if -of argument is called
	print("OrthoFinder results recieved")
	#save the input program ID for use in the output file
	prog_id = "OrthoFinder"

if args.ProteinOrtho:
	#if -tp argument is called
	print("ProteinOrtho results recieved")
	#save the input program ID for use in the output file
	prog_id = "ProteinOrtho"

if args.SonicParanoid:
	#if -en argument is called
	print("SonicParanoid results recieved")
	#save the input program ID for use in the output file
	prog_id = "SonicParanoid"


#################################   Main Program   ######################################


#Part 1: Set up outfile, import data into Pandas & variables

#define the output files based on the input file name
base = os.path.basename(infile)
out_full = os.path.splitext(base)[0]
#parsed OG output file
output_file = out_full + "_OGsMembership" + str(threshold_value) + ".txt"
#summary output file
output_summary_file = out_full + "_OGsMembership" + str(threshold_value) + "__SUMMARY.txt"

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


#convert membership percentage to a decimal
membership_decimal = float(threshold_value)/100


#Part 2: Set up data types (dataframe for ref file, dictionary for infile) that will be used

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


#Part 3: Create dictionary of species represented in each OG

#create empty dictionary for species information
species_OG_dict = {}

for key in ortho_dict.keys():
	#iterate over the dictionary via its keys
	species_list = []
	#create empty list that will be populated with species information
	og_prot_list = ortho_dict[key]
	#save list of protein query IDs associated with the given OG
	for prot in og_prot_list:
		#iterate over the list of protein query IDs
		prot_species = ref_df.loc[ref_df['Query'] == prot, 'Species_Category'].iloc[0]
		#with .loc, find the location where the protein query ID is found in the 'Query' column
		#then extract the contents of that cell, as well as the cell in the same row that is in the 'Species_Category' column
		#use slicing and .iloc to extract the contents of the 'Species_Category' column
		#and save the species category to variable prot_species
		#append the species category to the species_list
		species_list.append(prot_species)
	species_set = set(species_list)
	#turn the species_list into a set to eliminate duplicates
	#and save the species_set as the value in the OG to species dictionary
	species_OG_dict[key] = species_set


#Part 4: Identify OGs that meet the species percentage representation threshold

#get number of species represented
total_species = ref_df.Species_Category.unique()
#save list of species categories to a variable
total_species_num = len(total_species)
#count the number of elements of the species category list
#for the original Thesis project workflow, this should be 26

threshold_species_num = round(total_species_num*membership_decimal)
#get the minimum number of species needed to hit the species membership threshold
#round the number to the nearest integer (up or down)


#create new dictionary for data that meets the threshold
threshold_og_list = []

for key in species_OG_dict.keys():
	#iterate over the dictionary via its keys
	if len(species_OG_dict[key]) >= threshold_species_num:
		#identify the OGs that meet the minimum species inclusion threshold number
		#and save the OG to the list of threshold_og_list
		threshold_og_list.append(key)


#Part 5: Copy threshold-meeting OG information into a new dataframe & write out

#create new dataframe with non-paralog OGs
threshold_df = ortho_df[ortho_df[og_col].isin(threshold_og_list)].copy()
#use `.isin()` to iterate over entire list of non-paralog OGs
#use `.copy()` to ensure the dataframe is seperate from the ortho_df

#Writing out the results to a tab-separated text file
threshold_df.to_csv(output_file, sep='\t', index=False)


#Part 6: Create summary data text file

#compute statistics to include in the summary file
threshold_og_num = len(threshold_df[og_col].unique())
#calculate number of OGs included in the filtered dataframe
original_og_num = len(ortho_df[og_col].unique())
#calculate number of OGs included in the original dataframe
percent_ogs_remaining = (threshold_og_num/original_og_num)*100
#calculate percent of OGs remaining
rounded_percent = round(percent_ogs_remaining, 3)
#round the percentage to 3 decimal places

#get list of "good" OGs for summary file
good_OG_list = threshold_df[og_col].unique()


with open(output_summary_file, "w") as outfile: 
	#open the summary file for writing
	outfile.write("The number of orthologous clusters created by the " + prog_id + " program that meet " + "\n" + 
			   "the desired threshold value of " + str(threshold_value) + "% is " + str(threshold_og_num) + "." + "\n\n")
	outfile.write("In contrast, the total number of orthologous clusters created by this program was " + str(original_og_num) + ", " + "\n" + 
			   "which means that " + str(rounded_percent) + "% of the clusters met the desired threshold value." + "\n\n")
	outfile.write("The OGs that met the threshold percent are: " + "\n")
	for element in good_OG_list:
		#iterate through the list of good OGs and write them out to the file
		outfile.write(element + "\n")
