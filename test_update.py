'''
basically trash file, only for testing if dataProcess.py imported as expected
'''
from dataProcess import getDataFileNames, getMissingID, startStopRec
from scrap2 import scrape_steam_id
import pandas as pd
import time
# missing_id 包括了第一轮scrape所有的missingid，接下来重新遍历所有的missingid的steamid，每一次遍历间隔10分钟，直到missingid的数量=0
dataNames = getDataFileNames()
missing_id= getMissingID(dataNames)
missing_id.to_csv('missing_id.csv')



# count total number of userid
total_count=0
for names in dataNames:
    start, stop = startStopRec(names)
    total_count+= (stop-start)+1

# count the number of remaining missing number of steamid
def remainMissingCount(df_missing_id, total_count):
    remain_count = df_missing_id[df_missing_id['steamid']=='0']['userid'].count()

    missingPct = remain_count/total_count
    print(f'remain missing: {remain_count}, pct missing: {missingPct*100:.3f}% out of {total_count} users')
    return remain_count


# prepare for re-scrape
fake_header = {  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2"}

base_url = "http://203.135.101.236:47019/kztop//player.php?player={}"

# initialize: set all steamid to be 0
df_missing_id = pd.DataFrame({'userid':missing_id})
df_missing_id['steamid'] = '0'

# start re-scrape, if pass test, use while True structure together with remainMissingCount(df_missing_id, total_count)>0
# 30个以内，手动解决吧
thres = 30#int(input('max tolerance: default input 30'))
iter_outter = 0
# 1 of 2 condition met, while loop end: either remaining missing value smaller than 30 or loop repeat for more than 3 times.
while (remainMissingCount(df_missing_id,total_count)>thres and iter_outter<3):
    iter_outter +=1
    iter_inner = 0
    df_missing_id_tmp = df_missing_id.loc[df_missing_id['steamid']=='0']
    for i in df_missing_id_tmp.userid:
        url = base_url.format(i)
        start_time = time.time()
        iter_inner +=1
        try:
            steam_id = scrape_steam_id(url,header=fake_header,timeOut=20)
            end_time = time.time()
            if steam_id:
                df_missing_id.loc[df_missing_id[df_missing_id['userid']==i].index[0],'steamid'] = steam_id
                print(f"iter_in:{iter_inner}_{iter_outter}, curid:{i}, total: {total_count}: {steam_id}-cost {end_time-start_time:.2f} s")
            else:
                print(f"iter_in:{iter_inner}_{iter_outter}, curid:{i}, total: {total_count}: Steam ID not found -cost {end_time-start_time:.2f} s")
        except Exception as e:
            end_time=time.time()
            print(f"iter_in:{iter_inner}_{iter_outter}, curid:{i}, total: {total_count}, error at {i}: {e}-cost {end_time-start_time:.2f}")
        df_missing_id.to_csv('missing_id_rescrape.csv')
        remainMissingCount(df_missing_id,total_count)
    print(f'======={iter_outter} end, sleep for 10min =======')
    time.sleep(600)
    


# werid test: unable to acces simen locally.
# start_time = time.time()
# try:
#     tmp = scrape_steam_id('http://203.135.101.236:47019/kztop//player.php?player=15',header=fake_header,timeOut=20)
# except:
#     print('err')
# end_time = time.time()
# print(f'{end_time-start_time}')
