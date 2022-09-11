# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: extract_OG_MSA.py
Date: 2022.05.16
Author: Virág Varga

Description:
	This program iterates over a file produced by the og_prot_list.py program to create
		a FASTA file containing the amino acid sequences of all proteins in a given
		orthologous group. This is intended for use as an input for a Multiple Sequence
		Alignment (MSA) program.

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys
	os
	pandas

Procedure:
	1. Loading required modules; assigning command line arguments.
	2. Importing data into Pandas dataframe and creating dictionary of FASTA files
		to protein sequences contained within them.
	3. Creating reference dictionary for file names and species IDs.
	4. Extracting sequence data from files to create MSA prep FASTA file.
	5. Writing out results in single-line FASTA formatting.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is based on the input file name.

Usage
	./extract_OG_MSA.py input_db data_path
	OR
	python extract_OG_MSA.py input_db data_path

	Where the input_db is file in the format:
		Query\tSpecies_ID\t[OG_PROGRAM]_OG
	Where data_path is a string input in quotation marks on the command line of the
		absolute path to the directory where the data FASTA files are located.
		This should include a trailing backslash.

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments
import os #allow access to computer files
import pandas as pd #facilitates manipulation of dataframes in Python


#assign command line arguments; load input and output files
input_db = sys.argv[1]
#input_db = "TEST_SonicParanoid_OG__OG_25.txt"

data_path = sys.argv[2]
#data_path = "C:/Users/V/Documents/LundUni/Trich_Parab/Thesis_Work/ALE/"

#output file name should be based on input file name
base = os.path.basename(input_db)
out_full = os.path.splitext(base)[0]
#determine basename of input file
output_fasta = out_full + "_MSAprep.fasta"


#Part 2: Import data into Pandas dataframe & create species dictionary

#read in the Metamonad database to a Pandas dataframe
input_df = pd.read_csv(input_db, sep = '\t', header=0)
#then extract the name of the OG
query_og_id = input_df.iloc[:, 2].to_list()[0]
#transform the data in the 'Species_Id' column into the actual file names
input_df['Species_Id'] = input_df['Species_Id'] + '_edit.fasta'


#create a dictionary in the format: species_dict[species_file_name] = list_of_proteins
#this will allow easier analysis
grouped_species_df = input_df.groupby('Species_Id')['Query'].apply(list).reset_index(name="Species_members")
#the proteins in the 'Query' column are grouped into lists according to the species FASTA file they are from
#the new column of lists is named 'Species_members'
species_dict = grouped_species_df.set_index('Species_Id').to_dict()['Species_members']
#the new dataframe is converted into a dictionary,
#where the OG IDs are the keys, and the lists of protein members of the OGs are the values


#Part 3: Create reference dictionary for file names and species IDs

