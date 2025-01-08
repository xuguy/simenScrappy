'''
this .py file is dedicated for testing
'''
# load packages and define scrap function
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# Function to scrape the desired text
def scrape_steam_id(url,header,sleepTime=3,timeOut = 10):
    # Send a GET request to the URL
    response = requests.get(url,headers=header,timeout=timeOut)
    time.sleep(sleepTime)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to fetch the page: Status code {response.status_code}")
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Locate the specific button element by its "onclick" attribute
    button = soup.find('button', onclick=lambda value: value and "copyToClipboard" in value)
    
    # Extract the text inside the <b> tag nested within the button
    if button:
        b_tag = button.find('b')
        if b_tag:
            return b_tag.text.strip()
    
    # If no match is found, return None or raise an exception
    return None


fake_header = {  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2"}

base_url = "http://203.135.101.236:47019/kztop//player.php?player={}"

# scrapped url are stored in the following list:
if __name__ == '__main__':
    df_steamID = []

    start = int(input('start from:'))
    # stop to be set as the total number of players
    stop = int(input('end: '))
    outFile = f'simenSteamID-{start}-{stop}.csv'

    # scrapping loop
    for i in range(start,stop+1):
        url=base_url.format(i)
        start_time = time.time()
        try:
            
            steam_id = scrape_steam_id(url,header=fake_header)
            end_time = time.time()
            if steam_id:
                df_steamID.append(steam_id)
                print(f"{i}/{stop-start+1}: {steam_id}-cost {end_time-start_time:.3f} s")
            else:
                df_steamID.append(f'NaN_{i}-time cost {end_time-start_time:.3f} s')
                print(f"{i}/{stop-start+1}: Steam ID not found.")
        except Exception as e:
            end_time=time.time()
            df_steamID.append(f'err_{i}')
            print(f"error at {i}/{stop-start+1}: {e}-cost {end_time-start_time:.3f}")


    # output
    print('loop end, now ouput file')
    simenSteamID = pd.DataFrame(df_steamID,index = range(1,len(df_steamID)+1))
    simenSteamID.to_csv(outFile)
    print(f'output at {outFile}')
