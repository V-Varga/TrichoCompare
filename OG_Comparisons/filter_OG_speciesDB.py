# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_OG_speciesDB.py
Date: 2022-04-04
Author: Virág Varga

Description:
	This program filters the species and phyla representation per OG database created by
		the og_db_plusSpeciesRep__v2.py program (or a filtered version of the same, with
		the same column structure), based on the desired representation criteria of the user.
	The following can be used to filter for representation:
		- Presence or absence of specific species (or list of species) in an OG
		- Presence or absence of specific phylum (or list of phyla) in an OG
		- Percentage of species or phyla represented in an OG

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	argparse
	pandas
	os

Procedure:
	1. Assignment of command-line arguments with argparse.
	2. Parsing arguments.
		- Importing modules, determining inputs & outputs, importing data
		- Determining filtration category and performing dataframe querying

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.
	- The input file used for the program must be a file created by the og_db_plusSpeciesRep__v2.py
		program (or a filtered version of the same, with the same column structure).
	- The program cannot accept multiple input program files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Inputs & Outputs:
	- Inputs:
		+ The mandatory input file is a file created by the og_db_plusSpeciesRep__v2.py program
			(or a filtered version of the same, with the same column structure).
		+ This program accepts input query species/phyla lists in the following formats:
			- Singular species/phylum provided on the command line
			- Comma-separated list of species/phyla provided on the command line (ex. `ID_1,ID_2,ID_3`)
			- File containing list of species/phyla in format: ID1\nID2 etc.
		+ If the threshold option is selected, an integer percentage value must be given
			(ex. 80 for 80%), otherwise the default is 80.
	- Outputs:
		+ The program will output a text file containing the OGs that met the search criteria in
			the format: OG_ID1\nOG_ID2\nOG_ID3 etc
		+ If the -out flag is used, the program will output a filtered version of the dataframe,
			including all rows which match the query.

Usage:
	./filter_OG_speciesDB.py [-h] -type FILTRATION_TYPE -cat FILTRATION_CATEGORY [-single SINGLE_ID]
		[-list ID_LIST] [-file ID_FILE] [-val INTEGER] [-suf SUFFIX] [-out] [-v] -i INPUT_FILE
	OR
	python filter_OG_speciesDB.py [-h] -type FILTRATION_TYPE -cat FILTRATION_CATEGORY [-single SINGLE_ID]
		[-list ID_LIST] [-file ID_FILE] [-val INTEGER] [-suf SUFFIX] [-out] [-v] -i INPUT_FILE

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#################################   ARGPARSE   #######################################

import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


#The most general description of what this program can do is defined here
parser = argparse.ArgumentParser(description =
								 'This program filters the species and phyla representation per OG database created by \
									the og_db_plusSpeciesRep__v2.py program (or a filtered version of the same, with \
									the same column structure), based on the desired representation criteria of the user. \
								The following can be used to filter for representation: \
									- Presence or absence of specific species (or list of species) in an OG \
									- Presence or absence of specific phylum (or list of phyla) in an OG \
									- Percentage of species or phyla represented in an OG')

#create a group of arguments which will be required
requiredArgNames = parser.add_argument_group('required arguments')
#ref: https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments

#adding the arguments that the program can use
requiredArgNames.add_argument(
	'-type', '--filtration_type',
	metavar='FILTRATION_TYPE',
	dest='filt_type',
	choices=['include', 'exclude', 'threshold'],
	#ref: https://stackoverflow.com/questions/15836713/allowing-specific-values-for-an-argparse-argument
	help = 'This argument requires the user to specify the type of filtration that should be done. \
		Use "include" to include species/phylum IDs, "exclude" to exclude species/phylum IDs, \
			"threshold" to test for inclusion percentage >= the threshold value given',
	required=True
	)
	#the '-type' flag is used to tell the program what kind of analysis is going to be done
requiredArgNames.add_argument(
	'-cat', '--filtration_category',
	metavar='FILTRATION_CATEGORY',
	dest='filt_cat',
	choices=['species', 'phylum'],
	help = 'This argument requires the user to specify the type of data the filtration should be performed on. \
		The options are: "species" OR "phylum".',
	required=True
	)
	#the '-prog' flag is used to tell the program which pragram's data is being used as input

parser.add_argument(
	'-single', '--single_id',
	metavar='SINGLE_ID',
	dest='single_ID',
	help = 'This argument takes a single species or phylum ID as input.'
	)
	#the '-single' flag will import the input single species/phylum as a simple string
