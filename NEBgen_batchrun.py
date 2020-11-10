#!/usr/bin/env python

"""Directory Generator and job submitter for NEBgen.

This script creates directories for each Irreducible representations for NEB calculations using the makeNEB.sh script.
It reads the list of irreducible representations from output.out generated from the makeNEB.sh inside results/output.out.
Afterwards, it submits the jobs inside each directory with runNEB.sh provided it is called from the jobscript.sh submission script.
It also assumes that the input files (INCAR, KPOINTS, POTCAR, POSCAR_initial, POSCAR_final, OUTCAR_initial, OUTCAR_final, INPUT )
are in a directory named "inputs" in the root directory.


Usage:

1. Run makeNEB.sh in a tmp directory with the inputs to obtain the output.out file. Set outputfile to point to this file.
IRR_NUM in INPUT should be set to 1 for this initial temporary run and then to XXX prior to running this script.

2. Run this script in the root directory.

"""

import re
import os
import shutil
import subprocess

# location of output file
outputfile = "output.out"

# Force calculation for already calculated runs
force = False

# Read all the irreducible representations
fi = open(outputfile,"r")
data = fi.read()
fi.close()

reps = re.findall(r'Irrep\s*#([0-9]*):',data)
input_files = ["INCAR", "INPUT", "KPOINTS", "POTCAR", "POSCAR_initial", "POSCAR_final","jobscript.sh"]

def submitter(jobid):
    for j in input_files:
        infile = "./inputs/"+j
        shutil.copy(infile,jobid)

    cmd = "cd " + jobid + "; sbatch jobscript.sh;cd .."
    out, err = subprocess.Popen(cmd, shell=True).communicate()
    if err:
        print(err)
    else:
        print("Submitting irreducible representation : %s" %jobid)

for i in reps:
    if os.path.exists(i):
    # Assume a complete calculation if the file mep.eps exists.
        if os.path.exists(i+"/mep.eps"):
            if force:
                submitter(i)
            else:
                pass
        else:
            print("Incomplete calculation at irreducible representation : %s " %i)
            submitter(i)

    else:
        os.makedirs(i)
        submitter(i)

print("%s irreducible representations submitted." %len(reps))






