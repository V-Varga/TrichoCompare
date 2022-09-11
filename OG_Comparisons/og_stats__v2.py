# -*- coding: utf-8 -*-
#!/bin/python
"""
Title: og_stats__v2.py
Date: 2022-03-15
Author: Virág Varga

Description:
	This program performs basic statistical tests on the parsed results of orthologous
		clustering software (OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli).

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	argparse
	pandas
	os
	statistics
	numpy
	matplotlib.pyplot
	check_og_duplicates.py

Procedure:
	1. Assignment of command-line arguments with argparse.
	2. Importing modules and parsing arguments. Running code specific to individual
		arguments.
			If -dupl argument is used, check_og_duplicates.py module will be called
			and run immediately.
	3. Main program code:
		- If necessary, removing species column from dataframe
		- Importing OG data into dictionary with format ortho_dict[OG_ID] = list_of_queries
		- Creating additional dictionary with format og_size_dict[OG_ID] = number_of_queries
		- Identifying number of OGs created by program
		- Identifying largest and smallest OGs (initially search for 10)
		- Identifying OGs with only 1 protein
		- Creating histogram showing distribustion of OG sizes
	4. Writing out results to text file.

Known bugs and limitations:
	- IMPORTANT: The location of the check_og_duplicates.py module is HARDCODED into 
		this script! If the files structure of the user is different, then they will 
		need to alter that portion of the -dupl argument parsing script.
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.
	- The input file used for the program must be an un-pivoted results file of either
		Broccoli, OrthoFinder, SonicParanoid, or ProteinOrtho, following the structure
		used by the parsers used previously in this workflow.
	- The program cannot accept multiple input files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Version: 
	This is version 2.0 of the program. The following changes were make to the script, 
		to increase ease of program use: 
		- The output file names were made reliant on input file names - this allows 
			the script to be run in the same directory on different parsed OG files 
			orginating from the same program, without overwriting results or requiring
			the names of results files to be manually altered. 
		- Made the script more flexible re: number of columns. Now filtered parsed data
			can still be processed, even if the formatting does not match the original
			parsed OG data file. 
		- Functionality was added to print a histogram of OG sizes to an image file. 

Usage:
	./og_stats__v2.py [-h] [-br] [-of] [-po] [-sp] [-dupl] [-v] INPUT_FILE
	OR
	python og_stats__v2.py [-h] [-br] [-of] [-po] [-sp] [-dupl] [-v] INPUT_FILE

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""

#################################   ARGPARSE   #######################################
import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program performs basic statistical tests on the parsed results of orthologous \
									clustering software (OrthoFinder, SonicParanoid, ProteinOrtho, Broccoli).')
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
	'-dupl', '--Duplicates',
	action='store_true',
	help = 'This argument will call and execute the check_OG_duplicates.py module program.'
	)
	#the '-dupl' flag will check the parsed results file for duplicates using the check_OG_duplicates.py script module
parser.add_argument(
	#'-i', '--input',
	#the above line of code is left in as further clarification of this argument
	dest='input_file',
	metavar='INPUT_FILE',
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
import os #allows access to the file system
import statistics #allows calculation of statistics in Python
import numpy as np #allows straightforward manipulation of dataframes in Python
import matplotlib.pyplot as plt #enable plotting in Python


#designate input file name as variable
infile = args.input_file.name


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
	og_stats_outfile = out_full + "__OG_stats.txt"

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
	og_stats_outfile = out_full + "__OG_stats.txt"

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
	og_stats_outfile = out_full + "__OG_stats.txt"

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
	og_stats_outfile = out_full + "__OG_stats.txt"

if args.Duplicates:
	#if -dupl argument is called
	cmd = "python ../../Scripts/check_OG_duplicates.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the yLoc_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)


#################################   Main Program   ######################################


#Initial setup

#remove 3rd column from Pandas dataframe if necessary 
#needed for original parsed results of OrthoFinder, ProteinOrtho & SonicParanoid
col_num = len(ortho_df.columns)
#count number of columns
if col_num == 3:
	#select dataframes with 3 columns
	#remove middle column with species information
	ortho_df.drop(ortho_df.columns[1], axis=1, inplace=True)


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


#How many clusters are there (per program)?

og_number = ortho_df[og_col].nunique()
#nunique() counts the number of unique occurrences in the selected column


#Average number of proteins per cluster

#create an empty dictionary to populate with the length data
og_size_dict = {}

for key in ortho_dict.keys():
	#iterate through the ortho_dict dictionary by its keys
	length_og = len(ortho_dict[key])
	#save the length of each list of proteins (per OG) to variable length_og
	og_size_dict[key] = length_og
	#populate the og_size_dict dictionary using the OG IDs as the keys and the OG sizes as values

#save the lengths of the OGs to a list
#note that OG ID information is no longer attached to this data
og_size = list(og_size_dict.values())

#calculate the average OG size, and save the value to variable avg_prots_num
avg_prots_num = statistics.mean(og_size)
#calculate the median OG size, and save the value to variable med_prots_num
med_prots_num = statistics.median(og_size)


#10 largest & 10 smallest clusters, with how many proteins are in these.

#get the 10 largest OGs in the og_size list
#ref: https://stackoverflow.com/questions/13070461/get-indices-of-the-top-n-values-of-a-list
top_10_idx = np.argsort(og_size)[-10:]
#save the indices of those sizes to a variable
top_10_values = [og_size[i] for i in top_10_idx]
#get the actual values that those indices correspond to out of the og_size list

#ensure no duplicate values
set_top_10_values = set(top_10_values)

#create an empty list to hold the OG IDs of the largest OGs
largest_OGs = []

#loop through values of the og_size_dict dictionary to find the OGs that correspond to those sizes
for key, value in og_size_dict.items():
	#loop through the items in the dictionary by both keys & values
	for size in set_top_10_values:
		#loop through the members of the top_10_values list showing largest OG sizes
		if value == size:
			#if the OG length matches in the dictionary and the list
			#append the key associated with that value (ie. Query ID) to the largest_OGs list
			largest_OGs.append(key)


#get the 10 smallest OGs in the og_size list
bottom_10_idx = np.argsort(og_size)[:10]
#save the indices of those sizes to a variable
bottom_10_values = [og_size[i] for i in bottom_10_idx]

#ensure no duplicate values
set_bottom_10_values = set(bottom_10_values)

#create an empty list to hold the OG IDs of the smallest OGs
smallest_OGs = []

#loop through values of the og_size_dict dictionary to find the OGs that correspond to those sizes
for key, value in og_size_dict.items():
	#loop through the items in the dictionary by both keys & values
	for size in set_bottom_10_values:
		#loop through the members of the top_10_values list showing largest OG sizes
		if value == size:
			#if the OG length matches in the dictionary and the list
			#append the key associated with that value (ie. Query ID) to the largest_OGs list
			smallest_OGs.append(key)


#Are there orthologous groups with only 1 protein? If so, how many?

#create empty list for protein query IDs in unique OG
lonely_OGs = []

#look through set_bottom_10_values to see if any of them has a length of 1
if 1 in set_bottom_10_values:
	#if the number 1 is found in the set
	for key, value in og_size_dict.items():
		#loop thorugh the og_size_dictionary to find the places where the value is 1
		if value == 1:
			#where the size of the OG is 1 protein query, save the query ID to a list
			lonely_OGs.append(key)


#Create histogram showing distribustion of OG sizes

#create an empty list to store OG sizes
size_list = []

#loop over the OG size dictionary to extract the OG sizes
for key in og_size_dict.keys():
	#iterate over the OG size dictionary via its keys
	#and save the associated values to the size list
	size_list.append(og_size_dict[key])

#create a histogram from the OG size data
og_size_hist = plt.hist(size_list, bins = 200)

#define the x-axis label of the plot
plt.xlabel("Orthologous Cluster Size (integers)")
#define the y-axis label of the plot
plt.ylabel("Frequency of Cluster Size")
#define the title of the plot
plt.title("Distribution of Orthologous Cluster Sizes")

#use input file name as basis for histogram output file name
histogram_name = out_full + "__OG_stats_histogram.png"
#print resulting histogram to png file
plt.savefig(histogram_name, dpi=500)
#plt.show()


#Writing out the results file

with open(og_stats_outfile, "w") as outfile:
	#open the assigned outfile for writing
	#first, calrify the program that the data comes from (so the information is inside the file, too)
	outfile.write(prog_id + " parsed results file was given as input." + "\n" +
			   "The results of the analysis can be found below:" + "\n\n")
	#write out the number of OGs identified by the program
	outfile.write("The " + prog_id + " program generated " + str(og_number) + " orthologous clusters." + "\n")
	#write the average/mean and median sizes of the OGs identified by the program
	outfile.write("There were on average " + str(avg_prots_num) + " per orthologous cluster, with a median of " + str(med_prots_num) + "." + "\n")
	if len(largest_OGs) == 10:
		#write out the 10 largest OGs and their members
		outfile.write("The largest OG had " + str(top_10_values[9]) + " members." + "\n" +
				"The 10 largest clusters, their length and protein members are as follows: " + "\n")
	if len(largest_OGs) > 10:
		#write out the 10 largest OGs and their members
		outfile.write("The largest OG had " + str(top_10_values[9]) + " members." + "\n" +
				"The " + str(len(largest_OGs)) + " largest clusters, their length and protein members are included below." + "\n" +
				"Note that this program searches initially for the 10 largest OGs. More are reported here because multiple OGs had a length equivalent to the 'largest'." + "\n")
	for key in ortho_dict.keys():
		#looping through the ortho_dict dictionary keys
		for cluster in largest_OGs:
			#looping through the OG IDs of the largest clusters
			if cluster == key:
				#when a member of the list matches a dictionary key
				#convert the list in the dictionary value of query IDs into a string
				joined_OG_list = ",".join(ortho_dict[key])
				#write out the OG ID as well as the protein query IDs associated with it to the outfile
				outfile.write(cluster + "\t" + "size = " + str(len(ortho_dict[key])) + "\n\t" + joined_OG_list + "\n")
	if len(smallest_OGs) == 10:
		#write out the 10 smallest OGs and their members
		outfile.write("The smallest OG had " + str(bottom_10_values[0]) + " members." + "\n" +
				"The 10 smallest clusters, their length and protein members are as follows: " + "\n")
	if len(smallest_OGs) > 10:
		#write out the 10 smallest OGs and their members
		outfile.write("The smallest OG had " + str(bottom_10_values[0]) + " members." + "\n" +
				"The " + str(len(smallest_OGs)) + " smallest clusters, their length and protein members are included below." + "\n" +
				"Note that this program searches initially for the 10 smallest OGs. More are reported here because multiple OGs had a length equivalent to the 'smallest'." + "\n")
	for key in ortho_dict.keys():
		#looping through the ortho_dict dictionary keys
		for cluster in smallest_OGs:
			#looping through the OG IDs of the smallest clusters
			if cluster == key:
				#when a member of the list matches a dictionary key
				#convert the list in the dictionary value of query IDs into a string
				joined_OG_list = ",".join(ortho_dict[key])
				#write out the OG ID as well as the protein query IDs associated with it to the outfile
				outfile.write(cluster + "\t" + "size = " + str(len(ortho_dict[key])) + "\n\t" + joined_OG_list + "\n")
	outfile.write("There are " + str(len(lonely_OGs)) + " orthologous clusters with only 1 protein." + "\n")
	if len(lonely_OGs) > 0:
		#if there are any OGs with only 1 protein member, then enter this loop
		#write out the OG IDs, as well as the protein query IDs of these "clusters"
		outfile.write("The orthologous clusters with only one member and their associated member protein are: " + "\n")
		for key in ortho_dict.keys():
			#loop through the keys of the ortho_dict dictionary
			for element in lonely_OGs:
				#loop through the members of the lonely_OGs list of OG IDs
				if element == key:
					#when a member of the lonely_OGs list matches a key in the ortho_dict dictionary
					#convert the list in the dictionary value of the query ID into a string
					joined_OG_list = "".join(ortho_dict[key])
					#write out the OG ID as well as the associated protein query ID
					outfile.write(element + ": " + joined_OG_list + "\n")
