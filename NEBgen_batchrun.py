#!/usr/bin/env python

"""Batch job submitter for NEBgen.

This script creates directories for each irreducible representations and performs the NEB calculation on each of them.

Author: Uthpala Herath
email: ukh0001@mix.wvu.edu

Instructions:

1. Create a directory "inputs" in the root directory of the calculation which includes the INCAR, KPOINTS, POTCAR, POSCAR_initial, POSCAR_final,
OUTCAR_initial, OUTCAR_final, INPUT and jobscript.sh. OUTCAR_initial and OUTCAR_final are from SCF calculations of the end point images. jobscript.sh
is a job script for the job scheduler on the cluster that calls runNEB.sh and would look like the following:

E.g.-
    cd $SLURM_SUBMIT_DIR/
    runNEB.sh POSCAR_initial POSCAR_final 10 320 1.0

where,

    runNEB.sh <POSCAR_initial> <POSCAR_final> <Total no. of images> <num of cores> <minimum atom separation in Angstroms>

2. Run makeNEB.sh with IRR_NUM=1 in INPUT in a temporary directory with the input files to obtain the results/output.out file.
Copy the output.out file to the root directory. Now set IRR_NUM=XXX in INPUT in the "inputs" directory.

3. Run NEBgen_batchrun.py in the root directory.

"""

import re
import os
import shutil
import subprocess

# location of output file
outputfile = "output.out"

# Force calculation for already calculated runs
force = False

# Name of scheduler on cluster
scheduler = "qsub"  # "sbatch"

# Read all the irreducible representations
fi = open(outputfile, "r")
data = fi.read()
fi.close()

reps = re.findall(r"Irrep\s*#([0-9]*):", data)
input_files = [
    "INCAR",
    "INPUT",
    "KPOINTS",
    "POTCAR",
    "POSCAR_initial",
    "POSCAR_final",
    "jobscript.sh",
]


def submitter(jobid):
    """
    Submits the job to cd into the directory and calls runNEB.sh.
    i.e.
    runNEB.sh POSCAR_initial POSCAR_final 10 320 1.0

    """
    for j in input_files:
        infile = "./inputs/" + j
        shutil.copy(infile, jobid)

    cmd = "cd " + jobid + ";" + scheduler + " jobscript.sh;cd .."
    out, err = subprocess.Popen(cmd, shell=True).communicate()
    if err:
        print(err)
    else:
        print("Submitting irreducible representation : %s" % jobid)


for i in reps:
    if os.path.exists(i):
        # Assume a complete calculation if the file mep.eps exists.
        if os.path.exists(i + "/mep.eps"):
            if force:
                submitter(i)
            else:
                print("Completed calculation at : %s " % i)

        elif os.path.exists(i + "/makeNEB.out"):
            fi = open(i + "/makeNEB.out", "r")
            data = fi.readlines()
            fi.close()
            doneword = data[-1].split()[0]

            if doneword == "Invalid":
                print("Invalid irreducible representation at : %s" % i)
            elif doneword == "Done.":
                print("Calculation in progress at : %s" % i)

        else:
            print("Incomplete calculation at irreducible representation : %s " % i)
            submitter(i)

    else:
        os.makedirs(i)
        submitter(i)

print("%s irreducible representations submitted." % len(reps))
