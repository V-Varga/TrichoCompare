# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: link_data_files.py
Date: 2022-03-07
Author: Virág Varga

Description:
	This program creates symbolic links (symlinks) between parsed data files stored
		in a per-analysis program structure, to to directories specific to the
		strain or species being analyzed.
	This linking is necessary as preparation for the construction of species-specific
		databases with annotations on each protein query.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	subprocess

Procedure:
	1. Loading required modules; defining inputs as command line
		arguments; loading the contents of the reference file as a list.
	2. Matching the substrings contained in the reference file to the subdirectory
		and results file names. When matches are found, creating a symlink from 
		the source file to the destination directory. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the following formatting for inputs: 
		-> Source and distination directories must be given without a trailing 
			forwardslash ("/") at the end of the path. The full path must be given 
			as the argument, relative paths will not work. 
		-> The input reference file must contain substrings to search for in file
			and directory names in the format of one substring per line. 

Usage
	./link_data_files.py parsed_data_dir species_file species_dir
	OR
	python link_data_files.py parsed_data_dir species_file species_dir

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, files; determine command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allows access to the files and directories of the computer/system
import subprocess #allows the running of bash commands from within python

#assign command line arguments; load input and output files
parsed_data_dir = sys.argv[1]
#parsed_data_dir = "TEST_dir/Parsed_dir"
species_file = sys.argv[2]
#species_file = "TEST_dir/Ref_file.txt"
species_dir = sys.argv[3]
#species_dir = "TEST_dir/Assembly_dir"

#easy part first - import the reference file
with open(species_file, "r") as infile:
	#open the reference file for reading
	species_list = infile.read().splitlines()
	#read the contents of the file into a list, and remove end-line characters ("\n")


#Part 2: Loop through directories of analyzed data and symlink the appropriate files

for subdir, dirs, files in os.walk(parsed_data_dir):
	#iterate over the files contained in the subdirectories of the parsed data directory
	for file in files:
		#specifically iterate over the files themselves
		for species in species_list:
			#iterate over the list of species/strains
			if species in file:
				#identify places where the species/strain ID is a substring of a results file
				symlink_path = species_dir + "/" + species
				#define the destination path of the symlink as a string
				source_path = subdir + "/" + file
				#define the source file path as a string
				bash_cmd = "ln -s " + source_path + " " + symlink_path
				#define the bash command to be executed as a string
				#for the next two lines, ref: https://stackoverflow.com/questions/4256107/running-bash-commands-in-python
				process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
				output, error = process.communicate()
				#execute the bash command defined above
