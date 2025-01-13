from dataProcess import getDataFileNames,startStopRec
import pandas as pd
import numpy as np

dataNames = getDataFileNames()

df_simenID = pd.read_csv(dataNames[1])
start_id, stop_id = startStopRec(dataNames[1])
df_simenID['userid'] = np.arange(start_id, stop_id+1)
df_simenID.columns = ['origin_userid','steamid','userid']

# create an empty dataframe to store all processed ori data
df_simenID_full = pd.DataFrame(columns=df_simenID.columns)
# iterate all data files and process data
for filePath in dataNames:
    df_simenID = pd.read_csv(filePath)
    
    start_id, stop_id = startStopRec(filePath)
    df_simenID['userid'] = np.arange(start_id, stop_id+1)
    df_simenID.columns = ['origin_userid','steamid','userid']
    
    df_simenID_full = pd.concat([df_simenID_full,df_simenID])

rescrape = pd.read_csv('missing_id_rescrape.csv')

# update

merged_df = df_simenID_full.merge(rescrape[['userid', 'steamid']], on='userid', how='left', suffixes=('', '_rescrape'))

row_indexer = (merged_df['steamid'].str.startswith('STEAM_')==False)
merged_df['steamid'].loc[row_indexer] = merged_df['steamid_rescrape'].loc[row_indexer]

outputName = f'{merged_df.index.start+1}-{merged_df.index.stop}.csv'

merged_df.to_csv(outputName)
