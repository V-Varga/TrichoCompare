# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_ALE_Nodes_GFam_Annot.py
Date: 2022.09.13
Author: Virág Varga
With gratitude to: Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil)

Description:
	This program iterates over a file containing data on the types of events taking place
		at each node per OG, and consolidates it into a summary data table showing the 
		total number of each type of event occurring at each node with respect to OGs.
	The data to be used as input should be dreived from the results of the ALE program, 
		after the initial parsing of the data with the parse_ALE_Events.py script and subsequent
		consolidation, or a filtered version of the same (via the parse_ALE_Annotations.py
		program in this workflow). 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; assigning command-line arguments.
	2. Importing the contents of the DTL events data table into a Pandas dataframe.
		Optionally, create a indexing dictionary to enable conversion of nodes in 
			the dataframe to those used in R. 
	3. Simplifying the database to match the structure of the Count results. 
	4. Iterate over the database, converting the protein-based annotation to OG-based
	5. Writing out the results to a tab-separated text file. Optionally, converting 
		the dataframe to the R node format & writing out. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but is instead based on the input
		file name.  

Citation: 
	This program is a based off of the ALE parsing programs used in the ALE-pipeline 
		program written by Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil), 
		which can be found here: https://github.com/maxemil/ALE-pipeline

Version: 
	This is can be considered an alternate version of the parse_ALE_Nodes_GFam.py program,
		which is itself an alternate version of the parse_ALE_Nodes__v2.py program. 
		This version of the program outputs the OG-formatted ALE data (vs. the protein-based
		original form of the data), without summarizing per node, thus keeping the node IDs
		intact for perusal. 

Usage
	./parse_ALE_Nodes_GFam_Annot.py input_events [R_indexing_file]
	OR
	python parse_ALE_Nodes_GFam_Annot.py input_events [R_indexing_file]

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_events = sys.argv[1]
#input_events = "OF_Mito3__Events_Final__EXCERPT.txt"

#determine output file name based on input file name
base = os.path.basename(input_events)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_db = out_full + "_GFam.txt"

if len(sys.argv) == 3: 
	#if the optional indexig file for node number conversion
	#to match the numbering system internal to R
	#is provided, then identify the indexng file
	R_indexing_file = sys.argv[2]
	#R_indexing_file = "ALE_2R_Indexing.txt"
	#and define a new output file
	output_db_R = out_full + "_R_GFam.txt"


#Part 2: Import the contents of the DTL events data table into a Pandas dataframe
events_df = pd.read_csv(input_events, sep = '\t', header=0)
#the file is a tab-delimited text file, so the separator needs to be specified


if 'output_db_R' in vars(): 
	#check to see whether the option R-formatted node file has been requested
	#if so, create a an empty dictionary to store the node indexing information
	#ref: https://stackoverflow.com/questions/53961659/python-how-to-convert-txt-file-two-columns-to-dictionary-elements
	indexing_dict = {}
	with open(R_indexing_file, "r") as infile: 
		#open the indexing file for reading
		next(infile)
		#and skip the first line of the file  since it's a header line
		for line in infile: 
			#read through the indexing file line by line
			value, key = line.strip().split() 
			#split each line into two elements based on the tab placement
			#and remove the newline character at the end of the line
			#then save the node values to the indexing dictionary
			indexing_dict[key] = (value) 


#Part 3: Simplify the database to match the structure of the Count results

#first copy the relevant columns to a new dataframe
count_df = events_df[['Gene_Family', 'Node', 'Losses', 'Originations', 'Copies']].copy()
#note that the concepts of duplications and transfers
#are not relevant when discussing gene families, instead of proteins
#losses are not strictly speaking meaningful, either, 
#but we'll deal with that in a moment
#ALE doesn't predict multiple originations per OG, so that one will be fine

#round the values in the data columns
count_df = count_df.round({'Losses': 0, 'Originations': 0, 'Copies': 0})
#ref: https://stackoverflow.com/questions/31247763/round-float-columns-in-pandas-dataframe