parser.add_argument(
	'-list', '--id_list',
	metavar='ID_LIST',
	dest='ID_list',
	help = 'This argument takes a comma-separated list of species or phylum IDs as input (ex. ID1,ID2,ID3).'
	)
	#the '-list' flag will import the input list of species/phyla IDs from the command line
parser.add_argument(
	'-file', '--ID_file',
	dest='ID_file',
	metavar='ID_FILE',
	help = "The file containing species or phylum IDs should be in the format: ID\nID\nID etc.",
	type=argparse.FileType('r')
	)
	#the 'file' flag will import the list of species or phyla IDs from the given file
parser.add_argument(
	'-val', '--threshold_value',
	dest='threshold',
	metavar='INTEGER',
	type=int,
	default=80,
	help = "Integer value of minimum percent of species or phyla that should be represented in OGs. (Default = 80)"
	)
	#the `type=int` argument allows argparse to accept the input as an integer
	#the `default=80` gives a default minimum membership filtration value
	#ref: https://stackoverflow.com/questions/44011031/how-to-pass-a-string-as-an-argument-in-python-without-namespace
	#ref: https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
parser.add_argument(
	'-suf', '--suffix',
	metavar='SUFFIX',
	dest='suffix',
	help = 'This argument allows the user to define a suffix to be used for the output file name.'
	)
	#the '-suf' flag allows the user to define a suffix to be used for the output file name.
parser.add_argument(
	'-out', '--filt_db_out',
	action='store_true',
	help = 'This argument will enable the program to print the entire filtered database, not only the list of OG IDs.'
	)
	#the '-out' flag will enable the program to print the entire filtered database, not only the list of OG IDs
parser.add_argument(
	'-v', '--version',
	action='version',
	version='%(prog)s 1.0'
	)
	#This portion of the code specifies the version of the program; currently 1.0
	#The user can call this flag ('-v') without specifying input and output files
requiredArgNames.add_argument(
	'-i', '--input',
	dest='input_file',
	metavar='INPUT_FILE',
	help = "The input file should be a species and phyla representation per OG database created by \
		the og_db_plusSpeciesRep__v2.py program (or a filtered version of the same, with \
		the same column structure).",
	type=argparse.FileType('r'),
	required=True
	)
	#this portion of code specifies that the program requires an input file, and it should be opened for reading ('r')


args = parser.parse_args()
#this command allows the program to execute the arguments in the flags specified above


#################################   Parse Arguments   ######################################


#Part 1: Import modules, determine inputs & outputs, import data

#import necessary modules
import pandas as pd #allows manipulation of dataframes in Python
import os #allow access to computer files


#designate input file name as variable
infile = args.input_file.name
#import the dataframe into Pandas
ortho_df = pd.read_csv(infile, sep = '\t', header = 0)
#identify OG column name (for use later)
og_col = ortho_df.columns[0]


#define the output file basename based on the input file name
base = os.path.basename(infile)
out_full = os.path.splitext(base)[0]


#import the query list
if args.single_ID:
	#if the option to enter only one query species/phylum on the command line was selected
	search_IDs = args.single_ID
	#save the query species/phylum to a variable
	#and save that variable to a 1-member list
	search_list = [search_IDs]

if args.ID_list:
	#if the option to give a list of species/phyla IDs was given
	search_IDs = args.ID_list
	#save the contents of the comma-separated string to a variable
	#and save the species/phyla IDs to a list based on comma placement in the input string
	search_list = search_IDs.split(",")

if args.ID_file:
	#if an input file was given containing the species/phyla IDs to search
	#save the file to a variable
	search_file = args.ID_file
	#save the contents of the file (should be a column of species/phyla IDs) to a list
	search_list = [line.rstrip('\n') for line in search_file]


#Part 2: Determine filtration category and perform dataframe querying

if args.filt_cat == 'species':
	#if the species category was selected
	#identify the relevant dataframe columns and save to variables
	percent_col = "Species_Percent"
	#species percent column
	rep_col = "Species_Represented"
	#list of species represented
if args.filt_cat == 'phylum':
	#if the phylum category was selected
	#identify the relevant dataframe columns and save to variables
	percent_col = "Phylum_Percent"
	#phylum percent column
	rep_col = "Phyla_Represented"
	#list of phylum represented


