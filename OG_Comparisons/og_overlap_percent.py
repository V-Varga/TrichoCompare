# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og_overlap_percent.py
Date: 2022-03-21
Author: Virág Varga

Description:
	This program imports the JSON dictionary output by the og_membership_test.py program
		containing information on the OGs associated with a protein query ID from the 4 analysis
		programs used in this workflow (Broccoli, OrthoFinder, ProteinOrtho, SonicParanoid),
		and performs all-vs-all comparisons to identify the OGs with the greatest similarity.
	The program outputs the following files:
		- JSON dictionaries:
			prot_comparison_dict[query_ID] = [[prog1, prog1_OG_ID, prog2, prog2_OG_ID, similiarity_score],
									 [prog1, prog1_OG_ID, prog3, prog3_OG_ID, similiarity_score]]
			comparison_dict[prog_vs_prog] = [[prog1_OG1, prog1_OG2, etc.], [prog2_OG2, prog2_OG2]]
			Filtered version of the dictionary above, excluding protein queries with no comparisons 
				that met the threshold value. 
		- Tab-separated dataframe text files:
			Query\tBroccoli_OG\tOrthoFinder_OG\tPrtoeinOrtho_OG\tSonicParanoid
			And filtered version of the above, removing Query IDs and filtering out duplicate rows
			Dataframes for individual programs, with standard parsed OG format: Query\tPROG_OG
		- Text file summarizing results

List of functions:
	list_duplicates_of(seq,item): Creates list of indexes of repeated element of list
		Source: https://stackoverflow.com/a/5419576/18382033

List of standard and non-standard modules used:
	sys
	json
	difflib
	pandas
	itertools.chain

Procedure:
	1. Importing necessary modules, assigning command-line arguments.
	2. Opening data files and importing into best data types for manipulation.
	3. Finding orthologous groups that meet the threshold similarity using all-vs-all membership tests,
		before filtering out protein queries that have no matching OG pairs that meet the similarity 
		threshold value. 
		Note that 3 JSON dictionaries will be written out at the conclusion of this process.
	4. Creating and writing out comparison dictionaries-based dataframes.
	5. Creating and writing out program-specific OG dataframes.
	6. Writing out summary text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The names of the output files are not user-defined.
	- The input file used for the program must be either the prot_dict.json file or
		filt_prot_dict.json file produced by the og_membership_test.py script.
	- This program must be run from the directory containing the input .json file. It will
		automatically search in that directory for the following files: broccoli_dict.json,
		orthofinder_dict.json, proteinortho_dict.json, and sonicparanoid_dict.json. These
		files are all also produced by the og_membership_test.py program.
	- This program is intended for use with parsed Broccoli results from which duplicates have 
		already been removed. 

Usage:
	./og_overlap_percent.py prot_to_OG_db output_base [membership_threshold]
	OR
	python og_overlap_percent.py prot_to_OG_db output_base [membership_threshold]

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import json #allows transfer of data into and out of JSON files
import difflib #compare and calculate differences between datasets
import pandas as pd #allows manipulation of dataframes in Python
from itertools import chain #allows manipulation of nested lists


#define function to identify indexes of recorring element in list
#ref: https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list
def list_duplicates_of(seq, item):
	#takes the list to search in as first argument
	#takes the string/element to search for the indices of as the second argument
    start_at = -1
	#begins searching at the final postion in the list
    locs = []
	#defines an empty list to 
    while True:
		#loops through the elements of the list
        try:
            loc = seq.index(item,start_at+1)
			#indexes the location of the element
        except ValueError:
			#when there are no more elements to loop through, break the loop
            break
        else:
			#add the index to the list of indices
            locs.append(loc)
			#and update the index being looped through
            start_at = loc
	#return the list of indices as function output
    return locs


#assign and interpret inputs
prot_to_OG_db = sys.argv[1]
#prot_to_OG_db = "filt_prot_dict.json"

