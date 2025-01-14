import requests
from bs4 import BeautifulSoup

def curNumPlayers(url='http://203.135.101.236:47019/kztop//', timeOut=20):
    # Send a GET request to the provided URL
    fake_header = {  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2"}
    
    response = requests.get(url, headers = fake_header, timeout=timeOut)
    
    if response.status_code != 200:
        print(f"Failed to access the page. Status code: {response.status_code}")
        return None

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the target element
    # Adjust the selector based on your target element
    target_element = soup.find('med')  # Update this selector based on the actual page structure

    if target_element:
        return int(target_element.get_text())
    else:
        print("Target element not found.")
        return None


# Example usage
if __name__ == "__main__":
    # Replace 'your_url_here' with the actual URL
    url = 'http://203.135.101.236:47019/kztop//'
    result = curNumPlayers(url) # ,timeOut = 20
    if result:
        print(f"Extracted text: {result}")
