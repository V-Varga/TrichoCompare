# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: assess_OG_startAA_scores.py
Date: 2022-04-28
Author: Virág Varga

Description:
	This program assesses the quality of OGs in the Metamonad database (or filtered
		version of the same, including at minimum the columns 'Query', 'Secretion_Score',
		'Mitochondria_Score', 'StartAA' and the OG information column of the OG program
		desired to be used as input for the search), based on the desired representation
		criteria of the user.
	The following can be used to filter for representation:
		- Percent of proteins in a given OG which meet a given minimum prediction
			score for either the mitochondrial or secretory pathway
		- Percent of proteins in a given OG which start with Methionine, or with
			either Methionine or Leucine

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	argparse
	pandas
	sys
	os
	datetime.datetime
	statistics

Procedure:
	1. Assignment of command-line arguments with argparse.
	2. Parsing arguments.
		- Importing modules, determining inputs & outputs, importing data
		- Determining filtration category and performing dataframe querying

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output files are only partially user-defined.
	- The input file used for the program must be the large Metamonad database or filtered version
		of the same, including at minimum the columns 'Query', 'Secretion_Score',
		'Mitochondria_Score', 'StartAA' and the OG information column of the OG program
		desired to be used as input for the search.
	- The program cannot carry out multiple analyses simultaneously with one command.

Inputs & Outputs:
	- Inputs:
		+ The mandatory input file is the large Metamonad database or filtered version
			of the same, including at minimum the columns 'Query', 'Secretion_Score',
			'Mitochondria_Score', 'StartAA' and the OG information column of the OG program
			desired to be used as input for the search.
		+ This program accepts input query OG ID lists in the following formats:
			- Singular OG ID provided on the command line
			- Comma-separated list of OG IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
			- File containing list of OG IDs in format: ID1\nID2 etc.
	- Outputs:
		The program will output two text files containing the following:
			- [BASENAME]_filt[THRESHOLD]_stats.txt: Summary statistics file \n \
			- [BASENAME]_filt[THRESHOLD]_OGs.txt: File containing OGs meeting the search criteria in format:
				OG_ID1\nOG_ID2\nOG_ID3 etc.

Usage:
	./assess_OG_startAA_scores.py [-h] -cat FILTRATION_CATEGORY -query QUERY_IDS -prog OG_PROGRAM
		[-val THRESHOLD] [-score SCORE] [-incl INCLUDED_AA] [-out OUT_NAME] [-v] -i INPUT_FILE
	OR
	python assess_OG_startAA_scores.py [-h] -cat FILTRATION_CATEGORY -query QUERY_IDS -prog OG_PROGRAM
		[-val THRESHOLD] [-score SCORE] [-incl INCLUDED_AA] [-out OUT_NAME] [-v] -i INPUT_FILE

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""

#################################   ARGPARSE   #######################################

import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


#The most general description of what this program can do is defined here
parser = argparse.ArgumentParser(description =
								 'This program asseses the quality of OGs in the Metamonad database (or filtered \
									version of the same, including at minimum the columns "Query", "Secretion_Score", \
									"Mitochondria_Score", "StartAA" and the OG information column of the OG program \
									desired to be used as input for the search), based on the desired representation \
									criteria of the user. \n \
								The following can be used to filter for representation: \n \
									- Percent of proteins in a given OG which meet a given minimum prediction \
										score for either the mitochondrial or secretory pathway \n \
									- Percent of proteins in a given OG which start with Methionine, or with \
										either Methionine or Leucine')

#create a group of arguments which will be required
requiredArgNames = parser.add_argument_group('required arguments')
#ref: https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments

