# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_scored_OGs.py
Date: 2022.04.07
Author: Virág Varga

Description:
	This program filters the proteins included in the Metamonad database (or a subset
		of the same) based on a user-provided threshold score for either the Mitochondrial
		or Secretory pathway, as well as a user-provided minimum percent of proteins in an
		OG for a selected program that should meet that score.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Creating Pandas dataframe & OG dictionary from input data.
	3. Creating dictionary of scores in each OG.
	4. Evaluating OG quality based on scores.
	5. Filtering the dataframe based on the good quality OGs and writing out results
		to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a flat database created by prot_DB_plus_OGs.py
		(named Metamonada_pred_OG_DB.txt in the original workflow), or a filtered version
		of the same, plus scoring columns generated by score_mitochondrialPathway.py and/or
		score_secretoryPathway.py (or alternative scoring script not in original workflow).
	- Only the input file name is user-defined; the naming of the output file is based on
		the input file name.
	- The score threshold should be a value between 0-4, and the inclusion percentage
		should be a percentage value (ex. 80 for 80% matching the minimum threshold
		score).

Usage
	./filter_scored_OGs.py input_db score_col og_col score_min percent_inclusion
	OR
	python filter_scored_OGs.py input_db score_col og_col score_min percent_inclusion

	Where the user should give the column name of the scores column being filtered as
		input for the score_col variable; the column name of the OG program being
		filtered on as the input for the score_col variable; a value between 0-4 for the
		score_min variable; and a numeric percentage value for the percent_inclusion
		variable (ex. 80 for 80% inclusion).

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__filt_scores-pfam.txt"

#determine type of score filtration
score_col = sys.argv[2]
#score_col = "Secretion_Score"

if score_col == "Secretion_Score":
	#if the user selected the Secretome filtration option,
	#save the category name of the Secretome scores to the score_type variable
	score_type = "Secretome"
elif score_col == "Mitochondria_Score":
	#if the user selected the Mitochondria filtration option,
	#save the category name of the Mitochondria scores to the score_type variable
	score_type = "Mitochondria"
else:
	#if none of the above core filtration options are selected,
	#print the following message to the console in order to gain user input
	score_type = input("You have selected a score column not included in the original workflow. \n Please provide a score type category:")

#determine category of OG program
og_col = sys.argv[3]
#og_col = "SonicParanoid_OG"

#determine score threshold to use
score_min = sys.argv[4]
#score_min = 4

#determine the % of proteins matching the score threshold that make an OG "good"
percent_inclusion = sys.argv[5]
#percent_inclusion = 85


#output_db name is based on the input_db name, filtration type & score
output_db = ".".join(input_db.split('.')[:-1]) + '__filt-' + score_type + str(percent_inclusion) + "-" + str(score_min) + '.txt'


#Part 2: Create Pandas dataframe & OG dictionary from input data

#read in the input OG database file, assigning the first row as a header row
ortho_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)

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
#remove these from teh dicitonary before proceeding


#Part 3: Create dictionary of scores in each OG

#create empty dictionary for score information
score_dict = {}

for key in ortho_dict.keys():
	#iterate over the dictionary via its keys
	score_list = []
	#create empty list that will be populated with score information
	og_prot_list = ortho_dict[key]
	#save list of protein query IDs associated with the given OG
	for prot in og_prot_list:
		#iterate over the list of protein query IDs
		prot_score = ortho_df.loc[ortho_df['Query'] == prot, score_col].iloc[0]
		#with .loc, find the location where the protein query ID is found in the 'Query' column
		#then extract the contents of that cell, as well as the cell in the same row that is in the applicable score column
		#use slicing and .iloc to extract the contents of the applicable score column
		#and save the score to variable prot_score
		#append the score to the score_list
		score_list.append(prot_score)
	#save the list of scores as the value in the OG to scores dictionary
	score_dict[key] = score_list


#Part 4: Evaluate OG quality based on scores

#convert the score thresholds into usable values
#need to float() to ensure the input won't be read as a string
score_min = float(score_min)
#first the minimum score
#and then the threshold score, rounded to 3 decimal places
threshold_decimal = round(float(percent_inclusion)/100, 3)

#create empty list for good OGs
good_OG_list = []


for key in score_dict.keys():
	#iterate over the score dictionary via its keys
	og_score_list = score_dict[key]
	#save the list of scores to a list independent of the dictionary for ease of manipulation
	og_length = len(og_score_list)
	#determine the size of the og based on its length
	good_og_length = og_length*threshold_decimal
	#save the minimum number of good scores needed to mark the OG as good to a variable
	good_count = 0
	#set up a counter for the good scores
	for item in og_score_list:
		#iterate over the list of scores
		if item >= score_min:
			#if the value of the score is >= the minimum score value given
			#increase the counter by one
			good_count +=1
	#now compare the number of good scores to the length of the OG (ie. number of protein members)
	if good_count >= good_og_length:
		#if the number of good proteins is >= the minimum number of good proteins to deem the OG good
		#then save the OG ID to the good OG list
		good_OG_list.append(key)


#Part 5: Filter the dataframe based on the scores, and write out results

#create new filtered datafarme based on the scores
filt_ortho_df = ortho_df[ortho_df[og_col].isin(good_OG_list)]
#only rows containing OGs that have been deemed good will be kept


if filt_ortho_df.empty:
	#let the user know if no protein queries met the scoring threshold used
	print("No protein queries met the desired score thresholds!")
else:
	#if the dataframe exists
	#write the scored dataframe out to the assigned result file
	filt_ortho_df.to_csv(output_db, sep = '\t', index=False)
	#results will be written out to a tab-separated text file
