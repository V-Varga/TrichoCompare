###
#
# IMPORTANT NOTE!!!
#
# THIS SCRIPT IS NOT INTENDED TO BE SELF-CONTAINED
# IT CANNOT BE RUN ON ITS OWN
#
#
# This script (visualize_ALE_selection.R) was written to accompany the parse_ALE_VisualizeAnnot.R script. 
# This script contains the code modifications necessary (ie. unique file names & new working directory)
# to run the parse_ALE_VisualizeAnnot.R script for the selcted OGs analyzed in the final stage of the TrichoCompare project. 
# These additions to that script are kept separate to avoid cluttering up that script with unnecessary lines of code. 
#
###

#setting up the workspace
#clear the environment
rm(list = ls())

#set working directory
setwd('C:/Users/V/Documents/LundUni/Trich_Parab/Thesis_Work/Biol_Interpret/ALE_Data')


#determining the output file names from the input file names
#strip the file extension
#ref: https://stackoverflow.com/questions/29113973/get-filename-without-extension-in-r
out_base <- file_path_sans_ext(basename(events_file))

#ref: https://www.rdocumentation.org/packages/svglite/versions/2.1.0/topics/svglite
svglite(paste(out_base, "svg", sep = "."), width = 80, height = 30)


#Mito OF
#events_file <- "OF_Mito3__Events_Final_PFam__OG0000021_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0000095_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0002517_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0001149_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0001763_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0001107_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0000573_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0002422_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0000060_Nodes_R.txt"
#events_file <- "OF_Mito3__Events_Final_PFam__OG0000622_Nodes_R.txt"

#Mito SP
#events_file <- "SP_Mito3__Events_Final_PFam__OG_14_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_2705_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_4_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_470_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_141_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_571_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_504_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_55_Nodes_R.txt"
#events_file <- "SP_Mito3__Events_Final_PFam__OG_761_Nodes_R.txt"

#Sec OF
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000019_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000021_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000676_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001551_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001187_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000095_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000566_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002331_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002517_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002575_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002623_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002903_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0003539_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0004167_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0006080_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0006972_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0007664_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0008051_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0008267_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0008999_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0013056_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0013137_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0013654_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0013661_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0016109_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0016279_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0017109_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0018812_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0018852_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0019887_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000911_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0005001_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0024821_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0004934_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0005930_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0011500_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0021737_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001012_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001149_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0018837_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0020781_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001763_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0012862_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0016908_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000308_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0012073_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0002700_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0000012_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001259_Nodes_R.txt"
#events_file <- "OF_Sec3__Events_Final_PFam__OG0001492_Nodes_R.txt"

#Sec SP
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1015_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_10301_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1169_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_122_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_12460_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1357_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1317_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_14_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_226_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_2278_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_2309_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_2407_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_2759_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_4_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_5397_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_902_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_9976_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_319_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_4494_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_3306_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_3919_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_5234_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_14244_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_470_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_9768_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_369_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_149_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_2282_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1245_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_8_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1519_Nodes_R.txt"
#events_file <- "SP_Sec3__Events_Final_PFam__OG_1610_Nodes_R.txt"