#adding the arguments that the program can use
requiredArgNames.add_argument(
	'-cat', '--filtration_category',
	metavar='FILTRATION_CATEGORY',
	dest='filt_cat',
	choices=['Secretion_Score', 'Mitochondria_Score', 'StartAA'],
	#ref: https://stackoverflow.com/questions/15836713/allowing-specific-values-for-an-argparse-argument
	help = 'This argument requires the user to specify the type of data the filtration should be performed on. \
		The options are: "Secretion_Score" OR "Mitochondria_Score" OR "StartAA".',
	required=True
	)
	#the '-cat' flag is used to tell the program which column will be used for scoring
requiredArgNames.add_argument(
	'-query', '--query_ids',
	dest='query_ids',
	metavar='QUERY_IDS',
	help = 'Here specify the query protein IDs in one of the following formats: \n \
		single protein ID OR comma-separated list of protein IDs (ex. `ID_1,ID_2,ID_3`) \n \
			OR file with protein IDs separated by newlines \n \
			When using unencoded query IDs, a key portion of the protein name is sufficient - \n \
				The entirety of the protein header does not need to be used.',
	required=True
	)
	#the '-query' flag specifies that a query protein ID (or list of them) is required,
	#as well as the formats that can be used
requiredArgNames.add_argument(
	'-prog', '--og_program',
	metavar='OG_PROGRAM',
	dest='og_program',
	choices=['Br_Grouped_OGs', 'Br_Single_OGs', 'ProteinOrtho_OG', 'OrthoFinder_OG', 'SonicParanoid_OG'],
	#ref: https://stackoverflow.com/questions/15836713/allowing-specific-values-for-an-argparse-argument
	help = 'This argument requires the user to specify the OG program whose data the filtration should be performed on. \n \
		The options are: "Br_Grouped_OGs" OR "Br_Single_OGs" OR "ProteinOrtho_OG" OR "OrthoFinder_OG" OR "SonicParanoid_OG".',
	required=True
	)
	#the '-cat' flag is used to tell the program which column will be used for scoring

parser.add_argument(
	'-val', '--threshold_value',
	dest='threshold',
	metavar='THRESHOLD',
	type=int,
	default=80,
	help = "Integer value of minimum percent of proteins to meet the given test criteria in OGs. \n \
		Test criteria are: \n \
		- Percent proteins in OG predicted to score at or above given score threshold for given pathway \n \
		- Percent proteins in OG achieving given completion level based on first amino acid in sequence \n \
		(Default = 80)"
	)
	#the `type=int` argument allows argparse to accept the input as an integer
	#the `default=80` gives a default minimum membership filtration value
	#ref: https://stackoverflow.com/questions/44011031/how-to-pass-a-string-as-an-argument-in-python-without-namespace
	#ref: https://stackoverflow.com/questions/14117415/in-python-using-argparse-allow-only-positive-integers
parser.add_argument(
	'-score', '--filt_score',
	metavar='SCORE',
	dest='filt_score',
	type=float,
	default=4.0,
	help = 'This argument allows the user to define he scoring threshold that should be used \n \
		for the given pathway scoring filtration. (Default = 4.0) \n \
		This argument is automatically called for mitochondrial or sectretory pathway testing.'
	)
	#the '-score' flag will enable the user to provide the desired score threshold to be tested
parser.add_argument(
	'-incl', '--includedAA',
	metavar='INCLUDED_AA',
	dest='included_aa',
	choices=['Met', 'Leu'],
	default='Met',
	help = 'This argument allows the user to define the sequence quality checking to be used. \n \
		The options are: "Met" OR "Leu" \n \
		Where "Met" will filter for percent of proteins that start with Methionine; \n \
		while "Leu" will filter for percent of proteins that start with Methionine or Leucine. \n \
		This argument is automatically called for completion quality testing. The default is "Met".'
	)
	#the '-incl' flag will enable the user to provide the desired sequence completion quality
	#based on the starting amino acid in the protein sequence

