'''
this .py file is dedicated for testing
'''
# load packages and define scrap function
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

# Function to scrape the desired text
def scrape_steam_id(url,header,sleepTime=3):
    # Send a GET request to the URL
    response = requests.get(url,headers=header)
    sleep(sleepTime)
    
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
df_steamID = []

start = 1
# stop to be set as the total number of players
stop = 1000

# scrapping loop
for i in range(start,stop+1):
    url=base_url.format(i)
    try:
        steam_id = scrape_steam_id(url,header=fake_header)
        if steam_id:
            df_steamID.append(steam_id)
            print(f"{i}: {steam_id}")
        else:
            df_steamID.append(f'NaN_{i}')
            print(f"{i}: Steam ID not found.")
    except Exception as e:
        df_steamID.append(f'err_{i}')
        print(f"error at {i}: {e}")


# output
simenSteamID = pd.DataFrame(df_steamID,index = range(1,len(df_steamID)+1))
simenSteamID.to_csv('simenSteamID.csv')