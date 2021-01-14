#!/usr/bin/env python3

from scipy.io import loadmat
import pandas as pd
import argparse

def getColumnPaths(array, title, path):
    columns = []
    if len(array[title]) == 0:	
        path.append(title)	
        returned = [path]	
        return returned
    array = array[title][0][0]
    path.append(title)
    # pxth = list(path)
    names = array.dtype.names
    if names == None:
        return [path]
    for n in names:
        columns = columns + (getColumnPaths(array, n, list(path)))
    return columns

def getDataByColumns(array, cols):
    dataSet = []
    for c in cols:
        data = array
        for d in c[1:]:
            if len(data[d]) == 0:
                data = data[d]
            elif len(data[d][0]) == 0:
                data = data[d][0]
            else:
                data = data[d][0][0]
        dataSet.append(data.squeeze())
    return dataSet

def mat2pdDataFrame(filepath, test=False):
    annots = loadmat(filepath)
    keys = [k for k in annots.keys() if not k.startswith('_')]
    title = keys[0] #usually there is only one single key that doesn't start with '__'

    # 'columns' is of the form [[root, child1, childOfChild1], [root, child2], ... ]
    # where each list is the path through the .mat file to some data
    # and also where each list functions as the multi-leveled column names
    columns = getColumnPaths(annots, title, [])
    if test: print(title, columns) #for debugging

    df = pd.DataFrame()
    for a in range(0, annots[title].shape[1]):
        df = df.append([getDataByColumns(annots[title][0][a], columns)], ignore_index = True)

    col_depth = max([len(c) for c in columns])
    # Creates list of tuples for each header based on path to data, and also adds '↓' to shorter paths
    test = [tuple([a for a in c[1:]] + ['↓']*(col_depth-len(c))) for c in columns]
    df.columns = pd.MultiIndex.from_tuples(test)

    return df
# print(df['costmap_translator_obstacles', 'header'])

def main(file_path): 
    df = mat2pdDataFrame(file_path)
    return df

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='path to where ros mat topics are saved.', default='/mnt/mountpoint/2018-Adaptive-Autonomy-Wheelchair/data/study/S01/mats/S01_HA_A0_S7/S01_HA_A0_S7_task_status.mat', type=str)
    args = parser.parse_args()

    main(args.path)
    
    # # Run unit test:
    # df = mat2pdDataFrame('/mnt/mountpoint/2018-Adaptive-Autonomy-Wheelchair/data/study/S01/mats/S01_HA_A0_S7/S01_HA_A0_S7_task_status.mat')

    # pd.set_option('display.max_rows', 30)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    # pd.set_option('display.max_colwidth', 100)  # None for no limit