parser.add_argument(
	'-out', '--outname',
	metavar='OUT_NAME',
	dest='out_name',
	help = 'This argument allows the user to define an output file basename. \n \
		The default basename is "Assessed_[FILTRATION_CATEGORY]_[SCORE/INCLUDED_AA]_[datetime]", \n \
			and the output files are: \n \
				- [BASENAME]_filt[THRESHOLD]_stats.txt: Summary statistics file \n \
				- [BASENAME]_filt[THRESHOLD]_OGs.txt: File containing OGs meeting threshold in format OG1\nOG2 etc.'
	)
	#the '-out' flag allows the user to define a the output file basename
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
	help = "The input file should be the Metamonad database (or filtered version of the same, \
		including at minimum the columns 'Query', 'Secretion_Score', 'Mitochondria_Score', \
			'StartAA' and the OG information column of the OG program desired to be used as input for the search).",
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
import sys #allows access to command-line
import os #allow access to computer files
from datetime import datetime #access data from system regarding date & time
import statistics #enables calculation of statistics in Python


#designate input file name as variable
infile = args.input_file.name
#import the dataframe into Pandas
ortho_df = pd.read_csv(infile, sep = '\t', header = 0, low_memory=False)

#identify key columns of dataframe
filt_col = args.filt_cat
#filt_col will contain the name of the column to be searched
og_col = args.og_program
#og_col will contain the name of the OG program whose data is to be searched


#identify filtration thresholds & criteria
filt_threshold = args.threshold
#determine the filtration threshold for percent inclusion of any given test criteria

if filt_col == 'Secretion_Score':
	#if the user is filtering based on prediction probability of secretion
	#save the value of the score threshold to a variable
	score_threshold = args.filt_score
elif filt_col == 'Mitochondria_Score':
	#if the user is filtering based on the prediction probability of secretion
	#save the value of the score threshold to a variable
	score_threshold = args.filt_score
elif filt_col == 'StartAA':
	#if the user is filtering based on the identity of the first amino acid in each protein
	#save the level of completion to search for to a variable
	complete_aa = args.included_aa
else:
	#if the user does not determine the input query type as encoded or unencoded
	#display this error message
	print("Please select query type: 'Secretion_Score' OR 'Mitochondria_Score' OR 'StartAA'")
	#and exit the program
	sys.exit(1)


#define the output files
if args.out_name:
	#if the user provides an output file name
	#use that file name as the output file basename
	out_base = args.out_name
else:
	#if no output file name is provided by the user
	if 'score_threshold' in globals():
		#check to see if the score_threshold variable exists
		#if it does, save the contents to a new variable
		name_threshold = str(score_threshold)
	else:
		#if score_theshold doesn't exist, then by definition variable complete_aa does
		#so do the same as before with this variable
		name_threshold = complete_aa
	out_start = "Assessed_" + filt_col + str(filt_threshold) + "_" + name_threshold + "_"
	#first extract base file name
	#then determine date & time of query
	now = datetime.now()
	time_now = now.strftime("%d-%m-%Y--%H%M%S")
	#and create the resulting outfile name
	out_base = out_start + time_now
#define specific output files
output_stats = out_base + "_stats.txt"
output_ogs = out_base + "_OGs.txt"


#identify the list of query OG IDs
og_ids = args.query_ids

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


#Part 2: Create dictionary to hold information on proteins per OG

#create a dictionary in the format: og_dict[og_id] = list_of_proteins
#this will allow easier analysis
grouped_ortho_df = ortho_df.groupby(og_col)['Query'].apply(list).reset_index(name="OG_members")
#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
#the new column of lists is named 'OG_members'
ortho_dict = grouped_ortho_df.set_index(og_col).to_dict()['OG_members']
#the new dataframe is converted into a dictionary,
#where the OG IDs are the keys, and the lists of protein members of the OGs are the values
del ortho_dict['-']
#there will likely be proteins that do not have OG assignments, and so are "assigned" to OG '-'
#remove these from the dicitonary before proceeding


#Part 3: Perform dataframe querying & write out results

