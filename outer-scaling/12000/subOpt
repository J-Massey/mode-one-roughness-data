#!/bin/bash

#SBATCH --ntasks=256
#SBATCH --nodes=4
#SBATCH --partition=amd
#SBATCH --job-name=12k
#SBATCH --time=05:00:00
#SBATCH --output=JOB.out
# SBATCH --exclude=ruby035,ruby036,ruby037
# SBATCH --dependency=afterok:1908224

echo "Starting calculation at $(date)"
echo "---------------------------------------------------------------"

module purge
module load conda
source activate an
module load openmpi/4.0.5/amd

python run-val.py

