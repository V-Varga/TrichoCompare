#!/bin/python
"""
Title: predictionParser__v2.py
Date: 2022-03-05
Author: Virág Varga

Description:
	This program takes an input results file from a protein localization prediction software,
		and performs pre-determined data restructuring and extraction processes on the file.
		The resulting files can be combined into a large protein database.
	The prediction software whose results files can be used as input are:
		- DeepLoc
		- SignalP
		- TargetP
		- EggNOG
		- PFam via EggNOG
		- YLoc
		- MitoFates
		- InterProScan (with options: `--goterms --iprlookup --pathways`)

List of functions:
	No functions are used in this script.

List of standard and non-standard modules used:
	argparse
	os
	deepLoc_Parser__v2.py
	signalP_Parser__v2.py
	targetP_Parser__v2.py
	eggNOG_dn_Parser__v2.py
	eggNOG_dn_PFam_Parser__v2.py
	mitoFates_Parser__v2.py
	yLoc_Parser__v2.py
	iprScan_Parser.py

Procedure:
	1. Assignment of command-line arguments.
	2. The called argument is executed to parse the input file.
	3. Outputs from functions are written out to a results file.

Known bugs and limitations:
	- There is no quality-checking integrated into the code.
	- The name of the output file is not user-defined.
	- The program cannot accept multiple input files, nor can it determine the type
		of input file it was given (ie. which program's results file was used as input).

Version:
	This is version 2.0 of this program. Modifications were made to accomadate new versions
		of the imported module scripts, and a new command line argument was added for the
		InterProScan results parser.

Usage:
	./predictionParser__v2.py [-h] [-dl] [-sp] [-tp] [-en] [-pfen] [-mf] [-yl] [-ipr] [-v] input_file
	OR
	python predictionParser__v2.py [-h] [-dl] [-sp] [-tp] [-en] [-pfen] [-mf] [-yl] [-ipr] [-v] input_file

This script was written for Python 3.8.12, in Spyder 5.1.5.
"""

#################################   ARGPARSE   #######################################
import argparse
#the argparse module allows for a single program script to be able to carry out a variety of specified functions
#this can be done with the specification of unique flags for each command


parser = argparse.ArgumentParser(description =
								 'This program takes an input results file from a protein localization prediction software,\
								 and performs pre-determined data restructuring and extraction processes on the file. \
								 The resulting files can be combined into a large protein database. \
								 The prediction software whose results files can be used as input are: \
								 DeepLoc, SignalP, TargetP, eggNOG, PFam via eggNOG, MitoFates & YLoc.')
#The most general description of what this program can do is defined here


#adding the arguments that the program can use
parser.add_argument(
	'-dl', '--DeepLoc',
	action='store_true',
	help = 'This argument will parse the results of the DeepLoc program.'
	)
	#the '-dl' flag will call the deepLoc_Parser__v2.py program to parse the input file
parser.add_argument(
	'-sp', '--SignalP',
	action='store_true',
	help = 'This argument will parse the results of the SignalP program.'
	)
	#the '-sp' flag will call the signalP_Parser__v2.py program to parse the input file
parser.add_argument(
	'-tp', '--TargetP',
	action='store_true',
	help = 'This argument will parse the results of the TargetP program.'
	)
	#the '-tp' flag will call the targetP_Parser__v2.py program to parse the input file
parser.add_argument(
	'-en', '--EggNOG',
	action='store_true',
	help = 'This argument will parse the results of the eggNOG program.'
	)
	#the '-en' flag will call the eggNOG_dn_Parser__v2.py program to parse the input file
parser.add_argument(
	'-pfen', '--PFamEggNOG',
	action='store_true',
	help = 'This argument will parse the results of a PFam matching run of the eggNOG program.'
	)
	#the '-pfen' flag will call the eggNOG_dn_PFam_Parser__v2.py program to parse the input file
parser.add_argument(
	'-mf', '--MitoFates',
	action='store_true',
	help = 'This argument will parse the results of the MitoFates program.'
	)
	#the '-mf' flag will call the mitoFates_Parser__v2.py program to parse the input file
parser.add_argument(
	'-yl', '--YLoc',
	action='store_true',
	help = 'This argument will parse the results of the YLoc program.'
	)
	#the '-yl' flag will call the yLoc_Parser__v2.py program to parse the input file
parser.add_argument(
	'-ipr', '--InterProScan',
	action='store_true',
	help = 'This argument will parse the results of the InterProScan program, assuming the following options were used: `--goterms --iprlookup --pathways`.'
	)
	#the '-ipr' flag will call the iprScan_Parser.py program to parse the input file
parser.add_argument(
	#'-i', '--input',
	#the above line of code is left in as further clarification of this argument
	dest='input_file',
	metavar='INPUT_FILE',
	type=argparse.FileType('r')
	)
	#this portion of code specifies that the program requires an input file, and it should be opened for reading ('r')
parser.add_argument(
	'-v', '--version',
	action='version',
	version='%(prog)s 1.0'
	)
	#This portion of the code specifies the version of the program; currently 1.0
	#The user can call this flag ('-v') without specifying input and output files


args = parser.parse_args()
#this command allows the program to execute the arguments in the flags specified above


#################################   Main Program   ######################################


#import necessary module
import os #allows access to the operating system


#designate input file name as variable
infile = args.input_file.name


#parse arguments
if args.DeepLoc:
	#if -dl argument is called
	cmd = "python deepLoc_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the deepLoc_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.SignalP:
	#if -sp argument is called
	cmd = "python signalP_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the signalP_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.TargetP:
	#if -tp argument is called
	cmd = "python targetP_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the targetP_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.EggNOG:
	#if -en argument is called
	cmd = "python eggNOG_dn_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the eggNOG_dn_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.PFamEggNOG:
	#if -pfen argument is called
	cmd = "python eggNOG_dn_PFam_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the eggNOG_dn_PFam_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.MitoFates:
	#if -mf argument is called
	cmd = "python mitoFates_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the mitoFates_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.YLoc:
	#if -yl argument is called
	cmd = "python yLoc_Parser__v2.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the yLoc_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)

if args.InterProScan:
	#if -ipr argument is called
	cmd = "python inprScan_Parser.py {0}".format(infile)
	#since the `os.system()` method of calling a python script requires an input string
	#the command that would be used to run the yLoc_Parser.py program on its own
	#is formatted into a string together with the name of the input file
	#this is then passed as a command for execution
	os.system(cmd)