if len(sys.argv) == 3:
	#if no membership threshold is given by the user,
	#then 80% should be used as the default
	membership_threshold = 80
if len(sys.argv) == 4:
	#if the user gives a membership threshold, save the percent value to a variable
	membership_threshold = sys.argv[3]

#convert membership percentage to a decimal
membership_decimal = float(membership_threshold)/100


#define output files based on input
output_base = sys.argv[2]
#output_base = "OG_membership_overlap"

#output files (non-JSON)
#overlap dataframes
output_full_query_db = output_base + "_Query" + str(membership_threshold) + ".txt"
output_non_query_db = output_base + "_nonQuery" + str(membership_threshold) + ".txt"

#species-specific dataframes
broccoli_db = "Broccoli_OGs_parsed_overlap" + str(membership_threshold) + ".txt"
orthofinder_db = "OF_OGs_parsed_overlap" + str(membership_threshold) + ".txt"
proteinortho_db = "PO_OGs_parsed_overlap" + str(membership_threshold) + ".txt"
sonicparanoid_db = "SP_OGs_parsed_overlap" + str(membership_threshold) + ".txt"

#output text file
outfile_summary = output_base + "__SUMMARY_" + str(membership_threshold) + ".txt"


#Part 2: Opening data files and importing into best data types for manipulation

#the filtered protein ID to list of assigned OGs dictionary
with open(prot_to_OG_db) as json_file:
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


#Part 3: Finding orthologous groups that meet the threshold similarity using all-vs-all membership tests

#create empty dictionaries for comparison data
#dictionary format: prot_comparison_dict[query_ID] =
#[[prog1, prog1_OG_ID, prog2, prog2_OG_ID, similiarity_score], [prog1, prog1_OG_ID, prog3, prog3_OG_ID, similiarity_score], etc.]
#values from comparisons should only be saved to the dictionary if they meet the threshold similarity value
prot_comparison_dict = {}
#dictionary format: comparison_dict[prog_vs_prog] = [[prog1_OG1, prog1_OG2, etc.], [prog2_OG2, prog2_OG2]]
#values from comparisons should only be saved to the dictionary if they meet the threshold similarity value
comparison_dict = {}
#define the keys of the dictionary with empty lists as associated values
comparison_dict['Br_vs_OF'] = [[], []] #Broccoli vs OrthoFinder
comparison_dict['Br_vs_PO'] = [[], []] #Broccoli vs ProteinOrtho
comparison_dict['Br_vs_SP'] = [[], []] #Broccoli vs SonicParanoid
comparison_dict['OF_vs_PO'] = [[], []] #OrthoFinder vs ProteinOrtho
comparison_dict['OF_vs_SP'] = [[], []] #OrthoFinder vs SonicParanoid
comparison_dict['PO_vs_SP'] = [[], []] #ProteinOrtho vs SonicParanoid


