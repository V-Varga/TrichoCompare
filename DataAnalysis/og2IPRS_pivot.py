# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: og2IPRS_pivot.py
Date: 2022.08.14
Author: Virág Varga

Description:
	This program uses the Metamonad database, or a filtered copy of the same containing
		all IPRScan annotations and desired OG information to create tables linking all 
		OGs to their associated IPRScan accession numbers and GO annotations.
		The columns used are: iprS_InterPro_annotations-accession & iprS_GO_annotations

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
	3. Pivoting the dataframes and removing unnecessary data.
	4. Creating dataframes with count data on IPRS accession numbers and GO
		annotations per OG. 
	5. Creating a simple dataframes showing OGs and associated IPRS and GO 
		annotations.
	6. Writing out the results to tab-separated text files.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a version of the Metamonad database which
		includes both IPRS and OG assignments. The IPRS columns used by this program
		are iprS_InterPro_annotations-accession & iprS_GO_annotations.
	- The output file names are not user-defined.
	- IMPORTANT: The parsing of the GO terms is somewhat buggy! If only 1 GO term 
		is returned for a query, it will return as a "list" of characters instead
		of as a proper GO term. This is something that I hope to fix as I have time.
		Something similar to what was used to parse the IPRS data should hopefully work.

Version:
	This program is based off of the og2PFam_pivot__v2.py program. It has been modified 
		to extract IPRScan data from the Metamonad database, instead of the PFam 
		annotations. 

Usage
	./og2IPRS_pivot.py input_db og_col
	OR
	python og2IPRS_pivot.py input_db og_col

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


#output versions will contain information from IPRS associated with each OG
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#first extract base file name
#and then define the output file names
#first the IPRS accession databases
output_iprs = "OGs2IPRS_" + og_col + ".txt"
output_iprs_counts = "OGs2IPRS_" + og_col + "_Counts.txt"
#then the GO annotation databases
output_go = "OGs2GOs_" + og_col + ".txt"
output_go_counts = "OGs2GOs_" + og_col + "_Counts.txt"


#Part 2: Import database into Pandas, extract relevant columns

#read in the input OG database file, assigning the first row as a header row
input_df = pd.read_csv(input_db, sep = '\t', header=0, low_memory=False)
# sys:1: DtypeWarning: Columns (6,7,27,31) have mixed types.Specify dtype option on import or set low_memory=False.


#select the columns that will be used to create the pivot tables
iprs_og_RAW_df = input_df[['iprS_InterPro_annotations-accession', og_col]].copy()
#copy those columns only into a new dataframe
go_og_RAW_df = input_df[['iprS_GO_annotations', og_col]].copy()


#Part 3: Pivot the dataframes and remove unnecessary data

#pivot the tables
iprs_og_WIP_df = pd.pivot_table(iprs_og_RAW_df, index = og_col, aggfunc=concat).reset_index()
#use `.reset_index()` to pull the OG ID column out of the index
go_og_WIP_df = pd.pivot_table(go_og_RAW_df, index = og_col, aggfunc=concat).reset_index()

#the above method leaves extraneous whitespace, which needs to be removed
iprs_og_WIP_df['iprS_InterPro_annotations-accession'] = iprs_og_WIP_df['iprS_InterPro_annotations-accession'].str.replace(' ', '')
#then remove the row of the dataframe containing the "OG" of "-"
iprs_og_df = iprs_og_WIP_df[iprs_og_WIP_df[og_col] != "-"].copy()
#use `.copy()` to allow manipulation of the new dataframe
#doing it again for the GO data...
go_og_WIP_df['iprS_GO_annotations'] = go_og_WIP_df['iprS_GO_annotations'].str.replace(' ', '')
#then remove the row of the dataframe containing the "OG" of "-"
go_og_df = go_og_WIP_df[go_og_WIP_df[og_col] != "-"].copy()
#use `.copy()` to allow manipulation of the new dataframe


#Part 4: Create dataframes with count data on annotations

#create version of dataframe with count data (ie. non-set)
#starting with the IPR accession data
iprs_count_df = iprs_og_df.copy()
iprs_count_df['iprS_InterPro_annotations-accession'] = iprs_count_df['iprS_InterPro_annotations-accession'].apply(lambda x: ','.join(sorted(x.split(','))))
#now remove non-hits from the dataframe
iprs_count_df['iprS_InterPro_annotations-accession'] = iprs_count_df['iprS_InterPro_annotations-accession'].str.replace('-,', '')
#also remove OGs without PFam hits
iprs_count_prep_df = iprs_count_df[iprs_count_df['iprS_InterPro_annotations-accession'] != "-"].copy()
iprs_count_prep_df['iprS_InterPro_annotations-accession'] = iprs_count_prep_df['iprS_InterPro_annotations-accession'].apply(lambda x: x.split(','))
iprs_count_prep_df.set_index(og_col, inplace=True)
#and now do all the same for the GO annotations
go_count_df = go_og_df.copy()
go_count_df['iprS_GO_annotations'] = go_count_df['iprS_GO_annotations'].apply(lambda x: ','.join(sorted(x.split(','))))
#now remove non-hits from the dataframe
go_count_df['iprS_GO_annotations'] = go_count_df['iprS_GO_annotations'].str.replace('-,', '')
#also remove OGs without PFam hits
go_count_prep_df = go_count_df[go_count_df['iprS_GO_annotations'] != "-"].copy()
go_count_prep_df['iprS_GO_annotations'] = go_count_prep_df['iprS_GO_annotations'].apply(lambda x: x.split(','))
go_count_prep_df.set_index(og_col, inplace=True)


