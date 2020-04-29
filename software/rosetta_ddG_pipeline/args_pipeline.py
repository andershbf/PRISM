
"""folder.py creates and stores all relevant folders.

Author: Anders Frederiksen
Contribution: Johanna K.S. Tiemann

Date of last major changes: 2020-04-15

"""

# Standard library imports
from argparse import ArgumentParser, RawTextHelpFormatter
import os
import re

# Local application imports
import rosetta_paths


def parse_args2():
    """
    Argument parser function
    """

    parser = ArgumentParser(description=(
        '***Available options***\n'
        '-o output_path; \n'
        '-s Structure.pdb; \n'
        '-m Mutation_Input (optional); \n'
        '-r Relax_flags (optional); \n'
        '-c cartesian_ddg_flags (optional); \n'
        '-i modes [print,create,proceed,fullrun]; \n'
        '\tprint: prints default flag files \n'
        '\tcreate: Creates all run files \n'
        '\tproceed: Starts calculations with created run files \n'
        '\tfullrun: runs full pipeline'), formatter_class=RawTextHelpFormatter
    )

    parser.add_argument('--structure', '-s',
                        # type=lambda s: s.lower() in ['true', 't', 'yes',
                        # '1'],
                        default=False,
                        dest='STRUC_FILE',
                        help='Structure file'
                        )
    parser.add_argument('--uniprot', '-u',
                        default='',
                        dest='UNIPROT_ID',
                        help='Uniprot accession ID'
                        )
    parser.add_argument('--mutations', '-m',
                        default=None,
                        dest='MUTATION_INPUT',
                        help='mutation input file'
                        )
    parser.add_argument('--outputpath', '-o',
                        default=os.getcwd() + '/Run',
                        dest='OUTPUT_FILE',
                        help='Output path'
                        )
    parser.add_argument('--ddgflags', '-d',
                        default=rosetta_paths.path_to_parameters + '/cartesian_ddg_flagfile',
                        dest='DDG_FLAG_FILE',
                        help='ddG flag file'
                        )
    parser.add_argument('--relaxflags', '-r',
                        default=rosetta_paths.path_to_parameters + '/relax_flagfile',
                        dest='RELAX_FLAG_FILE',
                        help='Relaxation flag file'
                        )
    parser.add_argument('--mode', '-i',
                        choices=['print', 'create', 'proceed',
                                 'fullrun', 'relax', 'ddg_calculation'],
                        default='create',
                        dest='MODE',
                        help=('Mode to run:\n'
                              '\tprint: prints default flag files \n'
                              '\tcreate: Creates all run files \n'
                              '\tproceed: Starts calculations with created run files (incl. relax and ddG calculation) \n'
                              '\trelax: Starts relax calculations with created run files\n'
                              '\tddg_calculation: Starts ddg_calculation calculations with created run files\n'
                              '\tfullrun: runs full pipeline\n'
                              'Default value: create'
                              )
                        )
    parser.add_argument('--chainid',
                        default='A',
                        dest='CHAIN',
                        help='chain ID'
                        )
    parser.add_argument('--run_struc',
                        default=None,
                        dest='RUN_STRUC',
                        help=('Insert what chains you want to be part of the full structure format: ABC \n'
                              'ignorechain for full structure'
                              )
                        )
    parser.add_argument('--ligand',
                        default=None,
                        dest='LIGAND',
                        help='Set to true if you want to keep ligand'
                        )
    parser.add_argument('--is_membrane', '-mp',
                        default=False,
                        type=lambda s: s.lower() in ['true', 't', 'yes', '1'],
                        dest='IS_MP',
                        help='Checks if the provided protein is a memrane protein.'
                        )
    parser.add_argument('--mp_span',
                        default=None,
                        dest='MP_SPAN_INPUT',
                        help=('If span input file (defining the membrane spanning region) is prodived \n'
                              'coordinates will be used from there. Otherwise (default) it will be calculated \n'
                              '(see --mp_calc_span_mode).')
                        )
    parser.add_argument('--mp_calc_span_mode',
                        choices=['False', 'struc', 'DSSP', 'octopus',
                                 'bcl', 'Boctopus'],
                        default='False',
                        dest='MP_CALC_SPAN_MODE',
                        help=('Function/mode to calculate the membrane spanning region/file:\n'
                              '\tFalse: file will not be calculated \n'
                              '\tstruc: uses the information provided the structure \n'
                              '\tDSSP: uses DSSP & pdb orientation to calculate the span region (mp_span_from_pdb) \n'
                              '\toctopus: uses octopus \n'
                              '\tbcl: should be used for helix & beta sheets \n'
                              '\tBoctopus: should be used for beta sheets \n'
                              'Default value: False'
                              )
                        )
    parser.add_argument('--mp_thickness',
                        default=15,
                        type=int,
                        dest='MP_THICKNESS',
                        help='Half thickness of membrane.'
                        )
    parser.add_argument('--mp_align_ref',
                        default='',
                        dest='MP_ALIGN_REF',
                        help=('Reference PDB-id to membrane protein alignment.'
                              'Required for --mp_prep_align_mode options [OPM]'
                              )
                        )
    parser.add_argument('--mp_prep_align_mode',
                        choices=['False', 'OPM', 'PDBTM',
                                 'TMDET', 'MemProtMD'],
                        default='False',
                        dest='MP_ALIGN_MODE',
                        help=('Function/mode to align the membrane protein structure:\n'
                              '\tFalse: structure will not be rearranged \n'
                              '\tOPM: uses the information provided in OPM \n'
                              '\tPDBTM: uses the information provided in PDBTM (better than OPM) \n'
                              '\tTMDET: uses the information provided in TMDET \n'
                              '\tMemProtMD: uses the information provided in MemProtMD \n'
                              'Default value: OPM'
                              )
                        )
    parser.add_argument('--mp_relax_xml',
                        default=os.path.join(rosetta_paths.path_to_parameters, 'mp_relax.xml'),
                        dest='RELAX_XML_INPUT',
                        help='Relaxation xml file for membrane pipeline'
                        )
    parser.add_argument('--overwrite_path',
                        default=False,
                        type=lambda s: s.lower() in ['true', 't', 'yes', '1'],
                        dest='OVERWRITE_PATH',
                        help='Overwrites paths when creating folders'
                        )
    parser.add_argument('--slurm_partition',
                        default='sbinlab',
                        dest='SLURM_PARTITION',
                        help='Partition to run the SLURM jobs'
                        )
    args = parser.parse_args()

    return args
