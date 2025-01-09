'''
this program needs to be run recursively, stop untill there is no more missing user data.
'''

import pandas as pd
import numpy as np
import os, re

# get data file names
def getDataFileNames():
    curFileNames = os.listdir()
    dataNames = [name for name in curFileNames if name.endswith('.csv')]
    return dataNames

# due to flaws of scrap2.py, we cannot use the id within the data file but we have to extract start stop userid from the file name.

# rec for 'recognize'
def startStopRec(file):
# Pattern to match the start and stop numbers
    pattern = r'simenSteamID-(\d+)-(\d+)\.csv'

    # Loop through the file names and extract start and stop numbers
    
    match = re.match(pattern, file)
    if match:
        start = int(match.group(1))
        stop = int(match.group(2))
        print(f'File: {file} | Start: {start} | Stop: {stop}')

    return start,stop
# test if this function works as expected
# startStopRec(dataNames[0])

# exhaust all data file and concate all missing id data
def getMissingID(dataNames):
    missing_id_tmp = []
    for filePath in dataNames:
        df_steamID = pd.read_csv(filePath)
        start_id, stop_id = startStopRec(filePath)
        df_steamID['userid']=np.arange(start_id,stop_id+1)
        df_steamID.columns = ['origin_userid','steamid','userid']

        # check the userid of missing data
        missing_id_tmp.append(df_steamID[df_steamID['steamid'].str.startswith('STEAM_') != True]['userid'])

    missing_id = pd.concat(missing_id_tmp)
    missing_id.reset_index(drop=True,inplace=True)
    return missing_id
# del missing_id_tmp, df_steamID # release ram