#create empty dictionaries to store the data
iprs_count_dict = {}
go_count_dict = {}

#first create the IPRS dictionary
for index, row in iprs_count_prep_df.iterrows(): 
	#iterate over the dataframe row by row
	og_iprs_list = row[0]
	#save the list of IPR hits to a variable
	og_iprs_counts = str(dict(Counter(og_iprs_list)))
	#save the results of the counts to a variable as a string
	og_iprs_counts = og_iprs_counts.replace('{', '')
	#remove the {braces} currently in the string
	og_iprs_counts = og_iprs_counts.replace('}', '')
	#remove spaces from the string
	og_iprs_counts = og_iprs_counts.replace(' ', '')
	#remove the single quotes from inside the strin
	#need to use "\" character to prevent EOF parsing error
	og_iprs_counts = og_iprs_counts.replace('\'', '')
	#now populate the dictionary
	iprs_count_dict[index] = og_iprs_counts

#then create the GO counts dictionary
for index, row in go_count_prep_df.iterrows(): 
	#iterate over the dataframe row by row
	og_go_list = row[0]
	#save the list of GO hits to a variable
	og_go_counts = str(dict(Counter(og_go_list)))
	#save the results of the counts to a variable as a string
	og_go_counts = og_go_counts.replace('{', '')
	#remove the {braces} currently in the string
	og_go_counts = og_go_counts.replace('}', '')
	#remove spaces from the string
	og_go_counts = og_go_counts.replace(' ', '')
	#remove the single quotes from inside the strin
	#need to use "\" character to prevent EOF parsing error
	og_go_counts = og_go_counts.replace('\'', '')
	#now populate the dictionary
	go_count_dict[index] = og_go_counts

#convert dictionaries back to dataframes
#first the IPR accession data
final_iprs_count_df = pd.DataFrame.from_dict(iprs_count_dict, orient='index', columns=['iprS_InterPro_annotations-accession'])
#and pull the OG data out of the index
final_iprs_count_df.reset_index(inplace=True)
#before renaming it according to the OG program being used
final_iprs_count_df.rename(columns={'index': og_col}, inplace=True)
#then the GO annotation data
final_go_count_df = pd.DataFrame.from_dict(go_count_dict, orient='index', columns=['iprS_GO_annotations'])
#and pull the OG data out of the index
final_go_count_df.reset_index(inplace=True)
#before renaming it according to the OG program being used
final_go_count_df.rename(columns={'index': og_col}, inplace=True)


#Part 5: Create simple dataframes showing OGs and associated PFams

#aggregate IDs into a comma-separated string, and remove duplicate hits
iprs_og_df['iprS_InterPro_annotations-accession'] = iprs_og_df['iprS_InterPro_annotations-accession'].apply(lambda x: ','.join(sorted(list(set(x.split(','))))))
go_og_df['iprS_GO_annotations'] = go_og_df['iprS_GO_annotations'].apply(lambda x: ','.join(sorted(list(set(x.split(','))))))

#remove "-" "hits" from the column of data
iprs_og_df['iprS_InterPro_annotations-accession'] = iprs_og_df['iprS_InterPro_annotations-accession'].str.replace('-,', '')
go_og_df['iprS_GO_annotations'] = go_og_df['iprS_GO_annotations'].str.replace('-,', '')
#also remove OGs without annotation hits
final_iprs_og_df = iprs_og_df[iprs_og_df['iprS_InterPro_annotations-accession'] != "-"].copy()
final_go_og_df = go_og_df[go_og_df['iprS_GO_annotations'] != "-"].copy()


#Part 6: Write out results

#write out count data to tab-separated text files
final_iprs_count_df.to_csv(output_iprs_counts, sep='\t', index=False)
final_go_count_df.to_csv(output_go_counts, sep='\t', index=False)

#write out OGs to annotations simplified data to tab-separated text files
final_iprs_og_df.to_csv(output_iprs, sep='\t', index=False)
final_go_og_df.to_csv(output_go, sep='\t', index=False)
