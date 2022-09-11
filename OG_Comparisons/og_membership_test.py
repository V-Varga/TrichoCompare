# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og_membership_test.py
Date: 2022-03-08
Author: Virág Varga

Description:
	This program compares the parsed results files from Broccoli, OrthoFinder,
		ProteinOrtho and SonicParanoid, in order the score the similarity of the
		orthologous clusters created by these programs.
	The user can set a target threshold average similarity value, under which results
		should not be reported. Default is 50%.

List of functions:
	data_2_pandas(broccoli_db, orthofinder_db, proteinortho_db, sonicparanoid_db):
		Loads input parsed OG databases into Pandas dataframes and dictionaries. 
	create_prot_dict(broccoli_df, orthofinder_df, proteinortho_df, sonicparanoid_df):
		Creates the protein query ID to list of assigned OGs dictionary.
	filter_prot_dict(broccoli_df, orthofinder_df, proteinortho_df, sonicparanoid_df):
		Filter the contents of the protein query ID to list of assigned OGs
		dictinary to only include those OGs as keys that were clustered by more than 1
		clustering program.
	membership_test()
	avg_membership_scores()
	threshold_test()

List of standard and non-standard modules used:
	sys
	pandas
	json
	difflib
	statistics

Procedure:
	1. Loading required modules, setting the threshold value to be used in the
		comparison filtration and the corresponding output file name.
	2. Determining input files as command-line arguments, and importing the contents
		of these databases into Pandas dataframes and dictionaries. Dictionaries
		are exported in JSON format. Checkpoint 1 is reached at the completion of
		this step.
	3. Creation of the protein query ID to OG cluster assignments list dictionary.
		Checkpoint 2 is reached at the conclusion of this step, when this dictionary
		is exported in JSON format.
	4. Filtration of the protein query ID to OG assignment list dictionary to exclude
		protein queries that were only clustered by one program. Checkpoint 3 is reached
		at the conclusion of this step, when the new dictionary is exported in JSON
		format.
	5. The all-vs-all OG membership tests are completed, and a dictionary is created
		containing the similarity scores of the clusters created by the programs.
		Checkpoint 4 is reached at the conclusion of this step, when this comparison
		dictionary is exported in JSON format.
	6. The scores inside of the comparison dictionary are averaged. Checkpoint 4.5 is
		reached at the conclusion of this step, when this smaller dictionary is exported
		in JSON format.
	7. The threshold membership percentage value is used to filter the programs with
		the most similar clusters, and a new dictionary is created to containing only
		this data. Checkpoint 5 is reached at the conclusion of this step.
	8. The contents ot the dictionary created in the final step (ie. the final,
		membership threshold-filtered data) is written out to a text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The names of the JSON files created at the checkpoints are not user-defined. This
		means that running the program multiple times in the same directory will
		overwrite existing files from a previous run.
	- The final results file is similarly pre-determined, though the threshold percentage
		value is integrated into the file name, so the program will not overwrite the
		results file if a different threshold value is used.
	- The membership_percent threshold value must be given as an integer, not as a
		decimal percentage.
	- This program is intended for use with parsed Broccoli results from which duplicates have 
		already been removed. 

Usage:
	The full program can be run with:
		./og_membership_test.py broccoli_db orthofinder_db proteinortho_db sonicparanoid_db [membership_percent]
		OR
		python og_membership_test.py broccoli_db orthofinder_db proteinortho_db sonicparanoid_db [membership_percent]

		* Where the membership_percent threshold value should be given as an integer percentage value.

	Alternatively, the program can be run from a checkpoint, using a JSON file produced
		during the earlier stages of the analysis. In such a case, the program should
		be run like so:
			./og_membership_test.py [JSON_file] [membership_percent]
			OR
			python og_membership_test.py [JSON_file] [membership_percent]

		* Where the acceptable input JSON files include:
			- prot_dict.json: This will start the program after Checkpoint 2, by providing a
				complete version of the prot_dict protein query to OG list dictionary.
			- filt_prot_dict.json: This will start the program after Checkpoint 3, by providing
				a complete version of the filt_prot_dict filtered protein query to OG list,
				from which queries only predicted to cluster by one program have been removed.
			- compare_OG_dict.json: This will start the program after Checkpoint 4, by
				providing a version of the compare_dict clustering program to cluster score list
				dictionary.
			- og_score_dict.json: This will start the program after Checkpoint 4.5, by providing
				a version of the OG scoring dictionary in which the average scores have already
				been calculated.
		* Note! The membership testing, which occurs after Checkpoint 3, requires the input of
			dictionaries created from the orthologous clustering dataframes. These are produced
			during the Pandas dataframe imports, and are printed out to JSON files. While they should
			not be added as command-line arguments, they should be in the directory from which this
			program is run.

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