if filt_col == 'Secretion_Score' or filt_col == 'Mitochondria_Score':
	#if the user is filtering based on prediction probability of a pathway

	#create empty dictionary for score information
	score_dict = {}

	for key in ortho_dict.keys():
		#iterate over the dictionary via its keys
		if key in query_list:
			#identify those keys (OG IDs) that are in the query list,
			#and use only those when compiling the score dictionary
			score_list = []
			#create empty list that will be populated with score information
			og_prot_list = ortho_dict[key]
			#save list of protein query IDs associated with the given OG
			for prot in og_prot_list:
				#iterate over the list of protein query IDs
				prot_score = ortho_df.loc[ortho_df['Query'] == prot, filt_col].iloc[0]
				#with .loc, find the location where the protein query ID is found in the 'Query' column
				#then extract the contents of that cell, as well as the cell in the same row that is in the applicable score column
				#use slicing and .iloc to extract the contents of the applicable score column
				#and save the score to variable prot_score
				#append the score to the score_list
				score_list.append(prot_score)
			#save the list of scores as the value in the OG to scores dictionary
			score_dict[key] = score_list

	#create an empty dictionary for the scoring statistics per OG
	score_stats_dict = {}
	#the dictionary should be populated like so:
	#score_stats_dict[OG_ID] = [number_of_prots, percent_prots_meeting_score_threshold, avg_prot_score, median_prot_score, mode_prot_score]

	#create an empty list to contain the good quality OGs
	good_OG_list = []

	for score_key in score_dict.keys():
		#iterate over the dictionary of scores via its keys (OG IDs)
		og_prot_scores = score_dict[score_key]
		#save list of scores for the OG to a local list for ease of manipulation
		og_length = len(og_prot_scores)
		#save the number of proteins in the OG to a variable
		numb_good_prots = sum(i >= score_threshold for i in og_prot_scores)
		#save number of proteins that meet the score threshold to a variable
		percent_good_prots = numb_good_prots/og_length*100
		#save the percent of proteins in the OG meeting the score threshold to a variable
		if percent_good_prots >= filt_threshold:
			#identify OGs with percent of proteins that meet the score threshold,
			#that are >= the filtration threshold value for inclusion
			#and add those OGs to the list of good OGs
			good_OG_list.append(score_key)
		og_score_avg = statistics.mean(og_prot_scores)
		#save the average protein prediction score to a variable
		og_score_median = statistics.median(og_prot_scores)
		#save the median protein prediction score to a variable
		og_score_mode = statistics.mode(og_prot_scores)
		#save the most common value (mode) to a variable

		#save the calculated statistics to a list
		score_stats_list = [og_length, percent_good_prots, og_score_avg, og_score_median, og_score_mode]
		#and save the calculated statistics to the statistics dictionary
		score_stats_dict[score_key] = score_stats_list

	#convert the dictionary to a Pandas dataframe using the keys as the row indexes
	score_stats_df = pd.DataFrame.from_dict(score_stats_dict, orient='index')
	#then pull the query ID information out of the index
	score_stats_df.reset_index(inplace=True)
	#and rename the columns
	score_stats_df.rename(columns={"index": og_col, 0: "OG_Length", 1: "Percent_Good_Prots",
							2:"OG_Avg_Score", 3: "OG_Median_Score", 4: "OG_Mode_Score"}, inplace=True)

	#write out results
	#first, the summary statistics file as a tab-separated dataframe
	score_stats_df.to_csv(output_stats, sep='\t', index=False)
	#and then the list of good OGs
	with open(output_ogs, "w") as outfile:
		#open the file for writing
		#first write a header line
		outfile.write(og_col + "\n")
		for element in good_OG_list:
			#iterate over the list of good OGs
			#and write the OG IDs out to the file separated by newline characters
			outfile.write(element + "\n")


