# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: categorize_prot_species.py
Date: 2022-03-12
Author: Virág Varga

Description:
	This program creates a database which includes all protein query IDs, the
		"official" species/strain designation, a categorized species/strain/assemblage
		designation, and the phylum that the species belongs to.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	pandas

Procedure:
	1. Loading required modules; defining inputs and outputs as command line
		arguments.
	2. Using Pandas to import the contents of the query protein and species information-containing
		file into a dataframe.
	3. Creating species category and phylum information dictionaries.
	4. Adding the species category and phylum information into the dataframe.
	5. Writing out the dataframe to a tab-separated text file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- This program requires the input of a file with query IDs in the first column,
		and the species/strain IDs (derived from proteome file names) in the second column.

Usage
	./categorize_prot_species.py input_db output_db
	OR
	python categorize_prot_species.py input_db output_db

This script was written for Python 3.8.12, in Spyder 5.1.5.

"""


#Part1: Assign command-line arguments, import modules

#import necessary modules
import sys #allows assignment of command line arguments
import pandas as pd #facilitates manipulation of dataframes in Python

#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "species_prots_ref.txt"
output_db = sys.argv[2]
#output_db = "prots_species_phyla_db.txt"


#Part 2: Import Pandas dataframe

#set names of columns for imported dataframe
colnames=['Query', 'Species_ID']
#import input database into a Pandas dataframe
prot_df = pd.read_csv(input_db, sep = '\t', names=colnames, header=None)


#Part 3: Create species categorization and phylum dictionaries

#create dictionary connecting species designations to species categories
category_dict = {'BM_anaeromoeba': 'BM_newprots_may21.anaeromoeba',
				 'BS_anaeromoeba': 'BS_newprots_may21.anaeromoeba',
				 'Carpediemonas_membranifera': 'Carpediemonas_membranifera.PRJNA719540',
				 'Dientamoeba_fragilis': 'Dientamoeba_fragilis.43352.aa',
				 'Trepomonas_sp_PC1': 'EP00703_Trepomonas_sp_PC1',
				 'Paratrimastix_pyriformis': 'EP00708_Paratrimastix_pyriformis',
				 'Aduncisulcus_paluster': 'EP00764_Aduncisulcus_paluster',
				 'Chilomastix_caulleryi': 'EP00766_Chilomastix_caulleryi',
				 'Chilomastix_cuspidata': 'EP00767_Chilomastix_cuspidata',
				 'Dysnectes_brevis': 'EP00768_Dysnectes_brevis',
				 'Ergobibamus_cyprinoides': 'EP00769_Ergobibamus_cyprinoides',
				 'Monocercomonoides_exilis': 'EP00770_Monocercomonoides_exilis',
				 'Trimastix_marina': 'EP00771_Trimastix_marina',
				 'Barthelona_sp_PAP020': 'EP00792_Barthelona_sp_PAP020',
				 'Giardia_intestinalis_A': ['EP00701_Giardia_intestinalis', 'Giardia_intestinalis.PRJNA1439', 'GiardiaDB_GintestinalisADH'],
				 'Giardia_intestinalis_B': ['GiardiaDB_GintestinalisBGS_B', 'GiardiaDB_GintestinalisBGS'],
				 'Giardia_intestinalis_E': 'GiardiaDB_GintestinalisEP15',
				 'Giardia_muris': 'Giardia_muris.PRJNA524057',
				 'Histomonas_meleagridis': ['Histomonas_meleagridis.135588.aa', 'Histomonas_meleagridis.PRJNA594289'],
				 'Kipferlia_bialata': 'Kipferlia_bialata.PRJDB5223',
				 'Pentatrichomonas_hominis': 'Pentatrichomonas_hominis.5728.aa',
				 'SC_anaeromoeba': 'SC_newprots_may21.anaeromoeba',
				 'Spironucleus_salmonicida': 'Spironucleus_salmonicida.PRJNA60811',
				 'Tetratrichomonas_gallinarum': 'Tetratrichomonas_gallinarum.5730.aa',
				 'Tritrichomonas_foetus': 'Trichomonas_foetus.PRJNA345179',
				 'Trichomonas_vaginalis': ['Trichomonas_vaginalis_GenBank.PRJNA16084', 'Trichomonas_vaginalis_RefSeq.G3']}


#create a dictionary connecting phylum information to species categories
phylum_dict = {'Anaeramoebidae': ['BM_anaeromoeba', 'BS_anaeromoeba', 'SC_anaeromoeba'],
			   'Parabasalia': ['Dientamoeba_fragilis', 'Histomonas_meleagridis', 'Pentatrichomonas_hominis',
					  'Tetratrichomonas_gallinarum', 'Tritrichomonas_foetus', 'Trichomonas_vaginalis'],
			   'Fornicata': ['Carpediemonas_membranifera', 'Trepomonas_sp_PC1', 'Aduncisulcus_paluster',
					'Chilomastix_caulleryi', 'Chilomastix_cuspidata', 'Dysnectes_brevis', 'Ergobibamus_cyprinoides',
					'Giardia_intestinalis_A', 'Giardia_intestinalis_B', 'Giardia_intestinalis_E', 'Giardia_muris',
					'Kipferlia_bialata', 'Spironucleus_salmonicida'],
			   'Preaxostyla': ['Paratrimastix_pyriformis', 'Monocercomonoides_exilis', 'Trimastix_marina'],
			   'Other': 'Barthelona_sp_PAP020'}


#Part 4: Add the species categories and phyla into the dataframe

#create empty column for species category information
prot_df['Species_Category'] = "-"

for index, row in prot_df.iterrows():
	#iterate through the dataframe row by row
	for key in category_dict.keys():
		#iterate over the dictionary via its keys
		if row['Species_ID'] in category_dict[key]:
			#if the species ID associated with a particular query protein
			#is in the value (string or list) associated with a particular key in the category_dict
			#then copy the dictionary key into the Species_Category column of that row
			prot_df.at[index, 'Species_Category'] = key


#create empty column for phylum information
prot_df['Phylum'] = "-"

for index, row in prot_df.iterrows():
	#iterate through the dataframe row by row
	for key in phylum_dict.keys():
		#iterate over the dictionary via its keys
		if row['Species_Category'] in phylum_dict[key]:
			#if the species category associated with a particular query protein
			#is in the value (string or list) associated with a particular key in the phylum_dict
			#then copy the dictionary key into the Phylum column of that row
			prot_df.at[index, 'Phylum'] = key


#Part 5: Write out resulting dataframe to a tab-separated text file

#write out the resulting dataframe
prot_df.to_csv(output_db, sep='\t', index=False)
