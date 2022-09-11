# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: retrieve_PFam_XML.py
Date: 2022.05.18
Author: Virág Varga

Description:
	This program queries the PFam Database's RESTful interface in order to extract
		the XML-formatted data files containing the annotation available for that 
		PFam domain ID. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	subprocess

Procedure:
	1. Loading required modules; assigning command line argument.
	2. Querying the desired data from the PFam RESTful interface.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file names are based on the PFam domain ID names.

Usage
	./retrieve_PFam_XML.py pfam_list
	OR
	python retrieve_PFam_XML.py pfam_list

	Where pfam_list must be a query PFam domain ID list in one of the following formats:
		- Singular PFam domain ID provided on the command line
		- Comma-separated list of PFam domain IDs provided on the command line (ex. `ID_1,ID_2,ID_3`)
		- File containing list of PFam domain IDs in format: ID1\nID2 etc.

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import subprocess #allows execution of bash commands from Python


#assign command line argument & load input PFam domain list
pfam_list = sys.argv[1]
#pfam_list = "PAS_9"
#pfam_list = "MetamonadCtrl_sec_3_SP__CountPivot_PFamList.txt"
#import the PFam domain query list
if os.path.isfile(pfam_list):
	#if the input selection of PFam domain IDs is a file
	with open(pfam_list, 'r') as infile:
		#open the file for reading
		#and save the contents of the file (should be a column of PFam domain query IDs) to a list
		query_list = [line.rstrip('\n') for line in infile]
		#eliminate duplicates
		query_list = list(set(query_list))
else:
	#if the input protein query ID list is a string instead of a text file
	#save the contents of the comma-separated string to a list variable
	query_list = pfam_list.split(",")
	#eliminate duplicates
	query_list = list(set(query_list))


#Part 2: Query the desired data from the PFam RESTful interface

for i in query_list: 
	#iterate over the list of PFam domain IDs
	outfile = "PFam_" + i + ".xml"
	#determine output file name
	if not os.path.isfile(outfile):
		#ensure that the query PFam domain ID has not already been queried in a previous session
		#if the file does not already exist, continue on to querying
		#ref: https://pfam-docs.readthedocs.io/en/latest/restful-interface.html
		query_address = "https://pfam.xfam.org/family/" + i 
		#note that unlike in the documentation, I removed the single quotes around the web address
		#this is due to the way that `curl` interprets arguments
		#ref: https://stackoverflow.com/questions/70200540/python-subprocess-not-passing-curly-brackets-as-arguments-or-a-problem-with-dou
		#ref: https://docs.python.org/3/library/subprocess.html
		bashCommand = "curl -LH 'Expect:' -F output=xml " + query_address + " --output " + outfile
		bash_list = bashCommand.split()
		subprocess.run(bash_list, capture_output=True)