#convert the Node column to string format for easier parsing
count_df = count_df.astype({"Node": str})
#ref: https://www.stackvidhya.com/pandas-change-column-type/#:~:text=Pandas%20Change%20Column%20Type%20To%20String,-In%20this%20section&text=You%20can%20use%20it%20by,be%20converted%20to%20String%20format.


#create dictionary in format: {Node_Number: Previous_Node_Number}
#this will be used to determine gains and losses of OGs across the tree
phylo_dict = {"Anaeramoeba-lanta-160522": 49, 
			  "BM-newprots-may21.anaeromoeba": 45, 
			  "BS-newprots-may21.anaeromoeba": 32, 
			  "Carpediemonas-membranifera.PRJNA719540": 33, 
			  "Dientamoeba-fragilis.43352.aa": 47, 
			  "EP00701-Giardia-intestinalis": 34, 
			  "EP00703-Trepomonas-sp-PC1": 35, 
			  "EP00708-Paratrimastix-pyriformis": 36, 
			  "EP00764-Aduncisulcus-paluster": 58, 
			  "EP00766-Chilomastix-caulleryi": 37, 
			  "EP00767-Chilomastix-cuspidata": 37, 
			  "EP00768-Dysnectes-brevis": 55, 
			  "EP00769-Ergobibamus-cyprinoides": 33, 
			  "EP00770-Monocercomonoides-exilis": 38, 
			  "EP00771-Trimastix-marina": 36, 
			  "EP00792-Barthelona-sp-PAP020": 60, 
			  "Giardia-intestinalis.PRJNA1439": 34, 
			  "Giardia-muris.PRJNA524057": 50, 
			  "GiardiaDB-GintestinalisADH": 39, 
			  "GiardiaDB-GintestinalisBGS": 40, 
			  "GiardiaDB-GintestinalisBGS-B": 40, 
			  "GiardiaDB-GintestinalisEP15": 41, 
			  "Histomonas-meleagridis.135588.aa": 42, 
			  "Histomonas-meleagridis.PRJNA594289": 42, 
			  "Kipferlia-bialata.PRJDB5223": 56, 
			  "Pentatrichomonas-hominis.5728.aa": 43, 
			  "SC-newprots-may21.anaeromoeba": 32, 
			  "Spironucleus-salmonicida.PRJNA60811": 35, 
			  "Tetratrichomonas-gallinarum.5730.aa": 43, 
			  "Trichomonas-vaginalis-GenBank.PRJNA16084": 44, 
			  "Trichomonas-vaginalis-RefSeq.G3": 44, 
			  "Tritrichomonas-foetus.PRJNA345179": 51, 
			  32: 45, 
			  33: 59, 
			  34: 39, 
			  35: 54, 
			  36: 38, 
			  37: 57, 
			  38: 61, 
			  39: 41, 
			  40: 46, 
			  41: 46, 
			  42: 47, 
			  43: 48, 
			  44: 48, 
			  45: 49, 
			  46: 50, 
			  47: 51, 
			  47: 51, 
			  48: 52, 
			  49: 53, 
			  50: 54, 
			  51: 52, 
			  52: 53, 
			  53: 62, 
			  54: 55, 
			  55: 56, 
			  56: 57, 
			  57: 58, 
			  58: 59, 
			  59: 60, 
			  60: 61, 
			  61: 62
			  #do not need to include node 62 as a key
			  #since the origin will not be undergoing the same style of analysis 
			  #as the other nodes in the tree
			  }

#convert all elements of the dictionary to strings
#ref: https://stackoverflow.com/questions/67600510/convert-all-the-values-in-a-dictionary-to-strings
for keys in phylo_dict:
	#iterated over the dictionary via its keys
	#and convert all elements of the dictionary to strings
	phylo_dict[keys] = str(phylo_dict[keys])
