#!/bin/bash

# This script runs the NEB calculation.

# Inputs. num_img is the total number of images including endpoints.
POSCAR_in = POSCAR_initial
POSCAR_fin = POSCAR_final
num_img = 10
cores = 320
atom_sep = 1.0 # Minimum atom separation in Angstroms

# Change IRR_NUM in INPUT as the directry name number.
dirname=$PWD
folder="${dirname%"${dirname##*[!/]}"}"
folder="${folder##*/}"
sed -i -e "s/XXX/$folder/g" INPUT

# Run makeNEB.sh
makeNEB.sh $POSCAR_in $POSCAR_fin $num_img > makeNEB.out

# Only run VASP if valid irredicuble representation found.
done=$( tail -n 1 makeNEB.out )
if [$done == 'Done.']
then
    nebavoid.pl $atom_sep
    time mpirun -np $cores vasp_std
    nebresults.pl
else
    echo "Invalid Irreducible Representation!"
fi


