import requests
import json

def test_arbe_api():
    company_uid = 'C6.001'
    token = '6C12886D821B0414432886144328862F472F47'
    
    # Try the positions endpoint
    url = f"https://www.comeet.co/careers-api/2.0/company/{company_uid}/positions?token={token}&details=true"
    
    print(f"Fetching {url}...")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} jobs.")
            if len(data) > 0:
                print("First job sample:")
                print(json.dumps(data[0], indent=2))
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_arbe_api()