# Part 1: Loading required modules, setting the threshold value to be used
# in the comparison filtration and the corresponding output file name.

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
import json #allows import and export of data in JSON format
import difflib #compare and calculate differences between datasets
import statistics #simplify computation of basic statistics in Python


###
# Define the functions that will be used in this script
###


def data_2_pandas(broccoli_db, orthofinder_db, proteinortho_db, sonicparanoid_db):
	# Part 2: Determining input files as command-line arguments, and importing the contents
	# of these databases into Pandas dataframes and dictionaries. Dictionaries
	# are exported in JSON format. Checkpoint 1 is reached at the completion of this step.

	#import Broccoli database into a Pandas dataframe
	broccoli_df = pd.read_csv(broccoli_db, sep = '\t', header = 0)
	#create a dictionary in the format: og_dict[og_id] = list_of_proteins
	grouped_broccoli_df = broccoli_df.groupby('Broccoli_OG')['Query'].apply(list).reset_index(name="OG_members")
	#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
	#the new column of lists is named 'OG_members'
	broccoli_dict = grouped_broccoli_df.set_index('Broccoli_OG').to_dict()['OG_members']
	#the new dataframe is converted into a dictionary,
	#where the OG IDs are the keys, and the lists of protein members of the OGs are the values
	#write out the filtered protein query database
	with open('broccoli_dict.json', 'w') as broccoli_out:
		#open the JSON outfile for writing
		#and write out the contents of the broccoli_dict dictionary
		json.dump(broccoli_dict, broccoli_out)

	#import OrthoFinder database into a Pandas dataframe
	orthofinder_df = pd.read_csv(orthofinder_db, sep = '\t', header = 0)
	#remove middle column with species information
	orthofinder_df.drop(orthofinder_df.columns[1], axis=1, inplace=True)
	#create a dictionary in the format: og_dict[og_id] = list_of_proteins
	grouped_orthofinder_df = orthofinder_df.groupby('OrthoFinder_OG')['Query'].apply(list).reset_index(name="OG_members")
	#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
	#the new column of lists is named 'OG_members'
	orthofinder_dict = grouped_orthofinder_df.set_index('OrthoFinder_OG').to_dict()['OG_members']
	#the new dataframe is converted into a dictionary,
	#where the OG IDs are the keys, and the lists of protein members of the OGs are the values
	#write out the filtered protein query database
	with open('orthofinder_dict.json', 'w') as orthofinder_out:
		#open the JSON outfile for writing
		#and write out the contents of the orthofinder_dict dictionary
		json.dump(orthofinder_dict, orthofinder_out)

	#import ProteinOrtho database into a Pandas dataframe
	proteinortho_df = pd.read_csv(proteinortho_db, sep = '\t', header = 0)
	#remove middle column with species information
	proteinortho_df.drop(proteinortho_df.columns[1], axis=1, inplace=True)
	#create a dictionary in the format: og_dict[og_id] = list_of_proteins
	grouped_proteinortho_df = proteinortho_df.groupby('ProteinOrtho_OG')['Query'].apply(list).reset_index(name="OG_members")
	#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
	#the new column of lists is named 'OG_members'
	proteinortho_dict = grouped_proteinortho_df.set_index('ProteinOrtho_OG').to_dict()['OG_members']
	#the new dataframe is converted into a dictionary,
	#where the OG IDs are the keys, and the lists of protein members of the OGs are the values
	#write out the filtered protein query database
	with open('proteinortho_dict.json', 'w') as proteinortho_out:
		#open the JSON outfile for writing
		#and write out the contents of the proteinortho_dict dictionary
		json.dump(proteinortho_dict, proteinortho_out)

	#import SonicParanoid database into a Pandas dataframe
	sonicparanoid_df = pd.read_csv(sonicparanoid_db, sep = '\t', header = 0)
	#remove middle column with species information
	sonicparanoid_df.drop(sonicparanoid_df.columns[1], axis=1, inplace=True)
	#create a dictionary in the format: og_dict[og_id] = list_of_proteins
	grouped_sonicparanoid_df = sonicparanoid_df.groupby('SonicParanoid_OG')['Query'].apply(list).reset_index(name="OG_members")
	#the proteins in the 'Query' column are grouped into lists according to the OG they belong to
	#the new column of lists is named 'OG_members'
	sonicparanoid_dict = grouped_sonicparanoid_df.set_index('SonicParanoid_OG').to_dict()['OG_members']
	#the new dataframe is converted into a dictionary,
	#where the OG IDs are the keys, and the lists of protein members of the OGs are the values
	#write out the filtered protein query database
	with open('sonicparanoid_dict.json', 'w') as sonicparanoid_out:
		#open the JSON outfile for writing
		#and write out the contents of the filt_sonicparanoid_dict dictionary
		json.dump(sonicparanoid_dict, sonicparanoid_out)


	#Checkpoint 1 - let the user know program progress
	print("1st Checkpoint: All input datasets have been imported as Pandas dataframes.")


	#define objects to return
	return broccoli_df, broccoli_dict, orthofinder_df, orthofinder_dict, proteinortho_df, proteinortho_dict, sonicparanoid_df, sonicparanoid_dict