#strictly speaking, I could write fewer lines of code 
#if I individually put quotations around all of the numbers in the dictionary
#but this method is easier on my joints


#Part 4: Iterate over the database, converting the protein-based annotation to OG-based

#next, iterate over the database & convert protein loss to OG loss
for index, row in count_df.iterrows():
	#iterate through the dataframe row by row
	if row['Node'] != 62:
		#skip Node 62 (origin node) since there's nothing to compare to
			if row['Copies'] == 0: 
				#if the number of copies = 0, 
				#check to see if the OG was lost since the previous node
				for phylo_key in phylo_dict: 
					#iterate over the phylo_dict via its keys to obtain the parent node number
					if phylo_key == row['Node']: 
						#find the dictionary entry associated with the present node number
						prev_node = phylo_dict[phylo_key]
						#save the parent node number to the variable prev_node
						OG_ID = row['Gene_Family']
						#save the OG ID to a new variable
						#ref: https://thispointer.com/python-pandas-select-rows-in-dataframe-by-conditions-on-multiple-columns/
						filterinfDataframe = count_df[(count_df['Node'] == prev_node) & (count_df['Gene_Family'] == OG_ID) ]
						#filter out the portion of the count_df containing the previous node ID for that OG
						#and save that one line of the dataframe to a new "dataframe"
						if filterinfDataframe.iloc[0]['Copies'] > 0:  
							#if the parent node still had members of the OG
							prev_count = filterinfDataframe['Copies']
							#save the number of OG members at the parent node to a variable
							#use .iloc to get the value of the specific cell, 
							#since techinically this is still a dataframe
							#ref: https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
							#replace the value of losses at the search node 
							#with the number of OG members that existed at the parent node
							count_df.at[index, 'Losses'] = prev_count
			else: 
				#if the number of copies > 0
				#ref: https://stackoverflow.com/questions/13842088/set-value-for-particular-cell-in-pandas-dataframe-using-index
				#replace the value of Copies at the search node with 1
				#to show the presence of members of the OG at the node
				count_df.at[index, 'Copies'] = 1
				#note that this same procedure doesn't need to be repeated for originations
				#because there is never >1 origination per OG
				#but it does need to be repeated for the losses
				#since if the OG exists at a node, it hasn't been lost
				count_df.at[index, 'Losses'] = 0
	else: 
		#for the numbers at node 62 (the origin)
		if count_df.iloc[index]['Copies'] > 0: 
			#if the OG was present at the origin
			#replace the value of Copies at the origin with 1
			#to show the presence of members of the OG at the node
			count_df.at[index, 'Copies'] = 1
		if count_df.iloc[index]['Losses'] > 0: 
			#if the OG was "lost" at the origin
			#replace the value of Losses at the origin with 1
			#to show the "loss" of members of the OG at the node
			#airquotes used because this really shouldn't happen
			#if it does, it's an algorithmic error 
			#which should be kept in this output for clarity's sake
			count_df.at[index, 'Losses'] = 1
			#for the same reason, origination values should not be changed
			#there shouldn't be more than 1 origination
			#if there is, then the algorithm did something weird
			#and that's also important to know


#Part 5: Write out results to tab-separated text file

#node_summary_df.to_csv(output_db, sep = '\t', index=False)
count_df.to_csv(output_db, sep = '\t', index=False)

#optionally, convert the dataframe to the R node format & write out
if 'output_db_R' in vars(): 
	#check to see whether the option R-formatted node file has been requested
	#then use the dictionary to replace the ALE-derived node IDs 
	#with the R-generated node IDs
	#ref: https://sparkbyexamples.com/pandas/pandas-remap-values-in-column-with-a-dictionary-dict/#:~:text=Using%20Pandas%20DataFrame.-,replace(),regular%20expressions%20for%20regex%20substitutions.
	node_summary_df_R = count_df.replace({"Node": indexing_dict})
	#and write out the results to a tab-separated text file
	node_summary_df_R.to_csv(output_db_R, sep = '\t', index=False)