for key in filt_prot_dict.keys():
	#iterate through the prot_dict dictionary using its keys
	prot_comparison_list = []
	#initialize an empty list that will contain the program matching information for the protein query
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
		#and compute a numerical ratio of that similarity, which is saved to a variable
		br_vs_of = sm.ratio()
		if br_vs_of >= membership_decimal:
			#check whether the score meets the threshold requirement
			br_vs_of_comp_list = ["Broccoli", Br_OG, "OrthoFinder", OF_OG, br_vs_of]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(br_vs_of_comp_list)
			#append the OG IDs for Broccoli and OrthoFinder to the value list matching the
			#'Br_vs_OF' key in the comparison dictionary
			#first save the Broccoli OG to the first list in the list
			comparison_dict['Br_vs_OF'][0].append(Br_OG)
			#then save the OrthoFinder OG to the second list in the list
			comparison_dict['Br_vs_OF'][1].append(OF_OG)
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
		if br_vs_po >= membership_decimal:
			#check whether the score meets the threshold requirement
			br_vs_po_comp_list = ["Broccoli", Br_OG, "ProteinOrtho", PO_OG, br_vs_po]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(br_vs_po_comp_list)
			#append the OG IDs for Broccoli and ProteinOrtho to the value list matching the
			#'Br_vs_PO' key in the comparison dictionary
			#first save the Broccoli OG to the first list in the list
			comparison_dict['Br_vs_PO'][0].append(Br_OG)
			#then save the ProteinOrtho OG to the second list in the list
			comparison_dict['Br_vs_PO'][1].append(PO_OG)
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
		if br_vs_sp >= membership_decimal:
			#check whether the score meets the threshold requirement
			br_vs_sp_comp_list = ["Broccoli", Br_OG, "SonicParanoid", SP_OG, br_vs_sp]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(br_vs_sp_comp_list)
			#append the OG IDs for Broccoli and SonicParanoid to the value list matching the
			#'Br_vs_SP' key in the comparison dictionary
			#first save the Broccoli OG to the first list in the list
			comparison_dict['Br_vs_SP'][0].append(Br_OG)
			#then save the SonicParanoid OG to the second list in the list
			comparison_dict['Br_vs_SP'][1].append(SP_OG)
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
		if of_vs_po >= membership_decimal:
			#check whether the score meets the threshold requirement
			of_vs_po_comp_list = ["OrthoFinder", OF_OG, "ProteinOrtho", PO_OG, of_vs_po]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(of_vs_po_comp_list)
			#append the OG IDs for OrthoFinder and ProteinOrtho to the value list matching the
			#'OF_vs_PO' key in the comparison dictionary
			#first save the OrthoFinder OG to the first list in the list
			comparison_dict['OF_vs_PO'][0].append(OF_OG)
			#then save the ProteinOrtho OG to the second list in the list
			comparison_dict['OF_vs_PO'][1].append(PO_OG)
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
		if of_vs_sp >= membership_decimal:
			#check whether the score meets the threshold requirement
			of_vs_sp_comp_list = ["OrthoFinder", OF_OG, "SonicParanoid", SP_OG, of_vs_sp]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(of_vs_sp_comp_list)
			#append the OG IDs for OrthoFinder and SonicParanoid to the value list matching the
			#'OF_vs_SP' key in the comparison dictionary
			#first save the OrthoFinder OG to the first list in the list
			comparison_dict['OF_vs_SP'][0].append(OF_OG)
			#then save the SonicParanoid OG to the second list in the list
			comparison_dict['OF_vs_SP'][1].append(SP_OG)
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
		if po_vs_sp >= membership_decimal:
			#check whether the score meets the threshold requirement
			po_vs_sp_comp_list = ["ProteinOrtho", PO_OG, "SonicParanoid", SP_OG, po_vs_sp]
			#create list of information to append to entry for protein query dictionary
			#and append the information to the data comparison list of lists
			prot_comparison_list.append(po_vs_sp_comp_list)
			#append the OG IDs for Broccoli and OrthoFinder to the value list matching the
			#'PO_vs_SP' key in the comparison dictionary
			#first save the ProteinOrtho OG to the first list in the list
			comparison_dict['PO_vs_SP'][0].append(PO_OG)
			#then save the SonicParanoid OG to the second list in the list
			comparison_dict['PO_vs_SP'][1].append(SP_OG)
	#finally, adding the protein comparison data to the dictionary
	prot_comparison_dict[key] = prot_comparison_list
	#assign the list of lists contianing comparison data as the value to the protein query key
	#in the protein comparison dictionary

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

#write out JSON files containing the two dictionaries produced so far

#the prot_comparison_dict
with open('prot_comparison_dict.json', 'w') as temp_file:
	#open the JSON outfile for writing
	#and write out the contents of the filt_prot_dict dictionary
	json.dump(prot_comparison_dict, temp_file)
#the comparison_dict
with open('comparison_dict.json', 'w') as temp_file:
	#open the JSON outfile for writing
	#and write out the contents of the filt_prot_dict dictionary
	json.dump(comparison_dict, temp_file)