def create_prot_dict(broccoli_df, orthofinder_df, proteinortho_df, sonicparanoid_df):
	# Part 3: Creation of the protein query ID to OG cluster assignments list dictionary.
	# Checkpoint 2 is reached at the conclusion of this step, when this dictionary is exported in JSON format.

	#get lists of query proteins from the imported dataframes
	#Broccoli
	broccoli_queries = broccoli_df['Query'].to_list()
	#OrthoFinder
	orthofinder_queries = orthofinder_df['Query'].to_list()
	#ProteinOrtho
	proteinortho_queries = proteinortho_df['Query'].to_list()
	#SonicParanoid
	sonicparanoid_queries = sonicparanoid_df['Query'].to_list()

	#concatenate the lists of queries
	prot_queries = broccoli_queries + orthofinder_queries + proteinortho_queries + sonicparanoid_queries
	#turn the list of queries into a set to eliminate duplicates
	prot_queries = set(prot_queries)


	#create an empty dictionary to populate
	prot_dict = {}

	for prot in prot_queries:
		#iterate through the protein query IDs
		#initially, set the variables for all og categories as "-"
		#these will be overwritten in loops if the protein query was used in the given dataframe
		broccoli_og = "-"
		orthofinder_og = "-"
		proteinortho_og = "-"
		sonicparanoid_og = "-"
		if prot in broccoli_queries:
			#see if protein query ID is in the Broccoli dataframe
			broccoli_og = broccoli_df.loc[broccoli_df['Query'] == prot, 'Broccoli_OG'].iloc[0]
			#with .loc, dind the location where the protein query ID is found in the 'Query' column
			#then extract the contents of that cell, as well as the cell in the same row that is in the 'Broccoli_OG' column
			#use slicing and .iloc to extract the contents of the 'Broccoli_OG' column
			#and replace the contents of variable broccoli_og ("-") with the OG ID
		if prot in orthofinder_queries:
			#see if protein query ID is in the OrthoFinder dataframe
			orthofinder_og = orthofinder_df.loc[orthofinder_df['Query'] == prot, 'OrthoFinder_OG'].iloc[0]
			#with .loc, dind the location where the protein query ID is found in the 'Query' column
			#then extract the contents of that cell, as well as the cell in the same row that is in the 'OrthoFinder_OG' column
			#use slicing and .iloc to extract the contents of the 'OrthoFinder_OG' column
			#and replace the contents of variable orthofinder_og ("-") with the OG ID
		if prot in proteinortho_queries:
			#see if protein query ID is in the ProteinOrtho dataframe
			proteinortho_og = proteinortho_df.loc[proteinortho_df['Query'] == prot, 'ProteinOrtho_OG'].iloc[0]
			#with .loc, dind the location where the protein query ID is found in the 'Query' column
			#then extract the contents of that cell, as well as the cell in the same row that is in the 'ProteinOrtho_OG' column
			#use slicing and .iloc to extract the contents of the 'ProteinOrtho_OG' column
			#and replace the contents of variable proteinortho_og ("-") with the OG ID
		if prot in sonicparanoid_queries:
			#see if protein query ID is in the SonicParanoid dataframe
			sonicparanoid_og = sonicparanoid_df.loc[sonicparanoid_df['Query'] == prot, 'SonicParanoid_OG'].iloc[0]
			#with .loc, dind the location where the protein query ID is found in the 'Query' column
			#then extract the contents of that cell, as well as the cell in the same row that is in the 'SonicParanoid_OG' column
			#use slicing and .iloc to extract the contents of the 'SonicParanoid_OG' column
			#and replace the contents of variable sonicparanoid_og ("-") with the OG ID
		prot_dict[prot] = [broccoli_og, orthofinder_og, proteinortho_og, sonicparanoid_og]
		#populate the prot_dict dictionary with the protein query IDs as the keys
		#and a list of the Broccoli, OrthoFinder, ProteinOrtho & SonicParanoid OGs assigned to that protein query as the values


	#Checkpoint 2 - let the user know program progress
	print("2nd Checkpoint: Protein query to OG match list dictionary has been successfully created. \
		  Printing dicitonary to file.")

	with open('prot_dict.json', 'w') as temp_file:
		#open the JSON outfile for writing
		#and write out the contents of the filt_prot_dict dictionary
		json.dump(prot_dict, temp_file)


	#define objects to return
	return prot_dict


