"""helper.py contains helpful functions.

Author: Anders Frederiksen
Contribution: Johanna K.S. Tiemann

Date of last major changes: 2020-05-04

"""

# Standard library imports
import logging as logger
import os
import shutil
import urllib.request
import sys
from os import listdir
from os.path import isfile, join

# Third party imports
import numpy as np
from scipy import stats


def create_symlinks(source_file, dist_folder, name=''):
    # WIP
    # import stat
    if name == '':
        basename = os.path.basename(source_file)
    else:
        basename = name
    dist_file = os.path.join(dist_folder, basename)
    # st = os.stat(source_file)
    # os.chown(source_file, st[stat.ST_UID], st[stat.ST_GID])
    os.symlink(source_file, dist_file, True)
    logger.info(f'Symbolic link created: {dist_file} --> {source_file}')
    return dist_file


def create_copy(source_file, dist_folder, name='', directory=False):
    if name == '':
        basename = os.path.basename(source_file)
    else:
        basename = name
    dist_file = os.path.join(dist_folder, basename)
    if directory:
        try:
            shutil.copytree(source_file, dist_file)
        except FileExistsError:
            logger.warn(f'Directory {dist_file} already exists. No files will be copied.')
    else:
        shutil.copy(source_file, dist_file)
    logger.info(f'Hardcopy created: {dist_file} --> {source_file}')

    return dist_file


def find_copy(searchfolder, searchword, resultfolder, resultname):
    for file in os.listdir(searchfolder):
        if file.endswith(searchword):
            return create_copy(os.path.join(searchfolder, file), resultfolder, name=resultname)


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def get_mut_dict(mutfile):
    # extracts mutations & generates the mutation dictionary
    logger.info(
        'Extract information from mutfile and generate dictionary')
    mut_dic = {}
    with open(mutfile, 'r') as fp:
        for line in fp:
            muts = line.split()
            mut_dic[muts[1]] = muts[0] + muts[2]
    return mut_dic


def longest_common_subsequence(str1, str2):
    # adapted from
    # https://www.codespeedy.com/find-longest-common-subsequence-in-python/
    a = len(str1)
    b = len(str2)
    string_matrix = [[0 for i in range(b + 1)] for i in range(a + 1)]
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            if i == 0 or j == 0:
                string_matrix[i][j] = 0
            elif str1[i - 1] == str2[j - 1]:
                string_matrix[i][j] = 1 + string_matrix[i - 1][j - 1]
            else:
                string_matrix[i][j] = max(
                    string_matrix[i - 1][j], string_matrix[i][j - 1])
    index = string_matrix[a][b]
    res = [''] * index
    i = a
    j = b
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            res[index - 1] = str1[i - 1]
            i -= 1
            j -= 1
            index -= 1
        elif string_matrix[i - 1][j] > string_matrix[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return ''.join(res)


def extract_by_uniprot_fasta(keyword):
    # extract information from uniprot
    url_base = "https://www.uniprot.org/uniprot/"
    search_params = "?query=reviewed:yes" +\
        "+AND+accession:" + keyword
    return_params = "+&format=tab&columns=id,sequence,organism,entry%20name"
    url = url_base + search_params + return_params

    data_array = []
    for line in urllib.request.urlopen(url):
        line = line.decode('utf-8')
        unprocessed = line[:-1].split('\t')
        data_array.append(unprocessed)

    return data_array


def extract_uniprot_fasta(keyword):
    # extract information from uniprot
    url_base = "https://www.uniprot.org/uniprot/"
    search_params = "?query=reviewed:yes" +\
        "+AND+gene:" + keyword +\
        "+AND+organism:human"
    return_params = "+&format=tab&columns=id,sequence,organism,entry%20name"
    url = url_base + search_params + return_params

    data_array = []
    for line in urllib.request.urlopen(url):
        line = line.decode('utf-8')
        unprocessed = line[:-1].split('\t')
        data_array.append(unprocessed)

    return data_array


def drop_numerical_outliers(df, variant_col='variant', score_col='score', z_thresh=3):
    # Constrains will contain `True` or `False` depending on if it is a value
    # below the threshold.
    constrains = df[[score_col]].select_dtypes(include=[np.number]) \
        .apply(lambda x: np.abs(stats.zscore(x)) < z_thresh) \
        .all(axis=1)
    # Drop (inplace) values set to be rejected
    logger.info(df[variant_col][~constrains].tolist())
    logger.info(df[score_col][~constrains].tolist())
    df.drop(df.index[~constrains], inplace=True)

    df.sort_values('variant', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def read_fasta(fasta_file):
    fastau_file = open(fasta_file, 'r')
    fastau_lines = fastau_file.readlines()
    fastau_file.close()
    uniprot_seq = ''
    for line in fastau_lines[1:]:
        uniprot_seq = uniprot_seq + line.strip()
    return(uniprot_seq)

def check_path(path):
    os.chdir(os.getcwd())
    if path != None and path != '':

        if path[0] == "/" and path != None:
            path=path
        if path[0]!= "/" and path != None:
            path=os.path.join(os.getcwd(),path)
    return(path)

def read_slurms(path, printing=False):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    mypath=path
    warn = []
    warnings = 0
    canc = []
    cancels = 0
    slurm_file_canc = []
    slurm_file_warn = []
    nums_warn = []
    nums_canc = []
    for file in files:
        if str(file[0:5]) == "slurm":
            path = join(mypath, file)
            with open(path) as f:
                for line in f:
                    if "WARNING" in line:
                        num_warn = file.split('_')
                        num_warn = num_warn[1].split('.')
                        num_warn = num_warn[0]

                        nums_warn.append(num_warn)
                        warn.append(line)
                        warnings += 1
                        slurm_file_warn.append(file)
                    if "CANCELLED" in line:

                        num_canc = file.split('_')
                        num_canc = num_canc[1].split('.')
                        num_canc = num_canc[0]

                        nums_canc.append(num_canc)
                        slurm_file_canc.append(file)
                        canc.append(line)
                        cancels += 1

    nums_canc = list(dict.fromkeys(nums_canc))
    nums_warn = list(dict.fromkeys(nums_warn))
    print("Number of cancels = ", cancels)
    print(nums_canc)
    #print("Number of warnings = ",warnings)
    # print(nums_warn)
    if printing == True:
        if warnings != 0:
            with open(join(mypath, "warningfile"), 'w') as errorfile:
                errorfile.write("Number of warnings = "+str(warnings)+'\n')
                errorfile.write("Files= "+str(nums_warn)+'\n')
                for n, m in zip(warn, slurm_file_warn):
                    errorfile.write(m+'\n')
                    errorfile.write(n+'\n')
        if cancels != 0:
            with open(join(mypath, "cancelfile"), 'w') as cancelfile:
                cancelfile.write("Number of cancels = "+str(cancels)+'\n')
                cancelfile.write("Files = "+str(nums_canc)+'\n')
                for n, m in zip(canc, slurm_file_canc):
                    cancelfile.write(m+'\n')
                    cancelfile.write(n+'\n')
