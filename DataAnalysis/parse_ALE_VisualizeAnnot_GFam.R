#!/usr/bin/env Rscript

###


# Title: parse_ALE_VisualizeAnnot_GFam.R
# Date: 2022.08.24
# Author: Virág Varga
# With gratitude to: Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil)
# 
# Description:
#   This program annotates the nodes/branches of an input phylogenetic species tree with data 
#     derived from a summary data table showing information relevant to the nodes. 
#   The resulting tree is output to an SVG file. 
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
#   2. Import node annotation data & species tree
#   3. Add node label annotations to tree
#   4. Write out results to file
# 
# Known bugs and limitations:
#   - There is no quality-checking integrated into the code.
#   - The output file name is not entirely user-defined, but is instead based on the input
#     file name plus a user-provided extension.
# 
# Citation: 
#   This program is a based off of the ALE parsing programs used in the ALE-pipeline 
# program written by Max Emil Schön (@maxemil on GitHub: https://github.com/maxemil), 
# which can be found here: https://github.com/maxemil/ALE-pipeline
# 
# Version: 
#   This can be considered an alternative version of the original parse_ALE_VisualizeAnnot.R program. 
# It makes the results data which has been reformatted to match the results of the Count 
# program by the parse_ALE_Nodes_GFam.py program.
# 
# Usage: 
# ./parse_ALE_VisualizeAnnot_GFam.R tree_file events_file output_ext
# OR
# Rscript parse_ALE_VisualizeAnnot_GFam.R tree_file events_file output_ext
# 
# This script was written for R 4.2.1, in RStudio 2022.02.3 Build 492.


###


#Part 1: Load necessary libraries; assign command-line arguments

#setting up the workspace
#clear the environment
rm(list = ls())
#set working directory
setwd('C:/Users/V/Documents/LundUni/Trich_Parab/Thesis_Work/ALE')


#load libraries
library(tools)
library(ape)
library(svglite)


#load input files & determine output file names
#ref: https://stackoverflow.com/questions/750786/whats-the-best-way-to-use-r-scripts-on-the-command-line-terminal
#ref: https://www.r-bloggers.com/2015/09/passing-arguments-to-an-r-script-from-command-lines/
#set up R to take command-line input (ie. accept any input file)
#args = commandArgs(trailingOnly=TRUE)

#determine input files
#the tree file
#tree_file <- args[1]
#tree_file <- "SP_Mito3_Species_Tree.nwk"
#tree_file <- "OF_Mito3_Species_Tree.nwk"
#tree_file <- "SP_Sec3_Species_Tree.nwk"
tree_file <- "OF_Sec3_Species_Tree.nwk"

#the events dataframe
#events_file <- args[2]
#events_file <- "SP_Mito3__Events_Final_Nodes_R_GFam.txt"
#events_file <- "OF_Mito3__Events_Final_Nodes_R_GFam.txt"
#events_file <- "SP_Sec3__Events_Final_Nodes_R_GFam.txt"
events_file <- "OF_Sec3__Events_Final_Nodes_R_GFam.txt"

#determining the output file names from the input file names
#usr_file_ext <- args[3]
usr_file_ext <- "ALL_GFam"
#strip the file extension
#ref: https://stackoverflow.com/questions/29113973/get-filename-without-extension-in-r
tree_base <- file_path_sans_ext(basename(tree_file))
out_base <- paste(tree_base, usr_file_ext, sep = "_")

#ref: https://www.rdocumentation.org/packages/svglite/versions/2.1.0/topics/svglite
svglite(paste(out_base, "svg", sep = "."), width = 80, height = 30)


#Part 2: Import node annotation data & species tree

#import node annotation data
#events_df = read.table(args[2], sep="\t", header=TRUE)
events_df = read.table(events_file, sep="\t", header=TRUE)
#ref: https://www.portfolioprobe.com/user-area/documentation/portfolio-probe-cookbook/data-basics/read-a-tab-separated-file-into-r/

#read in species tree using the ape library
#ref: https://cran.r-project.org/web/packages/TreeTools/vignettes/load-trees.html
spp_tree <- read.tree(tree_file)
#ref: https://www.geeksforgeeks.org/create-plot-window-of-particular-size-in-r/
#dev.new(width=200, height=100, unit="cm")
#the above was used during initial testing of label dimensions & details, prior to export
plot(spp_tree)

#obtain key node & branch numbers with: 
# nodelabels()
# tiplabels()
# edgelabels()


#Part 3: Add node label annotations to tree

#ref: https://search.r-project.org/CRAN/refmans/ape/html/nodelabels.html
#ref: https://stackoverflow.com/questions/18706665/extracting-value-based-on-another-column
#ref: http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
#label the root node
#this one needs special adjustments due to placement
nodelabels(paste(paste(paste("Originations", events_df$Originations[events_df$Node==33], sep = ": "), "Losses", events_df$Losses[events_df$Node==33], sep = ": "), paste("Copies", events_df$Copies[events_df$Node==33], sep = ": "), sep = "; "), 33, adj = 0.2, cex = 0.8)
#labeling the tips of the tree
#ref: https://www.w3schools.com/r/r_for_loop.asp
for (y in 1:26) {
  tiplabels(paste(paste("Originations", events_df$Originations[events_df$Node==y], sep = ": "), paste("Losses", events_df$Losses[events_df$Node==y], sep = ": "), paste("Copies", events_df$Copies[events_df$Node==y], sep = ": "), sep = "; "), y, adj = -1.5, cex = 0.8, bg = "darkseagreen1")
}
for (y in 27:32) {
  tiplabels(paste(paste("Originations", events_df$Originations[events_df$Node==y], sep = ": "), paste("Losses", events_df$Losses[events_df$Node==y], sep = ": "), paste("Copies", events_df$Copies[events_df$Node==y], sep = ": "), sep = "; "), y, adj = -1.2, cex = 0.8, bg = "darkseagreen1")
}
#above, pulled the Giardias into a separate group
#labeling the internal nodes of the tree
for (x in 34:63) {
  nodelabels(paste(paste("Originations", events_df$Originations[events_df$Node==x], sep = ": "), paste("Losses", events_df$Losses[events_df$Node==x], sep = ": "), paste("Copies", events_df$Copies[events_df$Node==x], sep = ": "), sep = "; "), x, cex = 0.8)
}


#Part 4: Write out results to file
dev.off()