def filter_prot_dict(prot_dict):
	# Part 4: Filtration of the protein query ID to OG assignment list dictionary to exclude
	# protein queries that were only clustered by one program. Checkpoint 3 is reached
	# at the conclusion of this step, when the new dictionary is exported in JSON format.

	#remove from the dictionary proteins that only occur in 1 program
	remove_list = []
	#create an empty list for the protein queries to be deleted

	for key in prot_dict.keys():
		#iterate over the keys of the prot_dict dictionary
		prot_OG_test = set(prot_dict[key])
		#save the value list as a set, eliminating duplicates
		if len(prot_OG_test) == 2:
			#if the length of the set is 2 (ie. the query protein is only clustered by one of the programs)
			#add the protein query key to the list of queries to remove
			remove_list.append(key)


	#create empty dictionary for first filtration - removal of proteins with only 1 OG match
	filt_prot_dict = {}

	for key in prot_dict.keys():
		#iterated through the prot_dict dictionary keys (ie. protein query IDs)
		if key not in remove_list:
			#for keys that aren't in the list of queries that need to be removed
			#save both the key and the value to the new filtered dictionary
			filt_prot_dict[key] = prot_dict[key]


	#Checkpoint 3 - let the user know program progress
	print("3rd Checkpoint: Protein queries only clustered by one program have been eliminated \
		  from the protein query to OG list dictionary. Printing dictionary to file.")

	#write out the filtered protein query database
	with open('filt_prot_dict.json', 'w') as temp_file:
		#open the JSON outfile for writing
		#and write out the contents of the filt_prot_dict dictionary
		json.dump(filt_prot_dict, temp_file)


	#define objects to return
	return filt_prot_dict


