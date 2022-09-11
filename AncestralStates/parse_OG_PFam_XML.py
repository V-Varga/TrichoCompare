# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_OG_PFam_XML.py
Date: 2022.05.19
Author: Virág Varga

Description:
	This program iterates over an indexing file created by parse_OG_PFams.py (or similar 
		file in in the same format: [OG_PROGRAM]_OG\tAssocPFams) with the aid of PFam 
		domain XML-formatted informational files created with retrieve_PFam_XML.py, 
		in order to create a large database in the format: 
			PFam_IDs\tSonicParanoid_OG\tPFamAccesion\tAlt_Name\tPFam_Description\tMolFunc_GO_ID\t
				MolFunc_GO_Desc\tBiolProc_GO_ID\tBiolProc_GO_Desc\tCellComp_GO_ID\tCellComp_GO_Desc

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas
	re

Procedure:
	1. Loading required modules; assigning command line arguments.
	2. Importing data into Pandas dataframe and restructuring the data.
	3. Extracting relevant PFam information from the PFam XML files into the
		PFam grouped dataframe.
	4. Writing out results in tab-delimited text file. If any dead or renamed
		PFam domains were encountered, these are written out to a file in the 
		format PFam1\nPFam2\nPFam3 etc.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is only partially user-defined. 

Usage
	./parse_OG_PFam_XML.py input_db data_path output_base
	OR
	python parse_OG_PFam_XML.py input_db data_path output_base

	Where the input_db is file in the format:
		[OG_PROGRAM]_OG\tAssocPFams
	Where data_path is a string input in quotation marks on the command line of the
		absolute path to the directory where the data PFam XML files are located.
		This should include a trailing backslash.
	Where output_base is the basename to be used for the output annotation 
		database. 

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python
import re #enables regex pattern matching


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "MetamonadCtrl_sec_3_SP__CountPivot_PFamIndex.txt"
data_path = sys.argv[2]
#data_path = "C:/Users/V/Documents/LundUni/Trich_Parab/Thesis_Work/Count/Test_Files/"

output_base = sys.argv[3]
#output_base = "MetamonadCtrl_sec_3_SP"
output_db = output_base + "__AnnotTable.txt"


#Part 2: Import data into Pandas dataframe & restructure

#read in the Metamonad database to a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0)
#then extract the name of the OG program
og_program = input_df.columns[0]

#group the dataframe according to PFam IDs
grouped_pfam_df = input_df.groupby('AssocPFams')[og_program].apply(list).reset_index(name=og_program)
#the OG IDs in the og_program column are grouped into lists according to which PFam IDs have been matched to them
#the new column of lists is named after the original OG program OG ID column name
grouped_pfam_df.rename(columns={'AssocPFams': 'PFam_IDs'}, inplace=True)
#for clarity, rename the PFam ID column
#then join all lists into comma- and space-separated strings
grouped_pfam_df[og_program] = grouped_pfam_df[og_program].apply(lambda x: ', '.join(map(str, x)))
#and add columns for the new data to be imported from the XML files
#ref: https://stackoverflow.com/questions/30926670/add-multiple-empty-columns-to-pandas-dataframe
pfam_df = grouped_pfam_df.reindex(columns=[*grouped_pfam_df.columns.tolist(), 
										   'PFamAccesion', 'Alt_Name', 'PFam_Description', 'MolFunc_GO_ID', 'MolFunc_GO_Desc', 
										   'BiolProc_GO_ID', 'BiolProc_GO_Desc', 'CellComp_GO_ID', 'CellComp_GO_Desc'], 
								  fill_value="-")


#Part 3: Extract relevant PFam information from the PFam XML files

#create empty list of problematic PFam domains
bad_pfams_list = []

