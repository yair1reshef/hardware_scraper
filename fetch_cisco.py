import requests

url = "https://careers.cisco.com/global/en/search-results?qcountry=Israel"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    with open('cisco_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Successfully saved cisco_page.html")
    
except Exception as e:
    print(f"Error: {e}")
