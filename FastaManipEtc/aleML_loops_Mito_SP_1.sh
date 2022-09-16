#!/bin/bash -l
 
#SBATCH -A snic2022-22-256
#SBATCH -p core
#SBATCH -n 10
#SBATCH -t 24:00:00
#SBATCH -J ALE_Mito_SP
#SBATCH --mail-type=ALL
#SBATCH --mail-user=vi2505va-s@student.lu.se


#the actual loops to run, below: 
ls /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/SP_Mito3__OG_1*.names.ufboot.ale | while read file; do
	singularity exec /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/bin/ale.sif ALEml_undated /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/SpeciesTree_rooted_at_outgroup_22_ALE.names.nwk $file >> /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/ALEml_undated_MitoSP.log;
done

ls /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/SP_Mito3__OG_2*.names.ufboot.ale | while read file; do
	singularity exec /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/bin/ale.sif ALEml_undated /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/SpeciesTree_rooted_at_outgroup_22_ALE.names.nwk $file >> /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/ALEml_undated_MitoSP.log;
done

ls /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/SP_Mito3__OG_3*.names.ufboot.ale | while read file; do
	singularity exec /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/bin/ale.sif ALEml_undated /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/SpeciesTree_rooted_at_outgroup_22_ALE.names.nwk $file >> /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/ALEml_undated_MitoSP.log;
done

#cleaning up: 
mv /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/bin/SP_Mito3__OG_* /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/ALE_Files/Mito_SP/
rm /proj/rhodoquinone_2022/nobackup/Vi_TrichoCompare/bin/core.* #these files are unnecessary
