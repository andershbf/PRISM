#!/bin/sh
#SBATCH --job-name=relax_PagP
#SBATCH --time=10:00:00
#SBATCH --mem 5000
#SBATCH --partition=sbinlab

# launching rosetta relax 
bin/rosetta_scripts. -parser:protocol /relax/input/relax.xml -in:file:s /relax/input/input.pdb -mp:setup:spanfiles /relax/input/spanfiles/input.span -mp:scoring:hbond -relax:fast -relax:jump_move true -nstruct 3 -packing:pack_missing_sidechains 0 -out:pdb -out:file:scorefile /relax/run/relax_scores.sc -database  -ignore_unrecognized_res true -score:weights franklin2019  