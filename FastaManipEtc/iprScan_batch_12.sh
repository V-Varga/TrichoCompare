#!/bin/bash
# The name of the account you are running in, mandatory.
#SBATCH -A SNIC2021-22-658
# Name the job
#SBATCH -J iprScan_20220228

# NUMBER OF NODES
#SBATCH -N 1
# NUMER OF THREADS (PTHREADED)
#SBATCH -c 4
# Request  minutes of runtime for the job
#SBATCH --time=96:00:00
# Set the names for the error and output files
#SBATCH --error=job.%J.err
#SBATCH --output=job.%J.out

#SBATCH --mail-user=vi2505va-s@student.lu.se
# if you'd like to receive mails from the cluster :p
#SBATCH --mail-type=BEGIN
# you recieve a mail when the job has begun
#SBATCH --mail-type=END
# you recieve a mail when the job has completed


## TEMPLATE START

# Change directory to where you currently are
cd WORKING_DIRECTORY_FINDREPLACE


# Create directory for new files
mkdir INPUTFILE_DIRECTORY_FINDREPLACE
# Move into the newly created directory
#cd INPUTFILE_DIRECTORY_FINDREPLACE


# Java is needed for interprocan, 11.0.2 works for iprscan 5.52-86.0

module load Java/11.0.2

# Assign variables to file paths and options

interproscan=/proj/nobackup/trichocompare_2021/software/my_interproscan/interproscan-5.54-87.0/interproscan.sh
inputfile=INPUTFILE_FINDREPLACE
outputdirectory=WORKING_DIRECTORY_FINDREPLACE
tempdir=OUTPUTFILE_TEMPDIR_FINDREPLACE
options="--goterms --iprlookup --pathways --cpu 4"


$interproscan --input $inputfile --output-dir $outputdirectory --tempdir $tempdir $options