if args.filt_type == 'threshold':
	#if the threshold option was selected
	#parse the relevant argument to determine the threshold value
	threshold_value = args.threshold
	#now determine the decimal value of the threshold percent
	threshold_decimal = threshold_value/100

	#filter the relevant dataframe column on the basis of the threshold value
	filt_ortho_df = ortho_df[ortho_df[percent_col] >= threshold_decimal]
	#create a list of the OG IDs that met the threshold
	og_list = filt_ortho_df[og_col].unique()

	#now create the relevant results file(s)
	if len(og_list) == 0: 
		#check if any OGs have hit the threshold
		#and if not, print message to the console
		print("No OGs have met the filtration criteria!")
	else: 
		#if there are OGs to report
		if args.suffix:
			#if the user has provided a suffix
			suffix_out = args.suffix
			#save the suffix to a variable
			#and designate the outfile name
			output_file = out_full + "_" + suffix_out + "_" + str(threshold_value) + ".txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				output_db = out_full + "_" + suffix_out + "_filtDB_" + str(threshold_value) + ".txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)
		else:
			#if the user has not given a file suffix, use the default outfile name
			output_file = out_full + "_filt" + str(threshold_value) + ".txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				output_db = out_full + "_filtDB_" + str(threshold_value) + ".txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)


if args.filt_type == 'include':
	#if the inclusion option was selected
	#first, convert the relevant data colum elements into a list (vs. comma-separated string)
	ortho_df[rep_col] = ortho_df[rep_col].str.split(', ')
	#now see if the species/phyla are all represented in the list
	#ref: https://stackoverflow.com/questions/60932036/check-if-pandas-column-contains-all-elements-from-a-list
	search_set = set(search_list)
	#first create a set of the list of species/phyla to search for
	#then search the appropriate column for all OGs that include all of the species/phyla in the set
	filt_ortho_df = ortho_df[ortho_df[rep_col].map(search_set.issubset)].copy()
	#create a list of the OG IDs that met the threshold
	og_list = filt_ortho_df[og_col].unique()
	
	#now create the relevant results file(s)
	if len(og_list) == 0: 
		#check if any OGs have hit the threshold
		#and if not, print message to the console
		print("No OGs have met the filtration criteria!")
	else: 
		#if there are OGs to report
		if args.suffix:
			#if the user has provided a suffix
			suffix_out = args.suffix
			#save the suffix to a variable
			#and designate the outfile name
			output_file = out_full + "_incl_" + suffix_out + ".txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				#turn the lists in the cells into comma-separated strings
				filt_ortho_df[rep_col] = filt_ortho_df[rep_col].apply(lambda x: ', '.join(map(str, x)))
				output_db = out_full + "_incl_" + suffix_out + "_filtDB" + ".txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)
		else:
			#if the user has not given a file suffix, use the default outfile name
			output_file = out_full + "_include.txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				#turn the lists in the cells into comma-separated strings
				filt_ortho_df[rep_col] = filt_ortho_df[rep_col].apply(lambda x: ', '.join(map(str, x)))
				output_db = out_full + "_include_filtDB.txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)


if args.filt_type == 'exclude':
	#if the exclusion option was selected
	#then search the appropriate column for all OGs that do not include the species/phyla
	#ref: https://stackoverflow.com/questions/26577516/how-to-test-if-a-string-contains-one-of-the-substrings-in-a-list-in-pandas
	filt_ortho_df = ortho_df[~ortho_df[rep_col].str.contains('|'.join(search_list))].copy()
	#create a list of the OG IDs that met the threshold
	og_list = filt_ortho_df[og_col].unique()
	
	#now create the relevant results file(s)
	if len(og_list) == 0: 
		#check if any OGs have hit the threshold
		#and if not, print message to the console
		print("No OGs have met the filtration criteria!")
	else: 
		#if there are OGs to report
		if args.suffix:
			#if the user has provided a suffix
			suffix_out = args.suffix
			#save the suffix to a variable
			#and designate the outfile name
			output_file = out_full + "_excl_" + suffix_out + ".txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				output_db = out_full + "_excl_" + suffix_out + "_filtDB" + ".txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)
		else:
			#if the user has not given a file suffix, use the default outfile name
			output_file = out_full + "_exclude.txt"
			#now write out the list to a text file
			with open(output_file, "w") as outfile:
				#open the outfile for writing
				for element in og_list:
					#iterate over the elements in the list
					#and print them to the text file in the format OG_ID1\nOG_ID2\nOG_ID3 etc.
					outfile.write(element + "\n")
			if args.filt_db_out:
				#if the user has requested that the entire filtered database be written out
				output_db = out_full + "_exclude_filtDB.txt"
				#determine the output file name
				#and write out the results to a tab-separated text file
				filt_ortho_df.to_csv(output_db, sep='\t', index=False)