def membership_test(filt_prot_dict, broccoli_dict, orthofinder_dict, proteinortho_dict, sonicparanoid_dict):
	# Part 5: The all-vs-all OG membership tests are completed, and a dictionary is created
	# containing the similarity scores of the clusters created by the programs.
	# Checkpoint 4 is reached at the conclusion of this step, when this comparison dictionary is exported in JSON format.

	#create empty dictionary for comparison data
	#dictionary format: comparison_dict[og_vs_pair] = list_of_protein_group_comparison_values
	comparison_dict = {}
	#define the keys of the dictionary with empty lists as associated values
	comparison_dict['Br_vs_OF'] = [] #Broccoli vs OrthoFinder
	comparison_dict['Br_vs_PO'] = [] #Broccoli vs ProteinOrtho
	comparison_dict['Br_vs_SP'] = [] #Broccoli vs SonicParanoid
	comparison_dict['OF_vs_PO'] = [] #OrthoFinder vs ProteinOrtho
	comparison_dict['OF_vs_SP'] = [] #OrthoFinder vs SonicParanoid
	comparison_dict['PO_vs_SP'] = [] #ProteinOrtho vs SonicParanoid


	for key in filt_prot_dict.keys():
		#iterate through the prot_dict dictionary using both keys and values
		#only calculate comparisons in places where both of the compared programs have results for that protein
		if filt_prot_dict[key][0] != "-" and filt_prot_dict[key][1] != "-":
			#comparing OGs where a protein query ID is found in both Broccoli and OrthoFinder
			Br_OG = filt_prot_dict[key][0]
			#extract the OG that the protein query belongs to within the Broccoli results
			Br_OG_compare = broccoli_dict[Br_OG]
			#use the extracted OG ID to query the Broccoli OG dictionary, to get the list of proteins in that OG
			OF_OG = filt_prot_dict[key][1]
			#extract the OG that the protein query belongs to within the OrthoFinder results
			OF_OG_compare = orthofinder_dict[OF_OG]
			#use the extracted OG ID to query the OrthoFinder OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,Br_OG_compare,OF_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			br_vs_of = sm.ratio()
			#append the similarity ratio to the list associated with the 'Br_vs_OF' key in the comparison dictionary
			comparison_dict['Br_vs_OF'].append(br_vs_of)
		if filt_prot_dict[key][0] != "-" and filt_prot_dict[key][2] != "-":
			#comparing OGs where a protein query ID is found in both Broccoli and ProteinOrtho
			Br_OG = filt_prot_dict[key][0]
			#extract the OG that the protein query belongs to within the Broccoli results
			Br_OG_compare = broccoli_dict[Br_OG]
			#use the extracted OG ID to query the Broccoli OG dictionary, to get the list of proteins in that OG
			PO_OG = filt_prot_dict[key][2]
			#extract the OG that the protein query belongs to within the ProteinOrtho results
			PO_OG_compare = proteinortho_dict[PO_OG]
			#use the extracted OG ID to query the ProteinOrtho OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,Br_OG_compare,PO_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			br_vs_po = sm.ratio()
			#append the similarity ratio to the list associated with the 'Br_vs_PO' key in the comparison dictionary
			comparison_dict['Br_vs_PO'].append(br_vs_po)
		if filt_prot_dict[key][0] != "-" and filt_prot_dict[key][3] != "-":
			#comparing OGs where a protein query ID is found in both Broccoli and SonicParanoid
			Br_OG = filt_prot_dict[key][0]
			#extract the OG that the protein query belongs to within the Broccoli results
			Br_OG_compare = broccoli_dict[Br_OG]
			#use the extracted OG ID to query the Broccoli OG dictionary, to get the list of proteins in that OG
			SP_OG = filt_prot_dict[key][3]
			#extract the OG that the protein query belongs to within the SonicParanoid results
			SP_OG_compare = sonicparanoid_dict[SP_OG]
			#use the extracted OG ID to query the SonicParanoid OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,Br_OG_compare,SP_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			br_vs_sp = sm.ratio()
			#append the similarity ratio to the list associated with the 'Br_vs_SP' key in the comparison dictionary
			comparison_dict['Br_vs_SP'].append(br_vs_sp)
		if filt_prot_dict[key][1] != "-" and filt_prot_dict[key][2] != "-":
			#comparing OGs where a protein query ID is found in both OrthoFinder and ProteinOrtho
			PO_OG = filt_prot_dict[key][2]
			#extract the OG that the protein query belongs to within the ProteinOrtho results
			PO_OG_compare = proteinortho_dict[PO_OG]
			#use the extracted OG ID to query the ProteinOrtho OG dictionary, to get the list of proteins in that OG
			OF_OG = filt_prot_dict[key][1]
			#extract the OG that the protein query belongs to within the OrthoFinder results
			OF_OG_compare = orthofinder_dict[OF_OG]
			#use the extracted OG ID to query the OrthoFinder OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,PO_OG_compare,OF_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			of_vs_po = sm.ratio()
			#append the similarity ratio to the list associated with the 'PO_vs_OF' key in the comparison dictionary
			comparison_dict['OF_vs_PO'].append(of_vs_po)
		if filt_prot_dict[key][1] != "-" and filt_prot_dict[key][3] != "-":
			#comparing OGs where a protein query ID is found in both OrthoFinder and SonicParanoid
			SP_OG = filt_prot_dict[key][3]
			#extract the OG that the protein query belongs to within the SonicParanoid results
			SP_OG_compare = sonicparanoid_dict[SP_OG]
			#use the extracted OG ID to query the SonicParanoid OG dictionary, to get the list of proteins in that OG
			OF_OG = filt_prot_dict[key][1]
			#extract the OG that the protein query belongs to within the OrthoFinder results
			OF_OG_compare = orthofinder_dict[OF_OG]
			#use the extracted OG ID to query the OrthoFinder OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,SP_OG_compare,OF_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			of_vs_sp = sm.ratio()
			#append the similarity ratio to the list associated with the 'SP_vs_OF' key in the comparison dictionary
			comparison_dict['OF_vs_SP'].append(of_vs_sp)
		if filt_prot_dict[key][2] != "-" and filt_prot_dict[key][3] != "-":
			#comparing OGs where a protein query ID is found in both ProteinOrtho and SonicParanoid
			PO_OG = filt_prot_dict[key][2]
			#extract the OG that the protein query belongs to within the ProteinOrtho results
			PO_OG_compare = proteinortho_dict[PO_OG]
			#use the extracted OG ID to query the Broccoli OG dictionary, to get the list of proteins in that OG
			SP_OG = filt_prot_dict[key][3]
			#extract the OG that the protein query belongs to within the SonicParanoid results
			SP_OG_compare = sonicparanoid_dict[SP_OG]
			#use the extracted OG ID to query the SonicParanoid OG dictionary, to get the list of proteins in that OG
			sm=difflib.SequenceMatcher(None,PO_OG_compare,SP_OG_compare)
			#compare the similarity of the two protein lists
			#and compute a numerical ratio of that similarity
			po_vs_sp = sm.ratio()
			#append the similarity ratio to the list associated with the 'PO_vs_OF' key in the comparison dictionary
			comparison_dict['PO_vs_SP'].append(po_vs_sp)

	'''
	Some references for the list comparisons:

	Using difflib:
	https://docs.python.org/3/library/difflib.html
	https://stackoverflow.com/questions/6709693/calculating-the-similarity-of-two-lists

	Using cosine similarity:
	https://stackoverflow.com/questions/28819272/python-how-to-calculate-the-cosine-similarity-of-two-word-lists
	https://stackoverflow.com/questions/14720324/compute-the-similarity-between-two-lists
	https://en.wikipedia.org/wiki/Cosine_similarity

	Both of these methods yeild similar results, within 0.02 (compared two lists with different similarities).
	I chose to use difflib because of its far simpler implementation.

	'''

	'''
	A note on the scoring mechanism used above:

	The way the scoring is done, if clusters are particularly similar between two programs, with the same
	proteins appearing in the OGs of both, the OG's will in some sense be scored multiple times.

	I justify the choice to allow this because giving more weight to programs that are providing more
	similar clusters is useful when trying to quantify the quality of the orthologous clusters these
	programs produce. A cluster that is identified by multiple programs is more likely to be reliable; and
	programs that are identifying similar clusters are likely more adept at identifying OGs within
	these particularly divergent, unique organisms.

	'''

	#Checkpoint 4 - let the user know program progress
	print("4th Checkpoint: OG scoring dictionary has been successfully created. Printing dictionary to file.")

	with open('compare_OG_dict.json', 'w') as temp_file:
		#open the JSON outfile for writing
		#and write out the contents of the filt_prot_dict dictionary
		json.dump(comparison_dict, temp_file)


	#define objects to return
	return comparison_dict