for index, row in pfam_df.iterrows(): 
	#iterate over the pfam dataframe row by row (ie. by pfam IDs)
	key = row['PFam_IDs']
	#identify the PFam ID in the row and save it as variable key
	pfam_file = data_path + "PFam_" + key + ".xml"
	#define the file name and path
	if os.path.isfile(pfam_file):
		#ensure that the query PFam domain ID has an XML file associated with it
		with open(pfam_file, "r") as infile: 
			#open the PFam data xml file for reading
			if 'Dead family' in infile.read(): 
				#check if the PFam domain is considered dead
				#and if it is, let the user know
				print("Warning! The provided PFam ID, " + key + ", belongs to a dead family!")
				#and write the problematic PFam domain to the bad domain list
				bad_pfams_list.append(key)
			elif 'Renamed family' in infile.read(): 
				#check if the PFam domain has been renamed
				#and if so, let the user know
				print("Warning! The provided PFam ID, " + key + ", belongs to a renamed family!")
				#and write the problematic PFam domain to the bad domain list
				bad_pfams_list.append(key)
			else: 
				#if the PFam domain still exists, move forward with parsing the xml file
				#for some reason that I cannot figure out, the program enters the else statement
				#but does not proceed into the following for statement
				#so I am reopening the file here
				with open(pfam_file, "r") as infile:
					for line in infile:
						#iterate over the file line by line
						if line.startswith("  <entry"):
							#identify the line that contains basic PFam information
							#ref: https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
							pfam_accession_start = re.search('accession="(.*)" id', line)
							pfam_accession = pfam_accession_start.group(1)
							#extract the PFam accession number
							#and add it into the pfam_df
							#ref: https://stackoverflow.com/questions/25478528/updating-value-in-iterrow-for-pandas
							pfam_df.loc[index, 'PFamAccesion'] = pfam_accession
							next(infile)
							next(infile)
							#skip two lines to reach the line in the file with the alternative name
							alt_name = next(infile).strip()
							#extract the line contents without the endline character
							#and add the alternative name to the dataframe
							pfam_df.loc[index, 'Alt_Name'] = alt_name
						if line.startswith("    <comment>"):
							#identify the portion of the xml file right before the longform description
							next(infile)
							#skip one line
							#then extract teh description from the next line, minus the endline character
							pfam_desc = next(infile).strip()
							#add the description of the PFam domain to the dataframe
							pfam_df.loc[index, 'PFam_Description'] = pfam_desc
						if line.startswith('      <category name="process"'):
							#identify the part of the XML file where GO information is stored
							#specifically for the Biological Process GOs
							newline = next(infile)
							while newline.startswith("        <term go_id"):
								#iterate over the lines that have GO information stored in them
								go_id_start = re.search('go_id="(.*)">', newline)
								go_id = go_id_start.group(1)
								#extract the GO ID & add it to the PFam dataframe
								pfam_df.loc[index, 'BiolProc_GO_ID'] = go_id
								go_desc_start = re.search('">(.*)</term>', newline)
								go_desc = go_desc_start.group(1)
								#extract the GO description and add it to the PFam dataframe
								pfam_df.loc[index, 'BiolProc_GO_Desc'] = go_desc
								#redefine the next line as newline, to continue the while loop
								newline = next(infile)
						if line.startswith('      <category name="component"'):
							#identify the part of the XML file where GO information is stored
							#specifically for the Cellular Component GOs
							newline = next(infile)
							while newline.startswith("        <term go_id"):
								#iterate over the lines that have GO information stored in them
								go_id_start = re.search('go_id="(.*)">', newline)
								go_id = go_id_start.group(1)
								#extract the GO ID & add it to the PFam dataframe
								pfam_df.loc[index, 'CellComp_GO_ID'] = go_id
								go_desc_start = re.search('">(.*)</term>', newline)
								go_desc = go_desc_start.group(1)
								#extract the GO description and add it to the PFam dataframe
								pfam_df.loc[index, 'CellComp_GO_Desc'] = go_desc
								#redefine the next line as newline, to continue the while loop
								newline = next(infile)
						if line.startswith('      <category name="function"'):
							#identify the part of the XML file where GO information is stored
							#specifically for the Molecular Function GOs
							newline = next(infile)
							while newline.startswith("        <term go_id"):
								#iterate over the lines that have GO information stored in them
								go_id_start = re.search('go_id="(.*)">', newline)
								go_id = go_id_start.group(1)
								#extract the GO ID & add it to the PFam dataframe
								pfam_df.loc[index, 'MolFunc_GO_ID'] = go_id
								go_desc_start = re.search('">(.*)</term>', newline)
								go_desc = go_desc_start.group(1)
								#extract the GO description and add it to the PFam dataframe
								pfam_df.loc[index, 'MolFunc_GO_Desc'] = go_desc
								#redefine the next line as newline, to continue the while loop
								newline = next(infile)
	else: 
		#if the reference XML file for the PFam domain doesn't exist
		#write the following message to the stdout
		print("Warning! XML reference file for PFam domain " + key + " does not exist!")


#Part 4: Write out results

if len(bad_pfams_list) > 0:
	#if bad PFam domains were encountered during the parsing process
	#create an output file for these PFam domains
	output_bad = output_base + "__BadPFams.txt"
	with open(output_bad, "w") as outfile: 
		#open the output file for writing
		for i in bad_pfams_list: 
			#iterate over the elements in the bad PFam domains list
			#and write them to the file, 1 PFam domain per line
			outfile.write(i + "\n")


#write out main pfam dataframe to a tab-separated text file
pfam_df.to_csv(output_db, sep = '\t', index=False)