species_fasta_ref_dict = {"Anaeramoeba_lanta_160522_edit.fasta": "A_lanta__", 
						  "BM_newprots_may21.anaeromoeba_edit.fasta": "A_ignava_BM__", 
						  "BS_newprots_may21.anaeromoeba_edit.fasta": "A_flamelloides_BS__", 
						  "Carpediemonas_membranifera.PRJNA719540_edit.fasta": "C_membranifera__", 
						  "Dientamoeba_fragilis.43352.aa_edit.fasta": "D_fragilis__", 
						  "EP00701_Giardia_intestinalis_edit.fasta": "G_intestinalis_A_EukProt__", 
						  "EP00703_Trepomonas_sp_PC1_edit.fasta": "Trepomonas_PC1__", 
						  "EP00708_Paratrimastix_pyriformis_edit.fasta": "P_pyriformis__", 
						  "EP00764_Aduncisulcus_paluster_edit.fasta": "A_paluster__", 
						  "EP00766_Chilomastix_caulleryi_edit.fasta": "C_caulleryi__", 
						  "EP00767_Chilomastix_cuspidata_edit.fasta": "C_cuspidata__", 
						  "EP00768_Dysnectes_brevis_edit.fasta": "D_brevis__", 
						  "EP00769_Ergobibamus_cyprinoides_edit.fasta": "E_cyprinoides__", 
						  "EP00770_Monocercomonoides_exilis_edit.fasta": "M_exilis__", 
						  "EP00771_Trimastix_marina_edit.fasta": "T_marina__", 
						  "EP00792_Barthelona_sp_PAP020_edit.fasta": "Barthelona_PAP020__", 
						  "GiardiaDB_GintestinalisADH_edit.fasta": "G_intestinalis_ADH__", 
						  "GiardiaDB_GintestinalisBGS_edit.fasta": "G_intestinalis_BGS__", 
						  "GiardiaDB_GintestinalisBGS_B_edit.fasta": "G_intestinalis_BGS_B__", 
						  "GiardiaDB_GintestinalisEP15_edit.fasta": "G_intestinalis_EP15__", 
						  "Giardia_intestinalis.PRJNA1439_edit.fasta": "G_intestinalis_A_NCBI__", 
						  "Giardia_muris.PRJNA524057_edit.fasta": "G_muris__", 
						  "Histomonas_meleagridis.135588.aa_edit.fasta": "H_meleagridis_OLD__", 
						  "Histomonas_meleagridis.PRJNA594289_edit.fasta": "H_meleagridis_NEW__", 
						  "Kipferlia_bialata.PRJDB5223_edit.fasta": "K_bialata__", 
						  "Pentatrichomonas_hominis.5728.aa_edit.fasta": "P_hominis__", 
						  "SC_newprots_may21.anaeromoeba_edit.fasta": "A_flamelloides_SC__", 
						  "Spironucleus_salmonicida.PRJNA60811_edit.fasta": "S_salmonicida__", 
						  "Tetratrichomonas_gallinarum.5730.aa_edit.fasta": "T_gallinarum__", 
						  "Trichomonas_foetus.PRJNA345179_edit.fasta": "T_foetus__", 
						  "Trichomonas_vaginalis_GenBank.PRJNA16084_edit.fasta": "T_vaginalis_GenBank__", 
						  "Trichomonas_vaginalis_RefSeq.G3_edit.fasta": "T_vaginalis_RefSeq__"}


#Part 4: Extract sequence data from files to create MSA prep FASTA file

#create new empty dictionary for protein IDs and protein sequences
seq_dict = {}

for key in species_dict.keys():
	#iterate over the dictionary via its keys (ie. file names)
	file_path = data_path + key
	#define the full file name including the path
	spp_prot_list = species_dict[key]
	#pull out the query protein IDs into a list
	with open(file_path, 'r') as infile:
		#open the species FASTA proteome file for reading
		for line in infile:
			#iterate over the file line by line
			for prot in spp_prot_list:
				#iterate over the list of query prot IDs
				if prot in line:
					#if the query protein is found in the line
					header_start = line[1:].strip()
					#remove the ">" header line indicator and strip the endline character
					for ref_species_key in species_fasta_ref_dict.keys():
						#iterate over the FASTA reference dictionary
						if key == ref_species_key: 
							#find the location of the species FASTA name reference
							#and copy the header version of the species ID to a variable
							species_header_name = species_fasta_ref_dict[ref_species_key]
					header = species_header_name + header_start
					#create the new FASTA header as a combination of the original encoded protein ID
					#and the shortened species ID name designed for the header
					seq_line = next(infile).strip()
					#identify the sequence line associated with the header
					#and remove the endline character
					#finally, add the header and protein sequence to the dictionary
					seq_dict[header] = seq_line


#Part 5: Write out results to new FASTA file

with open(output_fasta, "w") as outfile:
	#open the output file for writing
	for prot_key in seq_dict.keys():
		#iterate over the encoded protein headers
		#and write the header and sequence lines out in FASTA format
		outfile.write(">" + prot_key + "\n" + seq_dict[prot_key] + "\n")
