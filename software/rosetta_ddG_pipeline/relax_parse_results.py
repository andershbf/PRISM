"""relax_parse_results.py 
This function will parse the results of a rosetta pre_relax run. it will be callable from an 
sbatch script, that can wait for the relaxation to finish, and then select the best one. The 
point is to implement the 20x pre relaxation for the stability pipeline, that Amelie requested.

Author: Anders Frederiksen

Date of last major changes: 2020-04

"""

# Standard library imports
import logging as logger
import os
import sys

# Local application imports
from helper import AttrDict, create_symlinks, create_copy, find_copy


def parse_relax_results(folder, sc_name='score_bn15_calibrated', logger_mode='info'):
    '''This function parses the scorefile from a rosetta
    pre-relaxation, and selects the lowest scoring one'''
    relax_scores = {}
    for n in range(20):
        path_to_scorefile = os.path.join(
            folder.relax_run, f'{n}-{sc_name}.sc')
        with open(path_to_scorefile) as scorefile:
            scorelines = scorefile.readlines()

        # Put the relaxation scores in this dict
        

        for line in scorelines:
            score_fields = line.split()
            name = score_fields[-1].strip()
            #print(name,score_fields)
            # check if this is an actual scoring line
            if score_fields[0].strip() == 'SCORE:' and name != 'description':
                score = float(score_fields[1])
                relax_scores[name] = score
    print(relax_scores)
    # now find the lowest scoring one.
    # set it to the last one, just to start with something
    most_relaxed = name
    for key in relax_scores:
        # it the key is more relaxed than the previous best, update the best.
        if relax_scores[key] < relax_scores[most_relaxed]:
            most_relaxed = key
            print(most_relaxed)

    logger.info(f'most relaxed structure is {most_relaxed}.')
    logger.info('deleting the rest')
#     and now delete all the structures that are not the best scoring one.
#     it seems a little crude, but whatever.
    for key in relax_scores:
        if key != most_relaxed:
            path_to_tense = os.path.join(folder.relax_run, f'{key}.pdb')
            print('deleting', path_to_tense)
            os.remove(path_to_tense)
    relax_output_strucfile = find_copy(
        folder.relax_run, f'{most_relaxed}.pdb', folder.relax_output, 'output.pdb')

    create_copy(
        os.path.join(folder.relax_output, 'output.pdb'), folder.ddG_input, name='input.pdb')

    return os.path.join(folder.relax_output, f'{most_relaxed}.pdb')


if __name__ == '__main__':
    folder = AttrDict()
    folder.update({'relax_run': sys.argv[1], 'relax_output': sys.argv[
                  2], 'ddG_input': sys.argv[3]})
    if len(sys.argv) > 4:
        parse_relax_results(folder, sc_name=sys.argv[4])
    else:
        parse_relax_results(folder)
