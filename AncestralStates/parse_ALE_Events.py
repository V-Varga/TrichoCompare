# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: parse_ALE_Events.py
Date: 2022.06.24
Author: Virág Varga
Based on the work of: Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil)

Description:
	This program parses a *.ale.uml_rec file produced by the ALEml_undated program (part 
		of the ALE suite, which can be found here: https://github.com/ssolo/ALE), in
		order to output a text file with only the DTL events summarized in a tab-separated
		format, which can be used for further data parsing. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required module; assigning command-line argument.
	2. Parsing DTL events data from the ALE *.ale.uml_rec file into a tab-separated 
		output text file.  

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but is instead based on the input
		file name.  

Citation: 
	This program is a based off of the ALE parsing programs used in the ALE-pipeline 
		program written by Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil), 
		which can be found here: https://github.com/maxemil/ALE-pipeline
		I have taken inspiration from their methods of parsing the ALE data, as well as 
		adapted portions of their code, particularly the extractDTLevents.py script, 
		which can be found here: 
				https://github.com/maxemil/ALE-pipeline/blob/master/templates/extractDTLevents.py

Usage
	./parse_ALE_Events.py input_tree
	OR
	python parse_ALE_Events.py input_tree
	
	Where the input_tree file should be a *.ale.uml_rec file produced be the ALEml_undated 
		program, which is part of the ALE suite. 

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary module; assign command-line argument

#import necessary modules
import sys #allows assignment of command line arguments


#assign command line arguments; load input and output files
input_tree = sys.argv[1]
input_tree = "SP_Mito3__OG_2636_MSA_IQ.names.ufboot.ale.uml_rec"

#determine output file name based on input file name
input_name_list = input_tree.split(".")
#save contents of the name to a list
gene_family_basename = input_name_list[0]
#save the file basename
#and the gene family ID
gene_family_ID = gene_family_basename.replace("_MSA_IQ", "")
#and finally, designate the output file name
output_events = gene_family_basename + "_ALE.events.txt"


#Part 2: Parsing DTL events into a data file
#This portion of code is adapted from the extractDTLevents.py script of the ALE-pipeline
#Original script: https://github.com/maxemil/ALE-pipeline/blob/master/templates/extractDTLevents.py

with open(input_tree, "r") as f, open(output_events, 'w') as outhandle:
	#open the input ALE results file fro reading; and the events parsing output file for writing
	outhandle.write("Gene_Family" + "\t" + "Node" + "\t" + "Duplications" + "\t" + "Transfers"+ "\t" + 
				 "Losses" + "\t" + "Originations" + "\t" + "Copies" + "\n")
	#write out column headers for the data that will go into the outfile
	for line in f:
		#iterate over the input file line by line
		if any([line.startswith(x) for x in ['S_terminal_branch', 'S_internal_branch']]):
			#find the lines of the file that have the DTL data table
			line = line.split()
			#split the line into a list, based on the tab placement
			#and print those portions, along with the gene family ID, to a tab-separated text file
			#print("\t".join([gene_family_ID] + line[1:]), file=outhandle)
			#the above raised a syntax error when I tried to run it on Uppmax
			out_string = "\t".join([gene_family_ID] + line[1:])
			outhandle.write(out_string + "\n")
