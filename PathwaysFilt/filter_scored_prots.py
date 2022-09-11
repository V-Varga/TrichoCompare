# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: filter_scored_prots.py
Date: 2022.04.04
Author: Virág Varga

Description:
	This program filters the proteins included in the Metamonad database (or a subset
		of the same) based on the threshold score and scoring category column provided
		by the user.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the input database.
	3. Filtering the dataframe based on the score threshold, and writing out results to a
		tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a flat database created by prot_DB_plus_OGs.py
		(named Metamonada_pred_OG_DB.txt in the original workflow), or a filtered version
		of the same, plus scoring columns generated by score_mitochondrialPathway.py and/or
		score_secretoryPathway.py (or alternative scoring script not in original workflow).
	- Only the input file name is user-defined; the naming of the output file is based on
		the input file name.
	- The score threshold should be a value between 0-4. The default value is 4
		(ie. good rating from all 4 prediction programs in the original workflow).

Usage
	./filter_scored_prots.py input_db score_col score_threshold
	OR
	python filter_scored_prots.py input_db score_col score_threshold

	Where the user should give the column name of the scores column being filtered as
		input for the score_col variable.

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

#determine threshold value for "good" score
if len(sys.argv) == 4:
	#see if the user has provided a score value
	#and if they have, save that value to variable score_threshold
	score_threshold = sys.argv[3]
else:
	#if a score threshold isn't provided,
	#use a score of 4 as the default
	score_threshold = 4

#output_db name is based on the input_db name, filtration type & score
output_db = ".".join(input_db.split('.')[:-1]) + '__filt-' + score_type + str(score_threshold) + '.txt'


#Part 2: Create Pandas dataframe from input data

#read in the input OG database file, assigning the first row as a header row
ortho_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)


#Part 3: Filter the dataframe based on the scores, and write out results

#create new filtered datafarme based on the scores
filt_ortho_df = ortho_df[ortho_df[score_col] >= float(score_threshold)]
#only scores >= the threshold score will be kept in this new dataframe


if filt_ortho_df.empty:
	#let the user know if no protein queries met the scoring threshold used
	print("No protein queries met the desired score threshold of " + str(score_threshold) + "!")
else:
	#if the dataframe exists
	#write the scored dataframe out to the assigned result file
	filt_ortho_df.to_csv(output_db, sep = '\t', index=False)
	#results will be written out to a tab-separated text file