def avg_membership_scores(comparison_dict):
	# Part 6: The scores inside of the comparison dictionary are averaged. Checkpoint 4.5 is
	# reached at the conclusion of this step, when this smaller dictionary is exported in JSON format.
	#create a new empty dictionary to hold the average scores
	og_score_dict = {}

	for key in comparison_dict.keys():
		#iterate over the comparison score dictionary keys
		og_score_avg = statistics.mean(comparison_dict[key])
		#compute the mean/average of the scores in each list in the comparison dictionary
		#and save the average score per commparison to a new dictionary, using the same keys
		og_score_dict[key] = og_score_avg


	#Checkpoint 4.5 - let the user know program progress
	print("4.5th Checkpoint: OG comparison scores have been successfully created. Printing dictionary to file.")

	with open('og_score_dict.json', 'w') as temp_file:
		#open the JSON outfile for writing
		#and write out the contents of the filt_prot_dict dictionary
		json.dump(og_score_dict, temp_file)


	#define objects to return
	return og_score_dict


def threshold_test(og_score_dict):
	# Part 7: The threshold membership percentage value is used to filter the programs with
	# the most similar clusters, and a new dictionary is created to containing only
	# this data. Checkpoint 5 is reached at the conclusion of this step.

	#create new dictionary for OG average scores that meet the desired threshold value
	threshold_dict = {}

	#convert membership percentage to a decimal
	membership_decimal = float(membership_percent)/100

	for key in og_score_dict.keys():
		#iterate over the average scores dictionary's keys
		if og_score_dict[key] >= membership_decimal:
			#filter the comparisons that are similar enough to pass the given threshold value
			#those comparisons that pass, as well as the associated score average, should be copied to the threshold dictionary
			threshold_dict[key] = og_score_dict[key]


	#Checkpoint 5 - let the user know program progress
	print("5th Checkpoint: Orthologous clustering program evaluation based on user-supplied threshold of " +
		  str(membership_percent) + " has been completed. \
			  Printing results to output file.")

	#define objects to return
	return threshold_dict


