# -*- coding: utf-8 -*-
#!/bin/python
"""

Title: ale_tree_spp_names.py
Date: 2022.06.14
Author: Virág Varga

Description:
	This program iterates over a file containing gene trees in order to replace the 
		shortened versions of the species names with the full versions found in the 
		species tree. 

List of functions:
	No functions are defined in this script.

List of standard and non-standard modules used:
	sys

Procedure:
	1. Loading required modules; assigning command-line arguments.
	2. Creating reference dictionary for shortened and official species names.
	3. Iterating over the tree file and changing the species designations, writing 
		out the new tree versions to the output file as each one is created. 

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The output file name is not user-defined, but is instead based on the input
		file name.  

Usage
	./ale_tree_spp_names.py input_tree
	OR
	python ale_tree_spp_names.py input_tree

This script was written for Python 3.8.12, in Spyder 5.1.5.


"""


#Part 1: Import necessary modules; assign command-line arguments

#import necessary modules
import sys #allows assignment of command line arguments


#assign command line arguments; load input and output files
input_tree = sys.argv[1]
#input_tree = "SP_Mito3__OG_2636_MSA_IQ.ufboot"

#determine output file name based on input file name
input_name_list = input_tree.split(".")
#save contents of the name to a list
input_name_list.insert(-1, 'names')
#add the string "name" in the second to last position in the list
#and join the list elements back together to form the output file name
output_tree = '.'.join(input_name_list)


#Part 2: Create reference dictionary for shortened and official species names

species_dict = {"A_lanta": "Anaeramoeba_lanta_160522", 
						  "A_ignava_BM": "BM_newprots_may21.anaeromoeba", 
						  "A_flamelloides_BS": "BS_newprots_may21.anaeromoeba", 
						  "C_membranifera": "Carpediemonas_membranifera.PRJNA719540", 
						  "D_fragilis": "Dientamoeba_fragilis.43352.aa", 
						  "G_intestinalis_A_EukProt": "EP00701_Giardia_intestinalis", 
						  "Trepomonas_PC1": "EP00703_Trepomonas_sp_PC1", 
						  "P_pyriformis": "EP00708_Paratrimastix_pyriformis", 
						  "A_paluster": "EP00764_Aduncisulcus_paluster", 
						  "C_caulleryi": "EP00766_Chilomastix_caulleryi", 
						  "C_cuspidata": "EP00767_Chilomastix_cuspidata", 
						  "D_brevis": "EP00768_Dysnectes_brevis", 
						  "E_cyprinoides": "EP00769_Ergobibamus_cyprinoides", 
						  "M_exilis": "EP00770_Monocercomonoides_exilis", 
						  "T_marina": "EP00771_Trimastix_marina", 
						  "Barthelona_PAP020": "EP00792_Barthelona_sp_PAP020", 
						  "G_intestinalis_ADH": "GiardiaDB_GintestinalisADH", 
						  "G_intestinalis_BGS": "GiardiaDB_GintestinalisBGS", 
						  #"G_intestinalis_BGS_B": "GiardiaDB_GintestinalisBGS_B", 
						  "G_intestinalis_EP15": "GiardiaDB_GintestinalisEP15", 
						  "G_intestinalis_A_NCBI": "Giardia_intestinalis.PRJNA1439", 
						  "G_muris": "Giardia_muris.PRJNA524057", 
						  "H_meleagridis_OLD": "Histomonas_meleagridis.135588.aa", 
						  "H_meleagridis_NEW": "Histomonas_meleagridis.PRJNA594289", 
						  "K_bialata": "Kipferlia_bialata.PRJDB5223", 
						  "P_hominis": "Pentatrichomonas_hominis.5728.aa", 
						  "A_flamelloides_SC": "SC_newprots_may21.anaeromoeba", 
						  "S_salmonicida": "Spironucleus_salmonicida.PRJNA60811", 
						  "T_gallinarum": "Tetratrichomonas_gallinarum.5730.aa", 
						  "T_foetus": "Tritrichomonas_foetus.PRJNA345179", 
						  "T_vaginalis_GenBank": "Trichomonas_vaginalis_GenBank.PRJNA16084", 
						  "T_vaginalis_RefSeq": "Trichomonas_vaginalis_RefSeq.G3"}


