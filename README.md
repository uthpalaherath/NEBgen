# NEBgen

NEBgen prepares POSCAR's for Nudged Elastic Band (NEB) calculations through Distortion Symmetry Method with [VTST](http://theory.cm.utexas.edu/vtsttools/) and [DiSPy](https://github.com/munrojm/DiSPy).
The nudged elastic band (NEB) method is a popular method for calculating the minimum energy pathways of kinetic processes. Although, linear interpolation between an initial and final structure (image) provides a decent estimate for the minimum energy pathway, the Distortion Symmetry Method takes into account symmetry-adapted perturbations to systematically lower the initial path symmetry, enabling the exploration of other low-energy pathways that may exist. 


## Installation

First install the following prerequisites:

1. [VTST](http://theory.cm.utexas.edu/vtsttools/) - Uses VTST scripts to perform a linear interpolation between the first and last image and performs the NEB calculation with VASP once the Distortion Symmetry Method is applied to the images with DiSPy. Recompile VASP with the VTST modules according to the steps given on the webpage. 

2. [DiSPy](https://github.com/munrojm/DiSPy) - Applies Distortion Symmetry Method to images.

Once installed, add the VTST scripts directory to your environment PATH. Additionally, add the NEBgen directory to $PATH as well.

E.g.-

```bash
export PATH="/home1/05979/uthpala/local/VTST/vtstscripts-957:$PATH"
```

## Usage

This script, makeNEB.sh, performs a linear interpolation between an initial state and a final state using ``nebmake.pl`` from VTST tools. Afterwards, it runs DiSPy with the provided ``INPUT`` to perform the perturbation. The perturbed files will be copied back to the respective directories ready for a NEB calculation with VASP. The default irreducible representation is set to #1 for the perturbation.

```bash
makeNEB.sh <initial POSCAR> <final POSCAR> <Total number of images>
```

Note that the total number of images here includes the initial and final images.

makeNEB.sh generates a log in ``results/output.out``. This provides a list of "Possible irreps of the distortion group".
Select the desired irreducible representation number (the default is #1) from this list and set it to ``IRR_NUM`` in ``INPUT``.
Finally, run ``makeNEB.sh`` again and the updated images will be prepared in the directories ready for the NEB calculation with VASP.

Check the ``examples`` directory for sample inputs. 

## NEB calculation

Once makeNEB.sh generates the required images, add the following to the INCAR in the current directory.

```
LCLIMB = .TRUE.
IBRION = 1
ICHAIN = 0
IMAGES = 8 # Excluding end points
SPRING = -5.0
LNEBCELL = .FALSE. # Requires ISIF = 3 and IOPT = 3
```

Note that ``IMAGES`` is the number of images excluding the end points. 

Run a VASP SCF calculation in the first and last image directory since VTST only performs the calculation for the intermediate images.

Now VASP can be run in the current directory to obtain the minimum energy path between the initial and final states. This calculation is computationally expensive since the number of nodes required is the same as ``IMAGES`` set in the ``INCAR``. The VTST scripts directory contains several scripts for post-processing the outputs. More info is available on their webpage. 

## Batch job submission

Using the ``NEBgen_batchrun.py`` script it is possible to run a complete NEB calculation for all the irredicible representations found. 

### Instructions

1. Create a directory "inputs" in the root directory of the calculation which includes the INCAR, KPOINTS, POTCAR, POSCAR_initial, POSCAR_final, OUTCAR_initial, OUTCAR_final, INPUT and jobscript.sh. OUTCAR_initial and OUTCAR_final are from SCF calculations of the end point images. jobscript.sh is a job script for the job scheduler on the cluster that calls runNEB.sh and would look like the following:

```
cd $SLURM_SUBMIT_DIR/
runNEB.sh POSCAR_initial POSCAR_final 10 320 1.0
```

where,

    runNEB.sh <POSCAR_initial> <POSCAR_final> <Total no. of images> <num of cores> <minimum atom separation in Angstroms>

2. Run makeNEB.sh with ``IRR_NUM=1`` in INPUT in a temporary directory with the input files to obtain the results/output.out file. Copy the output.out file to the root directory. Now set ``IRR_NUM=XXX`` in INPUT in the "inputs" directory.

3. Run ``NEBgen_batchrun.py`` in the root directory.


## Reference

- D. Sheppard, P. Xiao, W. Chemelewski, D. D. Johnson, and G. Henkelman, “A generalized solid-state nudged elastic band method,” J. Chem. Phys. 136, 074103 (2012).

- D. Sheppard and G. Henkelman, “Paths to which the nudged elastic band converges,” J. Comp. Chem. 32, 1769-1771 (2011).

- D. Sheppard, R. Terrell, and G. Henkelman, “Optimization methods for finding minimum energy paths, J. Chem. Phys. 128, 134106 (2008).

- G. Henkelman, B.P. Uberuaga, and H. Jónsson, “A climbing image nudged elastic band method for finding saddle points and minimum energy paths,” J. Chem. Phys. 113, 9901 (2000).

- G. Henkelman and H. Jónsson, “Improved tangent estimate in the nudged elastic band method for finding minimum energy paths and saddle points,” J. Chem. Phys. 113, 9978 (2000).

- H. Jónsson, G. Mills, K. W. Jacobsen, “Nudged Elastic Band Method for Finding Minimum Energy Paths of Transitions,” in Classical and Quantum Dynamics in Condensed Phase Simulations, Ed. B. J. Berne, G. Ciccotti and D. F. Coker (World Scientific, 1998), page 385.

- J.M. Munro et. al. Implementation of distortion symmetry for the nudged elastic band method with DiSPy. npj Comp. Mat. 5, 52 (2019).

- J.M. Munro et. al. Discovering minimum energy pathways via distortion symmetry groups. Phys. Rev. B. 98, 085107 (2018).

- B.K. VanLeeuwen & V. Gopalan. The antisymmetry of distortions. Nat. Commun. 6, 8818 (2015).