###
# Running program, based on command-line input
###


#first, set the membership percentage
if len(sys.argv) == 6: #if the primary method of running the program is used
	#check if the user gave a threshold value for filtering average cluster similarity
	#if so, import the selected membership test threshold as the fifth command-line argument
	membership_percent = sys.argv[5]
if len(sys.argv) == 3: #if the program is run from a later checkpoint
	#check if the user gave a threshold value for filtering average cluster similarity
	#if so, import the selected membership test threshold as the fifth command-line argument
	membership_percent = sys.argv[2]
else:
	#if no threshold value is given by the user, use the default value of 50
	membership_percent = 50

#define the output file with a pre-determined prefix & suffix, separated by the membership percent
membership_results = "OG_membership_results_" + str(membership_percent) + ".txt"


#next, set the dataframe command-line arguments for primary program usage method
if len(sys.argv) >= 5:
	#assign command line arguments; load input and output files
	#import the parsed Broccoli results as the first command-line argument
	broccoli_db = sys.argv[1]
	#broccoli_db = "Broccoli_OGs_parsed.txt"
	#import the parsed OrthoFinder results as the second command-line argument
	orthofinder_db = sys.argv[2]
	#orthofinder_db = "OF_OGs_parsed.txt"
	#import the parsed ProteinOrtho results as the third command-line argument
	proteinortho_db = sys.argv[3]
	#proteinortho_db = "PO_OGs_parsed.txt"
	#import the parsed SonicParanoid results as the fourth command-line argument
	sonicparanoid_db = sys.argv[4]
	#sonicparanoid_db = "SP_OGs_parsed.txt"

	#now, use appropriate functions - in this case, all
	broccoli_df, broccoli_dict, orthofinder_df, orthofinder_dict, proteinortho_df, proteinortho_dict, sonicparanoid_df, sonicparanoid_dict = data_2_pandas(broccoli_db, orthofinder_db, proteinortho_db, sonicparanoid_db)
	prot_dict = create_prot_dict(broccoli_df, orthofinder_df, proteinortho_df, sonicparanoid_df)
	filt_prot_dict = filter_prot_dict(prot_dict)
	comparison_dict = membership_test(filt_prot_dict, broccoli_dict, orthofinder_dict, proteinortho_dict, sonicparanoid_dict)
	og_score_dict = avg_membership_scores(comparison_dict)
	threshold_dict = threshold_test(og_score_dict)


