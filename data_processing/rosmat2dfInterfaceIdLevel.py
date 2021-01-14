#!/usr/bin/env python3

import argparse
from scipy.io import loadmat
import glob, os, pathlib
import numpy as np 
import pandas as pd
from IPython import embed
from rosmat2df import mat2pdDataFrame


def get_path(root_path, id, interface, level, topic): 
    # create the correct path name
    file_path = glob.glob(os.path.join(root_path, id, 'mats', id+'_'+interface+'_A0_*', '*_'+topic+'.mat'))
    assert len(file_path)==1 # make sure only one file
    assert os.path.exists(file_path[0]) # make sure only one file
    return file_path[0]

def rosmat2df(file_path): 
    df = mat2pdDataFrame(file_path)
    embed()


def main(root_path, subject_id, interface, level, topic): 
  
    file_path = get_path(root_path, id, i, level, topic)
    df = rosmat2df(file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='path to where ros mat topics are saved.', default='/mnt/mountpoint/2018-Adaptive-Autonomy-Wheelchair/data/study/', type=str)
    parser.add_argument('-id', '--subject_id', help='subject id for experiment trial', nargs='+', default=['*']) #default is all subjects
    parser.add_argument('-i', '--interface', help='interface used for experiment trial. options = JOY, HA, SNP', default='JOY') #default is all interfaces
    parser.add_argument('-l', '--level', help='autonomy level used for experiment trial. options = wst, A0, A1, A2', default='A0', type=str)
    parser.add_argument('-t', '--topic', help='topic of interest to be extracted from experiemnt trial', default='task_status_cleaned', type=str)
    args = parser.parse_args()

    main(args.path, args.subject_id, args.interface, args.level, args.topic)