#filter the comparison dicitonary to exlude protein query IDs that have no matching OG information
filt_prot_comparison_dict = {}
#create a new empy dictionary to house the information

for key in prot_comparison_dict.keys():
	#iterate over the large comparison dictionary via its keys
	if prot_comparison_dict[key] != []: 
		#eliminate those proteins that did not meet the threshold
		filt_prot_comparison_dict[key] = prot_comparison_dict[key]

#write this database out to a JSON file
with open('filt_prot_comparison_dict.json', 'w') as temp_file:
	#open the JSON outfile for writing
	#and write out the contents of the filt_prot_dict dictionary
	json.dump(filt_prot_comparison_dict, temp_file)


#Part 4: Creation of comparison dictionaries-based dataframes

'''
with open('comparison_dict.json') as json_in:
	#open the JSON file containing the filt_prot_dict data
	#and load it as a dictionary
	comparison_dict = json.load(json_in)
with open('prot_comparison_dict.json') as json_in:
	#open the JSON file containing the filt_prot_dict data
	#and load it as a dictionary
	prot_comparison_dict = json.load(json_in)
with open('filt_prot_comparison_dict.json') as json_in:
	#open the JSON file containing the filt_prot_dict data
	#and load it as a dictionary
	filt_prot_comparison_dict = json.load(json_in)
'''


#create the basis for the dataframe
query_ids = list(filt_prot_comparison_dict.keys())
#get the protein query IDs into a list
query_OG_df = pd.DataFrame(query_ids, columns = ['Query'])
#and now add empty columns for the OG data
query_OG_df["Broccoli_OG"] = "-"
query_OG_df["OrthoFinder_OG"] = "-"
query_OG_df["ProteinOrtho_OG"] = "-"
query_OG_df["SonicParanoid_OG"] = "-"
#make the query column the index column
query_OG_df = query_OG_df.set_index('Query')


#big query & matching OGs dataframe
for key in filt_prot_comparison_dict.keys():
	#iterate over the large filtered comparison dictionary via its keys
	value_list = filt_prot_comparison_dict[key]
	#save the information associated with the protein query to a list
	value_list = list(chain.from_iterable(value_list))
	#un-nest the nested list in variable value_list
	if "Broccoli" in value_list: 
		#identify queries with Broccoli OGs
		br_idx = value_list.index("Broccoli")
		#identify the index of the string "Broccoli"
		#note that doing it this way will only give the index of the first occurance of this string
		#this isn't an issue because only Broccoli assigns proteins to more than 1 OG
		#and this script is intended to be sed on input data from which duplicates have been filtered out
		br_idx = br_idx + 1
		#add 1 to the index to get the index of the OG ID in the value_list
		prot_br_og = value_list[br_idx]
		#identify the Broccoli OG and copy it to a variable
		#and then add the contents of that variable to the dataframe at the appropriate location
		query_OG_df.at[key, 'Broccoli_OG'] = prot_br_og
	if "OrthoFinder" in value_list: 
		#identify queries with OrthoFinder OGs
		of_idx = value_list.index("OrthoFinder")
		#identify the index of the string "OrthoFinder"
		#note that doing it this way will only give the index of the first occurance of this string
		#this isn't an issue because only Broccoli assigns proteins to more than 1 OG
		of_idx = of_idx + 1
		#add 1 to the index to get the index of the OG ID in the value_list
		prot_of_og = value_list[of_idx]
		#identify the OrthoFinder OG and copy it to a variable
		#and then add the contents of that variable to the dataframe at the appropriate location
		query_OG_df.at[key, 'OrthoFinder_OG'] = prot_of_og
	if "ProteinOrtho" in value_list: 
		#identify queries with ProteinOrtho OGs
		po_idx = value_list.index("ProteinOrtho")
		#identify the index of the string "ProteinOrtho"
		#note that doing it this way will only give the index of the first occurance of this string
		#this isn't an issue because only ProteinOrtho assigns proteins to more than 1 OG
		po_idx = po_idx + 1
		#add 1 to the index to get the index of the OG ID in the value_list
		prot_po_og = value_list[po_idx]
		#identify the ProteinOrtho OG and copy it to a variable
		#and then add the contents of that variable to the dataframe at the appropriate location
		query_OG_df.at[key, 'ProteinOrtho_OG'] = prot_po_og
	if "SonicParanoid" in value_list: 
		#identify queries with SonicParanoid OGs
		sp_idx = value_list.index("SonicParanoid")
		#identify the index of the string "OrthoFinder"
		#note that doing it this way will only give the index of the first occurance of this string
		#this isn't an issue because only Broccoli assigns proteins to more than 1 OG
		sp_idx = sp_idx + 1
		#add 1 to the index to get the index of the OG ID in the value_list
		prot_sp_og = value_list[sp_idx]
		#identify the SonicParanoid OG and copy it to a variable
		#and then add the contents of that variable to the dataframe at the appropriate location
		query_OG_df.at[key, 'SonicParanoid_OG'] = prot_sp_og