#for secondary usage method, loading prot_dict:
if sys.argv[1] == 'prot_dict.json':
	#open the primary JSON input file
	with open('prot_dict.json') as json_file:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		prot_dict = json.load(json_file)
	#open the clustering program dictionaries
	with open('broccoli_dict.json') as broccoli_in:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		broccoli_dict = json.load(broccoli_in)
	with open('orthofinder_dict.json') as orthofinder_in:
		#open the JSON file containing the orthofinder_dict data
		#and load it as a dictionary
		orthofinder_dict = json.load(orthofinder_in)
	with open('proteinortho_dict.json') as proteinortho_in:
		#open the JSON file containing the proteinortho_dict data
		#and load it as a dictionary
		proteinortho_dict = json.load(proteinortho_in)
	with open('sonicparanoid_dict.json') as sonicparanoid_in:
		#open the JSON file containing the sonicparanoid_dict data
		#and load it as a dictionary
		sonicparanoid_dict = json.load(sonicparanoid_in)

	#now, use appropriate functions - in this case, from filtration on
	filt_prot_dict = filter_prot_dict(prot_dict)
	comparison_dict = membership_test(filt_prot_dict, broccoli_dict, orthofinder_dict, proteinortho_dict, sonicparanoid_dict)
	og_score_dict = avg_membership_scores(comparison_dict)
	threshold_dict = threshold_test(og_score_dict)


#for secondary usage method, loading filt_prot_dict:
if sys.argv[1] == 'filt_prot_dict.json':
	#open the primary JSON intermediate results file
	with open('filt_prot_dict.json') as json_file:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		filt_prot_dict = json.load(json_file)
	#open the clustering program dictionaries
	with open('broccoli_dict.json') as broccoli_in:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		broccoli_dict = json.load(broccoli_in)
	with open('orthofinder_dict.json') as orthofinder_in:
		#open the JSON file containing the orthofinder_dict data
		#and load it as a dictionary
		orthofinder_dict = json.load(orthofinder_in)
	with open('proteinortho_dict.json') as proteinortho_in:
		#open the JSON file containing the proteinortho_dict data
		#and load it as a dictionary
		proteinortho_dict = json.load(proteinortho_in)
	with open('sonicparanoid_dict.json') as sonicparanoid_in:
		#open the JSON file containing the sonicparanoid_dict data
		#and load it as a dictionary
		sonicparanoid_dict = json.load(sonicparanoid_in)

	#now, use approtpriate functions - in this case, from membership test on
	comparison_dict = membership_test(filt_prot_dict, broccoli_dict, orthofinder_dict, proteinortho_dict, sonicparanoid_dict)
	og_score_dict = avg_membership_scores(comparison_dict)
	threshold_dict = threshold_test(og_score_dict)


#for secondary usage method, loading comparison_dict:
if sys.argv[1] == 'comparison_dict.json':
	with open('compare_OG_dict.json') as json_file:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		comparison_dict = json.load(json_file)

	#now, use appropriate functions - in this case, from avergaing the membership scores on
	og_score_dict = avg_membership_scores(comparison_dict)
	threshold_dict = threshold_test(og_score_dict)


#for secondary usage method, loading og_score_dict:
if sys.argv[1] == 'og_score_dict.json':
	with open('og_score_dict.json') as json_file:
		#open the JSON file containing the filt_prot_dict data
		#and load it as a dictionary
		og_score_dict = json.load(json_file)

	#now, use appropriate functions - in this case, only the threshold dictionary creation
	threshold_dict = threshold_test(og_score_dict)


###
# Outfile writing is executed for ALL variations of program runs
###


# Part 8: The contents ot the dictionary created in the final step (ie. the final,
# membership threshold-filtered data) is written out to a text file.

with open(membership_results, "w") as outfile:
	#open the results file for writing
	if bool(threshold_dict) == False:
		#test if the dictionary exists - high threshold values may yield an empty threshold_dict
		outfile.write("The given threshold value of " + str(membership_percent) + "% is too high. No OG comparisons met this criteria.")
	else: 
		#otherwise write an introductory line to the file
		outfile.write("The orthologous clustering similarity comparisons that met the desired threshold value of " + str(membership_percent) +
				   "% are listed below:" + "\n\n")
		for key in threshold_dict.keys():
			#iterate through the threshold dictionary by its keys
			#and write out to the results file the comparisons that met the required thresshold value
			outfile.write("For the " + key + " comparison, the average score value is: " + str(threshold_dict[key]) + "\n")