if filt_col == 'StartAA':
	#if the user is filtering based on the identity of the first amino acid in each protein

	#create empty dictionary for starting amino acid information
	aa_dict = {}

	for key in ortho_dict.keys():
		#iterate over the dictionary via its keys
		if key in query_list:
			#identify those keys (OG IDs) that are in the query list,
			#and use only those when compiling the score dictionary
			aa_list = []
			#create empty list that will be populated with the starting amino acids of the proteins in the OG
			og_prot_list = ortho_dict[key]
			#save list of protein query IDs associated with the given OG
			for prot in og_prot_list:
				#iterate over the list of protein query IDs
				prot_startAA = ortho_df.loc[ortho_df['Query'] == prot, filt_col].iloc[0]
				#with .loc, find the location where the protein query ID is found in the 'Query' column
				#then extract the contents of that cell, as well as the cell in the same row that is in the applicable score column
				#use slicing and .iloc to extract the contents of the applicable score column
				#and save the score to variable prot_score
				#append the score to the score_list
				aa_list.append(prot_startAA)
			#save the list of amino acids as the value in the OG to scores dictionary
			aa_dict[key] = aa_list

	#create an empty dictionary for the starting amino acids statistics per OG
	aa_stats_dict = {}
	#the dictionary should be populated like so:
	#score_stats_dict[OG_ID] = [number_of_prots, percent_prots_meeting_score_threshold, avg_prot_score, median_prot_score, mode_prot_score]

	#create an empty list to contain the good quality OGs
	good_OG_list = []

	for aa_key in aa_dict.keys():
		#iterate over the dictionary of starting amino acids via its keys (OG IDs)
		og_aa_list = aa_dict[aa_key]
		#save list of starting amino acids for the OG to a local list for ease of manipulation
		og_length = len(og_aa_list)
		#save the number of proteins in the OG to a variable
		if complete_aa == "Met":
			#if the user specified that only Methionine presence should be used to assess completion
			numb_good_prots = og_aa_list.count("Met")
			#save number of proteins that start with Methionine to a variable
		if complete_aa == "Leu":
			#if the user specified that only Methionine presence should be used to assess completion
			numb_bad_prots = og_aa_list.count("ELSE")
			#save number of proteins that start with something other than Methionine or Leucine to a variable
			numb_good_prots = og_length - numb_bad_prots
			#deterine the number of proteins that start with Methoinine or Leucine
		percent_good_prots = numb_good_prots/og_length*100
		#save the percent of proteins in the OG starting with Methionine to a variable
		if percent_good_prots >= filt_threshold:
			#identify OGs with percent of proteins that start with Methionine,
			#that are >= the filtration threshold value for inclusion
			#and add those OGs to the list of good OGs
			good_OG_list.append(aa_key)
		og_score_mode = statistics.mode(og_aa_list)
		#save the most common value (mode) to a variable

		#save the calculated statistics to a list
		aa_stats_list = [og_length, percent_good_prots, og_score_mode]
		#and save the calculated statistics to the statistics dictionary
		aa_stats_dict[aa_key] = aa_stats_list

		#convert the dictionary to a Pandas dataframe using the keys as the row indexes
		aa_stats_df = pd.DataFrame.from_dict(aa_stats_dict, orient='index')
		#then pull the query ID information out of the index
		aa_stats_df.reset_index(inplace=True)
		#and rename the columns
		aa_stats_df.rename(columns={"index": og_col, 0: "OG_Length", 1: "Percent_Good_Prots",
								2: "OG_Mode_Score"}, inplace=True)

		#write out results
		#first, the summary statistics file as a tab-separated dataframe
		aa_stats_df.to_csv(output_stats, sep='\t', index=False)
		#and then the list of good OGs
		with open(output_ogs, "w") as outfile:
			#open the file for writing
			#first write a header line
			outfile.write(og_col + "\n")
			for element in good_OG_list:
				#iterate over the list of good OGs
				#and write the OG IDs out to the file separated by newline characters
				outfile.write(element + "\n")
