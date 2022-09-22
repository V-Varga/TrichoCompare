#!/usr/bin/env Rscript

###


# Title: upSetR_plots.R
# Date: 2022.07.02
# Author: Virág Varga
# 
# Description:
#   This program creates upset plots using the binary presence/absence data of 
#       OGs per species. This binary data was obtained via the Count software. 
# 
# List of functions:
#   No functions are defined in this script.
# 
# List of standard and non-standard modules used:
#   tools
#   ape
#   svglite
# 
# Procedure:
#   1. Load necessary libraries; assign command-line arguments
#   2. Load input data into dataframe
#   3. Create UpSetR plot
#   4. Write out results to file
# 
# Known bugs and limitations:
#   - There is no quality-checking integrated into the code.
#   - The output file name is not entirely user-defined, but is instead based on the input
#     file name plus a user-provided extension.
# 
# Version: 
#   This program can be considered a Version 2.0 of the upSetR_etAll.R script prepared
#       for the preliminary exploratory project. 
# 
# Usage: 
# ./upSetR_plots.R input_data output_ext
# OR
# Rscript upSetR_plots.R input_data output_ext
# 
# This script was written for R 4.2.1, in RStudio 2022.02.3 Build 492.


###


#Part 1: Load necessary libraries; assign command-line arguments

#setting up the workspace
#clear the environment
rm(list = ls())
#set working directory
setwd('C:/Users/V/Documents/LundUni/Trich_Parab/Thesis_Work/Figures')


#load libraries
library(UpSetR)
library(tools)
library(grid)


#load input files & determine output file names
#ref: https://stackoverflow.com/questions/750786/whats-the-best-way-to-use-r-scripts-on-the-command-line-terminal
#ref: https://www.r-bloggers.com/2015/09/passing-arguments-to-an-r-script-from-command-lines/
#set up R to take command-line input (ie. accept any input file)
#args = commandArgs(trailingOnly=TRUE)

#determine input file - binary count data
#the tree file
#input_data <- args[1]
#input_data <- "Alanta_mito_3_OF_ALL__CountPivot__Binary.txt"
#input_data <- "Alanta_mito_3_SP_ALL__CountPivot__Binary.txt"
#input_data <- "Alanta_sec_3_OF_ALL__CountPivot__Binary.txt"
input_data <- "Alanta_sec_3_SP_ALL__CountPivot__Binary.txt"

#Figure title variable
#upset_fig_title <- "OrthoFinder OGs Targeted to the MRO"
#upset_fig_title <- "SonicParanoid OGs Targeted to the MRO"
#upset_fig_title <- "OrthoFinder OGs Targeted to the Secretome"
upset_fig_title <- "SonicParanoid OGs Targeted to the Secretome"

#determining the output file names from the input file names
#usr_file_ext <- args[2]
#usr_file_ext <- "UpSetR"
usr_file_ext <- "UpSetR_fin"
#strip the file extension
#ref: https://stackoverflow.com/questions/29113973/get-filename-without-extension-in-r
input_base <- file_path_sans_ext(basename(input_data))
out_base <- paste(input_base, usr_file_ext, sep = "_")
out_base
#copy the printout above to use as the file name when exporting


#Part 2: Load input data into dataframe

#can't use raw frequency data - need to use binary presence/absence data
binary_df <- read.table(input_data, header=TRUE)


#Part 3: Create UpSetR plot
#GitHub package ref: https://github.com/hms-dbmi/UpSetR
#other upset plot ref: https://jokergoo.github.io/ComplexHeatmap-reference/book/upset-plot.html
#upset(binary_df)
#the simple version above shows only a small subsection
upset(binary_df,
      sets = c("Anaeramoeba_lanta_160522", "BM_newprots_may21.anaeromoeba", "SC_newprots_may21.anaeromoeba", 
               "BS_newprots_may21.anaeromoeba", "Tetratrichomonas_gallinarum.5730.aa", "Pentatrichomonas_hominis.5728.aa", 
               "Trichomonas_vaginalis_GenBank.PRJNA16084", "Trichomonas_vaginalis_RefSeq.G3", "Dientamoeba_fragilis.43352.aa", 
               "Histomonas_meleagridis.PRJNA594289", "Histomonas_meleagridis.135588.aa", "Tritrichomonas_foetus.PRJNA345179", 
               "EP00708_Paratrimastix_pyriformis", "EP00771_Trimastix_marina", "EP00770_Monocercomonoides_exilis", 
               "EP00792_Barthelona_sp_PAP020", "EP00769_Ergobibamus_cyprinoides", "Carpediemonas_membranifera.PRJNA719540", 
               "EP00764_Aduncisulcus_paluster", "EP00766_Chilomastix_caulleryi", "EP00767_Chilomastix_cuspidata", 
               "Kipferlia_bialata.PRJDB5223",  "EP00768_Dysnectes_brevis", "Spironucleus_salmonicida.PRJNA60811", 
               "EP00703_Trepomonas_sp_PC1", "Giardia_muris.PRJNA524057", "GiardiaDB_GintestinalisEP15", 
               "GiardiaDB_GintestinalisADH", "EP00701_Giardia_intestinalis", "Giardia_intestinalis.PRJNA1439", 
               "GiardiaDB_GintestinalisBGS", "GiardiaDB_GintestinalisBGS_B" ),
      order.by = "freq")
#adding a title to the plot
#ref: https://github.com/hms-dbmi/UpSetR/issues/76
grid.text(upset_fig_title, x = 0.7, y=0.95, gp=gpar(fontsize=60))
#note that this font size does not look good in the RStudio Plots preview
#however it works well with the width 3000 export maintaining the aspect ratio
#this gives the final dimensions at 3000x1854


#Part 4: Save data to file

#Originally, planned to save the image as png (dimensions given below)
#however, export as an SVG image maintains the quality much better
#so export from the plot window in SVG format
#with width 3000 and aspect ration maintained
#this gives final image dimensions of 3000x1854


#Dimensions for a .PNG should be: 
#Width 3000; Height 1500
#Dimensions for a .PDF should be: 
#20 x 15 in Potrait mode
