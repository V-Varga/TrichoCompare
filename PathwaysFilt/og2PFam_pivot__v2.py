# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og2PFam_pivot__v2.py
Date: 2022.04.18
Author: Virág Varga

Description:
	This program uses the Metamonad database, or a filtered copy of the same containing
		all PFam and desired OG information to create a table linking all OGs to their
		associated PFam domains.
		The PFam colum used is: pfamEN_hit

List of functions:
	concat (Source: IPRpivot.py, Courtney Stairs)

List of standard and non-standard modules used:
	sys
	pandas
	os
	collections.Counter

Procedure:
	1. Importing necessary modules & function; determining inputs & outputs.
	2. Importing database into Pandas and extracting relevant columns.
	3. Pivoting the dataframe and removing unnecessary data.
	4. Creating a dataframe with count data on PFams per OG. 
	5. Creating a simple dataframe showing OGs and associated PFams.
	6. Writing out the results to two tab-separated text files.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a version of the Metamonad database which
		includes both PFam and OG assignments. The PFam column used by this program
		is pfamEN_hit.
	- The output file names are not user-defined.

Version:
	This program can be considered Version 2.0 of the og2PFam_pivot.py program.
		The funcitonality of the orginal program has been expanded to account for the
		larger, more complex dataset of the Metamonad database.

Usage
	./og2PFam_pivot__v2.py input_db og_col
	OR
	python og2PFam_pivot__v2.py input_db og_col

	Where og_col should be the name of the OG column for which the PFam domains should
		be aggregated.

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules & function, determine inputs & outputs

#import necessary modules
import sys #allow execution of code from the command line
import pandas as pd #facilitates manipulation of dataframes in Python
import os #allow access to computer files
from collections import Counter #enables easy counting of elements


#make function for joining strings with ','
#Source: IPRpivot.py, Courtney Stairs
def concat(str):
	return ','.join(str)


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "Metamonada_pred_OG_DB__200prots.txt"

og_col = sys.argv[2]
#og_col = "SonicParanoid_OG"


#output_db will contain information on PFams associated with each OG
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#first extract base file name
#and then define the output file names
output_db = "OGs2PFams_" + og_col + ".txt"
output_counts = "OGs2PFams_" + og_col + "_Counts.txt"


#Part 2: Import database into Pandas, extract relevant columns

#read in the input OG database file, assigning the first row as a header row
input_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)
# sys:1: DtypeWarning: Columns (6,7,27,31) have mixed types.Specify dtype option on import or set low_memory=False.


#select the columns that will be used to create the pivot table
pfam_og_RAW_df = input_df[['pfamEN_hit', og_col]].copy()
#copy those columns only into a new dataframe


#Part 3: Pivot the dataframe and remove unnecessary data

#pivot the table
pfam_og_WIP_df = pd.pivot_table(pfam_og_RAW_df, index = og_col, aggfunc=concat).reset_index()
#use `.reset_index()` to pull the OG ID column out of the index

#the above method leaves extraneous whitespace, which needs to be removed
pfam_og_WIP_df['pfamEN_hit'] = pfam_og_WIP_df['pfamEN_hit'].str.replace(' ', '')
#then remove the row of the dataframe containing the "OG" of "-"
pfam_og_df = pfam_og_WIP_df[pfam_og_WIP_df[og_col] != "-"].copy()
#use `.copy()` to allow manipulation of the new dataframe


#Part 4: Create dataframe with count data on PFams

#create version of dataframe with count data (ie. non-set)
pfam_count_df = pfam_og_df.copy()
pfam_count_df['pfamEN_hit'] = pfam_count_df['pfamEN_hit'].apply(lambda x: ','.join(sorted(x.split(','))))
#now remove non-hits from the dataframe
pfam_count_df['pfamEN_hit'] = pfam_count_df['pfamEN_hit'].str.replace('-,', '')
#also remove OGs without PFam hits
pfam_count_prep_df = pfam_count_df[pfam_count_df['pfamEN_hit'] != "-"].copy()
pfam_count_prep_df['pfamEN_hit'] = pfam_count_prep_df['pfamEN_hit'].apply(lambda x: x.split(','))
pfam_count_prep_df.set_index(og_col, inplace=True)


#create an empty dictionary to store the data
pfam_count_dict = {}

for index, row in pfam_count_prep_df.iterrows(): 
	#iterate over the dataframe row by row
	og_pfam_list = row[0]
	#save the list of PFam hits to a variable
	og_pfam_counts = str(dict(Counter(og_pfam_list)))
	#save the results of the PFam counts to a variable as a string
	og_pfam_counts = og_pfam_counts.replace('{', '')
	#remove the {braces} currently in the string
	og_pfam_counts = og_pfam_counts.replace('}', '')
	#remove spaces from the string
	og_pfam_counts = og_pfam_counts.replace(' ', '')
	#remove the single quotes from inside the strin
	#need to use "\" character to prevent EOF parsing error
	og_pfam_counts = og_pfam_counts.replace('\'', '')
	#now populate the dictionary
	pfam_count_dict[index] = og_pfam_counts

#convert dictionary back to dataframe
final_pfam_count_df = pd.DataFrame.from_dict(pfam_count_dict, orient='index', columns=['pfamEN_hits_Counts'])
#and pull the OG data out of the index
final_pfam_count_df.reset_index(inplace=True)
#before renaming it according to the OG program being used
final_pfam_count_df.rename(columns={'index': og_col}, inplace=True)


#Part 5: Create simple dataframe showing OGs and associated PFams

#aggregate PFam IDs into a comma-separated string, and remove duplicate PFam hits
pfam_og_df['pfamEN_hit'] = pfam_og_df['pfamEN_hit'].apply(lambda x: ','.join(sorted(list(set(x.split(','))))))

#remove "-" "hits" from the pfamEN_hits column of data
pfam_og_df['pfamEN_hit'] = pfam_og_df['pfamEN_hit'].str.replace('-,', '')
#also remove OGs without PFam hits
final_pfam_og_df = pfam_og_df[pfam_og_df['pfamEN_hit'] != "-"].copy()


#Part 6: Write out results

#write out count data to tab-separated text file
final_pfam_count_df.to_csv(output_counts, sep='\t', index=False)

#write out OGs to PFams simplified data to a tab-separated text file
final_pfam_og_df.to_csv(output_db, sep='\t', index=False)
