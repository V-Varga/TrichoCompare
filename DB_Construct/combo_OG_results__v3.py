# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: combo_OG_results__v3.py
Date: 2022-03-16
Author: Virág Varga

Description:
	This program parses the results files for 1 species from the eggNOG_dn_PFam_Parser__v2.py, 
		eggNOG_dn_Parser__v2.py, signalP_Parser__v2.py, targetP_Parser__v2.py, 
		deepLoc_Parser__v2.py, mitoFates_Parser__v2.py, iprScan_Parser.py and 
		yLoc_Parser__v2.py scripts. The data in these parsed files is concatenated 
		into one large, flat database.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas
	numpy

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas import the contents of the de novo PFam via EggNOG, de novo EggNOG
		SignalP, TargetP, InterProScan, DeepLoc, Yloc and MitoFates results files.
	3. Cpncatenating the databases and filling NaN values with "-".
	4. Writing out the results to a tab-delimited text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of the parsed files created thorugh the use of
		eggNOG_dn_PFam_Parser__v2.py, eggNOG_dn_Parser__v2.py, signalP_Parser__v2.py, 
		targetP_Parser__v2.py, deepLoc_Parser__v2.py, mitoFates_Parser__v2.py, iprScan_Parser.py 
		and yLoc_Parser__v2.py.
	- All input and output files are user-defined: This means the user must ensure that
		the correct file names have been assigned to the program.

Version:
	This is version 3.0 of this program. A species ID column will now be added before the database
		is written out to a file. 

Usage
	./combo_OG_results__v3.py PFam_EN_Parsed EggNOG_Parsed DeepLoc_Parsed SignalP_Parsed
		TargetP_Parsed IPRScan_Parsed MitoFates_Parsed YLoc_Parsed Species_ID Output_DB
	OR
	python combo_OG_results__v3.py PFam_EN_Parsed EggNOG_Parsed DeepLoc_Parsed SignalP_Parsed
		TargetP_Parsed IPRScan_Parsed MitoFates_Parsed YLoc_Parsed Species_ID Output_DB

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part 1: Import necessary modules, assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python
import numpy as np #facilitates manipulation of arrays in Python


#assign command line arguments: input & output files
PFam_EN_Parsed = sys.argv[1]
#PFam_EN_Parsed = "BM_anaeromoeba_EN_PFam.txt"
EggNOG_Parsed = sys.argv[2]
#EggNOG_Parsed = "BM_anaeromoeba_EN_eggNOG.txt"
DeepLoc_Parsed = sys.argv[3]
#DeepLoc_Parsed = "BM_anaeromoeba_DL_DeepLoc.txt"
SignalP_Parsed = sys.argv[4]
#SignalP_Parsed = "BM_anaeromoeba\BM_newprots_may21_SignalP.txt"
TargetP_Parsed = sys.argv[5]
IPRScan_Parsed = sys.argv[6]
MitoFates_Parsed = sys.argv[7]
YLoc_Parsed = sys.argv[8]
Species_ID = sys.argv[9]
Output_DB = sys.argv[10]
#Output_DB = "BM_anaeromoeba_DB_TEST.txt"


#Part 2: Importing parsed data file contents into Pandas dataframes

#PFam results
with open(PFam_EN_Parsed, "r") as pfam_infile:
	#open the parsed PFam via eggNOG data file
	pfam_df = pd.read_csv(pfam_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	pfam_df = pfam_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	pfam_df = pfam_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	pfam_df = pfam_df.add_prefix('pfamEN_')
	#add prefix to column names to prevent duplicates between the dataframes

#eggNOG results
with open(EggNOG_Parsed, "r") as eggnog_infile:
	#open the parsed eggNOG data file
	eggnog_df = pd.read_csv(eggnog_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	eggnog_df = eggnog_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	eggnog_df = eggnog_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	eggnog_df = eggnog_df.add_prefix('EN_')
	#add prefix to column names to prevent duplicates between the dataframes

#DeepLoc results
with open(DeepLoc_Parsed, "r") as deeploc_infile:
	#open the parsed DeepLoc data file
	deeploc_df = pd.read_csv(deeploc_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	deeploc_df = deeploc_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	deeploc_df = deeploc_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	deeploc_df = deeploc_df.add_prefix('DeepL_')
	#add prefix to column names to prevent duplicates between the dataframes

#SignalP results
with open(SignalP_Parsed, "r") as signalp_infile:
	#open the parsed SignalP data file
	signalp_df = pd.read_csv(signalp_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	signalp_df = signalp_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	signalp_df = signalp_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	signalp_df = signalp_df.add_prefix('SigP_')
	#add prefix to column names to prevent duplicates between the dataframes

#TargetP results
with open(TargetP_Parsed, "r") as targetp_infile:
	#open the parsed TargetP data file
	targetp_df = pd.read_csv(targetp_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	targetp_df = targetp_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	targetp_df = targetp_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	targetp_df = targetp_df.add_prefix('TarP_')
	#add prefix to column names to prevent duplicates between the dataframes

#InterProScan results
with open(IPRScan_Parsed, "r") as iprscan_infile:
	#open the parsed InterProScan data file
	iprscan_df = pd.read_csv(iprscan_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	iprscan_df = iprscan_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	iprscan_df = iprscan_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	iprscan_df = iprscan_df.add_prefix('iprS_')
	#add prefix to column names to prevent duplicates between the dataframes

#MitoFates results
with open(MitoFates_Parsed, "r") as mitofates_infile:
	#open the parsed MitoFates data file
	mitofates_df = pd.read_csv(mitofates_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	mitofates_df = mitofates_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	mitofates_df = mitofates_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	mitofates_df = mitofates_df.add_prefix('MitoF_')
	#add prefix to column names to prevent duplicates between the dataframes

#YLoc results
with open(YLoc_Parsed, "r") as yloc_infile:
	#open the parsed YLoc data file
	yloc_df = pd.read_csv(yloc_infile, sep='\t', header = 0)
	#read the file into a pandas dataframe
	#specifying that the file is tab-separated with a header line
	yloc_df = yloc_df.set_index('Query')
	#set the first column (containing query sequence names) as an index
	yloc_df = yloc_df.replace(r'^\s*$', np.NaN, regex=True)
	#replace empty cells with 'NaN'
	yloc_df = yloc_df.add_prefix('YLoc_')
	#add prefix to column names to prevent duplicates between the dataframes


#Part 3: Merge the dataframes and write out

merged_df = pd.concat([pfam_df, eggnog_df, iprscan_df, signalp_df, targetp_df, deeploc_df, mitofates_df, yloc_df], axis=1)
#concatenate the dataframes along the x axis, horizontally
merged_df.fillna('-', inplace=True)


#add in species ID column
merged_df = pd.concat([pd.Series(Species_ID, index=merged_df.index, name='Species_Id'), merged_df], axis=1)


#write out results to tab-delimited text file
merged_df.to_csv(Output_DB, sep='\t', index=True)
#since the Query columns got shifted into indexes, need to use `index=True`
