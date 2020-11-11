#!/bin/bash
#----------------------------------------------------
# Slurm job script for NEB calculations
#   for TACC Stampede2 KNL nodes
#----------------------------------------------------

#SBATCH -J LaNiO3_OV_NEB           # Job name
#SBATCH -p normal               # Queue (partition) name
#SBATCH -N 8                    # Total # of nodes
#SBATCH --tasks-per-node 40     # Total # of mpi tasks
#SBATCH -t 48:00:00             # Run time (hh:mm:ss)
#SBATCH --mail-type=fail        # Send email at failed job
#SBATCH --mail-type=end        # Send email at end of job
#SBATCH --mail-user=ukh0001@mix.wvu.edu

ulimit -s unlimited
cd $SLURM_SUBMIT_DIR/
time runNEB.sh POSCAR_initial POSCAR_final 10 320 1.0