#write out the query_OG_df to a tab-separated text file
query_OG_df.to_csv(output_full_query_db, sep='\t', index=True)


#remove the query column by re-indexing
nonQuery_OG_df = query_OG_df.reset_index()
#move the query column out of the index
nonQuery_OG_df.drop('Query', axis=1, inplace=True)
#and drop the column
nonQuery_OG_df.drop_duplicates(keep='first', inplace=True)
#filter dataframe by removing duplicate rows

#write out the query_OG_df to a tab-separated text file
nonQuery_OG_df.to_csv(output_non_query_db, sep='\t', index=False)


#Part 5: Create and write out program-specific OG dataframes

#Broccoli
#create empty dictionary to hold the reversed Broccoli dictionary
pivot_broccoli_dict = {}

for keys, values in broccoli_dict.items():
	#iterate over the Broccoli dictionary via its keys and values
    for i in values:
		#iterate over the elements of the list in each value
		#and save to the dictionary in format pivot_dict[Query] = OG
        pivot_broccoli_dict[i]=keys

#filter the dictionary to only include the proteins that meet the overlap threshold
filt_pivot_broccoli_dict = {}
#create a new dictionary to store the data in

#OrthoFinder
#create empty dictionary to hold the reversed Broccoli dictionary
pivot_orthofinder_dict = {}

for keys, values in orthofinder_dict.items():
	#iterate over the OrthoFinder dictionary via its keys and values
    for i in values:
		#iterate over the elements of the list in each value
		#and save to the dictionary in format pivot_dict[Query] = OG
        pivot_orthofinder_dict[i]=keys

#filter the dictionary to only include the proteins that meet the overlap threshold
filt_pivot_orthofinder_dict = {}
#create a new dictionary to store the data in

#PrtoeinOrtho
#create empty dictionary to hold the reversed Broccoli dictionary
pivot_proteinortho_dict = {}

for keys, values in proteinortho_dict.items():
	#iterate over the ProteinOrtho dictionary via its keys and values
    for i in values:
		#iterate over the elements of the list in each value
		#and save to the dictionary in format pivot_dict[Query] = OG
        pivot_proteinortho_dict[i]=keys

#filter the dictionary to only include the proteins that meet the overlap threshold
filt_pivot_proteinortho_dict = {}
#create a new dictionary to store the data in

#SonicParanoid
#create empty dictionary to hold the reversed Broccoli dictionary
pivot_sonicparanoid_dict = {}

for keys, values in sonicparanoid_dict.items():
	#iterate over the SonicParanoid dictionary via its keys and values
    for i in values:
		#iterate over the elements of the list in each value
		#and save to the dictionary in format pivot_dict[Query] = OG
        pivot_sonicparanoid_dict[i]=keys

#filter the dictionary to only include the proteins that meet the overlap threshold
filt_pivot_sonicparanoid_dict = {}
#create a new dictionary to store the data in


