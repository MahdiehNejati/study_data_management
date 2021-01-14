#!/usr/bin/env python3 

# Code developed my Mahdieh Nejati Javaremi in January 2021. Copyright (c) 2021. 

import argparse
from enum import Enum
import pandas as pd 
from IPython import embed

subject_group = {
    'S': ['injured', 'sci'],
    'U': ['uninjured', 'ui']
}

class Interface(Enum): 
    JOY = 0
    HA = 1
    SNP = 2


# hardcoded paths. 
def get_session_order_file(subject_id): 
    id = subject_id[0]
    session_balance_file = f"/mnt/mountpoint/2018-Adaptive-Autonomy-Wheelchair/data/balanced_tasks/{subject_group[id][0]}/{subject_group[id][1]}_interface_balance.csv"
    df = pd.read_csv(session_balance_file)
    return df

def session_order(subject_id, interface): 
    session_order_df = get_session_order_file(subject_id)
    col = int(subject_id[1:3])
    session_order_ind = session_order_df.iloc[col, Interface[interface].value]
    return session_order_ind

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-id', '--subject_id', help='subject id for experiment trial') #default is all subjects
    parser.add_argument('-i', '--interface', help='interface used for experiment trial. options = JOY, HA, SNP', default='JOY') #default is all interfaces
    args = parser.parse_args()

    session_order(args.subject_id, args.interface)