'''
#adjusting for the BGS_B gene issue
bgs_b_genes_list = ["BLORVD0pGH4kejnx", "BRjoXadcs79DtjjF", "BB2HAPVsl9lf351v", "BUsgl1nKIPQG1ucj", 
					"BYl0e5oRqMzYC6wa", "BTzVlEzomPpywGb0", "Bzo2CNkJawQ6Pyhl", "BKzslU785QvQF0ad", 
					"B5j2b5nm4M2m3mic", "BFvSp0l4Ln6mjVUC", "BiadCsqVhO1MBks1", "BKgLWt9bWfuI3DEn", 
					"B0gbE44LXH9djDHT", "BYLnN871mzBbkFuJ", "BMeGKFdtNYL2g2fH", "BBTPCcDLReHslTDI", 
					"BHXel28xfXPp1Ra0", "BFszMXUvv0SOcdZa", "BkwJo5zXEnJhv3Sz", "BsWpnXvrlFQyeDAP", 
					"BAos68CMKm9k9QCr", "BeoRNavusDsOiRb3", "BkikAI4aSPZ7Y97Q", "BC5cv8sa7Gzvvt1X", 
					"ByVlU35cYj6OffrB", "BUUCjwM9PYfOMI5P", "Bq41wMZ8M7rzZro6", "BOl7XHzhCBb31XW2", 
					"BQfm5C47MGMr2abH", "BMH8YDcbCngex7fR", "BegUCpQNbgDUowkA", "BSQHQW34S9dRyGY8", 
					"BtPA7Ui5t9RJU71x", "BtqJd8jjmM4rVu6n", "Bx1bafhnUtOdNv1N", "BJQBqTGluqwTr34I", 
					"BmKtOHnymUBa33eg", "BjnfjcDnMs1zt8Xl", "BAgN9eLniiX2Jxmc", "BamHO4WZojR51OAE", 
					"B6FFVp87EoD4IblZ", "B8bWSHSt0bL0MMOT", "BGEdRqx4eipnt7Z1", "B7TU32EyBKRsELp8", 
					"BRizxJ6HWlHCrNdR", "BkOwqdFhPOKmXJNS", "B47OEOOOjw9mK73B", "BBgfNKZ8zUO0PUQT", 
					"BmSD9EcptubXHDyf", "B9bI4bcLWKzQVgwX", "BwmjEBJI4FirMzIi", "Bs3oX68lFioeG1ef", 
					"BvCeIzeBgjYwFhP6", "BqYrA1RYW0PhADyJ", "BFREhbPv4r5Sdiqi", "BYgeh8Uo77O2YZ4g", 
					"BTcP6q1Aw83YibpG", "Bsrb7Dk8mM3ET74A", "Bk0YeYCPJ1jthKBA", "BD4JED05Dx6kgAvy", 
					"BfRijwHuvXNd7JFn", "B9V9S8JXsleiVQHh", "Bqm5IkqF70P2R0dX", "BjsgPIqrNvGbJRMs", 
					"Bg62EMQIS0wzBGjG", "B29MSdxhRqxsfNOp", "BgaCciT5RJx7A5RE", "B5HaCfRVw97nDkci", 
					"BeGinTggURwLPQ1f", "BwefHOmQ5brWEMuz", "BLCszYHp48mn4LeS", "B8i362TviaJkAVCf", 
					"B0tEv21BwSfDTggC", "BqpARYLmFSdVxc70", "BBmD330dsGexAzQp", "BspGZdfe1TtP5FGV", 
					"BMvRrb5Sq2v9IzfU", "BnZF7IfjyTYvzZv1", "BkwaIUaJX26RcX03", "BRsTJAbzZBQc8ttq", 
					"BWMgvapEBfsLyobd", "BMG5n4ochzot6Uew", "BxuAIF5oe5Em8TG9", "BZg6wivF4OYW2ADu", 
					"BU0cs1deeBWOaSvA", "BmbAoXjE2ZEGm9Ln", "Bv1uSsX3aakePX4G"]
'''


#Part 3: Iterate over the tree file and change the species designations

with open(input_tree, "r") as infile, open(output_tree, "w") as outfile: 
	#open the input tree for reading, and the output tree file for writing
	for line in infile: 
		#iterate over the tree file line by line
		tree_line = line.strip()
		#save the old gene tree to a variable, stripping the end-line character
		if "G_intestinalis_BGS_B__" in tree_line: 
			#check to see if thee BGS_B Giardia genome occurs in the tree
			#if it occurs, overwrite the genome prior to match searching
			tree_line = tree_line.replace("G_intestinalis_BGS_B__", "GiardiaDB-GintestinalisBGS-B__")
		for spp_key in species_dict.keys(): 
			#iterate over the keys of the dictionary, 
			#to identify which of the species occur in the tree file
			if spp_key in tree_line: 
				#check to see if the shorter species designation occurs in the gene tree
				#if it is, save the full species designation to a variable
				#and replace the "_" characters with "-" characters in the species names
				value_edit = species_dict[spp_key].replace("_", "-")
				#and overwrite the tree with the full species designation
				tree_line = tree_line.replace(spp_key, value_edit)
				tree_line = tree_line.replace("__", "_")
				#the modifications to the naming scheme with regards to the underscores is necessary
				#because ALE (or at least the container version of it)
				#doesn't accept the `separators` argument shown on their GitHub
				#that would allow the user to specify the separator 
				#between a species name and gene ID
		#once all species have been checked, write out the new tree to the output file
		#write each tree to a new line
		outfile.write(tree_line + "\n")