for query in query_ids:
	#iterate over the list of protein query IDs
	if query in pivot_broccoli_dict.keys():
		#find those protein query IDs that are in clustered by Broccoli
		#and save the query protein ID and associated OG to the filtered pivoted Broccoli dictionary
		filt_pivot_broccoli_dict[query] = pivot_broccoli_dict[query]
	if query in pivot_orthofinder_dict.keys():
		#find those protein query IDs that are in clustered by OrthoFinder
		#and save the query protein ID and associated OG to the filtered pivoted OrthoFinder dictionary
		filt_pivot_orthofinder_dict[query] = pivot_orthofinder_dict[query]
	if query in pivot_proteinortho_dict.keys():
		#find those protein query IDs that are in clustered by ProteinOrtho
		#and save the query protein ID and associated OG to the filtered pivoted ProteinOrtho dictionary
		filt_pivot_proteinortho_dict[query] = pivot_proteinortho_dict[query]
	if query in pivot_sonicparanoid_dict.keys():
		#find those protein query IDs that are in clustered by SonicParanoid
		#and save the query protein ID and associated OG to the filtered pivoted SonicParanoid dictionary
		filt_pivot_sonicparanoid_dict[query] = pivot_sonicparanoid_dict[query]


#convert the filtered pivoted dictionaries into dataframes & write out

#Broccoli
filt_broccoli_df = pd.DataFrame.from_dict(filt_pivot_broccoli_dict, orient='index')
#create the dataframe
filt_broccoli_df.reset_index(inplace=True)
#reset the index
#and rename the columns
filt_broccoli_df.rename(columns={'index': 'Query', 0: 'Broccoli_OG'}, inplace=True)

#write out to tab-separated text file
filt_broccoli_df.to_csv(broccoli_db, sep='\t', index=False)

#OrthoFinder
filt_orthofinder_df = pd.DataFrame.from_dict(filt_pivot_orthofinder_dict, orient='index')
#create the dataframe
filt_orthofinder_df.reset_index(inplace=True)
#reset the index
#and rename the columns
filt_orthofinder_df.rename(columns={'index': 'Query', 0: 'OrthoFinder_OG'}, inplace=True)

#write out to tab-separated text file
filt_orthofinder_df.to_csv(orthofinder_db, sep='\t', index=False)

#ProteinOrtho
filt_proteinortho_df = pd.DataFrame.from_dict(filt_pivot_proteinortho_dict, orient='index')
#create the dataframe
filt_proteinortho_df.reset_index(inplace=True)
#reset the index
#and rename the columns
filt_proteinortho_df.rename(columns={'index': 'Query', 0: 'ProteinOrtho_OG'}, inplace=True)

#write out to tab-separated text file
filt_proteinortho_df.to_csv(proteinortho_db, sep='\t', index=False)

#SonicParanoid
filt_sonicparanoid_df = pd.DataFrame.from_dict(filt_pivot_sonicparanoid_dict, orient='index')
#create the dataframe
filt_sonicparanoid_df.reset_index(inplace=True)
#reset the index
#and rename the columns
filt_sonicparanoid_df.rename(columns={'index': 'Query', 0: 'SonicParanoid_OG'}, inplace=True)

#write out to tab-separated text file
filt_sonicparanoid_df.to_csv(sonicparanoid_db, sep='\t', index=False)


#Part 6: Write out summary text file

with open(outfile_summary, "w") as outfile: 
	#open the summary file for writing
	outfile.write("The number of orthologous clusters in each pairwise comparison of two orthologous clustering" + "\n" +
			   "programs that met the desired threshold value of " + str(membership_threshold) + "% are listed below:" + "\n\n")
	for key in comparison_dict.keys():
		#iterate through the comparison dictionary via its keys
		#and write out the number of OGs that met that threshold
		outfile.write("For the " + key + " comparison," + "\n" + 
				"\t" + "the number of OGs that meet the threshold similarity is: " + str(len(set(comparison_dict[key][0]))) + "\n")
