# sed script to create batch files for slurm
#specifically edited for the IPR_Scan runs

for file in /home/v/vivarga/ThesisTrich/Data/SplitStdData/*.fasta; do
  full_file="${file##*/}"; #this line removes the path before the file name
  file_base="${full_file%.*}"; #this line removes the file extension
  slurmsubfile=interproscan_${file_base}.sh;
  sed 's/WORKING_DIRECTORY_FINDREPLACE/\/proj\/nobackup\/trichocompare_2021\/Vi_storage\/IPRScan_Results_PROSITE\//g' iprScan_batch_12.sh > $slurmsubfile;
  sed -i "s|INPUTFILE_DIRECTORY_FINDREPLACE|${file_base}|g" $slurmsubfile;
  sed -i "s|INPUTFILE_FINDREPLACE|${file}|g" $slurmsubfile;
  sed -i 's/OUTPUTFILE_TEMPDIR_FINDREPLACE/\/proj\/nobackup\/trichocompare_2021\/Vi_storage\/IPR_temp\//g' $slurmsubfile;
done
