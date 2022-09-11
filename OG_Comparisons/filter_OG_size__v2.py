# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_OG_size__v2.py
Date: 2022-03-15
Author: Virág Varga

Description:
	This program performs filters the parsed results of orthologous clustering software
		(OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) in order to exclude OGs
		that do not meet a user-determined minimum membership size (default = 3 proteins).

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
		- Importing OG data into dictionary with format ortho_dict[OG_ID] = list_of_queries
		- Identifying OGs that meet the threshold minimum size, and compiling them into a list
		- Creating a Pandas dataframe containing only the OGs that meet the threshold
			minimum size
	4. Writing out dataframe of threshold size-meeting OGs to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.
	- The input file used for the program must be an un-pivoted results file of either
		Broccoli, OrthoFinder, SonicParanoid, or ProteinOrtho, following the structure
		used by the parsers used previously in this workflow.
	- The program cannot accept multiple input parsed OG files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Version: 
	This is version 2.0 of the program. The following changes were make to the script, 
		to increase ease of program use: 
		- Made the script more flexible re: number of columns. Now filtered parsed data
			can still be processed, even if the formatting does not match the original
			parsed OG data file. 

Usage:
	./filter_OG_size.py [-h] [--threshold_minimum THRESHOLD_MINIMUM] [-br] [-of] [-po] [-sp] [-v] INPUT_FILE
	OR
	python filter_OG_size.py [-h] [--threshold_minimum THRESHOLD_MINIMUM] [-br] [-of] [-po] [-sp] [-v] INPUT_FILE

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""

#################################   ARGPARSE   #######################################

import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program performs filters the parsed results of orthologous \
								 clustering software (OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli) \
								 in order to exclude OGs that do not meet a user-determined minimum \
								 membership size (default = 3 proteins).')
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
	default=3,
	help = "The minimum number of protein queries that should be part of an OG in order for that OG to be kept. (Default = 3)"
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
	'-v', '--version',
	action='version',
	version='%(prog)s 2.0'
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
#designate mimium OG membership threshold value as variable
threshold_value = args.threshold_minimum


#parse arguments
if args.Broccoli:
	#if -br argument is called
	print("Broccoli results recieved")
	#save the input program ID for use in the output file
	prog_id = "Broccoli"
	#import input file into pandas dataframe
	ortho_df = pd.read_csv(infile, sep = '\t', header = 0)
	#define the output file based on the input file name
	base = os.path.basename(infile)
	out_full = os.path.splitext(base)[0]
	output_file = out_full + "_threshold" + str(threshold_value) + ".txt"

if args.OrthoFinder:
	#if -of argument is called
	print("OrthoFinder results recieved")
	#save the input program ID for use in the output file
	prog_id = "OrthoFinder"
	#import input file into pandas dataframe
	ortho_df = pd.read_csv(infile, sep = '\t', header = 0)
	#define the output file based on the input file name
	base = os.path.basename(infile)
	out_full = os.path.splitext(base)[0]
	output_file = out_full + "_threshold" + str(threshold_value) + ".txt"

if args.ProteinOrtho:
	#if -tp argument is called
	print("ProteinOrtho results recieved")
	#save the input program ID for use in the output file
	prog_id = "ProteinOrtho"
	#import input file into pandas dataframe
	ortho_df = pd.read_csv(infile, sep = '\t', header = 0)
	#define the output file based on the input file name
	base = os.path.basename(infile)
	out_full = os.path.splitext(base)[0]
	output_file = out_full + "_threshold" + str(threshold_value) + ".txt"

if args.SonicParanoid:
	#if -en argument is called
	print("SonicParanoid results recieved")
	#save the input program ID for use in the output file
	prog_id = "SonicParanoid"
	#import input file into pandas dataframe
	ortho_df = pd.read_csv(infile, sep = '\t', header = 0)
	#define the output file based on the input file name
	base = os.path.basename(infile)
	out_full = os.path.splitext(base)[0]
	output_file = out_full + "_threshold" + str(threshold_value) + ".txt"


#################################   Main Program   ######################################

#Complete setup

#remove 3rd column from Pandas dataframe if necessary 
#needed for original parsed results of OrthoFinder, ProteinOrtho & SonicParanoid
col_num = len(ortho_df.columns)
#count number of columns
if col_num == 3:
	#select dataframes with 3 columns
	#remove middle column with species information
	ortho_df.drop(ortho_df.columns[1], axis=1, inplace=True)


#Part 1: Set up dictionary of OG data that will be filtered

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


#Part 2: Identify OGs that meet the threshold minimum

#create empty list for non-paralog OGs
good_OG_list = []


for key in ortho_dict.keys():
	#iterate through the dictionary via its keys
	if len(ortho_dict[key]) >= threshold_value:
		#identify OGs that meet the minimum threshold value size
		#and add those OGs to the list of good OGs
		good_OG_list.append(key)


#Part 3: Copy threshold size OG information into a new dataframe & write out

#create new dataframe with non-paralog OGs
threshold_df = ortho_df[ortho_df[og_col].isin(good_OG_list)].copy()
#use `.isin()` to iterate over entire list of threshold-meeting OGs
#use `.copy()` to ensure the dataframe is seperate from the ortho_df

#Writing out the results to a tab-separated text file
threshold_df.to_csv(output_file, sep='\t', index=False)
